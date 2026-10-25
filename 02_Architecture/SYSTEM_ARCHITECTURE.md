# Robotrac System Architecture Specification

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Architecture Pattern:** Dual-Domain Hybrid Local-First Autonomy with Independent Safety Authority  

---

## 1. System Topology & Dual-Domain Compute

```text
                 ┌─────────────────────────────────────────────────────────┐
                 │ Rugged Android Field Tablet                             │
                 │ High-Contrast Day UI • Mission Maps • Health Alarms     │
                 │ Authorized High-Level Intent Requests (Pause/Stop/Start) │
                 └────────────┬───────────────────────────────┬────────────┘
                              │ Local Wi-Fi (Tractor AP / TLS) │ Cloud MQTT/HTTPS
                              ▼                               │ (Cellular)
┌────────────────────────────────────────────────────────┐    │
│ Cloud Infrastructure (Supervisory & Telemetry Ingest)  │◄───┘
│ - Device Registry & PKI Credential Lifecycle           │
│ - Mission Records, Field Polygons & PostGIS GeoJSON    │
│ - TimescaleDB High-Volume Telemetry Ingestion          │
│ - Over-the-Air (OTA) Signed Artifact Releases          │
└─────────────────────────────▲──────────────────────────┘
                              │ Cellular 4G LTE (Protobuf / MQTT QoS 1)
                              ▼
┌────────────────────────────────────────────────────────────────────────┐
│ DOMAIN 1: Soft Real-Time Autonomy Compute (NVIDIA Jetson AGX Orin)     │
│ OS: Ubuntu Linux (PREEMPT_RT patched) • Middleware: ROS 2 (CycloneDDS) │
│                                                                        │
│ - Dual-Antenna RTK-GNSS + Tactical IMU (15-State ES-EKF Pose @ 20 Hz)  │
│ - 3D Dynamic Terrain Roll/Pitch Tilt Compensation                     │
│ - Optical NIR Camera Semantic Row Segmentation (BiSeNet-V2)            │
│ - 77 GHz mmWave Radar Doppler Fusion & Dust Cloud Clutter Filtering    │
│ - Fields2Cover Coverage Path Planner (Swaths & Ω-Turns)                │
│ - NMPC Trajectory Generator (acados RTI solver @ 20 Hz)                │
│ - Edge Telemetry Store-and-Forward SQLite Buffer                       │
│ - Local Industrial Wi-Fi Access Point (WPA3-Enterprise / mDNS)         │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Isolated Deterministic CAN Bus 1
                                   │ (Trajectory Setpoints: Steer Angle, Speed, Mode)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│ DOMAIN 2: Hard Real-Time Safety Controller (TTControl TTC 580 / IFM)   │
│ Architecture: Dual-Core Lockstep MCU • Certified to ISO 25119 AgPL d  │
│                                                                        │
│ - Hard Real-Time Control Loop (Deterministic 100 Hz Cycle)            │
│ - Dual Hall Wheel Angle Sensor (WAS) Reading & Non-Linear Calibration  │
│ - Electro-Hydraulic Steering Valve (Danfoss OSPE) PWM Flow Control     │
│ - Proportional Service Brake Pressure Valve Modulation (0–120 bar)     │
│ - SAE J1939 Engine Speed / Torque Management (TSC1 Commands)          │
│ - ISO 11783 (ISOBUS Class 3 / TIM) 3-Point Hitch & PTO Coordination    │
│ - ISO 18497 Dual-Path Emergency Stop Supervision (Wired + Wireless RF) │
│ - Fast Hydraulic Dump Valve Venting (< 150 ms to Tank on Fault)       │
│ - Spring-Applied Pressure-Released (SAPR) Mechanical Brake Trigger     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │ Hardwired Physical Actuation Lines
                                   ▼
          Electro-Hydraulic Valves • SAPR Brakes • Engine ECU • Horn/Strobes
```

---

## 2. Component Boundaries & Responsibilities

