"""
CSV Logging Module for Biomedical Waste Segregation Monitoring System

This module handles recording detection results into a standardized CSV log file.
Features automatic sequential Waste ID generation (e.g., W001, W002, W003) and 
decimal confidence formatting. The output is directly compatible with Power BI.

Author: AI-Based Medical Waste Segregation System
Version: 1.1
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from config import SystemConfig


class WasteCSVLogger:
    """Manages CSV logging for waste detection records."""

    def __init__(self, csv_path: Optional[Path] = None):
        """
        Initialize the CSV logger.

        Args:
            csv_path (Optional[Path]): Custom path to the CSV file.
                                       If None, uses path from SystemConfig.
        """
        self.csv_path = csv_path or SystemConfig.CSV_LOG_PATH
        self.headers = SystemConfig.LOGGING_CONFIG["csv_headers"]
        self.timestamp_format = SystemConfig.LOGGING_CONFIG["timestamp_format"]

        # Ensure parent directory exists
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_csv()

    def _initialize_csv(self) -> None:
        """Create CSV file with headers if it does not already exist."""
        if not self.csv_path.exists():
            try:
                with open(self.csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(self.headers)
                print(f"✓ Created new waste log file at: {self.csv_path}")
            except IOError as e:
                print(f"✗ Failed to create CSV file: {e}")
                raise

    def get_next_waste_id(self) -> str:
        """
        Generate the next sequential Waste ID (W001, W002, W003, etc.)
        by scanning the existing entries in the CSV.

        Returns:
            str: The next unique Waste ID
        """
        if not self.csv_path.exists():
            return "W001"

        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                if not rows:
                    return "W001"
                
                # Fetch last row and attempt to extract numerical suffix
                last_row = rows[-1]
                last_id = last_row.get("Waste_ID", "W000")
                
                if last_id and last_id.startswith("W"):
                    try:
                        num_part = int(last_id[1:])
                        next_num = num_part + 1
                        return f"W{next_num:03d}"
                    except ValueError:
                        pass
                
                # Fallback if parsing fails
                return f"W{len(rows) + 1:03d}"
        except IOError as e:
            print(f"✗ Warning: Failed to read CSV to determine next Waste ID ({e}). Using default.")
            return "W001"

    def log_detection(
        self,
        waste_type: str,
        waste_category: str,
        recommended_bin: str,
        confidence: float,
        image_name: str,
    ) -> str:
        """
        Log a waste detection to the CSV file.

        Args:
            waste_type (str): Name of detected waste class
            waste_category (str): Assigned biomedical waste category
            recommended_bin (str): Recommended disposal bin
            confidence (float): Confidence score (0.0 to 1.0)
            image_name (str): Source image or frame name

        Returns:
            str: The Waste ID assigned to this detection
        """
        # Auto-generate next ID
        waste_id = self.get_next_waste_id()
        timestamp = datetime.now().strftime(self.timestamp_format)

        # Ensure confidence is formatted as decimal (e.g. 0.97)
        # If model outputs 97.0 (percentage), convert to fraction
        if confidence > 1.0:
            confidence = confidence / 100.0

        record = {
            "Timestamp": timestamp,
            "Waste_ID": waste_id,
            "Waste_Type": waste_type,
            "Waste_Category": waste_category,
            "Recommended_Bin": recommended_bin,
            "Confidence": f"{confidence:.2f}",
            "Image_Name": image_name,
        }

        try:
            # Open in append mode
            file_exists = self.csv_path.exists()
            with open(self.csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.headers)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(record)
            
            return waste_id
        except IOError as e:
            print(f"✗ Error writing detection to CSV file: {e}")
            raise

    def get_total_records(self) -> int:
        """Get total number of detections logged in the CSV."""
        if not self.csv_path.exists():
            return 0
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                # Count rows excluding header
                return max(0, sum(1 for _ in reader) - 1)
        except IOError:
            return 0


if __name__ == "__main__":
    # Standard testing
    print("=" * 60)
    print("CSV LOGGER MODULE - TEST RUN")
    print("=" * 60)
    
    # Instantiate logger (will write to logs/waste_log.csv relative to this script)
    logger = WasteCSVLogger()
    
    # Log test data
    test_id = logger.log_detection(
        waste_type="needle",
        waste_category="Sharps Waste",
        recommended_bin="White Bin",
        confidence=0.97,
        image_name="test.jpg"
    )
    print(f"Logged item successfully. Assigned ID: {test_id}")
    print(f"Total entries: {logger.get_total_records()}")
    print("=" * 60)
