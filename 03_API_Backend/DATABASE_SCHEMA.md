# Database Schema Specification (PostgreSQL + PostGIS + TimescaleDB)

**Status:** Technical Baseline Specification · **Review Level:** High-Integrity Autonomous Agricultural Machine  
**Database Engines:** PostgreSQL 16+ with **PostGIS 3.4** (Geospatial) and **TimescaleDB** (High-Frequency Time-Series)  

---

## 1. Relational & Geospatial Schema (DDL)

```sql
-- Enable Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Organizations & Multi-Tenant Registry
CREATE TABLE organizations (
    org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users & Role-Based Access Control
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(org_id),
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    role VARCHAR(50) CHECK (role IN ('VIEWER', 'OPERATOR', 'MAINTAINER', 'ADMIN')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Registered Autonomous Vehicles
CREATE TABLE devices (
    device_id VARCHAR(64) PRIMARY KEY,
    org_id UUID REFERENCES organizations(org_id),
    serial_number VARCHAR(128) UNIQUE NOT NULL,
    tractor_model VARCHAR(128),
    hardware_revision VARCHAR(64),
    software_version VARCHAR(64),
    firmware_version VARCHAR(64),
    capabilities_json JSONB,
    status VARCHAR(50) DEFAULT 'OFFLINE',
    last_seen_at TIMESTAMPTZ
);

-- Device Public Key Infrastructure (mTLS)
CREATE TABLE device_credentials (
    credential_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(64) REFERENCES devices(device_id),
    public_key_pem TEXT NOT NULL,
    fingerprint VARCHAR(128) UNIQUE NOT NULL,
    issued_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ
);

-- Field Boundaries & Mission Plans (PostGIS Geometry)
CREATE TABLE missions (
    mission_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(org_id),
    device_id VARCHAR(64) REFERENCES devices(device_id),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'DRAFT', -- DRAFT, APPROVED, EXECUTING, COMPLETED, ABORTED
    boundary_geom GEOMETRY(Polygon, 4326) NOT NULL,        -- Outer field geofence
    no_go_zones_geom GEOMETRY(MultiPolygon, 4326),         -- Internal obstacles / ponds
    swaths_geom GEOMETRY(MultiLineString, 4326),           -- Fields2Cover generated tracks
    implement_width_m NUMERIC(5,2) NOT NULL,
    plan_version INT DEFAULT 1,
    created_by UUID REFERENCES users(user_id),
    approved_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- High-Frequency Telemetry Hypertables (TimescaleDB)
CREATE TABLE telemetry_samples (
    timestamp_utc TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(64) NOT NULL,
    sequence_num BIGINT NOT NULL,
    location_geom GEOMETRY(Point, 4326) NOT NULL,
    altitude_m NUMERIC(6,2),
    heading_deg NUMERIC(5,2),
    speed_mps NUMERIC(4,2),
    roll_deg NUMERIC(5,2),
    pitch_deg NUMERIC(5,2),
    cross_track_error_m NUMERIC(5,3),
    gnss_fix VARCHAR(32),
    wheel_angle_deg NUMERIC(5,2),
    sapr_brake_engaged BOOLEAN,
    mode VARCHAR(32),
    safety_zone_status VARCHAR(32),
    received_at TIMESTAMPTZ DEFAULT NOW()
);
-- Convert to TimescaleDB hypertable partitioned by time (7-day chunks)
SELECT create_hypertable('telemetry_samples', 'timestamp_utc', chunk_time_interval => INTERVAL '7 days');

-- Audit Log & Safety Interventions
CREATE TABLE audit_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id VARCHAR(64) REFERENCES devices(device_id),
    actor_id UUID REFERENCES users(user_id),
    action VARCHAR(64) NOT NULL,
    outcome VARCHAR(32) NOT NULL, -- ACCEPTED, REJECTED, EXECUTED, FAILED
    correlation_id VARCHAR(128),
    details_json JSONB,
    timestamp_utc TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 2. Spatial & Performance Indexing Rules

```sql
-- Spatial GiST Index for boundary geofence lookups
CREATE INDEX idx_missions_boundary ON missions USING GIST(boundary_geom);
CREATE INDEX idx_missions_swaths ON missions USING GIST(swaths_geom);

-- Composite Time-Series & Location Index for Telemetry Queries
CREATE INDEX idx_telemetry_device_time ON telemetry_samples (device_id, timestamp_utc DESC);
CREATE INDEX idx_telemetry_location ON telemetry_samples USING GIST(location_geom);

-- Retention Policy: Compress chunks older than 14 days, drop raw samples after 90 days
SELECT add_compression_policy('telemetry_samples', INTERVAL '14 days');
SELECT add_retention_policy('telemetry_samples', INTERVAL '90 days');
```

