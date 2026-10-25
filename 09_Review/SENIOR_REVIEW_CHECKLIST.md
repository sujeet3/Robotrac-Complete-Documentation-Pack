# Senior Review Checklist

## Product
- [ ] First crop and task selected
- [ ] Tractor type, field, terrain, speed and implement constraints documented
- [ ] Success metrics and acceptance thresholds agreed
- [ ] Out-of-scope items agreed

## Architecture
- [ ] Onboard/cloud/Android boundaries approved
- [ ] Local operation and network-loss policy reviewed
- [ ] ROS 2, Python and Android stack approved
- [ ] Go decision based on measurable benchmark criteria
- [ ] API/data schema versioning approved

## Hardware
- [ ] Tractor and supplier interfaces documented
- [ ] Steering/braking/implement third-party access confirmed in writing
- [ ] Compute, camera, RTK, IMU and range sensor shortlisted
- [ ] Power, enclosure, vibration and environment reviewed
- [ ] Safety controller/E-stop design owner assigned

## AI/ML
- [ ] Dataset plan and annotation policy approved
- [ ] Train/validation/test split avoids field/session leakage
- [ ] Metrics per crop, stage, lighting and range agreed
- [ ] Model card and rollback requirements agreed
- [ ] ML is not sole safety barrier

## API/security
- [ ] Human/device authentication model approved
- [ ] Roles, revocation and rotation designed
- [ ] No secrets in repo/APK
- [ ] Command expiry/idempotency/audit approved
- [ ] Local/cloud TLS and pairing reviewed

## Validation
- [ ] Simulation and fault scenarios approved
- [ ] SIL/HIL strategy approved
- [ ] Hazard analysis and safety case owner assigned
- [ ] Field trial gates, safety driver and E-stop plan approved
- [ ] Applicable standards/local rules reviewed

Reviewer: ____________________  Date: __________  Decision: Approve / Revise / Reject
