"""
Utility Functions Module

Common helper functions for biomedical waste detection system.
Includes image processing, validation, and analysis utilities.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np


class ImageUtils:
    """Image processing utilities."""

    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file.

        Args:
            image_path (str): Path to image file

        Returns:
            Optional[np.ndarray]: Image array or None if error
        """
        if not os.path.exists(image_path):
            print(f"✗ Image file not found: {image_path}")
            return None

        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"✗ Error reading image: {image_path}")
                return None
            return image
        except Exception as e:
            print(f"✗ Error loading image: {e}")
            return None

    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> bool:
        """
        Save image to file.

        Args:
            image (np.ndarray): Image array
            output_path (str): Output file path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, image)
            return True
        except Exception as e:
            print(f"✗ Error saving image: {e}")
            return False

    @staticmethod
    def resize_image(
        image: np.ndarray, target_size: Tuple[int, int]
    ) -> np.ndarray:
        """
        Resize image to target size.

        Args:
            image (np.ndarray): Input image
            target_size (Tuple[int, int]): Target (width, height)

        Returns:
            np.ndarray: Resized image
        """
        return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def get_image_info(image: np.ndarray) -> dict:
        """
        Get image information.

        Args:
            image (np.ndarray): Input image

        Returns:
            dict: Image information
        """
        height, width = image.shape[:2]
        channels = image.shape[2] if len(image.shape) > 2 else 1
        return {
            "width": width,
            "height": height,
            "channels": channels,
            "shape": image.shape,
            "dtype": str(image.dtype),
        }

    @staticmethod
    def validate_image(image_path: str) -> bool:
        """
        Validate image file.

        Args:
            image_path (str): Path to image

        Returns:
            bool: True if valid, False otherwise
        """
        if not os.path.exists(image_path):
            return False

        # Check file extension
        valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        if not any(image_path.lower().endswith(ext) for ext in valid_extensions):
            return False

        # Try to load image
        image = cv2.imread(image_path)
        return image is not None


class FileUtils:
    """File system utilities."""

    @staticmethod
    def get_image_files(folder_path: str) -> List[str]:
        """
        Get all image files in a folder.

        Args:
            folder_path (str): Path to folder

        Returns:
            List[str]: List of image file paths
        """
        if not os.path.isdir(folder_path):
            return []

        valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
        image_files = []

        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                image_files.append(os.path.join(folder_path, file))

        return sorted(image_files)

    @staticmethod
    def create_directory(directory_path: str) -> bool:
        """
        Create directory if it doesn't exist.

        Args:
            directory_path (str): Path to directory

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"✗ Error creating directory: {e}")
            return False

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path)

    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """
        Get file size in bytes.

        Args:
            file_path (str): Path to file

        Returns:
            Optional[int]: File size or None if error
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return None

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """
        Get total size of directory in bytes.

        Args:
            directory_path (str): Path to directory

        Returns:
            int: Total size
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except Exception:
                    pass
        return total_size


class ValidationUtils:
    """Validation utilities."""

    @staticmethod
    def validate_confidence(confidence: float) -> bool:
        """
        Validate confidence score.

        Args:
            confidence (float): Confidence value (0.0-1.0 or 0-100)

        Returns:
            bool: True if valid, False otherwise
        """
        if isinstance(confidence, (int, float)):
            return (0 <= confidence <= 1) or (0 <= confidence <= 100)
        return False

    @staticmethod
    def validate_waste_type(waste_type: str, valid_types: List[str]) -> bool:
        """
        Validate waste type.

        Args:
            waste_type (str): Waste type to validate
            valid_types (List[str]): List of valid types

        Returns:
            bool: True if valid, False otherwise
        """
        return waste_type.lower() in [t.lower() for t in valid_types]

    @staticmethod
    def validate_coordinates(
        x1: int, y1: int, x2: int, y2: int, width: int, height: int
    ) -> bool:
        """
        Validate bounding box coordinates.

        Args:
            x1, y1, x2, y2: Box coordinates
            width, height: Image dimensions

        Returns:
            bool: True if valid, False otherwise
        """
        if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
            return False
        return True


