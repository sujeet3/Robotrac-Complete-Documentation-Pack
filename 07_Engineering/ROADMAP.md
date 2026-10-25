# Proposed Development Roadmap — Robotrac

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  

---

## Phase 0 — Discovery, Feasibility & Agronomic Requirements
* **Outputs:** Target crop profiles (row spacing, canopy height), tractor platform class (4WD, 75–120 HP), hydraulic type (CCLS vs Open Center), implement interfaces (Cat 2 3-point hitch, 540/1000 RPM PTO), and ISO 25119 HARA risk register.
* **Exit Gate:** Signed PRD/TRD and safety concept approval.

## Phase 1 — Deterministic Simulation MVP (SIL)
* **Build:** Gazebo / O3DE agricultural world, simulated tractor with terramechanics soil slip, Fields2Cover swath generator, and fault-injection suite (RTK degradation, camera glare, obstacle intrusion).
* **Exit Gate:** Repeatable closed-loop swath tracking and simulated ISO 18497 Zone 1 collision stops; zero real actuators.

## Phase 2 — Telemetry Ingestion & Android Operator App MVP
* **Build:** Protobuf over MQTT telemetry streaming, edge SQLite store-and-forward buffer, Android high-contrast outdoor day UI, and local Wi-Fi AP direct pairing.
* **Exit Gate:** Simulated tractor streams live telemetry locally and to cloud; remote pause/stop lifecycle verified under packet loss.

## Phase 3 — Perception Data Collection & Model Training
* **Build:** Multi-crop agricultural dataset (NIR + RGB), annotation pipeline (crop rows, soil, weeds, obstacles), BiSeNet-V2 / MobileNetV4 training, and TensorRT edge optimization.
* **Exit Gate:** Model cards approved with verified precision/recall in both high-noon glare and heavy shadow conditions.

## Phase 3.5 — Drive-by-Wire Sub-Scale Electric Mule Testbed (Critical De-risking)
* **Build:** Retrofit a small electric utility vehicle (UTV) or lawn tractor with dual-antenna RTK-GNSS, tactical IMU, Jetson Orin, Fields2Cover planner, and wireless RF E-stop remote.
* **Run:** Validate real-world sensor fusion, static heading, $\Omega$-turn execution, and wireless E-stop heartbeat trips at $< 5.0\text{ km/h}$ with zero rollover or crush hazard.
* **Exit Gate:** Sub-$5.0\text{ cm}$ pass-to-pass path tracking on actual grass/soil and $100\%$ verified RF E-stop trips on loss of signal.

## Phase 4 — Stationary Tractor Hardware-in-Loop (HIL) Rig
* **Build:** Jacked-up full-size tractor (wheels off ground); plumb Danfoss OSPE steering valve, install dual Hall Wheel Angle Sensor (WAS), wire TTControl safety PLC, and mount SAPR brake actuator.
* **Run:** Hydraulic system identification, valve deadband and hysteresis calibration, CAN J1939 throttle response, and dump valve venting latency ($< 150\text{ ms}$).
* **Exit Gate:** Closed-loop steering step response $\le 150\text{ ms}$; dual-channel safety de-energize circuits independently validated.

## Phase 5 — Supervised Proving-Ground Field Validation
* **Run:** Controlled closed-field trials with safety driver in cab, wireless RF remote supervisor at field perimeter, working 3-point hitch cultivator/sprayer at speeds up to $7.0\text{ km/h}$.
* **Exit Gate:** 50 hours of continuous autonomous field execution without false-positive emergency stops or uncommanded steering deviations.

## Phase 6 — Production Hardening & Regulatory Certification
* **Build:** Cryptographic key provisioning, OTA signed updates, maintenance documentation, and third-party ISO 18497 / ISO 25119 conformity certification.
* **Exit Gate:** Commercial deployment readiness review.

