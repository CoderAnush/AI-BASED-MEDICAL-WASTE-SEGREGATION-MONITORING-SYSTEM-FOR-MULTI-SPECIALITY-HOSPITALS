import os
import sys
import time
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

# Import existing system modules
from config import SystemConfig
from category_mapping import WasteCategoryMapper
from csv_logger import WasteCSVLogger
from utils import ImageUtils, VisualizationUtils

# Page Configuration
st.set_page_config(
    page_title="AI Medical Waste Segregation Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Try loading custom CSS
css_path = Path("css/style.css")
if css_path.exists():
    local_css(css_path)

# Initialize Session State
if 'webcam_running' not in st.session_state:
    st.session_state.webcam_running = False

# Cached model/pipeline loader to avoid reloading on every click
@st.cache_resource
def get_inference_pipeline():
    # Setup directories on startup
    SystemConfig.setup_directories()
    # Import here to prevent initialization output before streamlit config
    from inference import BiomedicalWasteInferencePipeline
    # Set default confidence from config, can be adjusted dynamically
    return BiomedicalWasteInferencePipeline(confidence_threshold=0.5)

# Initialize pipeline
try:
    pipeline = get_inference_pipeline()
except Exception as e:
    st.error(f"Failed to initialize YOLO Inference Pipeline: {e}")
    st.stop()

# --- TOP HEADER ---
st.markdown("""
<div class="main-header">
    <div class="header-title">🏥 AI-Based Biomedical Waste Classification & Bin Recommendation System</div>
    <div class="header-subtitle">YOLOv11 + Python + Power BI | Multi-Speciality Hospital Compliance Portal</div>
</div>
""", unsafe_allow_html=True)

# Sidebar configurations
st.sidebar.markdown("### ⚙️ Detection Settings")
confidence_slider = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=1.0,
    value=float(SystemConfig.MODEL_CONFIG["confidence_threshold"]),
    step=0.05,
    help="Minimum confidence score to detect objects."
)

# Update pipeline threshold dynamically without reloading model
pipeline.conf_threshold = confidence_slider

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏥 System Status")
st.sidebar.success("✓ YOLOv11 Model Ready")
st.sidebar.success("✓ CSV Logging Active")
st.sidebar.info(f"Model Path: `weights/best.pt``")
st.sidebar.info(f"Log Path: `logs/waste_log.csv``")

# Create tabs for structured page navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Waste Analysis", 
    "📹 Live Webcam Stream", 
    "📊 Statistics & History", 
    "📈 Power BI Integration"
])

