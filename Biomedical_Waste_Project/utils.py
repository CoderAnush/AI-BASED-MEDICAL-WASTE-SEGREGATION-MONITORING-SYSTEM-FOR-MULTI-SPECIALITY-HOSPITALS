"""
Utility Functions Module for Biomedical Waste Segregation Monitoring System

Contains core helper utilities for image loading/saving, validation, directory 
management, and high-quality OpenCV drawing of multi-line detection annotations.

Author: AI-Based Medical Waste Segregation System
Version: 1.1
"""

import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

import cv2
import numpy as np

from config import SystemConfig


class ImageUtils:
    """Helper methods for image loading, saving, and checking integrity."""

    @staticmethod
    def load_image(image_path: Path) -> Optional[np.ndarray]:
        """
        Load an image from a path using OpenCV.

        Args:
            image_path (Path): Path to the image file.

        Returns:
            Optional[np.ndarray]: Image matrix in BGR format, or None if error.
        """
        if not image_path.exists():
            print(f"✗ Image file does not exist: {image_path}")
            return None
        try:
            image = cv2.imread(str(image_path))
            if image is None:
                print(f"✗ OpenCV could not decode the image: {image_path}")
            return image
        except Exception as e:
            print(f"✗ Error loading image {image_path}: {e}")
            return None

    @staticmethod
    def save_image(image: np.ndarray, output_path: Path) -> bool:
        """
        Save an image matrix to file.

        Args:
            image (np.ndarray): Image to save.
            output_path (Path): Target file path.

        Returns:
            bool: True if save succeeded, False otherwise.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(output_path), image)
            return True
        except Exception as e:
            print(f"✗ Error saving image to {output_path}: {e}")
            return False

    @staticmethod
    def validate_image_file(image_path: Path) -> bool:
        """
        Perform verification of image path validity and basic header reading.

        Args:
            image_path (Path): File path to check.

        Returns:
            bool: True if file exists, has a valid image extension, and can be read.
        """
        if not image_path.is_file():
            return False
        
        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        if image_path.suffix.lower() not in valid_exts:
            return False
        
        try:
            # Try to read only shape to verify it's valid without heavy loading
            img = cv2.imread(str(image_path))
            return img is not None
        except Exception:
            return False


class VisualizationUtils:
    """Utilities for rendering bounding boxes and custom text panels on frames."""

    @staticmethod
    def draw_detections(image: np.ndarray, detections: List[Dict[str, Any]]) -> np.ndarray:
        """
        Draw bounding boxes and stacked textual info labels on the image.
        For every detection, shows:
        - Waste Type (Capitalized)
        - Waste Category
        - Recommended Bin
        - Confidence Percentage

        Uses color coding matched to the recommended bin.

        Args:
            image (np.ndarray): BGR image matrix.
            detections (List[Dict[str, Any]]): List of dicts, each containing:
                "box": (x1, y1, x2, y2)
                "waste_type": str
                "waste_category": str
                "recommended_bin": str
                "confidence": float (between 0.0 and 1.0)

        Returns:
            np.ndarray: Annotated BGR image.
        """
        annotated_img = image.copy()
        h, w = annotated_img.shape[:2]

        for det in detections:
            x1, y1, x2, y2 = det["box"]
            waste_type = det["waste_type"]
            category = det["waste_category"]
            rec_bin = det["recommended_bin"]
            conf = det["confidence"]

            # Convert confidence to percentage if it is a fraction
            conf_pct = conf if conf > 1.0 else conf * 100.0

            # Get color code based on the recommended bin
            box_color = SystemConfig.get_color_for_bin(rec_bin)

            # Draw bounding box
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), box_color, 2)

            # Build label lines according to display requirements
            label_lines = [
                f"{waste_type.capitalize()}",
                f"{category}",
                f"{rec_bin}",
                f"{int(round(conf_pct))}%"
            ]

            # Calculate height and width of labels to fit text background
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.45
            thickness = 1
            line_height = 16
            padding = 6

            text_width = 0
            for line in label_lines:
                size, _ = cv2.getTextSize(line, font, font_scale, thickness)
                text_width = max(text_width, size[0])

            box_height = len(label_lines) * line_height + (padding * 2)
            box_width = text_width + (padding * 2)

            # Determine label placement. Try placing above box, fallback to inside box
            label_y1 = y1 - box_height - 2
            if label_y1 < 0:
                # Place inside the box at the top
                label_y1 = y1 + 2

            label_x1 = x1
            if label_x1 + box_width > w:
                label_x1 = w - box_width - 2

            label_x2 = label_x1 + box_width
            label_y2 = label_y1 + box_height

            # Draw semi-transparent background box for text legibility
            overlay = annotated_img.copy()
            cv2.rectangle(overlay, (label_x1, label_y1), (label_x2, label_y2), (0, 0, 0), -1)
            # Apply alpha blending (0.6 opacity)
            cv2.addWeighted(overlay, 0.6, annotated_img, 0.4, 0, annotated_img)

            # Draw a border around the text box matching the bin color
            cv2.rectangle(annotated_img, (label_x1, label_y1), (label_x2, label_y2), box_color, 1)

            # Draw the stacked text lines
            current_y = label_y1 + padding + 10
            for line in label_lines:
                # Text color is white for readability, except bin name which can match its color
                text_color = (255, 255, 255)
                cv2.putText(
                    annotated_img,
                    line,
                    (label_x1 + padding, current_y),
                    font,
                    font_scale,
                    text_color,
                    thickness,
                    lineType=cv2.LINE_AA
                )
                current_y += line_height

        return annotated_img


class FileUtils:
    """Helper tools for scanning folders for media and cleaning directories."""

    @staticmethod
    def get_image_files_in_folder(folder_path: Path) -> List[Path]:
        """
        Recursively find all images with valid extensions in the folder.

        Args:
            folder_path (Path): Path to directory.

        Returns:
            List[Path]: Sorted list of Paths to image files.
        """
        if not folder_path.exists() or not folder_path.is_dir():
            return []

        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
        image_files = []
        for file in folder_path.iterdir():
            if file.is_file() and file.suffix.lower() in valid_exts:
                image_files.append(file)

        return sorted(image_files)
