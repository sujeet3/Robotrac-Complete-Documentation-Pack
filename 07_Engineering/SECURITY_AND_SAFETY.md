# Security and Functional Safety Specification

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Mandatory Standards:** ISO 18497:2023, ISO 25119 (AgPL d / Category 3), ISO 11783, ISO 7637-2  

---

## 1. Functional Safety Architecture (ISO 25119 AgPL d)

The steering, braking, engine throttle, and hydraulic dump circuits are categorized as **AgPL d (Agricultural Performance Level d / Category 3)** per ISO 25119-2:

```text
               ┌─────────────────────────────────────────────────────────┐
               │ Multi-Channel Power Source (Main 12V/24V + Battery Cut) │
               └────────────┬───────────────────────────────┬────────────┘
                            │                               │
                            ▼                               ▼
                 ┌──────────────────────┐        ┌──────────────────────┐
                 │ Safety MCU Channel A │◄──────►│ Safety MCU Channel B │
                 │ (High-Side Switch)   │ Cross- │ (Low-Side Switch)    │
                 └──────────┬───────────┘ Check  └──────────┬───────────┘
                            │                               │
                            └───────────────┬───────────────┘
                                            ▼
                      ┌───────────────────────────────────────────┐
                      │ Dual-Coil Failsafe Dump Valve             │
                      │ & Spring-Applied Emergency Brake Actuator │
                      └───────────────────────────────────────────┘
```

1. **Dual-Channel Actuator De-energize:**
   * High-side and low-side driver switches are independently controlled by isolated microcontroller cores.
   * If either channel detects a watchdog timeout, WAS sensor mismatch ($|V_1 + V_2 - 5.0\text{V}| > 0.1\text{V}$), or CAN setpoint stall, the circuit de-energizes within $< 10\text{ ms}$.
2. **Fail-Safe Hydraulic Dump Valve:**
   * Venting time to hydraulic tank is $\le 150\text{ ms}$, dropping steering cylinder pressure to zero and latching the mechanical steering lock.
3. **Mechanical SAPR Brake Engagement:**
   * Emergency braking relies on Spring-Applied, Pressure-Released (SAPR) mechanics. Hydraulic pressure release mechanically forces brake pads into friction lock, halting the tractor regardless of electrical bus collapse.

---

## 2. ISO 18497 Autonomous Perception Envelopes

The vehicle maintains dynamic, speed-dependent perception zones around its swept path and implement width:

```text
       ▲ Forward Travel Direction
       │
┌──────┴──────────────────────────────────────────────────────┐
│ ZONE 3: Warning Envelope (Range: L_Zone2 + 10.0 m)          │
│ Reaction: 360° Amber Strobe Beacon flashes + 90 dB Horn      │
├─────────────────────────────────────────────────────────────┤
│ ZONE 2: Deceleration Envelope (Range: L_Zone1 + 5.0 m)       │
│ Reaction: Modulated Service Brake decels vehicle to 0.3 m/s │
├─────────────────────────────────────────────────────────────┤
│ ZONE 1: Immediate Stopping Envelope (Range: L_stop)         │
│ Reaction: Category 0 E-Stop • Hydraulic Dump • Full Brake   │
├─────────────────────────────────────────────────────────────┤
│                 TRACTOR CHASSIS & IMPLEMENT                 │
└─────────────────────────────────────────────────────────────┘
```

### 2.1. Stopping Distance Calculation (Zone 1)
$$L_{Zone1} = v_x \cdot t_{system\_reaction} + \frac{v_x^2}{2 \cdot a_{decel}} + d_{safety\_margin}$$
* For maximum field speed $v_x = 2.5\text{ m/s}$ ($9.0\text{ km/h}$), reaction latency $t_{system} = 0.25\text{ s}$, deceleration $a_{decel} = 2.0\text{ m/s}^2$, and margin $d_{margin} = 1.0\text{ m}$:
  $$L_{Zone1} = (2.5 \cdot 0.25) + \frac{6.25}{4.0} + 1.0 = 0.625 + 1.56 + 1.0 = \mathbf{3.19\text{ m}}$$
* Any solid obstacle crossing Zone 1 boundary triggers an instantaneous **Category 0 Stop**.

---

## 3. Dual-Path Emergency Stop & Heartbeat Supervision

1. **Wired Safety Loop (Vehicle Body):**
   * Red mushroom pushbuttons on left fender, right fender, and cab interior wired in a normally-closed (NC) series dual-channel safety relay circuit.
2. **Industrial Wireless Safety Remote (Mandatory ISO 18497):**
   * **Hardware:** Certified handheld safety transmitter (HBC-radiomatic quadrix / Hetronic Nova).
   * **RF Protocol:** Deterministic 868 / 915 MHz frequency-hopping spread spectrum with rolling sequence counter.
   * **RF Heartbeat Ping:** Transmitter sends a keep-alive token every $100–150\text{ ms}$.
   * **Automatic Trip Condition:** If the safety controller fails to receive a valid RF heartbeat for $> 500\text{ ms}$ (due to operator collapse, out-of-range, or RF jam), the tractor **immediately executes an automatic Category 0 Emergency Safe Stop**.

---

## 4. Vehicle Warning Envelopes (Prior to Autonomous Motion)

Per ISO 18497 requirements:
1. **Startup Warning Sequence:**
   * When an autonomous mission start is authorized, the tractor remains stationary for **$3.0\text{ seconds}$** while sounding a pulsating $85–100\text{ dBA}$ acoustic alarm horn and flashing the $360^\circ$ amber strobe beacon.
2. **Implement Guarding:**
   * Rotating PTO shafts and implement cutting bars must have physical safety interlock switches that inhibit autonomous engine throttle if guards are open.

---

## 5. Cyber Security & Cryptographic Integrity

1. **PKI Device Identity:**
   * Each tractor carries an onboard hardware secure element (NVIDIA Jetson TPM 2.0 / ATECC608B) storing an isolated ECC private key.
   * Mutual TLS (mTLS) with client certificate authentication for all telemetry and cloud API calls.
2. **Command Anti-Replay & Authorization:**
   * Every high-level command (`REQUEST_MISSION_START`, `PAUSE_MISSION`) requires:
     * High-entropy `idempotency_key`.
     * Nanosecond UTC timestamp with a strict $\le 5.0\text{ second}$ expiration window.
     * Monotonic command sequence counter per device.
3. **Firmware & Model Signatures:**
   * All ROS 2 node binaries, micro-ROS firmware, and AI model weights (`.engine` / `.onnx`) must be cryptographically signed using Ed25519 keys; unsigned binaries are rejected by the bootloader.

