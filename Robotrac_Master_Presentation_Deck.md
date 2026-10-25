# Robotrac — Executive Technical Slide Deck Blueprint (15 Slides)

**Topic:** Autonomous Agricultural Tractor Engineering Specification  
**Presenter:** Chief Technology Officer & Principal AI Robotics Engineer  
**Format:** PowerPoint / Keynote / Marp Markdown Slide-by-Slide Script  

---

## Slide 1: Title Slide
* **Title:** Robotrac — Autonomous Agricultural Tractor Platform
* **Subtitle:** Technical Architecture, Drive-by-Wire Electro-Hydraulics, Dual-Domain Compute, Non-Linear Motion Control & ISO 18497 / ISO 25119 Safety Compliance
* **Presenter:** CTO & Principal Agricultural Robotics R&D Engineer
* **Status:** Production Engineering Baseline v1.0 · October 2026
* **Visual:** High-contrast logo badge `[🚜 ROBOTRAC R&D ENGINEERING]`, clean modern typography.
* **Speaker Notes:** 
  > "Good morning team and leadership. Today I am presenting the engineering baseline specification for Robotrac—our autonomous agricultural tractor platform. We have moved past simulation-only concepts to solve the hard terramechanics, hydraulic drive-by-wire actuation, high-speed RTK state estimation, and functional safety standards required to deploy real autonomous tractors in the field."

---

## Slide 2: The Agricultural Robotics Problem (Agronomic Context)
* **Title:** The Agricultural Robotics Challenge: Beyond Passenger AVs
* **Key Stats:**
  * **$15\% - 35\%$:** Dynamic Tire-Soil Wheel Slip in loose/tilled soil
  * **$100,000\text{ Lux}$:** Direct open sunlight glare & deep canopy shadows
  * **$\pm 2.5\text{ cm}$:** Pass-to-pass RTK repeatability target
* **Core Takeaways:**
  * *Terramechanics vs. Bicycle Models:* Tractors operate on deformable soil; lateral tire slip ($v_y \neq 0$) causes steady-state downhill drift into crop rows under standard kinematic algorithms.
  * *Hostile Sensory Environment:* Airborne soil silt and chaff coat camera and LiDAR lenses in minutes without active pneumatic purging.
  * *High-Mast Antenna Sway:* Roof-mounted antenna ($h = 2.8\text{ m}$) introduces up to $29.2\text{ cm}$ lateral error on a $6^\circ$ side-slope without dynamic terrain tilt compensation.
* **Speaker Notes:**
  > "Autonomous agriculture is far harder than on-road driving because the vehicle deforms the ground beneath it. If your control algorithms assume zero tire slip, your tractor will crush the crop rows within 50 meters. We must engineer from terramechanics first."

---

## Slide 3: Dual-Domain Compute & System Topology
* **Title:** System Architecture: Dual-Domain Hardware Split
* **Architecture Columns:**
  * **Domain 1 — Soft Real-Time Autonomy Compute (NVIDIA Jetson AGX Orin Industrial):**
    * Ubuntu Linux (PREEMPT_RT) + ROS 2 (CycloneDDS).
    * Dual-antenna RTK + IMU 15-state ES-EKF pose estimation (20 Hz).
    * Optical NIR semantic row segmentation (BiSeNet-V2 @ 30 FPS).
    * 77 GHz radar Doppler clutter filtering & Livox Mid-360 canopy profiling.
    * Fields2Cover coverage planner & acados NMPC solver (20 Hz).
  * **Domain 2 — Hard Real-Time Safety Controller (TTControl TTC 580 / IFM CR711S):**
    * Dual-core lockstep 32-bit MCU certified to ISO 25119 AgPL d.
    * Deterministic 100 Hz closed-loop steering & dual Hall WAS reading.
    * Electro-hydraulic Danfoss OSPE valve PWM flow control.
    * SAPR failsafe brake dump valve ($< 150\text{ ms}$).
    * ISO 18497 wireless RF remote heartbeat monitoring ($< 500\text{ ms}$ trip).
* **Speaker Notes:**
  > "Under ADR-002, we decoupled soft real-time perception from hard real-time actuation. A Python garbage collection pause or Linux scheduler hiccup cannot be allowed to stall steering commands on an 8-ton tractor. The safety MCU has ultimate veto authority over all hydraulic valves."

---

