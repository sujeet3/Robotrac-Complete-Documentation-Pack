# Proposed Repository File Structure

```text
robotrac/
├── README.md
├── docs/
│   ├── product/PRD.md
│   ├── product/TRD.md
│   ├── architecture/SYSTEM_ARCHITECTURE.md
│   ├── architecture/ADR.md
│   ├── api/API_SPECIFICATION.md
│   ├── api/openapi.yaml
│   ├── hardware/HARDWARE_BOM.md
│   ├── ai/ALGORITHMS.md
│   ├── ai/ML_PLAN.md
│   └── safety/SECURITY_AND_SAFETY.md
├── apps/
│   └── android/
│       ├── app/
│       ├── feature-overview/
│       ├── feature-map/
│       ├── feature-missions/
│       ├── feature-alerts/
│       ├── feature-settings/
│       ├── core-network/
│       ├── core-auth/
│       ├── core-model/
│       └── src/test/
├── services/
│   └── cloud-api/
│       ├── app/
│       │   ├── api/v1/
│       │   ├── auth/
│       │   ├── devices/
│       │   ├── missions/
│       │   ├── telemetry/
│       │   ├── commands/
│       │   ├── audit/
│       │   ├── db/
│       │   ├── schemas/
│       │   └── main.py
│       ├── migrations/
│       ├── tests/
│       ├── pyproject.toml
│       └── Dockerfile
├── onboard/
│   ├── bringup/
│   ├── drivers/
│   ├── localization/
│   ├── perception/
│   ├── planning/
│   ├── control/
│   ├── safety_supervisor/
│   ├── vehicle_adapter/
│   ├── telemetry/
│   ├── config/
│   ├── launch/
│   └── tests/
├── ml/
│   ├── datasets/README.md
│   ├── annotations/
│   ├── training/
│   ├── evaluation/
│   ├── export/
│   ├── model_cards/
│   └── experiments/README.md
├── simulation/
│   ├── world/
│   ├── tractor_model/
│   ├── field_generator/
│   ├── scenarios/
│   ├── fault_injection/
│   └── tests/
├── shared/
│   ├── schemas/
│   ├── messages/
│   └── units/
├── infra/
│   ├── docker/
│   ├── deployment/
│   ├── monitoring/
│   └── secrets/README.md
├── tests/
│   ├── contract/
│   ├── integration/
│   ├── security/
│   └── system/
├── .github/workflows/
├── .gitignore
└── SECURITY.md
```

## Rules
- Do not commit `.env`, private keys, APK signing keys, device credentials, real farm personal data or unapproved datasets.
- Keep hardware drivers behind interfaces; simulation drivers must be easy to select.
- Version API schemas and configuration.
- Add unit tests beside each module and integration tests at boundaries.
- Keep model artifacts in an approved artifact store, not necessarily Git.
- Every production release must identify app, onboard, backend, model and configuration versions.
