# AI-Based Medical Waste Segregation Monitoring System

**Project Title:** AI-BASED MEDICAL WASTE SEGREGATION MONITORING SYSTEM FOR MULTI-SPECIALITY HOSPITALS


**Technology Stack:** Python, Ultralytics YOLO, Pandas, Power BI

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Deployment Locations](#deployment-locations)
5. [Camera Placement Strategy](#camera-placement-strategy)
6. [Dataset Information](#dataset-information)
7. [Installation & Setup](#installation--setup)
8. [Training Instructions](#training-instructions)
9. [Inference Instructions](#inference-instructions)
10. [CSV Logging & Power BI Integration](#csv-logging--power-bi-integration)
11. [Power BI Dashboard Setup](#power-bi-dashboard-setup)
12. [Project Structure](#project-structure)
13. [Challenges & Limitations](#challenges--limitations)


---

## 🎯 Project Overview

### Objective

To continuously monitor biomedical waste items using a computer vision system and accurately identify:

- **Waste Type** - The specific waste item (needle, syringe, glove, etc.)
- **Biomedical Waste Category** - The classification category (Sharps, Infectious, Recyclable, Glass, Non-Biomedical)
- **Recommended Disposal Bin** - The appropriate disposal container (White, Yellow, Red, Blue, or General)

The system uses a **locally-deployed YOLOv11 Nano model** for real-time, privacy-preserving inference without cloud connectivity.

### Scope

✅ **What This System Does:**
- Detects biomedical waste items in real-time
- Classifies detected items into categories
- Recommends appropriate disposal bins
- Logs detections to CSV for analytics
- Provides Power BI dashboards for waste monitoring



### Key Metrics (YOLOv11 Nano Model)

| Metric | Value |
|--------|-------|
| mAP@50 | 95.5% |
| Precision | 91.4% |
| Recall | 95.4% |
| F1 Score | 93.3% |

---

## ✨ Features

### 1. **Multi-Input Inference**
- Single image inference
- Batch folder processing
- Real-time webcam inference
- Video file support (via command-line extension)

### 2. **Accurate Classification**
- 8 waste item classes
- High precision (91.4%) and recall (95.4%)
- Minimal false positives

### 3. **Automated Logging**
- CSV logging with automatic Waste ID generation (W001, W002, etc.)
- Timestamp recording
- Confidence tracking
- Image source tracking

### 4. **Real-Time Display**
- Console output with formatted results
- Annotated image generation
- Category and bin information overlay

### 5. **Analytics Ready**
- Power BI compatible CSV format
- Statistical summaries
- Aggregatable data structure

---

## 🏗️ System Architecture

### Local Inference Pipeline

```
Input (Image/Video/Webcam)
    ↓
Image Preprocessing
(Resize, Normalize)
    ↓
YOLO Inference
    ↓
Bounding Box Detection
    ↓
Waste Classification
    ↓
Waste Category Identification
    ↓
Rule-Based Bin Recommendation
    ↓
CSV Logging
    ↓
Annotated Output
    ↓
Console & Display Output
    ↓
Power BI Dashboard
```

### Detection Classes (8 Total)

1. **needle** → Sharps Waste → White Bin
2. **syringe** → Sharps Waste → White Bin
3. **glove** → Contaminated Recyclable Waste → Red Bin
4. **mask** → Contaminated Recyclable Waste → Red Bin
5. **iv_tube** → Contaminated Recyclable Waste → Red Bin
6. **cotton** → Infectious Waste → Yellow Bin
7. **medicine_bottle** → Glass Waste → Blue Bin
8. **general_waste** → Non-Biomedical Waste → General Waste Bin

---

## 🏥 Deployment Locations

The system is designed for deployment in high-volume biomedical waste generation areas:

### Primary Deployment Areas

1. **Intensive Care Unit (ICU)**
   - High volume of syringes, needles, IV tubes
   - Critical waste segregation required

2. **Operation Theatre (OT)**
   - Surgical waste (needles, gloves, gauze, instruments)
   - Time-sensitive segregation

3. **Diagnostic Laboratories**
   - Test tubes, medicine bottles, sharps
   - Sample-related waste

4. **Emergency Department**
   - Mixed waste types
   - High volume during peak hours

5. **General Wards**
   - General contaminated waste
   - Medication-related waste

6. **Biomedical Waste Collection Areas**
   - Central waste segregation points
   - High diversity of waste types

---

## 📷 Camera Placement Strategy

### Camera Specifications

| Parameter | Value |
|-----------|-------|
| Camera Type | Fixed Ceiling-Mounted RGB |
| Placement Height | 2.5 - 3.0 meters |
| Field of View | ~2m × 2m |
| Viewpoint | Top-Down |
| Image Quality | 1080p minimum (1280×720) |
| Frame Rate | 30 FPS recommended |

### Design Objectives

✅ **Minimize Occlusion** - Top-down angle reduces shadows and obstructions  
✅ **Ensure Clear Visibility** - Direct view of waste items  
✅ **Consistent Image Quality** - Controlled lighting and angle  
✅ **AI-Optimized** - Consistent perspective for accurate detection  

### Installation Checklist

- [ ] Mount camera 2.5-3.0 meters above waste handling area
- [ ] Position for top-down 45° to 90° angle
- [ ] Ensure 2m × 2m field of view coverage
- [ ] Test image quality before deployment
- [ ] Verify lighting conditions (avoid glare/shadows)
- [ ] Document camera position and calibration

---

## 📊 Dataset Information

### Dataset Structure

```
Biomedical_Waste/
├── train/                  # Training images (~70%)
│   ├── images/
│   └── labels/
├── valid/                  # Validation images (~15%)
│   ├── images/
│   └── labels/
├── test/                   # Test images (~15%)
│   ├── images/
│   └── labels/
├── data.yaml              # Dataset configuration
├── README.dataset.txt     # Dataset metadata
└── README.roboflow.txt    # Roboflow export info
```

### Data Annotation Strategy

The dataset was created by merging original Roboflow annotations into 8 unified classes:

| Final Class | Original Annotations |
|------------|----------------------|
| needle | needle, needle_cap |
| syringe | used_syringe |
| cotton | gauze, unused_gauze |
| iv_tube | tube |
| medicine_bottle | fluid_bottle, test_tube, glass |
| general_waste | paper, plastic, scrub |
| glove | glove |
| mask | mask |

### Training Dataset Specifications

- **Total Images:** 1000+ (varies based on Roboflow export)
- **Training Set:** ~700 images
- **Validation Set:** ~150 images
- **Test Set:** ~150 images
- **Image Format:** JPEG, PNG
- **Annotation Format:** YOLO format (xywh normalized)
- **Classes:** 8
- **min/max Dimension:** 640×640 (model input size)

---

## 🚀 Installation & Setup

### Prerequisites

- **Operating System:** Windows 10/11, Linux, or macOS
- **Python:** 3.9 or higher
- **GPU (Optional):** NVIDIA GPU with CUDA support (for faster training)
- **Disk Space:** 5GB minimum (including model, dataset, outputs)
- **RAM:** 8GB minimum (16GB recommended)

### Step 1: Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd Biomedical_Waste_Project

# Or manually download and extract the project folder
cd Biomedical_Waste_Project
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Installation Time:** 5-15 minutes (depending on internet speed and GPU drivers)

### Step 4: Verify Installation

```bash
python -c "from ultralytics import YOLO; import cv2; import torch; print('✓ All dependencies installed')"
```

### Step 5: Prepare Dataset

```bash
# Extract your Roboflow dataset to the project root
# Expected structure:
# Biomedical_Waste/
#   ├── train/
#   ├── valid/
#   ├── test/
#   └── data.yaml

# Verify structure
python -c "import os; print('✓ Dataset ready') if os.path.exists('Biomedical_Waste/data.yaml') else print('✗ data.yaml not found')"
```

### Step 6: Create Output Directories

```bash
mkdir -p sample_images
mkdir -p output_images
mkdir -p weights
mkdir -p utils
```

---

## 🎓 Training Instructions

### Option 1: Automatic Training (Recommended)

```bash
python train_model.py
```

### Option 2: Manual Training Steps

```python
from train_model import BiomedicalWasteModelTrainer

# Initialize trainer
trainer = BiomedicalWasteModelTrainer(
    dataset_path="Biomedical_Waste",
    epochs=100,
    imgsz=640,
    batch="auto"
)

# Validate dataset
if trainer.validate_dataset():
    # Load pretrained model
    trainer.load_pretrained_model()
    
    # Train
    trainer.train()
    
    # Validate
    trainer.validate()
    
    # Test
    trainer.test()
    
    # Save best model
    best_model_path = trainer.find_and_save_best_model()
    
    # Print summary
    trainer.print_training_summary()
```

### Training Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| epochs | 100 | Number of training cycles |
| imgsz | 640 | Input image size (pixels) |
| batch | auto | Automatic batch size selection |
| device | 0 | GPU device (0=first GPU, cpu=CPU) |
| patience | 15 | Early stopping patience |

### Training Output

Training creates the following structure:

```
runs/
└── detect/
    └── train/
        ├── weights/
        │   ├── best.pt      # Best model (copy to project root)
        │   └── last.pt      # Last checkpoint
        ├── results.csv      # Training metrics
        ├── confusion_matrix.png
        ├── P_curve.png
        ├── R_curve.png
        ├── F1_curve.png
        └── ...
```


### Sample Console Output

```
==================================================

Detected Waste : Syringe

Waste Category : Sharps Waste

Recommended Bin : White Bin

Confidence : 94.2%

Image : sample1.jpg

==================================================
```

---

## 📝 CSV Logging & Power BI Integration

### CSV Structure

**Filename:** `waste_log.csv`

**Columns:**

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| Timestamp | DateTime | 2024-06-06 14:23:45 | When detection occurred |
| Waste_ID | String | W001 | Unique identifier |
| Waste_Type | String | needle | Detected item class |
| Waste_Category | String | Sharps Waste | Biomedical category |
| Recommended_Bin | String | White Bin | Disposal recommendation |
| Confidence | Float | 97.5% | Detection confidence |
| Image_Name | String | sample1.jpg | Source image |

### Sample CSV Data

```csv
Timestamp,Waste_ID,Waste_Type,Waste_Category,Recommended_Bin,Confidence,Image_Name
2024-06-06 14:23:45,W001,needle,Sharps Waste,White Bin,97.50%,sample1.jpg
2024-06-06 14:23:46,W002,syringe,Sharps Waste,White Bin,94.20%,sample2.jpg
2024-06-06 14:23:47,W003,glove,Contaminated Recyclable Waste,Red Bin,89.80%,sample3.jpg
2024-06-06 14:23:48,W004,mask,Contaminated Recyclable Waste,Red Bin,92.10%,sample4.jpg
2024-06-06 14:23:49,W005,cotton,Infectious Waste,Yellow Bin,88.50%,sample5.jpg
```


### Power BI Integration

The `waste_log.csv` is designed for direct import into Power BI:

1. Open Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Browse to `waste_log.csv`
4. Click "Load"
5. Create dashboards (see next section)

---

## 📊 Power BI Dashboard Setup

### Prerequisites

- Power BI Desktop (free download)
- Generated `waste_log.csv` with detection data
- Basic Power BI knowledge

### Dashboard 1: Waste Overview

**Purpose:** High-level waste management summary

**Visualizations:**

1. **Total Waste Detected** (KPI Card)
   - Formula: `COUNT(Waste_ID)`
   - Display value and trend

2. **Most Common Waste Type** (Card)
   - Formula: Most frequent value in `Waste_Type`
   - Show count

3. **Most Common Waste Category** (Card)
   - Formula: Most frequent value in `Waste_Category`
   - Show percentage of total

4. **Average Detection Confidence** (Gauge)
   - Formula: `AVERAGE(Confidence)`
   - Min: 0%, Max: 100%, Target: 90%

**Layout:** 2×2 grid, top of dashboard

---

### Dashboard 2: Waste Type Analysis

**Purpose:** Identify which waste items are most frequently detected

**Visualizations:**

1. **Waste Type Distribution** (Clustered Bar Chart)
   - X-axis: Waste_Type
   - Y-axis: COUNT(Waste_ID)
   - Sort: Descending

2. **Waste Type Percentage Breakdown** (Pie Chart)
   - Values: Waste_Type
   - Percentages: COUNT(Waste_ID) / TOTAL

3. **Waste Type Trend Over Time** (Line Chart)
   - X-axis: Timestamp (Date)
   - Y-axis: COUNT(Waste_ID)
   - Series: Waste_Type

4. **Top 5 Waste Items** (Table)
   - Columns: Waste_Type, Count, Percentage, Avg_Confidence

**Key Insight:** Which waste item is generated most frequently?

---

### Dashboard 3: Waste Category Analysis

**Purpose:** Monitor biomedical waste categories

**Visualizations:**

1. **Waste Category Distribution** (Donut Chart)
   - Values: Waste_Category
   - Count: Waste_ID

2. **Category Breakdown Over Time** (Stacked Area Chart)
   - X-axis: Timestamp (Date)
   - Y-axis: COUNT(Waste_ID)
   - Series: Waste_Category

3. **Category Comparison** (Column Chart)
   - X-axis: Waste_Category
   - Y-axis: COUNT(Waste_ID)

4. **Category Metrics Table**
   - Columns: Waste_Category, Count, Percentage, Avg_Confidence

**Key Insight:** Which biomedical waste category contributes most to hospital waste?

---

### Dashboard 4: Recommended Bin Analysis

**Purpose:** Predict disposal bin load

**Visualizations:**

1. **Bin Color Distribution** (Horizontal Bar Chart)
   - X-axis: COUNT(Waste_ID)
   - Y-axis: Recommended_Bin
   - Color: Recommended_Bin

2. **Bin Load Trend** (Line Chart)
   - X-axis: Timestamp (Date)
   - Y-axis: COUNT(Waste_ID)
   - Series: Recommended_Bin

3. **Bin Capacity Planning** (Matrix)
   - Rows: Recommended_Bin
   - Values: COUNT(Waste_ID), AVG(Confidence)

4. **Color Legend**
   - White Bin → Sharps Waste
   - Red Bin → Contaminated Recyclable
   - Yellow Bin → Infectious Waste
   - Blue Bin → Glass Waste

**Key Insight:** Which disposal bin is expected to receive the highest load?

---

### Dashboard 5: Waste Generation Trend

**Purpose:** Monitor waste trends over time

**Visualizations:**

1. **Daily Waste Count** (Line Chart)
   - X-axis: Timestamp (Date)
   - Y-axis: COUNT(Waste_ID)
   - Show trend line

2. **Weekly Comparison** (Column Chart)
   - X-axis: Week
   - Y-axis: COUNT(Waste_ID)

3. **Waste Trend Indicator** (KPI with Trend)
   - Current period total
   - Previous period total
   - Percentage change

4. **Month-over-Month Growth** (Table)
   - Columns: Month, Total, Change%, Trend

**Key Insight:** Is waste generation increasing or decreasing over time?

**Expected Pattern:** More waste during peak hospital hours (9 AM - 5 PM)

---

### Dashboard 6: Hourly Waste Pattern

**Purpose:** Identify peak waste generation hours

**Visualizations:**

1. **Hourly Distribution** (Column Chart)
   - X-axis: Hour of Day (0-23)
   - Y-axis: COUNT(Waste_ID)
   - Highlight peak hours

2. **Heatmap by Hour & Day** (Matrix)
   - Rows: Day of Week
   - Columns: Hour
   - Values: COUNT(Waste_ID)

3. **Peak Hours Table**
   - Columns: Hour, Count, Percentage, Top_Waste_Type

4. **Average Confidence by Hour** (Line Chart)
   - X-axis: Hour
   - Y-axis: AVG(Confidence)

**Key Insight:** During which hours is waste generation highest?

**Use Case:** Optimize staff scheduling during peak waste generation

---

### Dashboard 7: Confidence Analysis

**Purpose:** Model reliability assessment

**Visualizations:**

1. **Confidence Distribution** (Histogram)
   - X-axis: Confidence (0-100%)
   - Y-axis: COUNT(Waste_ID)
   - Bins: 10%

2. **Confidence Trend** (Line Chart)
   - X-axis: Timestamp (Date)
   - Y-axis: AVG(Confidence)
   - Show min/max bands

3. **Confidence by Waste Type** (Box Plot)
   - Y-axis: Confidence
   - X-axis: Waste_Type

4. **Low Confidence Analysis** (Table)
   - Show detections with Confidence < 80%
   - Columns: Waste_Type, Confidence, Timestamp

**Key Insight:** How reliable is the AI model?

**Threshold:** 
- ✅ High Confidence: > 90%
- ⚠️ Medium Confidence: 80-90%
- ❌ Low Confidence: < 80%

---

## 📁 Project Structure

```
Biomedical_Waste_Project/
│
├── train_model.py              # Training script (YOLOv11 training)
├── inference.py                # Inference pipeline (image/folder/webcam)
├── category_mapping.py         # Waste-to-category mapping logic
├── csv_logger.py              # CSV logging functionality
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── best.pt                     # Trained model (generated after training)
├── waste_log.csv              # Detection log (auto-generated)
│
├── Biomedical_Waste/          # Dataset directory (user-provided)
│   ├── train/
│   ├── valid/
│   ├── test/
│   ├── data.yaml
│   └── README.roboflow.txt
│
├── sample_images/             # Test images for inference
│   ├── sample1.jpg
│   ├── sample2.jpg
│   └── ...
│
├── output_images/             # Annotated output images (auto-generated)
│   ├── annotated_sample1.jpg
│   ├── annotated_sample2.jpg
│   └── ...
│
├── weights/                   # Additional model weights (if needed)
│   └── ...
│
└── utils/                     # Utility scripts (optional)
    ├── data_augmentation.py
    ├── dataset_analysis.py
    └── model_evaluation.py
```

---

## 🚨 Challenges & Limitations

### 1. Limited Public Biomedical Waste Datasets

**Problem:**
- High-quality annotated biomedical waste datasets are extremely rare
- Most public datasets focus on generic objects (COCO, ImageNet)
- Compliance violation detection data is non-existent

**Current Solution:**
- Used Roboflow to create custom dataset with 8 unified classes
- Limited to segregation and bin recommendation (not compliance)

**Why This Matters:**
- Datasets exist for individual items: needle, glove, mask, cotton
- But no datasets for: waste in bins, disposal behavior, compliance violations
- This limits the system to detection/segregation only

**Workaround:**
```python
# System focuses on these verified tasks:
- Detect waste items ✓
- Classify items ✓
- Recommend bins ✓

# Compliance monitoring (future scope)
```

### 2. Similar Appearance of Waste Items

**Problem:**
- Some waste items visually similar (glove vs. mask, medicine bottle vs. test tube)
- Overlapping/occluded items
- Different lighting conditions

**Solution:**
- Model trained on diverse samples
- Confidence scores help identify ambiguous detections
- Log low-confidence items for manual review

**Code Implementation:**
```python
# Filter low-confidence detections
if confidence < 0.80:  # 80% threshold
    log_for_manual_review(detection)
else:
    auto_classify(detection)
```

### 3. Overlapping Waste Objects

**Problem:**
- Glove covering syringe
- Multiple items in frame
- Clustered waste

**Solution:**
- Dataset includes overlapping samples
- YOLO detects multiple objects simultaneously
- Bounding boxes handle multiple detections

**Example:**
```
Input: Glove covering syringe
Output:
  - Glove: 92% confidence → Red Bin
  - Syringe: 88% confidence → White Bin
```

### 4. Environmental Variations

**Problem:**
- Different lighting conditions
- Camera angles
- Background variations

**Mitigation:**
- Top-down camera fixed position
- Controlled lighting recommended
- Preprocessing handles variations

### 5. Dataset Size

**Problem:**
- Finite training data
- May not cover all edge cases
- Real-world variations

**Continuous Improvement:**
```python
# Log edge cases for retraining
if is_edge_case(detection):
    save_for_retraining(image, manual_annotation)
    
# Retrain periodically with new data
# Improves model over time
```
---


## 📄 License & Citation

**Project:** AI-Based Medical Waste Segregation Monitoring System  
**Author:** Anush Ramesh 

---

**Last Updated:** June 2026  

---
