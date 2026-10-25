#!/usr/bin/env python3
"""
Robotrac Executive Technical Presentation Generator
Generates a native 16:9 widescreen PowerPoint presentation (.pptx) based on the Robotrac engineering documentation.
Requires: pip install python-pptx
"""

import os
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    print("python-pptx is not installed. Run: pip install python-pptx")
    sys.exit(1)

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Dark agricultural executive color palette
    BG_DARK = RGBColor(11, 17, 24)       # #0B1118
    CARD_BG = RGBColor(19, 30, 41)       # #131E29
    CARD_BORDER = RGBColor(31, 48, 66)   # #1F3042
    TEXT_LIGHT = RGBColor(243, 246, 248) # #F3F6F8
    TEXT_MUTED = RGBColor(148, 163, 184) # #94A3B8
    ACCENT_TEAL = RGBColor(16, 185, 129) # #10B981
    ACCENT_CYAN = RGBColor(6, 182, 212)  # #06B6D4
    ACCENT_AMBER = RGBColor(245, 158, 11)# #F59E0B

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()

    def add_header(slide, subtitle, title, badge_text="SPECIFICATION v1.0"):
        # Header text box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(10), Inches(1.3))
        tf = header_box.text_frame
        tf.word_wrap = True
        
        # Subtitle
        p0 = tf.paragraphs[0]
        p0.text = subtitle.upper()
        p0.font.name = "Inter"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        
        # Title
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = "Inter"
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT

        # Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.6), Inches(1.8), Inches(0.45))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(16, 45, 35)
        badge.line.color.rgb = ACCENT_TEAL
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = badge_text
        bp.alignment = PP_ALIGN.CENTER
        bp.font.size = Pt(9)
        bp.font.bold = True
        bp.font.color.rgb = ACCENT_TEAL

    def add_card(slide, left, top, width, height, title, items):
        # Card shape
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        
        # Text
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.3)
        tf.margin_top = Inches(0.3)
        tf.margin_right = Inches(0.3)
        
        # Title
        tp = tf.paragraphs[0]
        tp.text = title
        tp.font.name = "Inter"
        tp.font.size = Pt(14)
        tp.font.bold = True
        tp.font.color.rgb = ACCENT_TEAL
        tp.space_after = Pt(12)
        
        # Bullet items
        for item in items:
            p = tf.add_paragraph()
            p.text = "• " + item
            p.font.name = "Inter"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(6)

    # ==================== SLIDE 1: Title Slide ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.0))
    ttf = tbox.text_frame
    ttf.word_wrap = True

    p_badge = ttf.paragraphs[0]
    p_badge.text = "🚜 ROBOTRAC R&D ENGINEERING SPECIFICATION"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_CYAN
    p_badge.space_after = Pt(14)

    p_title = ttf.add_paragraph()
    p_title.text = "Autonomous Agricultural Tractor Platform"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_LIGHT
    p_title.space_after = Pt(12)

    p_sub = ttf.add_paragraph()
    p_sub.text = "Technical Architecture, Drive-by-Wire Electro-Hydraulics, Dual-Domain Compute, Non-Linear Motion Control & ISO 18497 / ISO 25119 Compliance"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_after = Pt(36)

    p_meta = ttf.add_paragraph()
    p_meta.text = "Chief Technology Officer & Principal AI Robotics Engineer  |  October 2026"
    p_meta.font.size = Pt(12)
    p_meta.font.bold = True
    p_meta.font.color.rgb = ACCENT_TEAL

    # ==================== SLIDE 2: Agronomic Problem ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Section 01 · Agronomic Context", "The Agricultural Robotics Challenge", "REALITY CHECK")

    add_card(s2, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "⚠️ Why Passenger AV Stacks Fail in Agriculture", [
                 "Terramechanics & Slip: Loose soil invalidates bicycle kinematics; slip reaches 15%–35%.",
                 "Severe Environmental Blinding: Dust clouds and plant chaff coat optical sensors in 20 min.",
                 "High-Mast Antenna Roll: Antenna at 2.8m causes up to 29.2 cm lateral error on 6° slopes.",
                 "Dynamic Implement Drag: Asymmetric tillage forces (5–40 kN) generate violent yaw perturbations."
             ])

    add_card(s2, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "🎯 Robotrac Engineering Strategy", [
                 "Dual-Domain Compute: Hard Real-Time safety MCU for 100 Hz steering, separate from Linux.",
                 "NMPC with Soil Slip: Active Pacejka tire-soil friction models compensate for side-slopes.",
                 "Multi-Modal Radar Fusion: 77 GHz radar Doppler penetration validates obstacles in dust.",
                 "Sub-Scale Electric Mule: Validate RTK and wireless E-stop at low risk before diesel tractors."
             ])

    # ==================== SLIDE 3: System Architecture ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Section 02 · System Architecture", "Dual-Domain Compute Topology", "ADR-002 APPROVED")

    add_card(s3, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "🖥️ Domain 1: Soft Real-Time (NVIDIA Jetson)", [
                 "Hardware: NVIDIA Jetson AGX Orin Industrial (275 TOPS, -40°C to +85°C).",
                 "OS & Middleware: Ubuntu Linux (PREEMPT_RT) + ROS 2 (CycloneDDS / Iceoryx).",
                 "Perception: Optical NIR row segmentation (BiSeNet-V2 @ 30 FPS) + radar clutter filter.",
                 "State Estimation: 15-state ES-EKF fusing dual RTK + tactical IMU @ 20 Hz.",
                 "Planning: Fields2Cover coverage swaths, Ω-turns & acados NMPC solver (20 Hz)."
             ])

    add_card(s3, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "🛡️ Domain 2: Hard Real-Time (Safety Controller)", [
                 "Hardware: TTControl TTC 580 / IFM CR711S (Dual-core lockstep MCU).",
                 "Deterministic Loop: 100 Hz cycle (10.0 ms ± 0.1 ms jitter) running certified C/RTOS.",
                 "Steering Actuation: Dual Hall WAS reading + Danfoss OSPE electro-hydraulic valve PWM.",
                 "Fail-Safe Stopping: Spring-Applied Pressure-Released (SAPR) brake dump (< 150 ms).",
                 "ISO 18497 E-Stop: Wireless RF remote heartbeat monitoring (< 500 ms automatic trip)."
             ])

    # ==================== SLIDE 4: Drive-by-Wire Actuation ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Section 03 · Vehicle Control & DbW", "Electro-Hydraulic Drive-by-Wire Subsystems", "ISO 25119 AgPL d")

    add_card(s4, Inches(0.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Steering Actuation", [
                 "Danfoss OSPE / Eaton PVG 32 proportional valve with load-sensing priority.",
                 "Zero mechanical backlash; direct cylinder hydraulic connection.",
                 "Curtiss-Wright R300 dual Hall-effect WAS (IP69K sealed).",
                 "Inverted analog plausibility check: V1 + V2 = 5.0V ± 0.1V."
             ])

    add_card(s4, Inches(4.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Fail-Safe Braking", [
                 "Service Brake: Proportional pressure valve (0–120 bar) for smooth stops.",
                 "Emergency Brake: Spring-Applied Pressure-Released (SAPR) cylinder.",
                 "Fast Dump Valve: Vents hydraulic pressure to tank in < 150 ms on trip.",
                 "Mechanical spring locks wheels independently of electrical bus."
             ])

    add_card(s4, Inches(8.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Powertrain & Implement", [
                 "SAE J1939 Engine Control: Commands speed/torque limits via TSC1 message.",
                 "ISOBUS Class 3 (ISO 11783): Automates 3-point hitch lift/lower at headlands.",
                 "PTO Interlock: Disengages PTO automatically before tight Ω-turns.",
                 "Electronic governor prevents engine stall under peak implement drag."
             ])

    # ==================== SLIDE 5: Navigation & State Estimation ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Section 04 · State Estimation", "Dual-Antenna RTK & 3D Tilt Compensation", "SUB-2.5 CM PASS")

    add_card(s5, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "📡 Moving-Baseline Dual-Antenna RTK", [
                 "Hardware: Septentrio AsteRx-m3 Pro or Dual u-blox ZED-F9P on a 1.2m baseline.",
                 "Static Yaw: Measures carrier-phase double-differences, guaranteeing sub-0.09° heading.",
                 "Zero-Speed Reliability: True heading at 0 m/s; unaffected by wheel spin in mud.",
                 "Magnetic Immunity: 100% immune to heavy tractor steel chassis distortion."
             ])

    add_card(s5, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "📐 Dynamic Terrain Roll / Pitch Compensation", [
                 "Tactical MEMS IMU: Xsens MTi-680G (< 2°/hr gyro bias stability) @ 200 Hz.",
                 "Coordinate Transformation: Dynamic lever-arm tilt correction down to ground contact.",
                 "Formula: Δx = h * sin(θ_roll) + l * cos(θ_pitch) eliminates mast sway.",
                 "Ground Accuracy: Restricts lateral tilt error to ≤ 2.0 cm on uneven furrows."
             ])

    # ==================== SLIDE 6: Environmental Perception ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Section 05 · Perception Engineering", "Multi-Modal Sensor Fusion in Hostile Dust", "ZERO FALSE STOPS")

    add_card(s6, Inches(0.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "NIR HDR Cameras", [
                 "Leopard Imaging AR0820 GMSL2 (> 120 dB HDR, Global Shutter).",
                 "NIR 850 nm Filter: Enhances crop chlorophyll reflectance vs dry soil.",
                 "Pneumatic Air-Blast: 6-bar compressed air purge cleans lens dust every 5 min."
             ])

    add_card(s6, Inches(4.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "77 GHz mmWave Radar", [
                 "Continental ARS 408-21 automotive radar.",
                 "Dust Penetration: Millimeter waves (3.9 mm) pierce dense tilling dust plumes.",
                 "Direct Doppler: Instantly measures radial velocity of approaching humans."
             ])

    add_card(s6, Inches(8.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "3D Solid-State LiDAR", [
                 "Livox Mid-360 (360° x 59° FOV, 905 nm).",
                 "Canopy Profiling: 3D field boundary, ditch, and canopy density extraction.",
                 "Clutter Removal: Ground plane segmentation filters out harmless tall grass."
             ])

    # ==================== SLIDE 7: Crop-Row Perception & Visual Servoing ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Section 06 · Computer Vision", "Crop-Row Perception & Visual Servoing", "TENSORRT INT8")

    add_card(s7, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Deep Semantic Segmentation (BiSeNet-V2)", [
                 "Multi-Class Pixel Mask: [Soil, Crop Stalk, Weed Clutter, Negative Obstacle/Ditch].",
                 "Weed Resilience: Robust deep feature extraction replaces fragile Excess Green (ExG) thresholding.",
                 "High Throughput: Runs at 30 FPS (< 33 ms latency) on Jetson AGX Orin TensorRT INT8 engine.",
                 "RANSAC Parabolic Fitting: Extracts crop row centerlines even with discontinuous missing stalks."
             ])

    add_card(s7, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Hybrid Navigation State Machine", [
                 "Mode A (Headlands / Early Stage): Governed strictly by Dual-Antenna RTK-GNSS + IMU waypoints.",
                 "Mode B (Canopy Row-Following): Fuses visual-servoing lateral and heading errors (e_y, e_ψ) with RTK.",
                 "Root Protection: Prevents tractor tires or implement shanks from crushing crop root systems.",
                 "Dynamic Confidence Gate: Degrades gracefully to RTK if crop canopy is occluded or uneven."
             ])

    # ==================== SLIDE 8: Coverage Planning via Fields2Cover ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Section 07 · Coverage Path Planning", "Fields2Cover Swaths & Non-Holonomic Turns", "SWATH OPTIMIZED")

    add_card(s8, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Agricultural Coverage Hierarchy", [
                 "Headland Generator: Computes peripheral buffer swaths based on wheelbase and implement radius R_min.",
                 "Swath Generator: Generates parallel swaths aligned with field contours to minimize soil compaction.",
                 "Route Optimization: Solves swath traversal order via Google OR-Tools to minimize idle headland travel.",
                 "Implement Footprint: Compensates for variable working widths and asymmetric implement offsets."
             ])

    add_card(s8, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Non-Holonomic Headland Trajectories", [
                 "Ω-Turn (Omega Turn): Smooth forward loops when adjacent tracks are narrower than 2 · R_min.",
                 "Dubins & Reeds-Shepp: Generates kinematically feasible forward/reverse turning curves without wheel scuffing.",
                 "Swept Collision Envelope: Simulates towed implement swing moments to avoid field fence posts and ditches.",
                 "PTO Automation Interlock: Disengages implement drive and raises 3-point hitch before initiating headland turns."
             ])

    # ==================== SLIDE 9: Non-Linear MPC with Soil-Slip Dynamics ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Section 08 · Advanced Motion Control", "Non-Linear MPC with Soil-Slip Dynamics", "acados RTI @ 20 Hz")

    add_card(s9, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "The Dynamic Control Formulation", [
                 "Receding Horizon: Prediction horizon N = 20 steps (T_s = 0.05 s, lookahead = 1.0 s).",
                 "Pacejka Soil-Tire Dynamics: Incorporates lateral tire-soil friction models (F_yf, F_yr) into state equations.",
                 "Implement Drag Observer: Compensates for dynamic yaw perturbations caused by asymmetric tillage soil drag.",
                 "Pass-to-Pass Precision: Maintains sub-2.5 cm cross-track tracking even on 10° deformable side-slopes."
             ])

    add_card(s9, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Hard Actuation Constraints", [
                 "Knuckle Angle Bounds: |δ_steer| ≤ 35° (prevents steering cylinder mechanical hard stops).",
                 "Hydraulic Slew Rate: |δ̇_steer| ≤ 25°/s (matches Danfoss OSPE valve maximum spool flow rate).",
                 "Tip-Over Prevention: Lateral acceleration capped at |a_y| ≤ 0.25 · g on severe agricultural contours.",
                 "Deterministic Latency: acados Real-Time Iterations (RTI) converge in ≤ 20 ms on Jetson Orin."
             ])

    # ==================== SLIDE 10: Functional Safety & ISO Standards ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Section 09 · Safety Architecture", "ISO 18497 & ISO 25119 Compliance", "AgPL d / CAT 3")

    add_card(s10, Inches(0.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "ISO 18497 Perception Zones", [
                 "Zone 1 (Stop Zone): Immediate Category 0 E-Stop and hydraulic dump (L_stop ≈ 3.2 m at 8 km/h).",
                 "Zone 2 (Decel Zone): Modulated service braking down to creep speed (0.3 m/s) on obstacle approach.",
                 "Zone 3 (Warning Zone): 360° amber strobe flash + 100 dB acoustic horn to clear bystanders."
             ])

    add_card(s10, Inches(4.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Wireless RF Safety Remote", [
                 "Transmitter: HBC-radiomatic / Hetronic Nova (ISO 13849 PL d certified industrial remote).",
                 "Deterministic Heartbeat: 150 ms keep-alive token ping over dedicated 868 / 915 MHz RF channel.",
                 "Automatic Trip: Tractor halts within < 500 ms if RF link is lost, jammed, or battery depleted."
             ])

    add_card(s10, Inches(8.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Pre-Motion Safety Sequence", [
                 "Audible Alarm: Mandatory 3.0s continuous 100 dB horn sound prior to autonomous vehicle launch.",
                 "Dual-Channel Relays: High-side and low-side cross-monitored switches decouple valve power.",
                 "Spring Parking Brake: Spring-applied mechanical brake latches instantly upon power interruption."
             ])

    # ==================== SLIDE 11: Electrical Power Conditioning & Ingress ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Section 10 · Electrical Engineering", "ISO 7637-2 Power & Ingress Protection", "IP67 / IP69K")

    add_card(s11, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Tractor Electrical Hostility Mitigation", [
                 "Load Dump Protection (ISO 7637-2): Active TVS clamping handles +100 V alternator inductive spikes.",
                 "Cold-Cranking Ride-Through: Accepts battery drops down to 6.0 V during diesel starter motor cranking.",
                 "Supercapacitor Buffer: 50F bank provides 30 s ride-through to bridge brownouts or allow graceful OS shutdown.",
                 "Reverse Polarity & Surge: MOSFET-based reverse polarity protection and common-mode choke filtering."
             ])

    add_card(s11, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Harsh Environmental Ingress Hardening", [
                 "CNC Enclosure: Milled 6061 aluminum enclosure with Gore-Tex pressure equalization breather vent.",
                 "Washdown Rating: IP67 submersion + IP69K high-pressure, high-temperature (80°C) steam jet cleaning.",
                 "Automotive Cabling: Sealed Deutsch DT/DTM & Amphenol connectors; M12 X-coded industrial Ethernet.",
                 "Vibration Hardening: MIL-STD-810H rated against continuous heavy diesel harmonic vibration."
             ])

    # ==================== SLIDE 12: Low-Bandwidth Telemetry & Edge Buffering ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Section 11 · Telecommunications", "Protobuf, MQTT & Store-and-Forward", "85% BANDWIDTH SAVINGS")

    add_card(s12, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Binary Protocol Buffers v3 over MQTT", [
                 "Data Optimization: Compact binary Protobuf messages replace verbose JSON over WebSockets.",
                 "Data Budget: 10-hour continuous working shift consumes < 50 MB of cellular data (vs 350 MB JSON).",
                 "QoS 1 Guarantee: MQTT broker ensures critical mission transitions and safety alerts are acknowledged.",
                 "TimescaleDB Hypertables: Cloud backend partitions high-frequency telemetry into 7-day optimized chunks."
             ])

    add_card(s12, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Edge Store-and-Forward Ring Buffer", [
                 "Dead-Zone Resilience: Onboard SQLite circular buffer stores 72 hours of telemetry during cellular blackouts.",
                 "Throttled Sync: On cellular reconnect, buffered historical data uploads in compressed, throttled batches.",
                 "Zero Data Loss: Guarantees agronomic audit trails and spray logs remain 100% complete.",
                 "Direct Local Wi-Fi: Operator tablet streams live video and telemetry locally without needing internet."
             ])

    # ==================== SLIDE 13: Operator HMI & Android Field Tablet ====================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Section 12 · Human-Machine Interface", "High-Contrast Outdoor Day Theme & Local AP", "100,000 LUX READABLE")

    add_card(s13, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Outdoor Sunlight Field Ergonomics", [
                 "Pure White Canvas (#FFFFFF): Eliminates dark-mode 'mirror reflection' under 100,000 lux direct sunlight.",
                 "Glove-Friendly Touch: All actionable cards and buttons feature > 56 dp targets with 16 dp spacing.",
                 "Two-Step Slide-to-Start: Horizontal slider gesture prevents accidental vehicle movement in bumpy cabs.",
                 "State Visualizer: High-contrast color-coded indicators for RTK Fix, Heading Lock, and Valve Spool."
             ])

    add_card(s13, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Direct Local Wi-Fi AP & Acoustic Alarms", [
                 "Zero-Cloud Operation: Tablet pairs directly with tractor's onboard Wi-Fi hotspot via QR code mTLS.",
                 "Bypass Silent Mode: 2.5 kHz acoustic alarm siren and continuous haptic buzzers on emergency stops.",
                 "Tractor Horn Trigger: Sounds the tractor's physical 100 dB horn if perimeter intrusion is detected.",
                 "Map Layer Caching: Onboard vector field tile caching enables offline boundary and swath inspection."
             ])

    # ==================== SLIDE 14: Phased R&D Roadmap & Release Gates ====================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Section 13 · Execution Strategy", "Phased Development & Release Gates", "RISK-GATED R&D")

    add_card(s14, Inches(0.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Phase 1 & 2: SIL & Telemetry", [
                 "Gazebo / O3DE Simulation: Terramechanics soil slip and sensor fault injection with zero hardware risk.",
                 "Telemetry & Android App: Binary Protobuf pipeline, local Wi-Fi pairing, and cloud ingestion verified.",
                 "Model Verification: NMPC convergence validated against synthetic furrow and slope disturbances."
             ])

    add_card(s14, Inches(4.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Phase 3.5: Electric Mule Testbed", [
                 "Sub-Scale Mule: Retrofit small electric UTV / lawn tractor with steer-by-wire and dual RTK.",
                 "Field Validation: De-risks Fields2Cover swaths, Ω-turns, and wireless E-stop at low speed (< 5 km/h).",
                 "Zero Danger: Prevents rollover or crush hazard before touching 8-ton diesel machinery."
             ])

    add_card(s14, Inches(8.8), Inches(2.2), Inches(3.7), Inches(4.5),
             "Phase 4 & 5: Tractor HIL & Trials", [
                 "Stationary Tractor HIL: Jacked-up tractor hydraulic valve deadband calibration and dump timing (< 150 ms).",
                 "50-Hour Proving Trials: Supervised closed-field autonomous trials with perimeter safety driver.",
                 "Certification Sign-Off: Third-party auditor compliance verification for ISO 18497 and ISO 25119."
             ])

    # ==================== SLIDE 15: Executive Summary & Next Actions ====================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Section 14 · Executive Summary", "Conclusion & Procurement Milestones", "ACTION PLAN")

    add_card(s15, Inches(0.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Summary of Technical Advancements", [
                 "Certified Drive-by-Wire: Replaced fragile aftermarket steering kits with Danfoss OSPE valves & SAPR brakes.",
                 "Precision Motion Control: Upgraded kinematic Stanley to acados NMPC with Pacejka soil slip (≤ 2.5 cm).",
                 "Functional Safety: Engineered dual-channel ISO 25119 AgPL d safety controller & ISO 18497 RF remote.",
                 "Harsh Environmental Hardening: Integrated ISO 7637-2 load dump TVS clamping, supercaps & IP69K sealing."
             ])

    add_card(s15, Inches(6.8), Inches(2.2), Inches(5.6), Inches(4.5),
             "Immediate Procurement & Build Milestones", [
                 "Milestone 1: Confirm tractor hydraulic platform (CCLS load-sensing) and order Danfoss OSPE valve manifold.",
                 "Milestone 2: Procure and assemble Phase 3.5 Sub-Scale Electric Mule for low-cost field path proving.",
                 "Milestone 3: Fabricate and bench-test ISO 7637-2 power conditioning board with alternator dump pulses.",
                 "Milestone 4: Initiate dual-antenna RTK and tactical IMU moving-baseline integration tests."
             ])

    # Save presentation
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Robotrac_Autonomous_Tractor.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
