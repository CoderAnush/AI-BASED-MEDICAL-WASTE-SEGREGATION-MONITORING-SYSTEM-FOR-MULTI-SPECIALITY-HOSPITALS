# IMPLEMENTATION GUIDE - Biomedical Waste Segregation System
## Milestone 3: Complete Code Reference

---

## 📚 TABLE OF CONTENTS

1. [Module Architecture](#module-architecture)
2. [Class Reference](#class-reference)
3. [Function Reference](#function-reference)
4. [Configuration Reference](#configuration-reference)
5. [Integration Examples](#integration-examples)
6. [Customization Guide](#customization-guide)
7. [API Reference](#api-reference)
8. [Error Handling](#error-handling)

---

## 🏗️ MODULE ARCHITECTURE

### Core Modules Overview

```
┌─────────────────────────────────────────────────┐
│         BIOMEDICAL WASTE DETECTION SYSTEM       │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌────────────────────────────────────────┐   │
│  │  INFERENCE.PY (Main Entry Point)       │   │
│  │  - Single Image Inference              │   │
│  │  - Batch Folder Processing             │   │
│  │  - Real-time Webcam Detection          │   │
│  └────────────────────────────────────────┘   │
│           ↓           ↓           ↓             │
│  ┌──────────────┬──────────────┬──────────────┐ │
│  │  TRAIN.PY    │ CATEGORY_    │  CSV_LOGGER  │ │
│  │              │  MAPPING.PY  │   .PY        │ │
│  │ - Training   │ - Waste→Cat  │ - Logging    │ │
│  │ - Validation │ - Cat→Bin    │ - Storage    │ │
│  │ - Testing    │              │              │ │
│  └──────────────┴──────────────┴──────────────┘ │
│           ↓           ↓           ↓             │
│  ┌──────────────┬──────────────┬──────────────┐ │
│  │  CONFIG.PY   │  UTILS.PY    │ ANALYZE_CSV  │ │
│  │              │              │   .PY        │ │
│  │ - Parameters │ - Helpers    │ - Analytics  │ │
│  │ - Settings   │ - Validation │ - Reports    │ │
│  │              │ - Formatting │              │ │
│  └──────────────┴──────────────┴──────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
                         ↓
        ┌───────────────────────────────────────┐
        │  OUTPUTS                              │
        ├───────────────────────────────────────┤
        │ - Annotated Images (output_images/)   │
        │ - CSV Log (waste_log.csv)             │
        │ - Console Output                      │
        │ - Power BI Reports                    │
        └───────────────────────────────────────┘
```

---

## 💼 CLASS REFERENCE

### 1. BiomedicalWasteModelTrainer (train_model.py)

**Purpose:** Manages model training lifecycle

**Key Methods:**

```python
# Initialization
trainer = BiomedicalWasteModelTrainer(
    dataset_path="Biomedical_Waste",
    epochs=100,
    imgsz=640,
    batch="auto"
)

# Validation
trainer.validate_dataset() → bool

# Model operations
trainer.load_pretrained_model() → None
trainer.train() → Optional[dict]
trainer.validate() → Optional[dict]
trainer.test() → Optional[dict]

# Post-training
trainer.find_and_save_best_model() → Optional[str]
trainer.print_training_summary() → None
```

**Example Usage:**

```python
from train_model import BiomedicalWasteModelTrainer

trainer = BiomedicalWasteModelTrainer()
if trainer.validate_dataset():
    trainer.load_pretrained_model()
    trainer.train()
    trainer.find_and_save_best_model()
```

---

### 2. WasteCategoryMapper (category_mapping.py)

**Purpose:** Maps waste items to categories and bins

**Static Methods:**

```python
# Get waste category
category = WasteCategoryMapper.get_waste_category("needle")
# Returns: "Sharps Waste"

# Get recommended bin
bin_color = WasteCategoryMapper.get_recommended_bin("needle")
# Returns: "White Bin"

# Get complete mapping
category, bin_color = WasteCategoryMapper.get_complete_mapping("needle")
# Returns: ("Sharps Waste", "White Bin")

# Validate waste type
is_valid = WasteCategoryMapper.validate_waste_type("needle")
# Returns: True

# Get all waste types
waste_types = WasteCategoryMapper.get_all_waste_types()
# Returns: ['needle', 'syringe', 'glove', ...]
```

**Data Structures:**

```python
# Internal mappings (read-only)
WASTE_CATEGORY_MAP = {
    "needle": "Sharps Waste",
    "syringe": "Sharps Waste",
    # ... 8 total classes
}

WASTE_BIN_MAP = {
    "needle": "White Bin",
    "syringe": "White Bin",
    # ... 8 total classes
}
```

---

### 3. WasteCSVLogger (csv_logger.py)

**Purpose:** Manages waste detection logging to CSV

**Key Methods:**

```python
# Initialization
logger = WasteCSVLogger(csv_path="waste_log.csv")

# Logging
waste_id = logger.log_detection(
    waste_type="needle",
    waste_category="Sharps Waste",
    recommended_bin="White Bin",
    confidence=97.5,
    image_name="sample.jpg"
)

# Queries
total = logger.get_total_records() → int
csv_path = logger.get_csv_path() → str
stats = logger.get_summary_statistics() → dict
next_id = logger.get_next_waste_id() → str
```

**CSV Output Format:**

```
Timestamp,Waste_ID,Waste_Type,Waste_Category,Recommended_Bin,Confidence,Image_Name
2024-06-06 14:23:45,W001,needle,Sharps Waste,White Bin,97.50%,sample.jpg
```

---

### 4. BiomedicalWasteInference (inference.py)

**Purpose:** Runs inference on images, folders, or webcam

**Key Methods:**

```python
# Initialization
inference = BiomedicalWasteInference(
    model_path="best.pt",
    output_dir="output_images",
    csv_path="waste_log.csv",
    confidence_threshold=0.5
)

# Single image inference
detections = inference.infer_image("image.jpg", save_output=True)
# Returns: List[dict] with detection data

# Folder inference
all_detections = inference.infer_folder("sample_images/")

# Webcam inference
inference.infer_webcam(webcam_id=0)
```

**Detection Data Structure:**

```python
{
    "waste_id": "W001",
    "waste_type": "needle",
    "waste_category": "Sharps Waste",
    "recommended_bin": "White Bin",
    "confidence": 97.5,  # percentage
    "image_name": "sample.jpg",
    "box": (x1, y1, x2, y2)  # pixel coordinates
}
```

---

### 5. SystemConfig (config.py)

**Purpose:** Centralized configuration management

**Key Attributes:**

```python
# Access configurations
model_config = SystemConfig.get_model_config()
training_config = SystemConfig.get_training_config()
output_config = SystemConfig.get_output_config()

# Get mappings
class_name = SystemConfig.get_waste_class(0)
category = SystemConfig.get_waste_category("needle")
bin_color = SystemConfig.get_recommended_bin("Sharps Waste")

# Validation
SystemConfig.validate_config() → bool
SystemConfig.print_config() → None
```

---

### 6. WasteAnalyzer (analyze_csv.py)

**Purpose:** Analyzes waste detection logs

**Key Methods:**

```python
# Initialization
analyzer = WasteAnalyzer(csv_path="waste_log.csv")

# Statistics
basic_stats = analyzer.get_basic_statistics() → dict
waste_dist = analyzer.get_waste_type_distribution() → dict
category_dist = analyzer.get_waste_category_distribution() → dict
bin_dist = analyzer.get_bin_distribution() → dict
conf_stats = analyzer.get_confidence_statistics() → dict

# Analysis
hourly = analyzer.get_hourly_distribution() → dict
daily = analyzer.get_daily_distribution() → dict
top_items = analyzer.get_top_waste_items(n=5) → list
peak_hours = analyzer.get_peak_hours(n=3) → list
low_conf = analyzer.get_low_confidence_detections(threshold=80)

# Reports
report = analyzer.generate_summary_report() → str
analyzer.export_summary_to_file("report.txt") → bool
```

---

## 🔧 FUNCTION REFERENCE

### category_mapping.py

```python
# Module-level convenience functions
get_waste_category(waste_type: str) → str
get_recommended_bin(waste_type: str) → str
get_complete_mapping(waste_type: str) → Tuple[str, str]
```

### csv_logger.py

```python
# Factory function
create_csv_logger(csv_path: Optional[str]) → WasteCSVLogger
```

### utils.py

**ImageUtils:**
```python
ImageUtils.load_image(image_path: str) → Optional[np.ndarray]
ImageUtils.save_image(image: np.ndarray, output_path: str) → bool
ImageUtils.resize_image(image: np.ndarray, target_size) → np.ndarray
ImageUtils.get_image_info(image: np.ndarray) → dict
ImageUtils.validate_image(image_path: str) → bool
```

**FileUtils:**
```python
FileUtils.get_image_files(folder_path: str) → List[str]
FileUtils.create_directory(directory_path: str) → bool
FileUtils.file_exists(file_path: str) → bool
FileUtils.get_file_size(file_path: str) → Optional[int]
FileUtils.get_directory_size(directory_path: str) → int
```

**ValidationUtils:**
```python
ValidationUtils.validate_confidence(confidence: float) → bool
ValidationUtils.validate_waste_type(waste_type, valid_types) → bool
ValidationUtils.validate_coordinates(x1, y1, x2, y2, w, h) → bool
```

**StatisticsUtils:**
```python
StatisticsUtils.calculate_average(values: List[float]) → float
StatisticsUtils.calculate_percentile(values, percentile) → float
StatisticsUtils.get_min_max(values) → Tuple[float, float]
StatisticsUtils.get_distribution(values, bins) → dict
```

**FormatUtils:**
```python
FormatUtils.format_confidence(confidence, format_type) → str
FormatUtils.format_timestamp(timestamp, output_format) → str
FormatUtils.format_file_size(size_bytes: int) → str
FormatUtils.print_table(headers, rows) → None
```

---

## ⚙️ CONFIGURATION REFERENCE

### SystemConfig Parameters

**Model Configuration:**
```python
SystemConfig.MODEL_CONFIG = {
    "model_path": "best.pt",
    "confidence_threshold": 0.5,  # 0-1 range
    "iou_threshold": 0.45,        # NMS threshold
    "device": 0,                  # GPU ID or "cpu"
    "imgsz": 640,                 # Model input size
    "max_detections": 100,        # Max boxes/image
}
```

**Training Configuration:**
```python
SystemConfig.TRAINING_CONFIG = {
    "epochs": 100,
    "batch_size": "auto",
    "imgsz": 640,
    "lr0": 0.01,                  # Initial LR
    "patience": 15,               # Early stopping
    "seed": 42,                   # Reproducibility
}
```

**Waste Classes (8 total):**
```python
{
    0: "cotton",
    1: "general_waste",
    2: "glove",
    3: "iv_tube",
    4: "mask",
    5: "medicine_bottle",
    6: "needle",
    7: "syringe",
}
```

---

## 🔗 INTEGRATION EXAMPLES

### Example 1: Custom Training Pipeline

```python
from train_model import BiomedicalWasteModelTrainer
from config import SystemConfig

# Get training config
config = SystemConfig.get_training_config()

# Create trainer
trainer = BiomedicalWasteModelTrainer(
    dataset_path=config["dataset_path"],
    epochs=config["epochs"],
    imgsz=config["imgsz"],
    batch=config["batch_size"]
)

# Execute training
if trainer.validate_dataset():
    trainer.load_pretrained_model()
    trainer.train()
    trainer.validate()
    trainer.test()
    best_model = trainer.find_and_save_best_model()
    trainer.print_training_summary()
```

### Example 2: Batch Image Processing with Analysis

```python
from inference import BiomedicalWasteInference
from analyze_csv import WasteAnalyzer

# Initialize inference
inference = BiomedicalWasteInference()

# Process folder
detections = inference.infer_folder("sample_images/")

# Analyze results
analyzer = WasteAnalyzer("waste_log.csv")
report = analyzer.generate_summary_report()
print(report)
```

### Example 3: Custom Waste Classification Logic

```python
from category_mapping import WasteCategoryMapper
from csv_logger import WasteCSVLogger

# Detect waste item
detected_waste = "needle"

# Map to category
category = WasteCategoryMapper.get_waste_category(detected_waste)
bin_color = WasteCategoryMapper.get_recommended_bin(detected_waste)

# Log to CSV
logger = WasteCSVLogger()
waste_id = logger.log_detection(
    waste_type=detected_waste,
    waste_category=category,
    recommended_bin=bin_color,
    confidence=97.5,
    image_name="sample.jpg"
)

print(f"Logged: {waste_id} - {detected_waste} → {category} → {bin_color}")
```

### Example 4: Real-Time Monitoring with Statistics

```python
from inference import BiomedicalWasteInference
from csv_logger import WasteCSVLogger

# Start inference
inference = BiomedicalWasteInference()

# Run webcam
inference.infer_webcam(webcam_id=0)

# After inference, analyze
logger = inference.logger
stats = logger.get_summary_statistics()

print(f"Total detections: {stats['total_records']}")
print(f"Most common: {stats['most_common_waste_type']}")
print(f"Average confidence: {stats['average_confidence']}%")
```

---

## 🎨 CUSTOMIZATION GUIDE

### Customize Confidence Threshold

```python
# Option 1: Direct modification
inference = BiomedicalWasteInference(
    confidence_threshold=0.7  # 70% instead of default 50%
)

# Option 2: Via config
from config import SystemConfig
config = SystemConfig.MODEL_CONFIG.copy()
config["confidence_threshold"] = 0.7
```

### Customize Output Directory

```python
inference = BiomedicalWasteInference(
    output_dir="custom_output_path/"
)
```

### Customize CSV Logging

```python
logger = WasteCSVLogger(csv_path="custom_waste_log.csv")
```

### Add Custom Waste Class

```python
# Edit config.py
SystemConfig.WASTE_CLASSES[8] = "custom_waste"

SystemConfig.WASTE_CATEGORY_MAP["custom_waste"] = "Custom Category"

SystemConfig.WASTE_BIN_MAP["custom_waste"] = "Custom Bin"

# Note: Requires retraining model with new class
```

### Customize Console Output Format

```python
# Edit inference.py _format_output() method
def _format_output(self, detection: dict) -> str:
    # Customize formatting here
    output = f"Type: {detection['waste_type']}\n"
    output += f"Confidence: {detection['confidence']:.1f}%\n"
    return output
```

---

## 📡 API REFERENCE

### REST-Like Usage (for integration)

```python
# Initialize system
from inference import BiomedicalWasteInference

api = BiomedicalWasteInference()

# Detect in image
result = api.infer_image("image.jpg")
# Returns: List[dict] with detections

# Get statistics
stats = api.logger.get_summary_statistics()
# Returns: dict with statistics

# Export data
api.logger.get_csv_path()
# Returns: str (path to CSV)
```

### Programmatic Detection Flow

```python
from ultralytics import YOLO
from category_mapping import WasteCategoryMapper

# Load model
model = YOLO("best.pt")

# Run inference
results = model.predict("image.jpg", conf=0.5)

# Process detections
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        
        # Get class name
        class_name = result.names[class_id]
        
        # Map to category
        category = WasteCategoryMapper.get_waste_category(class_name)
        bin_color = WasteCategoryMapper.get_recommended_bin(class_name)
        
        print(f"{class_name}: {confidence:.2%} → {bin_color}")
```

---

## 🚨 ERROR HANDLING

### Common Exceptions and Handling

```python
# FileNotFoundError
try:
    inference = BiomedicalWasteInference(model_path="best.pt")
except FileNotFoundError as e:
    print(f"Model not found: {e}")
    print("Train model first: python train_model.py")

# ValueError
try:
    category = WasteCategoryMapper.get_waste_category("unknown_item")
except ValueError as e:
    print(f"Unknown waste type: {e}")

# IOError
try:
    logger = WasteCSVLogger("waste_log.csv")
except IOError as e:
    print(f"Cannot access CSV: {e}")
    print("Check file permissions")

# AttributeError
try:
    if inference.model is None:
        raise AttributeError("Model not loaded")
except AttributeError as e:
    print(f"Initialization error: {e}")
```

### Graceful Degradation

```python
# Try GPU, fallback to CPU
try:
    inference = BiomedicalWasteInference(
        model_path="best.pt"
    )
except RuntimeError:
    print("GPU not available, using CPU")
    # Model will automatically use CPU

# Handle missing detections
detections = inference.infer_image("image.jpg")
if not detections:
    print("No waste items detected")
else:
    for detection in detections:
        print(f"Detected: {detection['waste_type']}")
```

---

## 🧪 TESTING TEMPLATES

### Unit Test Example

```python
import unittest
from category_mapping import WasteCategoryMapper

class TestCategoryMapping(unittest.TestCase):
    
    def test_valid_waste_type(self):
        result = WasteCategoryMapper.validate_waste_type("needle")
        self.assertTrue(result)
    
    def test_get_category(self):
        category = WasteCategoryMapper.get_waste_category("needle")
        self.assertEqual(category, "Sharps Waste")
    
    def test_get_bin(self):
        bin_color = WasteCategoryMapper.get_recommended_bin("needle")
        self.assertEqual(bin_color, "White Bin")
    
    def test_invalid_waste_type(self):
        with self.assertRaises(ValueError):
            WasteCategoryMapper.get_waste_category("invalid_type")

if __name__ == "__main__":
    unittest.main()
```

### Integration Test Example

```python
from inference import BiomedicalWasteInference
from csv_logger import WasteCSVLogger

# Test full pipeline
inference = BiomedicalWasteInference()
detections = inference.infer_image("test_image.jpg")

assert len(detections) > 0, "No detections found"
assert inference.logger.get_total_records() > 0, "CSV not logged"

print("✓ Integration test passed")
```

---

## 📖 EXAMPLES FOR POWER BI

### Connecting CSV to Power BI

```
1. Open Power BI Desktop
2. Home → Get Data → Text/CSV
3. Select: waste_log.csv
4. Load
5. Create queries and visualizations
```

### DAX Formulas for Power BI

```dax
// Total Waste Detected
Total Waste = COUNTROWS('Waste Log')

// Average Confidence
Avg Confidence = AVERAGE(SUBSTITUTE('Waste Log'[Confidence],"%",""))/100

// Most Common Waste Type
Top Waste = MODE.SNGL(HASH('Waste Log'[Waste_Type]))

// Count by Category
Category Count = GROUPBY(
    'Waste Log',
    'Waste Log'[Waste_Category],
    "Count", COUNTROWS()
)
```

---

## 📝 LOGGING AND DEBUGGING

### Enable Detailed Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.debug("Starting inference")
logger.info(f"Detected: {waste_type}")
logger.warning(f"Low confidence: {confidence:.2%}")
logger.error("Model loading failed")
```

### Save Debug Information

```python
from utils import FormatUtils
import json

# Save detection data
detection_data = {
    "timestamp": datetime.now().isoformat(),
    "detections": detections,
    "statistics": stats,
}

with open("debug_log.json", "w") as f:
    json.dump(detection_data, f, indent=2)
```

---

## 🔄 VERSION CONTROL AND UPDATES

### Update Model

```python
# Retrain with new data
from train_model import BiomedicalWasteModelTrainer

trainer = BiomedicalWasteModelTrainer(
    dataset_path="Biomedical_Waste_v2",
    epochs=100
)
trainer.load_pretrained_model()
trainer.train()
trainer.find_and_save_best_model()
```

### Backup Old Model

```bash
# Before retraining, backup
cp best.pt best_v1.0.pt
```

### A/B Testing Models

```python
from inference import BiomedicalWasteInference

# Test model v1
inference_v1 = BiomedicalWasteInference(model_path="best_v1.0.pt")
results_v1 = inference_v1.infer_folder("test_images/")

# Test model v2
inference_v2 = BiomedicalWasteInference(model_path="best_v2.0.pt")
results_v2 = inference_v2.infer_folder("test_images/")

# Compare statistics
stats_v1 = inference_v1.logger.get_summary_statistics()
stats_v2 = inference_v2.logger.get_summary_statistics()

print(f"v1 Confidence: {stats_v1['average_confidence']}%")
print(f"v2 Confidence: {stats_v2['average_confidence']}%")
```

---

**End of Implementation Guide**

For questions or clarifications, refer to README.md or inline code comments.

