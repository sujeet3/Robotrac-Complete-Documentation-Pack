# Software Stack and Toolchain

| Layer | Candidate | Purpose / notes |
|---|---|---|
| Onboard OS | Ubuntu/Linux image supported by selected computer and ROS 2 | Pin image and kernel; confirm vendor driver support |
| Robotics middleware | ROS 2 distribution selected after compatibility check | Sensor topics, lifecycle, diagnostics, simulation and adapters |
| Autonomy logic | Python 3.11+ | Research, planning, fusion integration and orchestration |
| Perception training | Python, PyTorch, OpenCV | Dataset tooling, training and evaluation |
| Edge inference | ONNX Runtime/TensorRT where supported | Benchmark model accuracy, latency, power and thermal behavior |
| Simulation | Gazebo/Ignition or another reviewed simulator; custom deterministic field simulator | Validate algorithms and fault cases before hardware |
| Backend API | FastAPI initially | REST API, auth integration, validation, OpenAPI |
| Database | PostgreSQL | Users, devices, missions, commands, audit and reports |
| Telemetry | WebSocket; optional queue only if justified | Live streams, reconnection, ordering and buffering |
| Android | Kotlin, Android SDK, Jetpack libraries | Production operator app; WebView prototype can be temporary |
| Map UI | Map library chosen after offline/geospatial licensing review | Field polygons, row geometry and vehicle pose |
| Authentication | OIDC/OAuth2 provider; device certificate/credential provisioning | User and machine identity |
| Secrets | Cloud secret manager and Android Keystore-backed token storage | Never hardcode secrets |
| Build/test | GitHub Actions or equivalent; pytest; Android test tooling; static analysis | Repeatable CI, artifact signing and release |
| Observability | Structured logs, metrics and event IDs | Sensor age, faults, API latency, command lifecycle |
| Optional Go | Cloud gateway/service only if benchmark justifies | Not needed merely to make APK responsive |

## Development environments
- `dev`: simulation and synthetic data, fake credentials.
- `staging`: integration with test devices and non-production credentials.
- `production`: gated releases, signed artifacts, restricted access and backups.

## Language decision
Python first for autonomy/ML research. Benchmark on target hardware. Consider Go for high-throughput cloud ingestion only if evidence shows a need. Android app responsiveness is primarily an app/network/control-placement question, not a backend language choice.
