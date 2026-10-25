# Product Requirements Document (PRD) — Robotrac

**Version:** 0.1 · **Status:** Draft for senior review

## 1. Product summary
Robotrac is a proposed autonomous agricultural tractor system intended to perceive crop rows and obstacles, navigate within a field, execute approved missions, and expose live monitoring and authorized intervention through an Android app. A cloud backend manages users, devices, mission records, telemetry, reports and configuration.

## 2. Problem statement
Manual operation and inconsistent navigation can constrain repeatability and automation in agricultural tasks. Robotrac aims to provide a modular platform where perception, localization, planning, vehicle control, safety supervision, and future implement automation can be developed and validated incrementally.

## 3. Target users
- Tractor operator / field supervisor
- Farm owner / fleet manager
- Robotics technician / maintainer
- ML engineer / autonomy developer
- System administrator / safety reviewer

## 4. Product goals
1. Detect crop rows, crop/weed classes where data supports it, and relevant obstacles.
2. Estimate vehicle pose and motion with health/confidence information.
3. Plan and follow a path inside a validated field boundary.
4. Support mission lifecycle: draft, validate, approve, execute, pause, resume request, cancel, report.
5. Show live position, mode, sensor health, safety state, alerts and connectivity in Android.
6. Keep low-latency control and safety decisions onboard.
7. Operate safely under specified degraded conditions and report faults clearly.
8. Add implement automation later through explicit capability modules.

## 5. MVP scope
**MVP-0 (software only):** simulator, field map, row geometry, obstacle injection, telemetry schema, API stub, Android/web UI prototype.
**MVP-1 (integration):** backend authentication, device registry, mission management, WebSocket telemetry, audit events.
**MVP-2 (perception):** dataset and crop-row/obstacle detection evaluation using recorded or staged data.
**MVP-3 (bench):** sensor/vehicle adapter interfaces and hardware-in-loop tests with actuators disabled or on a safe rig.
**MVP-4 (field validation):** only after independent safety review, supplier compatibility and legal checks; supervised, low-speed, controlled trials.

## 6. Out of scope initially
- Public-road autonomous driving
- Unsupervised operation without an approved safety case
- Remote cloud direct control of steering, throttle or brakes
- Weed removal/spraying/fertilizer actuation before navigation and safety are validated
- Claiming simulation metrics as physical performance

## 7. Functional requirements
| ID | Requirement | Priority | Verification |
|---|---|---:|---|
| FR-001 | Register a device with unique identity | P0 | API/integration test |
| FR-002 | Report timestamped telemetry and sensor health | P0 | Schema + reconnect tests |
| FR-003 | Display live map, mode, speed, pose confidence and connection age | P0 | UI test |
| FR-004 | Create and validate mission drafts without moving hardware | P0 | Planner tests |
| FR-005 | Reject mission paths outside configured boundaries/no-go zones | P0 | Simulation tests |
| FR-006 | Detect stale sensor data and publish explicit fault state | P0 | Fault injection |
| FR-007 | Provide high-level pause/cancel/stop request controls | P0 | Authorization and HIL tests |
| FR-008 | Record command request, acceptance/rejection and acknowledgement | P0 | Audit test |
| FR-009 | Reconnect telemetry stream and indicate stale data | P0 | Network test |
| FR-010 | Automated 3-Point Hitch & PTO headland turn sequencing | P0 | ISOBUS / HIL validation |
| FR-011 | ISO 18497 multi-zone collision avoidance (Zones 1, 2, 3) | P0 | Proving ground obstacle test |
| FR-012 | Support versioned device configuration and rollback | P1 | Release test |
| FR-013 | Store mission reports, telemetry buffer, and fault timelines | P1 | Integration test |
| FR-014 | Crop/weed classification and canopy density estimation | P1 | ML evaluation |

## 8. Non-functional requirements (Mandatory Standards)
- **Functional Safety:** Architecture must achieve **ISO 25119 AgPL d / Category 3** on all steering, braking, and throttle shutoff circuits.
- **Autonomous Safety Envelopes:** Compliance with **ISO 18497:2023**; mandatory wireless safety remote with $< 500\text{ ms}$ loss-of-heartbeat trip.
- **Electrical Transients:** Immunity to alternator load dumps (+100V) and cranking drops (6V) per **ISO 7637-2**.
- **Availability:** Local autonomy execution must be 100% independent of internet or cellular connection.
- **Usability:** Outdoor sunlight-readable UI ($\ge 100,000\text{ lux}$ contrast), glove-compatible controls ($> 56\text{ dp}$), and high-decibel acoustic alarms.

## 9. Success metrics & Acceptance Thresholds
- **Pass-to-Pass Accuracy:** Cross-track error $e_y \le \pm 2.5\text{ cm}$ ($95\%$ confidence on flat terrain, $\le \pm 5.0\text{ cm}$ on $10^\circ$ slope).
- **Static Heading Accuracy:** $\sigma_\psi \le 0.09^\circ$ at $0\text{ m/s}$ forward velocity.
- **Dynamic Terrain Tilt Compensation:** Lateral ground-point error $\le 2.0\text{ cm}$ on uneven furrows.
- **Obstacle Detection Reliability:** $100\%$ recall for human-sized obstacles in Zone 1; $< 1$ false-positive stop per 10 hours in dust plumes.
- **Actuator Safe-State Response:** Hydraulic dump valve venting $\le 150\text{ ms}$; mechanical SAPR brake full lock $\le 250\text{ ms}$.
- **Local Control Latency:** NMPC solver iteration $\le 20\text{ ms}$; Safety Controller cycle $10.0\text{ ms} \pm 0.1\text{ ms}$.

## 10. Assumptions and dependencies
- Tractor platform equipped with Electro-Hydraulic Load Sensing (CCLS) steering or compatible manifold retrofit.
- Dual-antenna RTK setup with accessible NTRIP correction service or local base station.
- Testing conducted under controlled proving-ground conditions with a certified safety driver and perimeter wireless remote.

## 11. Release acceptance
A release is field-ready only when SIL simulation, sub-scale electric mule tests, stationary HIL valve calibration, and 50 continuous proving-ground hours have been formally signed off by the lead agricultural safety engineer.