class StatisticsUtils:
    """Statistics utilities."""

    @staticmethod
    def calculate_average(values: List[float]) -> float:
        """Calculate average of values."""
        if not values:
            return 0.0
        return sum(values) / len(values)

    @staticmethod
    def calculate_percentile(values: List[float], percentile: float) -> float:
        """Calculate percentile."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

    @staticmethod
    def get_min_max(values: List[float]) -> Tuple[float, float]:
        """Get min and max values."""
        if not values:
            return 0.0, 0.0
        return min(values), max(values)

    @staticmethod
    def get_distribution(values: List[float], bins: int = 10) -> dict:
        """Get distribution of values."""
        if not values:
            return {}

        min_val, max_val = min(values), max(values)
        bin_width = (max_val - min_val) / bins if max_val > min_val else 1

        distribution = {}
        for i in range(bins):
            bin_start = min_val + i * bin_width
            bin_end = bin_start + bin_width
            count = sum(1 for v in values if bin_start <= v < bin_end)
            distribution[f"{bin_start:.2f}-{bin_end:.2f}"] = count

        return distribution


class FormatUtils:
    """Output formatting utilities."""

    @staticmethod
    def format_confidence(confidence: float, format_type: str = "percent") -> str:
        """
        Format confidence value.

        Args:
            confidence (float): Confidence value
            format_type (str): Format type ("percent" or "decimal")

        Returns:
            str: Formatted confidence
        """
        if format_type == "percent":
            if confidence <= 1.0:
                return f"{confidence * 100:.1f}%"
            return f"{confidence:.1f}%"
        else:
            if confidence > 1.0:
                return f"{confidence / 100:.3f}"
            return f"{confidence:.3f}"

    @staticmethod
    def format_timestamp(
        timestamp: str, output_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> str:
        """Format timestamp."""
        try:
            from datetime import datetime

            dt = datetime.fromisoformat(timestamp)
            return dt.strftime(output_format)
        except Exception:
            return timestamp

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """
        Format file size in human-readable format.

        Args:
            size_bytes (int): Size in bytes

        Returns:
            str: Formatted size
        """
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    @staticmethod
    def print_table(headers: List[str], rows: List[List[str]]) -> None:
        """
        Print formatted table.

        Args:
            headers (List[str]): Column headers
            rows (List[List[str]]): Table rows
        """
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Print header
        header_str = " | ".join(
            f"{h:{col_widths[i]}}" for i, h in enumerate(headers)
        )
        print(header_str)
        print("-" * len(header_str))

        # Print rows
        for row in rows:
            row_str = " | ".join(
                f"{str(cell):{col_widths[i]}}" for i, cell in enumerate(row)
            )
            print(row_str)


if __name__ == "__main__":
    # Test utilities
    print("=" * 60)
    print("UTILITY FUNCTIONS - TEST")
    print("=" * 60)

    # Test file utils
    print("\n--- File Utils ---")
    print(f"Directory size: {FileUtils.get_directory_size('.')}")

    # Test format utils
    print("\n--- Format Utils ---")
    print(f"Confidence: {FormatUtils.format_confidence(0.945)}")
    print(f"File size: {FormatUtils.format_file_size(1234567)}")

    # Test statistics utils
    print("\n--- Statistics Utils ---")
    test_values = [0.85, 0.90, 0.88, 0.92, 0.87]
    print(f"Average: {StatisticsUtils.calculate_average(test_values):.2f}")
    print(f"Min/Max: {StatisticsUtils.get_min_max(test_values)}")

    # Test table formatting
    print("\n--- Table Formatting ---")
    headers = ["Waste Type", "Category", "Confidence"]
    rows = [
        ["needle", "Sharps Waste", "97.5%"],
        ["glove", "Recyclable", "89.2%"],
        ["cotton", "Infectious", "88.5%"],
    ]
    FormatUtils.print_table(headers, rows)

    print("\n" + "=" * 60)
