# Test Strategy and Agricultural Release Gates

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Mandatory Compliance Gates:** ISO 18497, ISO 25119 (AgPL d), ISO 7637-2  

---

## 1. Test Levels & Agricultural Validation Suites

1. **Unit Testing:**
   * Error-State EKF coordinate transforms, quaternion kinematics, and lever-arm dynamic roll/pitch compensation math.
   * Fields2Cover swath geometry, $\Omega$-turn non-holonomic kinematics, and boundary buffer margins.
   * Protobuf schema serialization and edge SQLite ring-buffer FIFO ordering.
2. **Deterministic Simulation (SIL):**
   * Terramechanics soil slip ($10\% - 35\%$), uneven furrow roll oscillations, and implement dynamic drag force injection.
   * Multi-sensor fault injection: RTK carrier-phase cycle slips, direct low-angle solar camera blinding, and dropped CAN frames.
3. **Sub-Scale Electric Mule Testing (Low-Risk Proving Ground):**
   * Field testing on a modified electric UTV or lawn tractor under $5.0\text{ km/h}$.
   * Verification of dual-antenna moving-baseline static yaw accuracy ($\sigma_\psi < 0.1^\circ$).
   * Verification of wireless RF remote heartbeat automatic trip ($< 500\text{ ms}$ upon power disconnect).
4. **Hardware-in-the-Loop (HIL) Bench & Stationary Rig:**
   * Electro-hydraulic proportional steering valve flow-rate mapping, deadband compensation, and hysteresis measurement.
   * Spring-Applied Pressure-Released (SAPR) brake venting time recording with high-speed pressure transducers ($\le 150\text{ ms}$ to tank).
   * Dual-channel WAS sensor plausibility checks ($V_1 + V_2 = 5.0\text{V} \pm 0.1\text{V}$) with simulated short-circuit and open-circuit wire cuts.
5. **Hostile Environment & Environmental Testing:**
   * **Dense Dust Plume Test:** Run tractor behind a disc harrow generating heavy dust clouds. Verify optical sensor degradation triggers radar Doppler cross-validation without uncommanded false stops.
   * **Pneumatic Air-Blast Cleaning Verification:** Validate lens clarity restoration after 1 hour of dry tilling.
   * **Electrical Transient Immunity:** Subject power supply to ISO 7637-2 Pulse 5a/5b (+100V alternator load dump) and 6.0V cranking drop test.
6. **Supervised Full-Scale Field Trials:**
   * Closed-field operation with safety driver in cab and remote wireless E-stop supervisor at field perimeter.
   * Pass-to-pass row tracking evaluation over minimum 50 continuous operational hours.

---

## 2. Release Gate Definitions

* **Gate A — Agronomic Requirements & Safety Concept:** Target crop geometry, tractor hydraulic interface, and ISO 25119 HARA risk register signed off.
* **Gate B — Software & Simulation Acceptance:** 100% automated test pass rate for NMPC solver convergence and Fields2Cover collision avoidance in simulation.
* **Gate C — Sub-Scale Mule Field Acceptance:** Sub-$5.0\text{ cm}$ pass-to-pass tracking and 100% verified wireless RF remote fail-safe trips on electric testbed.
* **Gate D — HIL Actuation & Electrical Safety:** ISO 7637-2 load dump immunity verified; hydraulic dump valve venting verified at $\le 150\text{ ms}$.
* **Gate E — Static Tractor Preflight:** Dual-antenna GNSS heading verified stationary; pre-movement $3.0\text{ s}$ acoustic horn and $360^\circ$ amber beacon verified.
* **Gate F — Supervised Field Proving:** 50 hours of autonomous operation with zero uncommanded steering departures and verified ISO 18497 Zone 1 collision stops.
* **Gate G — Third-Party Compliance:** AgPL d functional safety audit and CE / local agricultural machinery certification.

