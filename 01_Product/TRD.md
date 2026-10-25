# Technical Requirements Document (TRD) — Robotrac

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Mandatory Standards:** ISO 18497:2023, ISO 25119 (AgPL d), ISO 11783, ISO 7637-2  

---

## 1. Technical Principles
1. **Local-First Autonomy:** The tractor's navigation, steering, and emergency stop systems are 100% self-contained onboard; zero dependence on internet or cloud infrastructure.
2. **Dual-Domain Compute Architecture:** Hard separation between Soft Real-Time (Linux / ROS 2 on Jetson) and Hard Real-Time (Safety PLC / RTOS on automotive MCU).
3. **Independent Safety Authority:** Ultimate authority over hydraulic dump valves and fuel shutoff resides in hardware-level de-energize circuits, not user-space software.
4. **Protobuf & Low-Bandwidth Resilience:** Telemetry over cellular uses Protocol Buffers with local edge store-and-forward buffering.

---

## 2. System Boundaries & Domains
* **Domain 1 — Soft Real-Time Autonomy (NVIDIA Jetson AGX Orin):**
  * OS: Ubuntu Linux with `PREEMPT_RT` patch.
  * Tasks: Dual-antenna RTK + IMU 15-state ES-EKF pose estimation (20 Hz), optical NIR crop-row segmentation (BiSeNet-V2 @ 30 FPS), 77 GHz radar Doppler clutter filtering, Fields2Cover coverage planner, and NMPC trajectory optimizer (20 Hz).
* **Domain 2 — Hard Real-Time Safety & Actuation (TTControl TTC 580 / IFM):**
  * OS / Runtime: Certified SafeRTOS / C bare-metal loop ($100\text{ Hz}$).
  * Tasks: Dual Hall Wheel Angle Sensor (WAS) ratiometric reading, Danfoss OSPE electro-hydraulic steering valve PWM, SAPR brake pressure dump, SAE J1939 engine throttle (`TSC1`), ISO 11783 (ISOBUS) 3-point hitch coordination, and dual-channel wireless RF remote heartbeat monitoring.
* **Domain 3 — Android Field Tablet:**
  * Native Kotlin Jetpack Compose app connecting directly via tractor's onboard industrial Wi-Fi AP (mDNS / TLS) or cloud MQTT.
  * Renders 100,000 lux outdoor high-contrast day UI; triggers high-priority $2.5\text{ kHz}$ acoustic alarm on tractor stop.
* **Domain 4 — Cloud Supervisory Platform:**
  * FastAPI modular monolith with PostgreSQL / PostGIS and TimescaleDB. Ingests Protobuf telemetry over MQTT; manages device PKI certificates and mission archives.

---

## 3. Mandatory Timing & Latency Budgets

| Subsystem Loop | Execution Frequency | Maximum Allowable Latency (p99) | Jitter Threshold |
| :--- | :--- | :--- | :--- |
| **Safety Controller Main Loop** | $100\text{ Hz}$ | $10.0\text{ ms}$ | $\le \pm 0.1\text{ ms}$ |
| **WAS Reading & Cross-Check** | $100\text{ Hz}$ | $5.0\text{ ms}$ | $\le \pm 0.1\text{ ms}$ |
| **Hydraulic Dump Valve Venting** | On Trip Event | $\le 150\text{ ms}$ to zero pressure | N/A |
| **Wireless RF E-Stop Trip** | Continuous | $\le 500\text{ ms}$ on loss of signal | N/A |
| **ES-EKF Pose & Tilt Fusion** | $200\text{ Hz}$ (IMU) / $20\text{ Hz}$ (RTK) | $15.0\text{ ms}$ | $\le \pm 2.0\text{ ms}$ |
| **NMPC Optimal Control Solve** | $20\text{ Hz}$ | $20.0\text{ ms}$ (acados RTI) | $\le \pm 3.0\text{ ms}$ |
| **Optical Row Perception** | $30\text{ FPS}$ | $33.0\text{ ms}$ (TensorRT INT8) | $\le \pm 5.0\text{ ms}$ |
| **Local Wi-Fi Telemetry Stream** | $10\text{ Hz}$ | $\le 100\text{ ms}$ | $\le \pm 20.0\text{ ms}$ |

---

## 4. Availability & Fault Recovery Policy
* **Stale Message Invalidation:** Any trajectory setpoint older than $100\text{ ms}$ is discarded by the Safety Controller, dropping the tractor to `SAFE_STOP`.
* **Sensor Disagreement:** If dual WAS channels disagree by $> 0.1\text{V}$, or RTK accuracy degrades from fixed to float ($> 10\text{ cm}$) for $> 1.0\text{ s}$, the vehicle decelerates to creep speed ($0.3\text{ m/s}$) and halts within $3.0\text{ s}$.
* **Latched Fault State:** Category 0 emergency stops remain mechanically and electronically latched. Recovery requires physical walkaround inspection and a deliberate two-step authorization gesture.

---

## 5. Engineering Deliverables & Compliance Verification
PRD, TRD, system architecture diagrams, ADRs, ISO 25119 HARA risk assessment, ISO 18497 safety concept, open-source reference matrix, BOM, electrical schematic (ISO 7637-2 compliant), NMPC controller validation logs, and 50-hour proving-ground trial sign-off.

