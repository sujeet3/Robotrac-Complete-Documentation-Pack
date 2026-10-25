# Robotrac API & Telemetry Protocol Specification

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Protocols:** HTTPS / REST, MQTT over TLS (QoS 1 with Protobuf), Local WSS (WebSocket over TLS)  

---

## 1. Transport & Protocol Architecture

To withstand rural 2G/4G cellular constraints (patchy coverage, latency, data cost), Robotrac uses a dual-protocol transport:

1. **High-Frequency Telemetry (Onboard → Cloud / Tablet):**
   * **Protocol:** Protocol Buffers (Protobuf v3) serialized payloads over **MQTT with QoS 1** (Cloud) or direct binary WebSocket (Local Wi-Fi AP).
   * **Payload Compression:** $\approx 85\%$ smaller than equivalent JSON, reducing cellular data to $< 50\text{ MB}$ per 10-hour working shift.
2. **Transactional & Command Control (Tablet / Cloud → Onboard):**
   * **Protocol:** HTTPS REST with mTLS and JSON schemas for mission uploads, device pairing, and authenticated intent requests.

---

## 2. Telemetry Protocol Buffer Definition (`telemetry.proto`)

```protobuf
syntax = "proto3";
package robotrac.telemetry.v1;

enum VehicleMode {
  MODE_UNSPECIFIED = 0;
  MODE_BOOT_CHECK = 1;
  MODE_SAFE_STOP = 2;
  MODE_MANUAL = 3;
  MODE_MISSION_READY = 4;
  MODE_AUTONOMOUS = 5;
  MODE_PAUSED = 6;
  MODE_FAULT_LATCHED = 7;
}

enum GnssFixType {
  FIX_NONE = 0;
  FIX_SINGLE = 1;
  FIX_FLOAT = 2;
  FIX_RTK_FIXED = 3;
}

message TractorTelemetry {
  uint32 schema_version = 1;
  string device_id = 2;
  uint64 sequence_number = 3;
  int64 timestamp_utc_ms = 4;
  VehicleMode mode = 5;

  message Pose {
    double latitude = 1;
    double longitude = 2;
    float altitude_m = 3;
    float heading_deg = 4;        // Static dual-antenna heading
    float speed_mps = 5;          // Ground speed (radar/RTK fused)
    float roll_deg = 6;           // IMU dynamic terrain roll
    float pitch_deg = 7;          // IMU dynamic terrain pitch
    float cross_track_error_m = 8;// Lateral offset from current swath
    float position_std_dev_m = 9; // RTK accuracy (e.g. 0.018m)
    GnssFixType gnss_fix = 10;
  }
  Pose pose = 6;

  message ActuationHealth {
    float wheel_angle_deg = 1;    // Front knuckle angle from WAS
    float target_wheel_angle_deg = 2; // Commanded angle from NMPC
    float hydraulic_pressure_bar = 3;
    bool sapr_brake_engaged = 4;
    bool wireless_estop_heartbeat_ok = 5;
    uint32 estop_heartbeat_age_ms = 6;
  }
  ActuationHealth actuation = 7;

  message ObstacleStatus {
    uint32 tracked_obstacles_count = 1;
    bool zone1_breach = 2;        // Immediate Category 0 Stop active
    bool zone2_breach = 3;        // Deceleration active
    bool zone3_breach = 4;        // Warning active
  }
  ObstacleStatus obstacles = 8;
}
```

---

## 3. REST & Streaming Endpoints

| Method | Path | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| POST | `/api/v1/devices/enroll` | HTTPS mTLS | Device enrollment & PKI certificate issuance |
| GET | `/api/v1/devices/{device_id}/health` | HTTPS | Hardware subsystem health snapshot |
| POST | `/api/v1/devices/{device_id}/commands` | HTTPS | Submit authorized high-level command (Start, Pause, Stop) |
| GET | `/api/v1/missions` | HTTPS | Query approved mission plans and boundaries |
| POST | `/api/v1/missions/validate` | HTTPS | Validate boundary polygon, swaths, and implement envelopes |
| POST | `/api/v1/telemetry/sync` | HTTPS / Chunked | Batch upload offline telemetry from on-device SQLite buffer |
| GET | `/api/v1/ntrip/mountpoint` | TCP / NTRIP | CORS RTK correction proxy stream (RTCM 3.x messages) |
| SUB | `devices/{device_id}/telemetry` | MQTT (QoS 1) | Live binary Protobuf telemetry stream |
| SUB | `devices/{device_id}/alarms` | MQTT (QoS 2) | Real-time safety faults and latched E-stop notifications |
| WS | `/ws/v1/live` (Local AP) | WSS (Local TLS) | Zero-cloud direct local tablet streaming at 10 Hz |

---

## 4. Edge Store-and-Forward Telemetry Buffering

When the tractor operates in cellular dead zones:
1. **Local Ring Buffer:** The onboard computer serializes telemetry samples into an encrypted local **SQLite / DuckDB** circular buffer (retention: 72 operational hours).
2. **Reconnection Handshake:** Once 4G LTE or depot Wi-Fi is restored, the edge sync agent throttles and streams backlogged blocks in compressed chunks to `/api/v1/telemetry/sync`.
3. **De-duplication:** Cloud ingestion matches `(device_id, sequence_number)` to eliminate duplicate samples.

