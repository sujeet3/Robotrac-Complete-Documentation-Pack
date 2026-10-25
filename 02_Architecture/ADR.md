# Architecture Decision Records (ADR)

## ADR-001 — Hybrid local-first architecture
**Status:** Proposed  
**Decision:** Onboard computer runs autonomy; Android monitors/requests high-level actions; cloud manages devices, missions, logs and reports.  
**Reason:** Network latency/outages should not be part of the local control loop.  
**Consequences:** More onboard engineering; requires clear local/offline UX and device provisioning.

## ADR-002 — Dual-language autonomy & hard real-time split
**Status:** Approved  
**Decision:** Partition software across two domains: Python/C++ under Linux/ROS 2 on NVIDIA Jetson for high-level perception and planning (Soft Real-Time); MISRA-compliant C / RTOS on an automotive safety microcontroller (TTControl/IFM) for closed-loop valve control, WAS reading, and E-stop supervision at 100 Hz (Hard Real-Time).  
**Reason:** Python GIL and Linux scheduling jitter introduce unacceptable 20–100 ms pauses that violate functional safety when driving physical hydraulic steering valves.  

## ADR-003 — ROS 2 candidate for hardware abstraction
**Status:** Approved  
**Decision:** Adopt ROS 2 (Jazzy / Iron LTS) with CycloneDDS and Iceoryx zero-copy transport for perception, sensor drivers, and planning.  
**Reason:** Industry-standard modular robotics middleware with extensive driver support and Gazebo simulation integration.  

## ADR-004 — Kotlin production app
**Status:** Approved  
**Decision:** Prefer native Kotlin Jetpack Compose for production Android field tablet UI.  
**Reason:** Direct hardware lifecycle control, high-contrast canvas rendering, and zero-latency local Wi-Fi TLS streaming.  

## ADR-005 — Modular monolith backend
**Status:** Approved  
**Decision:** Single deployable FastAPI backend with PostgreSQL / PostGIS and TimescaleDB extension.  
**Reason:** Avoid premature microservices complexity while maintaining strong modular boundaries.  

## ADR-006 — Dual-antenna moving baseline RTK for static heading
**Status:** Approved  
**Decision:** Mandate dual-antenna RTK-GNSS (Septentrio / dual u-blox ZED-F9P) across a fixed 1.2m baseline.  
**Reason:** Single-antenna GNSS heading fails during low-speed field crawl (< 0.5 m/s) and experiences magnetic distortion from heavy tractor chassis steel. Dual-antenna carrier phase double-differencing provides true heading at 0 m/s.  

## ADR-007 — Non-linear model predictive control (NMPC) over kinematic Stanley
**Status:** Approved  
**Decision:** Adopt NMPC with loose-soil tire slip dynamics solved via acados (RTI @ 20 Hz).  
**Reason:** Kinematic Stanley/Pure Pursuit controllers assume zero lateral slip, causing steady-state tracking errors of 15–30 cm on agricultural side-slopes and tilled soil.  

## ADR-008 — Fields2Cover library for agricultural coverage planning
**Status:** Approved  
**Decision:** Integrate Fields2Cover for swath generation, headland buffer generation, and non-holonomic turning curves (Ω-turns, Dubins/Reeds-Shepp).  
**Reason:** Agricultural fields require implement-constrained turning maneuvers and swath ordering that standard 2D path planners cannot generate.  

## ADR-009 — Protobuf and MQTT with store-and-forward for field telemetry
**Status:** Approved  
**Decision:** Replace verbose JSON WebSockets with Protocol Buffers (Protobuf) over MQTT (QoS 1) with an edge SQLite buffer.  
**Reason:** Rural cellular networks are bandwidth-constrained and intermittent. Protobuf reduces payload sizes by 85%, and local buffering prevents telemetry loss during cellular blackouts.
