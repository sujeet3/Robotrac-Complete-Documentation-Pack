# ML / Computer Vision Plan

## 1. ML scope
Separate perception tasks; do not train one opaque model to make all vehicle decisions.
- Crop-row geometry/segmentation
- Crop species/stage classification if needed
- Weed/crop distinction only when the target operation is defined
- Obstacle detection: people, animals, vehicles, equipment and relevant objects
- Optional implement-specific vision tasks later

## 2. Dataset plan
Capture representative data across:
- Target crop species and growth stages
- Row spacing, canopy closure and crop density
- Morning/noon/evening lighting, shadows, glare and overcast
- Dry/wet soil, dust, residue, uneven terrain and vibration
- Camera heights, angles and field of view
- Positive examples and hard negatives (weeds that resemble crops, missing plants, occlusion)
- Safe staged obstacle targets; avoid unsafe data collection near operating machinery

Document consent/privacy, location handling and retention for any identifiable people in imagery.

## 3. Annotation
- Define class ontology and annotation handbook before labeling.
- Use segmentation masks or row/centerline annotations for crop rows.
- Bounding boxes or segmentation for obstacles, with occlusion/truncation labels.
- Record crop, growth stage, lighting, terrain, camera and collection session metadata.
- Review inter-annotator agreement and adjudicate ambiguous samples.

## 4. Data split
Split by field/session/date, not random neighboring frames, to reduce leakage. Keep a locked test set from separate field sessions. Include edge cases and distribution-shift sets.

## 5. Training workflow
1. Baseline classical CV and pretrained model.
2. Establish dataset version and experiment tracking.
3. Train/fine-tune model.
4. Evaluate per class, range, lighting, crop stage and field.
5. Calibrate confidence and define low-confidence behavior.
6. Export candidate model and benchmark on target onboard hardware.
7. Run recorded-data replay and simulation; do not connect model output directly to actuators.
8. Review false negatives and failure cases; repeat data collection.
9. Release signed model with version, hash, training data lineage and rollback.

## 6. Metrics and gates
- Precision/recall, per-class recall and false-negative review
- Segmentation IoU or row-line error
- Latency p50/p95/p99, memory, power and thermal stability
- Robustness by lighting/weather/crop stage
- Confidence calibration and out-of-distribution detection
- System-level crop damage and safe-stop behavior in supervised tests

## 7. Model card fields
Model name/version, intended use, excluded use, dataset version, classes, performance by condition, known limitations, hardware/runtime, latency/power, safety dependencies, approval owner and rollback version.

## 8. ML safety boundary
ML produces observations with confidence and timestamp. Deterministic system logic and independently reviewed safety mechanisms decide whether operation may continue. An ML model must not be the only protection against collision or crop damage.