### 2.1. Hard Real-Time Safety Controller (Domain 2)
* **Execution Environment:** Bare-metal or RTOS (SafeRTOS / OSEK / certified C runtime) executing at a guaranteed $100\text{ Hz}$ cycle ($10.0\text{ ms} \pm 0.1\text{ ms}$ jitter).
* **Authority:** Holds ultimate actuation authority over the tractor's physical electro-hydraulic valves, brake dump solenoids, and engine fuel cutoffs.
* **Watchdogs:**
  * Monitors hardware heartbeat from the NVIDIA Jetson autonomy computer. If setpoints stop arriving for $> 100\text{ ms}$, the safety controller drops the tractor to **SAFE_STOP**.
  * Monitors wireless RF E-stop remote heartbeat. If RF signal drops for $> 500\text{ ms}$, triggers **Category 0 Stop**.
  * Monitors dual-channel Wheel Angle Sensor (WAS) plausibility: $V_1 + V_2 = 5.0\text{V} \pm 0.1\text{V}$. If disagreement occurs, triggers immediate hydraulic disconnect.

### 2.2. Soft Real-Time Autonomy Compute (Domain 1)
* **Execution Environment:** NVIDIA Jetson AGX Orin Industrial running Linux with `PREEMPT_RT` patch and ROS 2 middleware using CycloneDDS and shared-memory (Iceoryx) transport.
* **Perception & State Estimation:** Runs the 15-state Error-State EKF, camera deep learning inference, radar Doppler filtering, and LiDAR canopy profiling.
* **Planning:** Generates coverage swaths, headlands, and non-holonomic $\Omega$-turn paths via Fields2Cover.
* **NMPC Local Solver:** Formulates and solves the non-linear receding horizon optimal control problem at $20\text{ Hz}$ using **acados**, streaming kinematic setpoints to Domain 2.
* **Local Connectivity:** Hosts an onboard industrial Wi-Fi Access Point (AP), allowing direct tablet connection without cell tower availability.

### 2.3. Rugged Android Operator Tablet
* Connects locally via direct Wi-Fi AP or remotely via cellular cloud bridge.
* Displays high-contrast outdoor day UI, RTK accuracy, live position, sensor health, and latched alarms.
* Sends authorized high-level mission requests (Start, Pause, Resume, Abort). **Never carries low-latency steering, braking, or primary safety responsibilities.**

### 2.4. Cloud Infrastructure (Supervisory Only)
* Provides device identity registry, PKI certificate authority, mission archiving, and post-mission analytics.
* Ingests telemetry via **Protobuf over MQTT**.
* Complete cloud loss has zero impact on local autonomous tractor navigation.

---

## 3. Tractor Operating State Machine

```
              ┌──────────────┐
              │  BOOT_CHECK  │
              └──────┬───────┘
                     │ All self-tests pass (WAS, RTK, E-Stop, CAN)
                     ▼
              ┌──────────────┐      Manual Operator Override
              │  SAFE_STOP   │◄─────────────────────────────────┐
              └──────┬───────┘                                  │
                     │ Operator confirms preflight checks       │
                     ▼                                          │
              ┌──────────────┐                                  │
              │MISSION_READY │                                  │
              └──────┬───────┘                                  │
                     │ Authorized Start Command (RF Remote / App)│
                     ▼                                          │
              ┌──────────────┐                                  │
         ┌───►│  AUTONOMOUS  │                                  │
         │    └──────┬───────┘                                  │
Resume   │           │ Fault or Pause Request                   │
Request  │           ▼                                          │
         │    ┌──────────────┐                                  │
         └────┤    PAUSED    │                                  │
              └──────┬───────┘                                  │
                     │ Severe Sensor/Safety Disagreement        │
                     ▼                                          │
              ┌──────────────┐                                  │
              │FAULT_LATCHED ├──────────────────────────────────┘
              └──────────────┘ (Requires physical inspection & manual reset)
```

---

## 4. Connectivity & Network Loss Policy

1. **Cellular Cloud Link Loss:**
   * Tractor continues autonomous field mission uninterrupted.
   * Telemetry is buffered locally in an on-device SQLite database.
   * On cellular reconnection, buffered data is throttled and synced using store-and-forward logic.
2. **Android Tablet Wi-Fi Link Loss:**
   * If local tablet link drops while the mission is running, the tractor continues along its pre-validated swath path **only if the physical wireless RF E-stop remote is within range and its heartbeat is active**.
   * If the wireless E-stop remote is lost, the safety controller executes an immediate controlled stop within $500\text{ ms}$.
3. **Sensor Disagreement / RTK Loss:**
   * If RTK drops from `RTK_FIXED` to `FLOAT` or single-point positioning for $> 1.0\text{ s}$, the vehicle decelerates to creep speed ($0.3\text{ m/s}$).
   * If RTK is not recovered within $3.0\text{ s}$, the tractor enters a controlled **SAFE_STOP** and alerts the operator.