## Slide 4: Drive-by-Wire (DbW) & Electro-Hydraulic Actuation
* **Title:** Electro-Hydraulic Drive-by-Wire Actuation
* **Subsystems:**
  1. *Proportional Steering:* Danfoss OSPE / Eaton PVG 32 load-sensing proportional valve. Eliminates mechanical backlash and gear slipping seen in aftermarket steering wheel motors.
  2. *Wheel Angle Sensor (WAS):* Curtiss-Wright R300 dual Hall-effect contactless sensor ($0.5\text{V} - 4.5\text{V}$ inverted ratiometric outputs: $V_1 + V_2 = 5.0\text{V} \pm 0.1\text{V}$).
  3. *Fail-Safe Braking:* Proportional service brake (0–120 bar) + Spring-Applied Pressure-Released (SAPR) emergency cylinder venting to tank in $< 150\text{ ms}$.
  4. *Powertrain & Implement:* SAE J1939 engine throttle (`TSC1`) + ISOBUS Class 3 (ISO 11783) 3-point hitch and PTO headland automation.
* **Speaker Notes:**
  > "We reject friction-based steering wheel motors for commercial autonomy. Our system uses factory-integrated electro-hydraulic valves with dual-redundant contactless knuckle angle feedback and failsafe spring brakes."

---

## Slide 5: High-Precision Navigation & State Estimation
* **Title:** Dual-Antenna RTK & 3D Terrain Compensation
* **Highlights:**
  * **Moving Baseline Dual-Antenna RTK (Septentrio / Dual u-blox F9P):**
    * Fixed $1.2\text{ m}$ baseline across cab roof.
    * Calculates carrier-phase double-differences for true static heading ($\sigma_\psi < 0.09^\circ$) at $0\text{ m/s}$ forward velocity.
    * Completely immune to tractor steel chassis magnetic distortion and zero-speed drift.
  * **Tactical MEMS IMU (Xsens MTi-680G):**
    * 200 Hz propagation with Coning/Sculling compensation.
    * Dynamic lever-arm roll/pitch transformation down to ground contact patch ($\Delta x = h \sin\theta$).
    * Restricts ground tilt error to $\le 2.0\text{ cm}$ over severe ruts.
* **Speaker Notes:**
  > "Single-antenna GPS cannot determine heading when a tractor is stationary or crawling in mud. Our dual-antenna moving baseline setup guarantees sub-degree heading at zero velocity, with active tilt compensation down to the soil."

---

## Slide 6: Multi-Modal Perception in Hostile Environments
* **Title:** Multi-Modal Perception: Dust, Glare & Clutter Resilience
* **Sensor Trio:**
  * **NIR HDR Cameras (Leopard Imaging AR0820):** $> 120\text{ dB}$ dynamic range, Global Shutter, 850 nm Near-Infrared filter (NDVI vegetation contrast). Fitted with 6-bar pneumatic air-blast purge nozzles to clean lens dust.
  * **77 GHz mmWave Radar (Continental ARS 408-21):** Direct Doppler radial velocity measurement. Pierces dense airborne dust plumes behind tillers without signal attenuation.
  * **3D Solid-State LiDAR (Livox Mid-360):** 360° x 59° FOV. Ground plane segmentation separates solid obstacles from harmless tall grass clutter.
* **Obstacle Confirmation Gate:** Camera/LiDAR obstacle detections are cross-validated with radar Doppler before commanding an emergency stop, eliminating phantom stops in dust clouds.
* **Speaker Notes:**
  > "In harrowing or dry tilling, dust clouds blind optical sensors. Our 77 GHz radar acts as the ground-truth gate to ensure the vehicle only stops for real physical obstructions."

---

## Slide 7: AI/ML Crop-Row Perception & Visual Servoing
* **Title:** Crop-Row Deep Segmentation & Visual Servoing
* **Architecture:**
  * *BiSeNet-V2 / MobileNetV4 Semantic Segmentation:* Predicts pixel classes: `[Soil, Crop Stalk, Weed Clutter, Obstacle]`. Quantized to TensorRT INT8 ($< 33\text{ ms}$ latency).
  * *RANSAC Line Fitting:* Projects ground-contact crop pixels into 3D camera coordinates to extract centerline error $e_y$ and yaw angle $e_\psi$.
  * *Hybrid Navigation State Machine:*
    * *Mode A (Open Headlands / Early Emergence):* Guided strictly by RTK-GNSS + IMU path following.
    * *Mode B (Established Crop Canopy):* Visual-servoing row centering takes precedence to adapt to planting irregularities and protect plant roots.
* **Speaker Notes:**
  > "We use deep semantic segmentation instead of color thresholding to ignore heavy weeds, and a state machine that seamlessly transitions between GPS waypoint following in headlands and visual row-centering inside crops."

