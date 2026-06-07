# AI-Based Medical Waste Segregation Monitoring System

An automated, local computer vision monitoring system designed for multi-speciality hospitals to detect, classify, and recommend disposal bins for biomedical waste in real-time.

The system utilizes a locally-deployed YOLO model (`best.pt`) mounted overhead to monitor waste disposal areas, logging every detection to a CSV format optimized for direct integration with Power BI dashboards.

---

## 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Final Detection Classes &amp; Mappings](#-final-detection-classes--mappings)
3. [System Architecture &amp; Camera Placement](#-system-architecture--camera-placement)
4. [Folder Structure](#-folder-structure)
5. [Installation &amp; Requirements](#-installation--requirements)
6. [How to Run Inference](#-how-to-run-inference)
7. [CSV Logging &amp; Power BI Integration](#-csv-logging--power-bi-integration)
8. [Troubleshooting &amp; Error Handling](#-troubleshooting--error-handling)

---

## 🎯 Project Overview

In hospital environments, proper segregation of medical waste is critical for biosafety compliance and environmental protection. This system:

* **Performs YOLO Inference** using the pre-trained `best.pt` model.
* **Identifies Biomedical Waste Category** (Sharps, infectious, contaminated recyclable, glass, etc.).
* **Recommends Bins** (White, Red, Yellow, Blue, or General).
* **Logs Detections** with unique sequential Waste IDs (`W001`, `W002`, etc.) and decimal confidence scores.
* **Feeds Power BI Dashboards** for real-time compliance monitoring and waste generation analysis.

---

## 🔍 Final Detection Classes & Mappings

The model is trained to detect exactly **8 distinct waste classes**. The categories and color-coded disposal recommendations are mapped as follows:

| Detected Class            | Biomedical Waste Category     | Recommended Disposal Bin    | BGR Color Code      |
| :------------------------ | :---------------------------- | :-------------------------- | :------------------ |
| **needle**          | Sharps Waste                  | **White Bin**         | `(240, 240, 240)` |
| **syringe**         | Sharps Waste                  | **White Bin**         | `(240, 240, 240)` |
| **glove**           | Contaminated Recyclable Waste | **Red Bin**           | `(0, 0, 255)`     |
| **mask**            | Contaminated Recyclable Waste | **Red Bin**           | `(0, 0, 255)`     |
| **iv_tube**         | Contaminated Recyclable Waste | **Red Bin**           | `(0, 0, 255)`     |
| **cotton**          | Infectious Waste              | **Yellow Bin**        | `(0, 255, 255)`   |
| **medicine_bottle** | Glass Waste                   | **Blue Bin**          | `(255, 0, 0)`     |
| **general_waste**   | Non-Biomedical Waste          | **General Waste Bin** | `(80, 80, 80)`    |

---

## 🏗️ System Architecture & Camera Placement

### Local Inference Pipeline

```
Input Frame (Image / Directory / Webcam)
     ↓
Image Preprocessing (OpenCV)
     ↓
YOLO Inference (using weights/best.pt)
     ↓
Class Detection & Confidence Calculation
     ↓
Waste Category Identification (Rule-Based Engine)
     ↓
Disposal Bin Recommendation (Rule-Based Engine)
     ↓
OpenCV Live Overlay & Frame Saving
     ↓
CSV Logging (logs/waste_log.csv)
     ↓
Power BI Analytics
```

### Camera Strategy

* **Placement:** Fixed ceiling-mounted RGB camera.
* **Height:** 2.5 – 3.0 meters directly above the waste disposal table or bins.
* **Perspective:** Top-down orthographic view to minimize perspective occlusion.
* **Coverage Area:** Approximately 2m × 2m coverage.
* **Deployment Locations:** ICU, Operation Theatres, Diagnostic Laboratories, Emergency Departments, General Wards, and Biomedical Waste Collection Areas.

---

## 📂 Folder Structure

```
Biomedical_Waste_Project/
│
├── weights/
│   └── best.pt               # Pre-trained YOLO weights (place here)
│
├── sample_images/            # Put test images here
│
├── output_images/            # Annotated outputs (auto-saved)
│
├── logs/
│   └── waste_log.csv         # Power BI ready CSV log (auto-generated)
│
├── reports/                  # Placeholder for generated analytics reports
│
├── config.py                 # Central configuration variables & paths
├── category_mapping.py       # Rule engine mapping classes to categories/bins
├── csv_logger.py             # Appends detections and increments Waste IDs
├── utils.py                  # OpenCV drawing & file utilities
├── inference.py              # Main execution script
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation (this file)
```

---

## 🛠️ Installation & Requirements

### Prerequisites

* Python 3.10+ installed.
* NVIDIA GPU (Optional but highly recommended for fast inference).

### Installation

1. Navigate into the project directory:
   ```bash
   cd Biomedical_Waste_Project
   ```
2. Create and activate a clean virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/macOS
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place the trained weights file (`best.pt`) inside the `weights/` directory.

---

## 🚀 How to Run Inference

The script `inference.py` supports three runtime modes.

### 1. Single Image Inference (MODE 1)

Pass a single image path. The model will run prediction, output results to the terminal, append entries to the CSV, and save the annotated image under `output_images/`.

```bash
python inference.py --image sample_images/test.jpg
```

### 2. Folder Batch Inference (MODE 2)

Process a directory of images sequentially. Ideal for retrospective audit checks.

```bash
python inference.py --folder sample_images/
```

### 3. Webcam Live Inference (MODE 3)

Run live inference using the local webcam.

* Shows live bounding boxes, categories, recommended bins, and confidence overlays.
* Displays real-time FPS on the upper left.
* **Debounced Auto-logging:** Saves the frame automatically when a new waste item is detected (saved to `output_images/`) and records it in `logs/waste_log.csv`.
* Press **`Q`** inside the live window to safely quit.

```bash
python inference.py --webcam
```

*Note: You can override the default confidence threshold of `0.50` using the `--conf` argument:*

```bash
python inference.py --image sample_images/test.jpg --conf 0.65
```

---

## 📊 CSV Logging & Power BI Integration

Every detection is recorded into `logs/waste_log.csv` using the following data model:

### Fact Table Schema (`Waste_Classification_Log`):

* **Timestamp:** DateTime in `%Y-%m-%d %H:%M` format.
* **Waste_ID:** Unique sequential identifier (`W001`, `W002`, `W003`, etc.).
* **Waste_Type:** Text class name (e.g., `needle`, `glove`).
* **Waste_Category:** Text category name (e.g., `Sharps Waste`).
* **Recommended_Bin:** Text bin recommendation (e.g., `White Bin`).
* **Confidence:** Decimal confidence ratio (e.g., `0.97` instead of `97%` for clean Power BI decimal calculations).
* **Image_Name:** The file name of the source image or the saved live frame (e.g., `webcam_frame_W001.jpg`).

### CSV Sample Output:

```csv
Timestamp,Waste_ID,Waste_Type,Waste_Category,Recommended_Bin,Confidence,Image_Name
2026-06-05 10:01,W001,needle,Sharps Waste,White Bin,0.97,test.jpg
2026-06-05 10:02,W002,glove,Contaminated Recyclable Waste,Red Bin,0.89,webcam_frame_W002.jpg
```

### Power BI Dashboard Setup Guides

The CSV data format directly feeds these 7 dashboards:

1. **Waste Overview:** Use Card visualizations for *Total Waste Items Detected* (`COUNT(Waste_ID)`), *Most Common Waste Type*, *Most Common Waste Category*, and a Gauge for *Average Detection Confidence*.
2. **Waste Type Analysis:** Clustered bar chart showing the frequency distribution of individual items.
3. **Waste Category Analysis:** Donut chart showcasing the proportional breakdown of biomedical waste divisions (e.g., Sharps vs. Infectious).
4. **Recommended Bin Analysis:** Column chart displaying predicted load allocations per bin color.
5. **Waste Generation Trend:** Line chart plotting detection counts grouped by day/week.
6. **Hourly Waste Pattern:** Bar chart plotting detections by hour of day (0-23) to optimize waste disposal staff shifts.
7. **Confidence Analysis:** Histogram of confidence intervals to monitor model reliability.
