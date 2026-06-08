# AI-Based Biomedical Waste Classification & Bin Recommendation System
## Streamlit Frontend Integration & Deployment Guide

This report details the design and deployment of the frontend dashboard built for your final-year medical waste segregation project. The frontend serves as a premium, hospital-ready user interface connecting your pre-trained YOLOv11 model (`weights/best.pt`) with real-time logging (`logs/waste_log.csv`) and Power BI analytics.

---

## 📂 Project Directory Structure

```
c:/Users/anush/Desktop/L&T/
├── app.py                      # Main Streamlit Dashboard Application
├── config.py                   # Centralized Configuration Parameters
├── category_mapping.py         # Category Map (e.g. needle -> Sharps Waste)
├── csv_logger.py               # Auto-Logging Manager (W001, W002, etc.)
├── inference.py                # Core YOLOv11 Inference Pipeline
├── utils.py                    # OpenCV Drawing & Image Helpers
├── requirements.txt            # Project Dependencies (including Streamlit)
├── weights/
│   └── best.pt                 # Pre-trained YOLOv11 Weights
├── logs/
│   └── waste_log.csv           # Persistent Detection Database
├── css/
│   └── style.css               # Custom CSS Healthcare Theme Styling
├── output_images/              # Saved Detections & Webcam Frames
├── sample_images/              # Test images (test.jpg, etc.)
└── reports/
    └── frontend_deployment_guide.md  # Local copy of this Guide
```

---

## 💻 Technical Stack & Integration

- **Frontend:** Streamlit (`app.py`) for clean dashboard structures.
- **Deep Learning:** Ultralytics (`YOLOv11`) backend for object detection.
- **Data Engineering:** Pandas & NumPy for real-time aggregation and CSV handling.
- **Visual Styles:** Vanilla CSS with custom layout tokens (borders, shadows, grid flexboxes, and a dark/light medical color palette).

---

## ⚙️ Dashboard Features Breakdown

### 1. Tab 1: 🔍 Waste Analysis
- **Drag-and-Drop Uploader:** Supports `.jpg`, `.jpeg`, and `.png` images.
- **Side-by-Side Verification:** Renders the original upload and the YOLOv11 annotated bounding box image in parallel columns.
- **Data Table:** Renders a clean Pandas DataFrame of all items detected, showing item, category, recommended bin, and confidence.
- **Recommendation Cards:** High-contrast, color-coded cards corresponding to the physical disposal bin colors (Red, Yellow, Blue, White, or General).

### 2. Tab 2: 📹 Live Webcam Stream
- **Self-Cleaning Thread:** A custom `VideoCapture` loop with a `try...finally` block that automatically releases webcam hardware if the user leaves or clicks stop.
- **Debounced Logging:** Implements a 2-second logging cooldown per waste type. This prevents overloading the CSV log with redundant rows for the same object held in front of the camera.
- **Live Overlays:** Renders the current bounding boxes, labels, and running FPS on-screen.

### 3. Tab 3: 📊 Statistics & Audit logs
- **KPI Dash Card Array:** Custom styled cards showing total records, the most common waste item, average model confidence, top category, and the most heavily utilized bin.
- **Sortable History:** An interactive data grid showing the last 20 detections (newest first) with pagination and search.
- **Secure Download:** A button allowing operators to instantly download the full audit trail as a CSV file.

### 4. Tab 4: 📈 Power BI Integration
- **Direct Sync Info:** Explains the data sync pipeline to ensure seamless hand-offs.
- **Explorer Opener:** Leverages Python's `os.startfile` on Windows to open the log directory in Windows File Explorer with a single click.

---

## 🚀 Running the Application

Follow these steps to launch the frontend on your local system:

1. Open a terminal or PowerShell prompt in your project root:
   ```powershell
   cd "c:\Users\anush\Desktop\L&T"
   ```
2. Activate your project virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```
3. Run the Streamlit server:
   ```powershell
   streamlit run app.py
   ```
4. A web browser page will open automatically at:
   `http://localhost:8501`