---

## Slide 8: Agricultural Coverage Planning via Fields2Cover
* **Title:** Implement-Aware Coverage Path Planning (Fields2Cover)
* **Pipeline:**
  1. *Headland Generator:* Computes boundary margins based on tractor wheelbase and minimum turning radius $R_{min}$.
  2. *Swath Generator:* Calculates optimal parallel tracks aligned with field contours to minimize soil compaction and overlap.
  3. *Route Optimizer:* Solves swath traversal order via Google OR-Tools to eliminate deadhead travel.
  4. *Non-Holonomic Turning:* Generates $\Omega$-turns (loop turns), Dubins, and Reeds-Shepp curves while modeling towed implement swept envelopes.
* **Speaker Notes:**
  > "Fields2Cover solves the agricultural coverage problem with realistic implement turning curves. It ensures our tractor executes smooth loop turns without jack-knifing or driving implements into ditches."

---

## Slide 9: Non-Linear Model Predictive Control (NMPC)
* **Title:** NMPC Path Tracking with Deformable Soil Slip
* **Control Formulation:**
  * *Receding Horizon:* $N = 20$ steps ($T_s = 0.05\text{ s}$, lookahead $= 1.0\text{ s}$) solved at $20\text{ Hz}$ via **acados** Real-Time Iterations (RTI).
  * *Terramechanics Modeling:* Integrates simplified Pacejka lateral tire forces ($F_{yf}, F_{yr}$) and slip ratios into state equations.
  * *Disturbance Observer:* Compensates for implement drag moments ($F_{drag} \in [5, 40\text{ kN}]$) on side-slopes.
  * *Hard Physical Constraints:* Knuckle steer angle $|\delta| \le 35^\circ$, slew rate $|\dot{\delta}| \le 25^\circ/\text{s}$, and roll-over acceleration ceiling $|a_y| \le 0.25 \cdot g$.
* **Speaker Notes:**
  > "Kinematic Stanley controllers drift on side slopes. Our NMPC controller actively models lateral soil slip and implement drag forces to guarantee sub-2.5cm pass-to-pass accuracy."

---

## Slide 10: Functional Safety Architecture (ISO 18497 & ISO 25119)
* **Title:** Functional Safety & Regulatory Compliance
* **Safety Mandates:**
  * **ISO 18497 Perception Envelopes:**
    * *Zone 1 (Stop):* Immediate Category 0 E-Stop & hydraulic dump ($L_{stop} \approx 3.2\text{ m}$).
    * *Zone 2 (Decel):* Proportional service braking down to $0.3\text{ m/s}$.
    * *Zone 3 (Warn):* 360° amber strobe + 100 dB acoustic horn.
  * **ISO 25119 AgPL d / Category 3:** Dual-channel cross-monitored high-side and low-side safety switches.
  * **Wireless RF Safety Remote:** HBC-radiomatic / Hetronic transmitter with $150\text{ ms}$ RF heartbeat. Auto-trips to Category 0 stop within $< 500\text{ ms}$ of signal loss.
  * **Pre-Motion Warning:** Mandatory 3.0s horn sound and beacon flash before any autonomous motion.
* **Speaker Notes:**
  > "Safety cannot be a software promise. We adhere strictly to ISO 18497 and ISO 25119 AgPL d with dual-channel hardware de-energize circuits and an active wireless RF heartbeat remote."

---

## Slide 11: Electrical Power Conditioning & Ingress Protection
* **Title:** Electrical Hardening & Environmental Enclosures
* **Specifications:**
  * **ISO 7637-2 Electrical Surge Immunity:** Active TVS clamping absorbs $+100\text{ V}$ alternator load dumps (Test Pulse 5a/5b).
  * **Cold-Cranking Ride-Through:** Accepts battery bus drops down to $6.0\text{ V}$ during starter motor engagement.
  * **Supercapacitor Buffer:** 50F bank provides a $30\text{ s}$ ride-through to bridge cranking or execute graceful shutdown.
  * **Enclosures & Wiring:** CNC milled aluminum IP67/IP69K enclosures with Gore-Tex breather vents. Amphenol/Deutsch DT connectors and sealed M12 industrial Ethernet.
* **Speaker Notes:**
  > "Tractor electrical buses are notoriously noisy. Without active load-dump clamping and supercapacitor ride-through, starter motor cranking resets your compute every time the engine turns over."

---