# ==========================================
# TAB 1: WASTE ANALYSIS (IMAGE UPLOAD)
# ==========================================
with tab1:
    st.markdown("### 📥 Single Waste Item Analysis")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Drag and drop file uploader
        uploaded_file = st.file_uploader(
            "Upload Biomedical Waste Image", 
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG"
        )
        
        if uploaded_file is not None:
            # Display uploaded image preview
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image Preview", width="stretch")
            
            # Analyze button
            analyze_btn = st.button("🔍 Analyze Waste", type="primary", width="stretch")
    
    with col2:
        if uploaded_file is not None and 'analyze_btn' in locals() and analyze_btn:
            with st.spinner("Running YOLOv11 Model Inference..."):
                # Convert PIL image to BGR numpy array
                img_np = np.array(image)
                if len(img_np.shape) == 2:  # Grayscale
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)
                elif img_np.shape[2] == 4:  # RGBA
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
                else:  # RGB
                    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
                
                # Perform inference and log results to CSV automatically
                annotated_bgr, detections = pipeline.run_inference_on_frame(
                    img_bgr, 
                    source_name=uploaded_file.name, 
                    log_results=True
                )
                
                # Display Annotated Image
                annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
                st.image(annotated_rgb, caption="Annotated Detections (YOLOv11)", width="stretch")
                
                # Section 4: Detection Results Table
                if detections:
                    st.markdown("<h3 class='section-title'>📋 Detection Results</h3>", unsafe_allow_html=True)
                    
                    # Formulate display table
                    table_data = []
                    for det in detections:
                        table_data.append({
                            "Waste Item": det["waste_type"].replace('_', ' ').title(),
                            "Waste Category": det["waste_category"],
                            "Recommended Bin": det["recommended_bin"],
                            "Confidence": f"{det['confidence'] * 100:.1f}%"
                        })
                    
                    df_detections = pd.DataFrame(table_data)
                    st.dataframe(df_detections, width="stretch", hide_index=True)
                    
                    # Section 5: Summary Card
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 🏷️ Classification Summary")
                    
                    total_objs = len(detections)
                    st.markdown(f"**Total Objects Found:** `{total_objs}`")
                    
                    # Render custom styled cards for each detection
                    for det in detections:
                        w_type = det["waste_type"]
                        cat = det["waste_category"]
                        bin_name = det["recommended_bin"]
                        conf = det["confidence"]
                        waste_id = det["waste_id"]
                        
                        # Set styling classes
                        css_class = "bin-general"
                        if "White" in bin_name:
                            css_class = "bin-white"
                        elif "Red" in bin_name:
                            css_class = "bin-red"
                        elif "Yellow" in bin_name:
                            css_class = "bin-yellow"
                        elif "Blue" in bin_name:
                            css_class = "bin-blue"
                            
                        # Class specific icons
                        icon = "♻️"
                        if w_type == "needle": icon = "📍"
                        elif w_type == "syringe": icon = "💉"
                        elif w_type == "glove": icon = "🧤"
                        elif w_type == "mask": icon = "😷"
                        elif w_type == "iv_tube": icon = "🧪"
                        elif w_type == "cotton": icon = "🧻"
                        elif w_type == "medicine_bottle": icon = "🍼"
                        elif w_type == "general_waste": icon = "🗑️"
                        
                        st.markdown(f"""
                        <div class="bin-card {css_class}">
                            <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 0.4rem;">{icon} {w_type.replace('_', ' ').title()}</div>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; font-size: 0.95rem;">
                                <div><b>Category:</b> {cat}</div>
                                <div><b>Disposal Bin:</b> {bin_name}</div>
                                <div><b>Confidence:</b> {conf * 100:.1f}%</div>
                                <div><b>Waste ID:</b> {waste_id}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No waste items detected above the confidence threshold. Please try another image or lower the threshold.")
        elif uploaded_file is None:
            st.info("ℹ️ Upload an image on the left and click 'Analyze Waste' to get recommendations.")

# ==========================================
# TAB 2: LIVE WEBCAM STREAM
# ==========================================
with tab2:
    st.markdown("### 📹 Real-Time Webcam Segregation Monitoring")
    st.write("Connect an external or integrated webcam to run real-time waste analysis.")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Control Buttons
        st.markdown("#### Stream Controls")
        start_btn = st.button("📹 Start Live Detection", type="primary", width="stretch", disabled=st.session_state.webcam_running)
        stop_btn = st.button("🛑 Stop Live Detection", type="secondary", width="stretch", disabled=not st.session_state.webcam_running)
        
        if start_btn:
            st.session_state.webcam_running = True
            st.rerun()
            
        if stop_btn:
            st.session_state.webcam_running = False
            st.rerun()
            
        st.markdown("---")
        st.markdown("""
        **Webcam Operation Info:**
        - Detection frame rate depends on system hardware.
        - Automatic logging is **debounced** (2-second cooldown per item type) to prevent duplicate log entries.
        - Annotated frames are auto-saved in `output_images/` when logged.
        """)
        
    with col2:
        if st.session_state.webcam_running:
            # Open Video Capture
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Error: Webcam could not be accessed. Ensure it is connected and not in use by another application.")
                st.session_state.webcam_running = False
            else:
                # Web-stream layout
                st.info("Live Video Feed Active - Bounding boxes and labels are rendered in real-time.")
                frame_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                # Debounce logic parameters
                last_logged_time = {}
                log_cooldown_seconds = 2.0
                
                try:
                    # Live inference loop
                    while st.session_state.webcam_running:
                        ret, frame = cap.read()
                        if not ret:
                            st.error("Failed to capture video frame.")
                            break
                        
                        # Calculate current FPS
                        start_time = time.time()
                        
                        # Predict frame without committing log directly (we do it debounced)
                        annotated_frame, detections = pipeline.run_inference_on_frame(
                            frame, 
                            source_name="webcam_live", 
                            log_results=False
                        )
                        
                        current_time = time.time()
                        
                        # Handle debounced logging
                        for det in detections:
                            w_type = det["waste_type"]
                            if w_type not in last_logged_time or (current_time - last_logged_time[w_type] > log_cooldown_seconds):
                                last_logged_time[w_type] = current_time
                                
                                # Generate new ID and Log
                                waste_id = pipeline.logger.get_next_waste_id()
                                webcam_image_name = f"webcam_frame_{waste_id}.jpg"
                                
                                # Log to CSV
                                pipeline.logger.log_detection(
                                    waste_type=w_type,
                                    waste_category=det["waste_category"],
                                    recommended_bin=det["recommended_bin"],
                                    confidence=det["confidence"],
                                    image_name=webcam_image_name
                                )
                                
                                # Save the frame
                                frame_save_path = pipeline.output_dir / webcam_image_name
                                ImageUtils.save_image(annotated_frame, frame_save_path)
                                
                                # Display toast notification in Streamlit
                                st.toast(f"Logged {waste_id}: {w_type.capitalize()} -> {det['recommended_bin']}", icon="✅")
                        
                        # Calculate FPS
                        fps = 1.0 / (time.time() - start_time) if (time.time() - start_time) > 0 else 30.0
                        
                        # Draw FPS overlay inside Streamlit UI
                        cv2.putText(
                            annotated_frame,
                            f"FPS: {fps:.1f}",
                            (15, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2,
                            lineType=cv2.LINE_AA
                        )
                        
                        # Show current live detection list
                        if detections:
                            det_list = [f"{d['waste_type'].capitalize()} ({d['confidence'] * 100:.0f}%)" for d in detections]
                            stats_placeholder.markdown(f"**🔴 Live Detections:** {', '.join(det_list)}")
                        else:
                            stats_placeholder.markdown("**🟢 Scanning...** No waste item detected.")
                        
                        # Render frame
                        rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(rgb_frame, channels="RGB", width="stretch")
                        
                        # Short sleep to give control back to system
                        time.sleep(0.01)
                        
                except Exception as e:
                    st.error(f"Webcam session error: {e}")
                finally:
                    # Release camera on exit or interruption
                    cap.release()
                    frame_placeholder.empty()
                    stats_placeholder.empty()
                    st.session_state.webcam_running = False
                    st.rerun()
        else:
            st.info("ℹ️ Click 'Start Live Detection' to launch the webcam stream.")

# ==========================================
# TAB 3: STATISTICS & HISTORY
# ==========================================
with tab3:
    st.markdown("### 📊 Detection Insights & Audit Logs")
    
    # Reload stats/logs
    csv_path = SystemConfig.CSV_LOG_PATH
    
    if not csv_path.exists() or os.path.getsize(csv_path) <= 60:
        st.info("ℹ️ No logs recorded yet. Run detections to generate statistics.")
    else:
        try:
            # Read CSV, skipping any malformed lines to prevent crashes
            df = pd.read_csv(csv_path, on_bad_lines='skip')
            
            # Remove any trailing empty rows
            df = df.dropna(subset=["Waste_ID"])
            
            # --- Section 8: Live Statistics ---
            st.markdown("<h3 class='section-title'>📈 KPI Performance Metrics</h3>", unsafe_allow_html=True)
            
            total_detections = len(df)
            
            # Calculate values
            if total_detections > 0:
                most_common_waste = df['Waste_Type'].mode()[0].replace('_', ' ').title() if not df['Waste_Type'].mode().empty else "N/A"
                
                # Confidence average
                avg_conf_raw = df['Confidence'].mean()
                # Handle cases where confidence is already percentage
                if avg_conf_raw <= 1.0:
                    avg_confidence = f"{avg_conf_raw * 100:.1f}%"
                else:
                    avg_confidence = f"{avg_conf_raw:.1f}%"
                    
                most_common_category = df['Waste_Category'].mode()[0] if not df['Waste_Category'].mode().empty else "N/A"
                most_used_bin = df['Recommended_Bin'].mode()[0] if not df['Recommended_Bin'].mode().empty else "N/A"
            else:
                most_common_waste = "N/A"
                avg_confidence = "N/A"
                most_common_category = "N/A"
                most_used_bin = "N/A"
            
            # Render Premium HTML KPI Cards
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card" style="border-top-color: #0d6efd;">
                    <div class="kpi-icon">📊</div>
                    <div class="kpi-value">{total_detections}</div>
                    <div class="kpi-label">Total Detections</div>
                </div>
                <div class="kpi-card" style="border-top-color: #20c997;">
                    <div class="kpi-icon">♻️</div>
                    <div class="kpi-value">{most_common_waste}</div>
                    <div class="kpi-label">Most Common Waste</div>
                </div>
                <div class="kpi-card" style="border-top-color: #fd7e14;">
                    <div class="kpi-icon">🎯</div>
                    <div class="kpi-value">{avg_confidence}</div>
                    <div class="kpi-label">Avg Confidence</div>
                </div>
                <div class="kpi-card" style="border-top-color: #6f42c1;">
                    <div class="kpi-icon">🏥</div>
                    <div class="kpi-value">{most_common_category}</div>
                    <div class="kpi-label">Most Common Category</div>
                </div>
                <div class="kpi-card" style="border-top-color: #dc3545;">
                    <div class="kpi-icon">🗑️</div>
                    <div class="kpi-value">{most_used_bin}</div>
                    <div class="kpi-label">Most Used Bin</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- Section 7: Detection History ---
            st.markdown("<h3 class='section-title'>📋 Recent Detections History (Last 20)</h3>", unsafe_allow_html=True)
            
            # Prepare df for showing
            df_history = df.tail(20).copy()
            # Sort with newest first
            df_history = df_history.iloc[::-1]
            
            # Standardize columns to display nicely
            display_df = df_history[[
                "Waste_ID", 
                "Waste_Type", 
                "Waste_Category", 
                "Recommended_Bin", 
                "Confidence", 
                "Timestamp"
            ]].copy()
            
            # Format display strings
            display_df["Waste_Type"] = display_df["Waste_Type"].apply(lambda x: str(x).replace('_', ' ').title())
            display_df["Confidence"] = display_df["Confidence"].apply(lambda x: f"{float(x)*100:.1f}%" if float(x) <= 1.0 else f"{float(x):.1f}%")
            
            # Display interactive sortable table
            st.dataframe(
                display_df, 
                width="stretch", 
                hide_index=True,
                column_config={
                    "Waste_ID": st.column_config.TextColumn("Waste ID", width="small"),
                    "Waste_Type": st.column_config.TextColumn("Waste Type"),
                    "Waste_Category": st.column_config.TextColumn("Waste Category"),
                    "Recommended_Bin": st.column_config.TextColumn("Recommended Bin"),
                    "Confidence": st.column_config.TextColumn("Confidence", width="small"),
                    "Timestamp": st.column_config.TextColumn("Timestamp")
                }
            )
            
            # --- Section 9: Download Logs ---
            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Detection Logs (CSV)",
                data=csv_data,
                file_name="waste_log.csv",
                mime="text/csv",
                width="stretch"
            )
            
        except Exception as e:
            st.error(f"Error parsing log file: {e}")

# ==========================================
# TAB 4: POWER BI INTEGRATION
# ==========================================
with tab4:
    st.markdown("### 📈 Power BI Business Intelligence Dashboard Integration")
    
    st.markdown("""
    <div class="info-banner">
        <b>💡 Analytics Dashboard System Architecture</b><br>
        The Power BI dashboard reads <b>waste_log.csv</b> directly and updates automatically when the report is refreshed.
    </div>
    """, unsafe_allow_html=True)
    
    # Show stats
    csv_path = SystemConfig.CSV_LOG_PATH
    total_records = 0
    if csv_path.exists():
        try:
            df_records = pd.read_csv(csv_path, on_bad_lines='skip')
            total_records = len(df_records.dropna(subset=["Waste_ID"]))
        except Exception:
            pass
            
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📂 Data Pipeline Paths")
        st.markdown(f"**Log File Location:** `{csv_path.resolve()}`")
        st.markdown(f"**Dashboard Output Folder:** `{SystemConfig.LOGS_DIR.resolve()}`")
        st.markdown(f"**Total Records Available:** `{total_records}`")
        
        # Local Folder Opener
        open_folder = st.button("📂 Open Dashboard Folder", width="stretch")
        if open_folder:
            try:
                # Windows command to open directory
                os.startfile(str(SystemConfig.LOGS_DIR.resolve()))
                st.success(f"✓ Opened Directory in File Explorer: `{SystemConfig.LOGS_DIR.resolve()}`")
            except Exception as e:
                st.error(f"Could not open directory: {e}. If running in containerized environment, path must be opened manually.")
                
    with col2:
        st.markdown("#### 📊 Dashboard Refresh Instructions")
        st.markdown("""
        To sync the Power BI dashboard with the Streamlit app's logs:
        1. Open your Power BI Project (`Biomedical_Waste_Dashboard.pbix`).
        2. Verify that the Data Source settings point to the exact **Log File Location** shown on the left.
        3. Click **Refresh** in the Power BI ribbon.
        4. The dashboard will automatically recalculate compliance metrics, waste percentages, and confidence distributions.
        """)


