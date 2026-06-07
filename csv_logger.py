"""
CSV Logging Module for Biomedical Waste Detection

This module handles logging of detected biomedical waste items to a CSV file
with automatic Waste ID generation (W001, W002, etc.) and timestamp recording.

The CSV is designed for direct import into Power BI dashboards.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class WasteCSVLogger:
    """Manages CSV logging for waste detection records."""

    CSV_FILENAME = "waste_log.csv"
    CSV_HEADERS = [
        "Timestamp",
        "Waste_ID",
        "Waste_Type",
        "Waste_Category",
        "Recommended_Bin",
        "Confidence",
        "Image_Name",
    ]

    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the CSV logger.

        Args:
            csv_path (Optional[str]): Path to the CSV file.
                                     If None, uses current directory.
        """
        if csv_path is None:
            self.csv_path = self.CSV_FILENAME
        else:
            self.csv_path = csv_path

        # Create CSV file with headers if it doesn't exist
        self._initialize_csv()

    def _initialize_csv(self) -> None:
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.CSV_HEADERS)
                    writer.writeheader()
                print(f"✓ Created new waste log: {self.csv_path}")
            except IOError as e:
                print(f"✗ Error creating CSV file: {e}")
                raise
        else:
            print(f"✓ Using existing waste log: {self.csv_path}")

    def get_next_waste_id(self) -> str:
        """
        Generate the next sequential Waste ID (W001, W002, W003, etc.).

        Returns:
            str: The next waste ID
        """
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                waste_ids = []

                for row in reader:
                    if row and "Waste_ID" in row and row["Waste_ID"]:
                        waste_ids.append(row["Waste_ID"])

                if not waste_ids:
                    return "W001"

                # Extract number from last waste ID and increment
                last_waste_id = waste_ids[-1]
                try:
                    last_number = int(last_waste_id[1:])  # Remove 'W' prefix
                    next_number = last_number + 1
                    return f"W{next_number:03d}"
                except (ValueError, IndexError):
                    return "W001"

        except IOError as e:
            print(f"✗ Error reading CSV file: {e}")
            return "W001"

    def log_detection(
        self,
        waste_type: str,
        waste_category: str,
        recommended_bin: str,
        confidence: float,
        image_name: Optional[str] = None,
    ) -> str:
        """
        Log a waste detection to the CSV file.

        Args:
            waste_type (str): The detected waste item (e.g., 'needle')
            waste_category (str): The biomedical waste category
            recommended_bin (str): The recommended disposal bin
            confidence (float): Detection confidence (0.0-100.0)
            image_name (Optional[str]): Name of the source image

        Returns:
            str: The Waste ID assigned to this detection
        """
        try:
            waste_id = self.get_next_waste_id()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Prepare the record
            record = {
                "Timestamp": timestamp,
                "Waste_ID": waste_id,
                "Waste_Type": waste_type,
                "Waste_Category": waste_category,
                "Recommended_Bin": recommended_bin,
                "Confidence": f"{confidence:.2f}%",
                "Image_Name": image_name or "N/A",
            }

            # Append to CSV file
            with open(self.csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.CSV_HEADERS)
                writer.writerow(record)

            return waste_id

        except IOError as e:
            print(f"✗ Error writing to CSV file: {e}")
            raise

    def get_total_records(self) -> int:
        """
        Get the total number of waste records logged (excluding header).

        Returns:
            int: Total number of records
        """
        try:
            with open(self.csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                count = sum(1 for _ in reader)
                return count
        except IOError as e:
            print(f"✗ Error reading CSV file: {e}")
            return 0

    def get_csv_path(self) -> str:
        """Get the path to the CSV file."""
        return os.path.abspath(self.csv_path)

    def get_summary_statistics(self) -> dict:
        """
        Get summary statistics from the waste log.

        Returns:
            dict: Dictionary containing various statistics
        """
        try:
            waste_types = {}
            waste_categories = {}
            recommended_bins = {}
            total_records = 0
            avg_confidence = 0.0
            confidences = []

            with open(self.csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    if row and "Waste_Type" in row:
                        total_records += 1

                        # Count waste types
                        waste_type = row.get("Waste_Type", "Unknown")
                        waste_types[waste_type] = waste_types.get(waste_type, 0) + 1

                        # Count waste categories
                        waste_cat = row.get("Waste_Category", "Unknown")
                        waste_categories[waste_cat] = (
                            waste_categories.get(waste_cat, 0) + 1
                        )

                        # Count recommended bins
                        bin_color = row.get("Recommended_Bin", "Unknown")
                        recommended_bins[bin_color] = (
                            recommended_bins.get(bin_color, 0) + 1
                        )

                        # Collect confidence values
                        try:
                            confidence_str = row.get("Confidence", "0%").rstrip("%")
                            confidence_val = float(confidence_str)
                            confidences.append(confidence_val)
                        except ValueError:
                            pass

            # Calculate average confidence
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)

            # Find most common items
            most_common_waste_type = (
                max(waste_types, key=waste_types.get) if waste_types else "N/A"
            )
            most_common_category = (
                max(waste_categories, key=waste_categories.get)
                if waste_categories
                else "N/A"
            )
            most_common_bin = (
                max(recommended_bins, key=recommended_bins.get)
                if recommended_bins
                else "N/A"
            )

            return {
                "total_records": total_records,
                "waste_types": waste_types,
                "waste_categories": waste_categories,
                "recommended_bins": recommended_bins,
                "average_confidence": round(avg_confidence, 2),
                "most_common_waste_type": most_common_waste_type,
                "most_common_category": most_common_category,
                "most_common_bin": most_common_bin,
            }

        except IOError as e:
            print(f"✗ Error reading CSV file: {e}")
            return {}


def create_csv_logger(csv_path: Optional[str] = None) -> WasteCSVLogger:
    """
    Factory function to create a WasteCSVLogger instance.

    Args:
        csv_path (Optional[str]): Path to the CSV file

    Returns:
        WasteCSVLogger: Initialized logger instance
    """
    return WasteCSVLogger(csv_path)


if __name__ == "__main__":
    # Test the CSV logger
    print("=" * 60)
    print("WASTE CSV LOGGER - TEST")
    print("=" * 60)

    logger = create_csv_logger()

    # Simulate logging some waste detections
    test_data = [
        ("needle", "Sharps Waste", "White Bin", 97.5, "sample_image_1.jpg"),
        ("syringe", "Sharps Waste", "White Bin", 94.2, "sample_image_2.jpg"),
        ("glove", "Contaminated Recyclable Waste", "Red Bin", 89.8, "sample_image_3.jpg"),
        ("mask", "Contaminated Recyclable Waste", "Red Bin", 92.1, "sample_image_4.jpg"),
        ("cotton", "Infectious Waste", "Yellow Bin", 88.5, "sample_image_5.jpg"),
    ]

    print("\nLogging test detections...")
    for waste_type, category, bin_color, confidence, image_name in test_data:
        waste_id = logger.log_detection(
            waste_type, category, bin_color, confidence, image_name
        )
        print(f"✓ Logged: {waste_id} - {waste_type} ({confidence}%)")

    print(f"\nTotal records: {logger.get_total_records()}")
    print(f"CSV location: {logger.get_csv_path()}")

    print("\n--- Summary Statistics ---")
    stats = logger.get_summary_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\n" + "=" * 60)
