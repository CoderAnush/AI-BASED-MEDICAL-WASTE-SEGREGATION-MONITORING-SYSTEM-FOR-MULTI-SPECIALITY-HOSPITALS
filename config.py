"""
Configuration Module for Biomedical Waste System

Centralized configuration management for all system parameters.
Allows easy adjustment of detection thresholds, paths, and settings.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

from typing import Dict, Optional


class SystemConfig:
    """Centralized system configuration."""

    # ==================== MODEL CONFIGURATION ====================
    MODEL_CONFIG = {
        "model_path": "best.pt",
        "model_type": "YOLOv11",
        "model_variant": "Nano",
        "imgsz": 640,
        "confidence_threshold": 0.5,  # Minimum 50% confidence
        "iou_threshold": 0.45,  # NMS IOU threshold
        "device": 0,  # 0 for GPU, "cpu" for CPU
        "max_detections": 100,  # Max boxes per image
    }

    # ==================== DATASET CONFIGURATION ====================
    DATASET_CONFIG = {
        "dataset_path": "Biomedical_Waste",
        "data_yaml": "Biomedical_Waste/data.yaml",
        "train_split": "train",
        "valid_split": "valid",
        "test_split": "test",
        "num_classes": 8,
    }

    # ==================== TRAINING CONFIGURATION ====================
    TRAINING_CONFIG = {
        "epochs": 100,
        "batch_size": "auto",
        "imgsz": 640,
        "optimizer": "SGD",
        "lr0": 0.01,  # Initial learning rate
        "lrf": 0.01,  # Final learning rate
        "momentum": 0.937,
        "weight_decay": 0.0005,
        "warmup_epochs": 3.0,
        "patience": 15,  # Early stopping
        "device": 0,
        "workers": 8,
        "seed": 42,
    }

    # ==================== OUTPUT CONFIGURATION ====================
    OUTPUT_CONFIG = {
        "output_dir": "output_images",
        "csv_path": "waste_log.csv",
        "save_annotated": True,
        "save_format": "jpg",
        "save_confidence": True,
    }

    # ==================== LOGGING CONFIGURATION ====================
    LOGGING_CONFIG = {
        "csv_filename": "waste_log.csv",
        "csv_headers": [
            "Timestamp",
            "Waste_ID",
            "Waste_Type",
            "Waste_Category",
            "Recommended_Bin",
            "Confidence",
            "Image_Name",
        ],
        "enable_console_output": True,
        "enable_file_logging": True,
    }

    # ==================== WASTE CLASSES ====================
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
    BIN_RECOMMENDATION_MAP = {
        "Sharps Waste": "White Bin",
        "Contaminated Recyclable Waste": "Red Bin",
        "Infectious Waste": "Yellow Bin",
        "Glass Waste": "Blue Bin",
        "Non-Biomedical Waste": "General Waste Bin",
    }

    # ==================== VISUALIZATION COLORS ====================
    VISUALIZATION_COLORS = {
        "needle": (255, 0, 0),  # Red
        "syringe": (255, 0, 0),  # Red
        "glove": (0, 255, 0),  # Green
        "mask": (0, 255, 0),  # Green
        "iv_tube": (0, 255, 0),  # Green
        "cotton": (0, 0, 255),  # Blue
        "medicine_bottle": (255, 255, 0),  # Cyan
        "general_waste": (128, 128, 128),  # Gray
    }

    # ==================== INFERENCE CONFIGURATION ====================
    INFERENCE_CONFIG = {
        "single_image_mode": {
            "save_output": True,
            "display_output": True,
        },
        "batch_mode": {
            "save_output": True,
            "display_summary": True,
            "max_batch_size": 100,
        },
        "webcam_mode": {
            "frame_width": 1280,
            "frame_height": 720,
            "fps": 30,
            "save_frames": False,
        },
    }

    # ==================== PERFORMANCE THRESHOLDS ====================
    PERFORMANCE_THRESHOLDS = {
        "high_confidence": 0.90,  # > 90%
        "medium_confidence": 0.80,  # 80-90%
        "low_confidence": 0.50,  # 50-80%
        "minimum_confidence": 0.50,  # Below this is rejected
    }

    # ==================== ALERT THRESHOLDS ====================
    ALERT_THRESHOLDS = {
        "low_confidence_alert": 0.75,  # Alert if below 75%
        "high_detections_alert": 100,  # Alert if > 100 detections/minute
        "model_degradation_alert": 0.85,  # Alert if avg confidence drops below 85%
    }

    @classmethod
    def get_model_config(cls) -> Dict:
        """Get model configuration."""
        return cls.MODEL_CONFIG.copy()

    @classmethod
    def get_training_config(cls) -> Dict:
        """Get training configuration."""
        return cls.TRAINING_CONFIG.copy()

    @classmethod
    def get_output_config(cls) -> Dict:
        """Get output configuration."""
        return cls.OUTPUT_CONFIG.copy()

    @classmethod
    def get_waste_class(cls, class_id: int) -> Optional[str]:
        """Get waste class name by ID."""
        return cls.WASTE_CLASSES.get(class_id)

    @classmethod
    def get_waste_category(cls, waste_type: str) -> Optional[str]:
        """Get waste category for a waste type."""
        return cls.WASTE_CATEGORY_MAP.get(waste_type)

    @classmethod
    def get_recommended_bin(cls, waste_category: str) -> Optional[str]:
        """Get recommended bin for a waste category."""
        return cls.BIN_RECOMMENDATION_MAP.get(waste_category)

    @classmethod
    def get_color_for_waste(cls, waste_type: str) -> tuple:
        """Get visualization color for waste type."""
        return cls.VISUALIZATION_COLORS.get(waste_type, (128, 128, 128))

    @classmethod
    def print_config(cls) -> None:
        """Print all configuration settings."""
        print("\n" + "=" * 60)
        print("SYSTEM CONFIGURATION")
        print("=" * 60)

        print("\nMODEL CONFIGURATION:")
        for key, value in cls.MODEL_CONFIG.items():
            print(f"  {key}: {value}")

        print("\nTRAINING CONFIGURATION:")
        for key, value in cls.TRAINING_CONFIG.items():
            print(f"  {key}: {value}")

        print("\nOUTPUT CONFIGURATION:")
        for key, value in cls.OUTPUT_CONFIG.items():
            print(f"  {key}: {value}")

        print("\nWASTE CLASSES:")
        for class_id, class_name in cls.WASTE_CLASSES.items():
            print(f"  {class_id}: {class_name}")

        print("\n" + "=" * 60)

    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration consistency."""
        errors = []

        # Check waste classes
        if len(cls.WASTE_CLASSES) != 8:
            errors.append(f"Expected 8 waste classes, got {len(cls.WASTE_CLASSES)}")

        # Check waste categories
        for waste_type in cls.WASTE_CLASSES.values():
            if waste_type not in cls.WASTE_CATEGORY_MAP:
                errors.append(f"Missing category mapping for: {waste_type}")

        # Check bin recommendations
        for category in cls.WASTE_CATEGORY_MAP.values():
            if category not in cls.BIN_RECOMMENDATION_MAP:
                errors.append(f"Missing bin mapping for category: {category}")

        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  ✗ {error}")
            return False

        print("✓ Configuration validation passed")
        return True


def create_custom_config(**kwargs) -> Dict:
    """
    Create a custom configuration by overriding defaults.

    Args:
        **kwargs: Configuration overrides

    Returns:
        Dict: Custom configuration
    """
    config = SystemConfig.MODEL_CONFIG.copy()
    config.update(kwargs)
    return config


if __name__ == "__main__":
    # Print and validate configuration
    SystemConfig.print_config()
    SystemConfig.validate_config()
