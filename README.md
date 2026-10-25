# Robotrac — Complete Engineering Documentation Pack

**Version:** 0.1 · **Date:** 25 October 2026 · **Status:** Research / concept review  
**Product vision:** A fully autonomous agricultural tractor with crop-row perception, safe navigation, modular agricultural automation, and an Android monitoring/operator application.

## Important status and safety boundary
The supplied *Robotrac Autopilot Release 1.3* document says the prototype is simulated and has not driven a real tractor. The documents in this pack are proposed starting points for senior review, not certified designs, verified product specifications, or instructions to operate a real machine. No real actuator should be connected until a qualified engineering team has completed hazard analysis, independent safety design, supplier-interface verification, and controlled validation.

## Document index
1. `01_Product/PRD.md` — Product requirements and scope
2. `01_Product/TRD.md` — Technical requirements and quality attributes
3. `02_Architecture/SYSTEM_ARCHITECTURE.md` — Logical architecture, data flow, boundaries
4. `02_Architecture/ADR.md` — Architecture decision records
5. `03_API_Backend/API_SPECIFICATION.md` — Proposed REST/WebSocket contracts
6. `03_API_Backend/openapi.yaml` — Starter OpenAPI 3.1 contract (draft)
7. `03_API_Backend/DATABASE_SCHEMA.md` — Initial data model
8. `04_Android_UI/UI_DESIGN_KIT.md` — UI principles, screens, components and states
9. `04_Android_UI/USER_FLOWS.md` — Key operator flows
10. `05_Hardware_Software/HARDWARE_BOM.md` — Hardware shortlist and procurement gates
11. `05_Hardware_Software/SOFTWARE_STACK.md` — Software stack and toolchain
12. `06_AI_ML_Algorithms/ALGORITHMS.md` — Navigation, perception, control and fusion algorithms
13. `06_AI_ML_Algorithms/ML_PLAN.md` — Dataset, training, evaluation and deployment plan
14. `07_Engineering/FILE_STRUCTURE.md` — Proposed monorepo structure
15. `07_Engineering/TEST_STRATEGY.md` — Simulation, integration, security and field test gates
16. `07_Engineering/SECURITY_AND_SAFETY.md` — Credential model and safety boundaries
17. `07_Engineering/ROADMAP.md` — Phased delivery plan
18. `08_Prompts/END_TO_END_BUILD_PROMPT.md` — Master prompt for coding agents/team
19. `09_Review/SENIOR_REVIEW_CHECKLIST.md` — Review and sign-off checklist
20. `09_Review/OPEN_QUESTIONS.md` — Decisions required before implementation
21. `10_References/SIMILAR_PROJECTS_AND_REFERENCES.md` — Similar projects, open-source references and industry benchmarks

## Recommended review sequence
PRD → TRD → System Architecture/ADRs → Safety & Security → Hardware shortlist → API contract/data model → UI design → Algorithms/ML plan → File structure → Test plan → References & Benchmarks → build prompt.

## Source versus proposal
Source-derived: Release 1.3 lists example sensors, protocols, software modules, a simulated system, and a path to hardware integration. Proposed additions in this pack include the production-oriented hybrid architecture, API contracts, database, UI design kit, repo structure, ML plan, and roadmap. Product selections must be validated with vendors; simulation metrics are not real-world guarantees.

## Core architectural recommendation
- **Onboard computer:** perception, localization, planning, control and local runtime monitoring.
- **Independent safety controller and E-stop path:** safety-critical actuation authority, independent of cloud and Android.
- **Android app:** monitoring, mission setup, alerts and authorized high-level requests.
- **Cloud backend:** identity, device registry, missions, telemetry storage, reports, audit and configuration.
- **Network loss:** cloud loss must not be part of the low-latency steering loop; onboard behavior on faults must be specified and validated.
# Robotrac-Complete-Documentation-Pack