## Slide 12: Low-Bandwidth Telemetry & Edge Buffering
* **Title:** Resilient Telemetry: Protobuf, MQTT & Store-and-Forward
* **Features:**
  * **Binary Protocol Buffers v3:** 85% bandwidth reduction compared to JSON; entire 10-hour working shift consumes $< 50\text{ MB}$ of cellular data.
  * **MQTT v5 with QoS 1:** Guaranteed delivery of mission state transitions and safety fault events over lossy rural cell towers.
  * **Edge SQLite Store-and-Forward Buffer:** Onboard circular buffer stores 72 hours of telemetry during cellular dead zones, automatically syncing on reconnection without data loss.
  * **TimescaleDB & PostGIS:** Cloud backend uses TimescaleDB hypertables partitioned into 7-day chunks with GiST spatial indexing for field boundaries.
* **Speaker Notes:**
  > "Farmland cell coverage is notoriously unreliable. We use binary Protobuf over MQTT with an edge SQLite ring buffer to guarantee zero telemetry loss even during multi-hour cellular blackouts."

---

## Slide 13: Operator HMI & Android Field Tablet
* **Title:** Field Ergonomics: High-Contrast Day UI & Local AP
* **Features:**
  * **Outdoor High-Contrast Day Theme:** Pure white background (`#FFFFFF`) with solid black typography (`#05080A`), completely eliminating the dark-mode mirror reflection under $100,000\text{ lux}$ open sunlight.
  * **Glove Ergonomics:** All clickable cards exceed $56\text{ dp}$ with $16\text{ dp}$ padding. Two-step horizontal "Slide-to-Start" gesture prevents accidental vehicle movement.
  * **Direct Local Wi-Fi AP:** Tablet connects directly to tractor's onboard Wi-Fi router via QR code mTLS handshake for 100% offline field operation.
  * **High-Decibel Audio Alarm:** Bypasses tablet volume settings with a continuous $2.5\text{ kHz}$ alarm siren on tractor safety stops.
* **Speaker Notes:**
  > "Dark mode is useless in direct sunlight. Our field UI uses pure white canvases with high-contrast typography, glove-friendly touch targets, and a direct local Wi-Fi AP that requires zero cell signal."

---

## Slide 14: Phased R&D Roadmap & Release Gates
* **Title:** Phased Development & Validation Strategy
* **Phases:**
  * **Phase 1: Deterministic SIL Simulation (Gazebo / O3DE):** Terramechanics soil slip, sensor fault injection; zero physical hardware risk.
  * **Phase 2: Telemetry & Android MVP:** Protobuf streaming and local Wi-Fi pairing.
  * **Phase 3: Perception Data & ML Optimization:** Multi-crop training and TensorRT quantization.
  * **Phase 3.5: Sub-Scale Electric Mule Testbed:** Retrofit small electric UTV/lawn-tractor to validate dual-antenna RTK, Fields2Cover, and wireless E-stop at $< 5.0\text{ km/h}$ with zero rollover risk.
  * **Phase 4: Stationary Tractor HIL Rig:** Jacked-up tractor hydraulic valve deadband calibration and dump valve response measurement ($< 150\text{ ms}$).
  * **Phase 5: Supervised Field Proving:** 50 hours of autonomous proving-ground trials with safety driver and perimeter wireless remote.
* **Speaker Notes:**
  > "We do not jump directly from simulation to an 8-ton machine. Phase 3.5 introduces an electric mule testbed to de-risk navigation and safety at low speed and low cost before touching a diesel tractor."

---

## Slide 15: Executive Summary & Next Engineering Actions
* **Title:** Conclusion & Procurement Action Plan
* **Core Takeaways:**
  * Certified electro-hydraulic valves replace aftermarket steering wheel motors.
  * Dual-antenna RTK and NMPC replace kinematic Stanley controllers for sub-2.5cm field accuracy.
  * Dual-domain compute and ISO 18497 / ISO 25119 standards enforce high-integrity functional safety.
* **Immediate Milestones:**
  1. *Milestone 1:* Confirm tractor hydraulic platform (CCLS load-sensing) and order Danfoss OSPE valve manifold.
  2. *Milestone 2:* Assemble Phase 3.5 Sub-Scale Electric Mule testbed for proving-ground trials.
  3. *Milestone 3:* Bench-test custom ISO 7637-2 power conditioning unit against alternator load dumps.
* **Speaker Notes:**
  > "We now have a complete, production-grade engineering specification. With your approval, our next step is to order the hydraulic manifold and begin assembly of the Phase 3.5 electric mule testbed. Thank you."
