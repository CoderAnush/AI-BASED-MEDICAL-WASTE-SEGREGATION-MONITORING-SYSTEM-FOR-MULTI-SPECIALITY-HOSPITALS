"""
Configuration Module for Biomedical Waste Segregation Monitoring System

Centralized configuration management for all system parameters.
Allows easy adjustment of detection thresholds, paths, and settings.

Author: AI-Based Medical Waste Segregation System
Version: 1.1
"""

import os
from pathlib import Path
from typing import Dict, Any, Tuple


class SystemConfig:
    """Centralized system configuration."""

    # ==================== PATH CONFIGURATION ====================
    # BASE_DIR is the root of the Biomedical_Waste_Project folder
    BASE_DIR = Path(__file__).resolve().parent

    # Output directory paths (created automatically at startup)
    WEIGHTS_DIR = BASE_DIR / "weights"
    SAMPLE_IMAGES_DIR = BASE_DIR / "sample_images"
    OUTPUT_IMAGES_DIR = BASE_DIR / "output_images"
    LOGS_DIR = BASE_DIR / "logs"
    REPORTS_DIR = BASE_DIR / "reports"

    # Files
    MODEL_PATH = WEIGHTS_DIR / "best.pt"
    CSV_LOG_PATH = LOGS_DIR / "waste_log.csv"

    # ==================== MODEL CONFIGURATION ====================
    MODEL_CONFIG = {
        "imgsz": 640,
        "confidence_threshold": 0.5,  # Minimum 50% confidence for detection
        "iou_threshold": 0.45,         # NMS IOU threshold
        "device": "",                  # Empty string for auto-selection (CUDA if available, else CPU)
    }

    # ==================== LOGGING CONFIGURATION ====================
    LOGGING_CONFIG = {
        "csv_headers": [
            "Timestamp",
            "Waste_ID",
            "Waste_Type",
            "Waste_Category",
            "Recommended_Bin",
            "Confidence",
            "Image_Name",
        ],
        "timestamp_format": "%Y-%m-%d %H:%M",
        "enable_console_output": True,
    }

    # ==================== WASTE CLASSES ====================
    # The exact 8 classes from best.pt and their display labels
    WASTE_CLASSES = {
        0: "cotton",
        1: "general_waste",
        2: "glove",
        3: "iv_tube",
        4: "mask",
        5: "medicine_bottle",
        6: "needle",
        7: "syringe",
    }

    # ==================== WASTE CATEGORY MAPPING ====================
    # Maps detected waste items to their biomedical waste categories
    WASTE_CATEGORY_MAP = {
        "needle": "Sharps Waste",
        "syringe": "Sharps Waste",
        "glove": "Contaminated Recyclable Waste",
        "mask": "Contaminated Recyclable Waste",
        "iv_tube": "Contaminated Recyclable Waste",
        "cotton": "Infectious Waste",
        "medicine_bottle": "Glass Waste",
        "general_waste": "Non-Biomedical Waste",
    }

    # ==================== BIN RECOMMENDATION MAP ====================
    # Maps waste categories to specific colored disposal bins
    BIN_RECOMMENDATION_MAP = {
        "Sharps Waste": "White Bin",
        "Contaminated Recyclable Waste": "Red Bin",
        "Infectious Waste": "Yellow Bin",
        "Glass Waste": "Blue Bin",
        "Non-Biomedical Waste": "General Waste Bin",
    }

    # ==================== VISUALIZATION COLORS ====================
    # BGR format colors for drawing bounding boxes and labels in OpenCV
    VISUALIZATION_COLORS = {
        "White Bin": (240, 240, 240),      # Light Grey/White
        "Red Bin": (0, 0, 255),            # Bright Red
        "Yellow Bin": (0, 255, 255),       # Yellow
        "Blue Bin": (255, 0, 0),           # Blue
        "General Waste Bin": (80, 80, 80), # Dark Grey
    }

    # Text overlay fonts and configurations
    FONT = cv2_font = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.5
    THICKNESS = 1

    @classmethod
    def setup_directories(cls) -> None:
        """Create all required project subdirectories if they do not exist."""
        for dir_path in [cls.WEIGHTS_DIR, cls.SAMPLE_IMAGES_DIR, cls.OUTPUT_IMAGES_DIR, cls.LOGS_DIR, cls.REPORTS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_color_for_bin(cls, bin_name: str) -> Tuple[int, int, int]:
        """Get the visual BGR color code for a specific recommended bin."""
        return cls.VISUALIZATION_COLORS.get(bin_name, (0, 255, 0))  # Default to Green if not found
