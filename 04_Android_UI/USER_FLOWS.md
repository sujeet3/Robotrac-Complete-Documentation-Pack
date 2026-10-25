# Robotrac Operator User Flows Specification

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  

---

## Flow A — Pair Device (Cloud or Local AP Mode)
* **Cloud Mode:** Sign in → select organization → scan provisioning QR code → download mTLS client certificate → link established.
* **Direct Local Wi-Fi Mode (Zero-Cellular Field):** Operator scans tractor's physical provisioning QR code (SSID: `Robotrac-AP-XXXX`, WPA3-Personal passphrase) → tablet connects directly to onboard industrial Wi-Fi router → verifies local mTLS fingerprint → establishes direct streaming session.

## Flow B — Prepare & Validate Mission Plan
Select tractor → load GeoJSON field boundary → configure row spacing ($w_{row}$), implement width, and headland turning radius → Fields2Cover generates swaths and $\Omega$-turns → review terrain slope warnings → operator approves plan version.

## Flow C — Preflight & Autonomous Motion Authorization (ISO 18497)
1. **Preflight Safety Gate:** App verifies:
   * Dual-antenna RTK status (`RTK_FIXED`, error $< 2.5\text{ cm}$).
   * Tactical IMU terrain compensation active.
   * Safety Controller online with zero active latched faults.
   * Handheld Wireless RF E-stop remote heartbeat confirmed active ($\Delta t < 150\text{ ms}$).
   * Tractor in `MISSION_READY` state.
2. **Slide-to-Start Authorization:** Operator executes horizontal slide gesture → command dispatched with idempotency key.
3. **Mandatory 3-Second Warning:** Tractor initiates ISO 18497 safety sequence: sounds 100 dB acoustic horn and flashes amber strobe for $3.0\text{ seconds}$ before releasing SAPR brakes and engaging steering.

## Flow D — In-Mission Monitoring & Dynamic Alert Escalation
Tablet displays high-contrast overview map with live tractor pose, front knuckle angle $\delta$, implement status, and radar-tracked obstacle vectors.
* **Zone 3 Breach:** Amber alert on screen, beacon flashes rapidly.
* **Zone 2 Breach:** Vehicle decelerates to $0.3\text{ m/s}$, horn chirps.
* **Zone 1 Breach:** Tractor executes Category 0 E-Stop; tablet triggers continuous $2.5\text{ kHz}$ siren and persistent haptic vibration.

## Flow E — Network Loss & Safe Continuing Policy
* **Cloud Cellular Drop:** Screen displays `OPERATING LOCALLY — CLOUD UNREACHABLE`. Mission continues uninterrupted as long as tractor internal safety checks pass and wireless RF remote is within range.
* **Local Wi-Fi Drop:** Screen displays `TABLET DISCONNECTED — SUPERVISION TRANSFERRED TO RF REMOTE`. Tractor continues current swath; operator retains emergency stop capability via the physical wireless remote.

## Flow F — Mission Completion & Implement Safe Parking
Upon swath completion, planner raises the 3-point hitch, disengages PTO, centers steering knuckle, applies SAPR mechanical brakes, and transitions tractor state to `SAFE_STOP`. Tablet generates final coverage report (hectares worked, cross-track error distribution, fuel/battery consumed).

