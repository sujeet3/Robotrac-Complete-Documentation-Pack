# Algorithms Specification for Robotrac Autonomy

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Core Frameworks:** Fields2Cover, Error-State EKF (ES-EKF), Non-Linear Model Predictive Control (acados/CasADi), ROS 2  

---

## 1. Localization & State Estimation (Error-State EKF)

Agricultural vehicles experience severe tire slip ($10\% - 35\%$) and slow crawl speeds ($< 0.5\text{ m/s}$), rendering single-antenna GNSS heading and wheel-encoder dead reckoning invalid.

### 1.1. 15-State Error-State Extended Kalman Filter (ES-EKF)
The filter fuses 20 Hz Dual-Antenna RTK-GNSS, 200 Hz Tactical MEMS IMU, and CAN bus steering angle:
$$\delta \mathbf{x} = \begin{bmatrix} \delta \mathbf{p}^n & \delta \mathbf{v}^n & \delta \boldsymbol{\theta}^n & \delta \mathbf{b}_a & \delta \mathbf{b}_g \end{bmatrix}^T \in \mathbb{R}^{15}$$
* **Propagation (200 Hz):** Propagates nominal position $\mathbf{p}$, velocity $\mathbf{v}$, and quaternion attitude $\mathbf{q}$ using high-rate IMU specific forces $\mathbf{a}_m$ and angular rates $\boldsymbol{\omega}_m$, integrating Coning and Sculling compensations.
* **Dual-Antenna Moving Baseline Measurement Update (20 Hz):** Directly measures geographic yaw $\psi_{gnss}$ and pitch $\theta_{gnss}$ from carrier-phase double-differences across a fixed baseline ($L \ge 1.2\text{ m}$):
  $$\sigma_{heading} = \frac{\sigma_{carrier}}{L_{baseline}} \approx \frac{0.002\text{ m}}{1.2\text{ m}} \approx 0.09^\circ$$
  Static yaw is guaranteed at $0\text{ m/s}$ velocity, immune to tractor chassis magnetic disturbances.
* **3D Dynamic Terrain Tilt Compensation:** Transforms antenna coordinates down to the ground tire-contact patch:
  $$\Delta x_{ground} = h_{mast} \cdot \sin(\theta_{roll}) + l_{offset} \cdot \cos(\theta_{pitch})$$
  Eliminates the up to $30\text{ cm}$ lateral error caused by antenna sway over furrows and side-slopes.

---

## 2. Agricultural Coverage & Path Planning (Fields2Cover)

Waypoints alone are insufficient for field operations. Planning utilizes the **Fields2Cover** library architecture:

```
Field Polygon & Obstacles ──► Headland Generator ──► Swath Generator ──► Route Optimizer ──► Path Planner (Ω-Turns)
```

1. **Headland Generator:** Computes peripheral turning bands based on tractor wheelbase $L$, implement width $W_{impl}$, and minimum turning radius $R_{min}$. Creates a clean buffer separating working swaths from field boundaries.
2. **Swath Generator:** Computes parallel driving swaths aligned with the primary field axis or terrain contour lines to minimize soil erosion and fuel consumption.
3. **Route Optimizer (TSP):** Solves swath traversal order using traveling salesperson heuristics (Google OR-Tools integration) to minimize non-working headland travel time.
4. **Non-Holonomic Turning Curves:**
   * **$\Omega$-Turn (Omega Turn):** Computes smooth loop turns when adjacent swaths are closer than $2 \cdot R_{min}$.
   * **Reeds-Shepp / Dubins Curves:** For non-adjacent swaths.
   * **Implement Collision Envelope:** Verifies that towed implements or 3-point hitch attachments sweep safely within boundary margins.

---

## 3. Crop-Row & Multi-Modal Perception

Perception must function in direct $100,000\text{ lux}$ sunlight, fluctuating shadow canopies, and dense airborne dust plumes.

```
┌─────────────────────────────────┐      ┌───────────────────────────────────┐
│ HDR Optical Camera (NIR 850 nm) │      │ 77 GHz mmWave Radar (ARS 408)     │
└───────────────┬─────────────────┘      └─────────────────┬─────────────────┘
                │                                          │
                ▼                                          ▼
     BiSeNet-V2 Segmentation                     Direct Doppler Velocity
     & RANSAC Row Line Fitting                   & Cluster Tracking
                │                                          │
                └───────────────────┬──────────────────────┘
                                    ▼
                 Spatial Fusion & Cross-Validation Layer
                 - Confirms real obstacles through dust clouds
                 - Filters crop leaf clutter vs solid objects
```

* **Crop-Row Segmentation:** 
  * Near-Infrared (NIR) bandpass filter ($\approx 850\text{ nm}$) maximizes vegetative chlorophyl reflectance (NDVI contrast) against soil.
  * Real-time semantic segmentation network (BiSeNet-V2 / MobileNetV4) outputs pixel masks for crop stems, background soil, and weed clutter.
  * RANSAC line fitting extracts centerline lateral offset $e_y$ and heading error $e_\psi$ relative to the camera optical axis.
* **77 GHz mmWave Radar Penetration:**
  * Radar beams ($\lambda \approx 3.9\text{ mm}$) penetrate dust clouds, fog, and rain without attenuation.
  * Measures instantaneous radial velocity of dynamic targets (humans, livestock, other machinery).
  * **Obstacle Confirmation Gate:** A camera or LiDAR detection is cross-validated with radar Doppler data before triggering an emergency stop, preventing false stops caused by dust plumes or tall grass.
* **Hybrid Navigation State Machine:**
  * *Mode A (Open Field / Headlands / Early Emergence):* Guided strictly by RTK-GNSS + IMU path following.
  * *Mode B (Established Canopy):* Fuses visual-servoing row centering with RTK-GNSS, giving visual row perception precedence to protect plants from steering drift.

---

## 4. Vehicle Motion Control: Non-Linear Model Predictive Control (NMPC)

Kinematic Pure Pursuit and Stanley controllers assume zero lateral tire slip ($v_y = 0$). In agricultural soils, wheel slip ratios reach $15\% - 30\%$, causing severe steady-state offset on side-slopes.

```
Target Swath Path ──► NMPC Optimizer (acados @ 20 Hz) ──► Optimal Steering [δ*] & Speed [a*] ──► CAN Bus OSPE Valve
                      ▲
                      │ Dynamic Soil Slip & Implement Drag Observer
```

### 4.1. Non-Linear Vehicle Dynamics Formulation
State: $\mathbf{x} = [x, y, \psi, v_x, v_y, r]^T$, Control: $\mathbf{u} = [\delta_{steer}, a_x]^T$.

$$\dot{x} = v_x \cos\psi - v_y \sin\psi, \quad \dot{y} = v_x \sin\psi + v_y \cos\psi, \quad \dot{\psi} = r$$

$$\dot{v}_x = a_x + v_y \cdot r - \frac{F_{drag}}{m}$$

$$\dot{v}_y = -v_x \cdot r + \frac{1}{m}(F_{yf} \cos\delta_{steer} + F_{yr})$$

$$\dot{r} = \frac{1}{I_z}(l_f F_{yf} \cos\delta_{steer} - l_r F_{yr} + \tau_{disturb})$$

Where lateral tire forces $F_{yf}$ and $F_{yr}$ are calculated via the simplified Pacejka tire-soil model:
$$F_{yf} = -C_{\alpha f} \cdot \alpha_f, \quad F_{yr} = -C_{\alpha r} \cdot \alpha_r$$
$$\alpha_f = \arctan\left(\frac{v_y + l_f r}{v_x}\right) - \delta_{steer}, \quad \alpha_r = \arctan\left(\frac{v_y - l_r r}{v_x}\right)$$

### 4.2. Receding Horizon Cost Function
Solved at $20\text{ Hz}$ using **acados** Real-Time Iterations (RTI):
$$\min_{\mathbf{u}} \sum_{k=0}^{N-1} \left( \|\mathbf{x}_k - \mathbf{x}_{ref,k}\|_{\mathbf{Q}}^2 + \|\mathbf{u}_k\|_{\mathbf{R}}^2 + \|\Delta \mathbf{u}_k\|_{\mathbf{S}}^2 \right) + \|\mathbf{x}_N - \mathbf{x}_{ref,N}\|_{\mathbf{P}}^2$$
* **Physical Constraints Enforced:**
  * Maximum knuckle steer angle: $|\delta| \le 35^\circ$.
  * Maximum hydraulic steering slew rate: $|\dot{\delta}| \le 25^\circ/\text{s}$.
  * Lateral acceleration threshold (roll-over prevention): $|a_y| = |v_x \cdot r| \le 0.25 \cdot g$.

---

## 5. Implement Control & Headland Coordination

* **3-Point Hitch Electro-Hydraulic Raise/Lower:**
  * When approaching a headland turn line ($d < 2.0\text{ m}$), the planner commands the Electronic Hitch Control (EHR) via ISOBUS / CAN to raise the implement.
  * Disengages PTO before initiating turn to protect universal drive joints.
  * Re-engages PTO and lowers implement once the tractor aligns within $e_y < 5\text{ cm}$ of the incoming swath.

---

## 6. Verification & Quantitative Pass/Fail Gates

| Metric | Target Specification | Validation Method |
| :--- | :--- | :--- |
| **Pass-to-Pass Cross-Track Error ($e_y$)** | $\le \pm 2.5\text{ cm}$ (RTK fixed, flat soil)<br>$\le \pm 5.0\text{ cm}$ ($10^\circ$ side-slope) | High-speed differential GNSS verification rig over 10 km of driving. |
| **Static Yaw Accuracy ($\sigma_\psi$)** | $\le 0.09^\circ$ at $0\text{ m/s}$ velocity | Moving Baseline dual-antenna carrier-phase baseline verification. |
| **Dynamic Roll Compensation Error** | $\le 2.0\text{ cm}$ lateral offset error at ground | Measured against physical ground marker on $15^\circ$ test ramp. |
| **NMPC Solve Latency** | $\le 20\text{ ms}$ (p99) on NVIDIA Jetson | In-loop execution monitoring using acados RTI solver. |
| **False-Positive Emergency Stops** | $< 1\text{ per }10\text{ operating hours}$ in dust/canopy | Tested in dry tilling conditions with dense airborne dust plumes. |
| **E-Stop Actuator Response** | $\le 150\text{ ms}$ from command to hydraulic pressure drop | High-speed pressure transducer recording on brake/steering lines. |

