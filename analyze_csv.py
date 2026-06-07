"""
CSV Analysis and Reporting Module

Analyzes waste detection logs from CSV and generates reports and insights.
Useful for Power BI preparation and manual analytics.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import csv
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd


class WasteAnalyzer:
    """Analyzes waste detection logs."""

    def __init__(self, csv_path: str = "waste_log.csv"):
        """
        Initialize analyzer.

        Args:
            csv_path (str): Path to CSV file
        """
        self.csv_path = csv_path
        self.df = None
        self._load_data()

    def _load_data(self) -> bool:
        """
        Load CSV data into pandas DataFrame.

        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.csv_path):
            print(f"✗ CSV file not found: {self.csv_path}")
            return False

        try:
            self.df = pd.read_csv(self.csv_path)
            print(f"✓ Loaded {len(self.df)} records from CSV")
            return True
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
            return False

    def get_basic_statistics(self) -> Dict:
        """
        Get basic statistics from waste log.

        Returns:
            Dict: Basic statistics
        """
        if self.df is None or len(self.df) == 0:
            return {}

        stats = {
            "total_records": len(self.df),
            "unique_waste_types": self.df["Waste_Type"].nunique(),
            "unique_waste_categories": self.df["Waste_Category"].nunique(),
            "unique_bins": self.df["Recommended_Bin"].nunique(),
            "unique_images": self.df["Image_Name"].nunique(),
        }

        return stats

    def get_waste_type_distribution(self) -> Dict[str, int]:
        """
        Get distribution of waste types.

        Returns:
            Dict: Count of each waste type
        """
        if self.df is None:
            return {}

        return dict(self.df["Waste_Type"].value_counts())

    def get_waste_category_distribution(self) -> Dict[str, int]:
        """
        Get distribution of waste categories.

        Returns:
            Dict: Count of each category
        """
        if self.df is None:
            return {}

        return dict(self.df["Waste_Category"].value_counts())

    def get_bin_distribution(self) -> Dict[str, int]:
        """
        Get distribution of recommended bins.

        Returns:
            Dict: Count for each bin
        """
        if self.df is None:
            return {}

        return dict(self.df["Recommended_Bin"].value_counts())

    def get_confidence_statistics(self) -> Dict:
        """
        Get confidence statistics.

        Returns:
            Dict: Confidence statistics
        """
        if self.df is None:
            return {}

        # Clean confidence values
        confidences = []
        for conf in self.df["Confidence"]:
            try:
                conf_val = float(str(conf).rstrip("%"))
                confidences.append(conf_val)
            except ValueError:
                pass

        if not confidences:
            return {}

        return {
            "avg_confidence": round(sum(confidences) / len(confidences), 2),
            "min_confidence": round(min(confidences), 2),
            "max_confidence": round(max(confidences), 2),
            "median_confidence": round(sorted(confidences)[len(confidences) // 2], 2),
            "high_confidence_count": sum(1 for c in confidences if c >= 0.90),
            "low_confidence_count": sum(1 for c in confidences if c < 0.80),
        }

    def get_hourly_distribution(self) -> Dict[int, int]:
        """
        Get distribution of detections by hour.

        Returns:
            Dict: Count of detections per hour (0-23)
        """
        if self.df is None:
            return {}

        try:
            self.df["Hour"] = pd.to_datetime(self.df["Timestamp"]).dt.hour
            hourly = dict(self.df["Hour"].value_counts().sort_index())
            return hourly
        except Exception as e:
            print(f"✗ Error calculating hourly distribution: {e}")
            return {}

    def get_daily_distribution(self) -> Dict[str, int]:
        """
        Get distribution of detections by day.

        Returns:
            Dict: Count of detections per day
        """
        if self.df is None:
            return {}

        try:
            self.df["Date"] = pd.to_datetime(self.df["Timestamp"]).dt.date
            daily = dict(self.df["Date"].value_counts().sort_index())
            return daily
        except Exception as e:
            print(f"✗ Error calculating daily distribution: {e}")
            return {}

    def get_waste_type_by_category(self) -> Dict[str, List[str]]:
        """
        Get waste types grouped by category.

        Returns:
            Dict: Waste types per category
        """
        if self.df is None:
            return {}

        result = {}
        for category in self.df["Waste_Category"].unique():
            waste_types = self.df[self.df["Waste_Category"] == category][
                "Waste_Type"
            ].unique()
            result[category] = list(waste_types)

        return result

    def get_top_waste_items(self, n: int = 5) -> List[Tuple[str, int]]:
        """
        Get top N waste items by frequency.

        Args:
            n (int): Number of top items

        Returns:
            List[Tuple]: List of (waste_type, count) tuples
        """
        distribution = self.get_waste_type_distribution()
        return sorted(distribution.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_peak_hours(self, n: int = 3) -> List[Tuple[int, int]]:
        """
        Get peak hours for waste generation.

        Args:
            n (int): Number of peak hours to return

        Returns:
            List[Tuple]: List of (hour, count) tuples
        """
        hourly = self.get_hourly_distribution()
        return sorted(hourly.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_low_confidence_detections(
        self, threshold: float = 0.80
    ) -> pd.DataFrame:
        """
        Get detections with low confidence.

        Args:
            threshold (float): Confidence threshold (0-100)

        Returns:
            pd.DataFrame: Low confidence records
        """
        if self.df is None:
            return pd.DataFrame()

        try:
            confidences = []
            for conf in self.df["Confidence"]:
                try:
                    conf_val = float(str(conf).rstrip("%"))
                    confidences.append(conf_val)
                except ValueError:
                    confidences.append(0)

            return self.df[
                [c < threshold for c in confidences]
            ].reset_index(drop=True)
        except Exception as e:
            print(f"✗ Error filtering low confidence: {e}")
            return pd.DataFrame()

    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive summary report.

        Returns:
            str: Formatted report
        """
        report = "\n" + "=" * 70 + "\n"
        report += "WASTE DETECTION SUMMARY REPORT\n"
        report += "=" * 70 + "\n"

        # Basic statistics
        stats = self.get_basic_statistics()
        report += f"\nTotal Records: {stats.get('total_records', 0)}\n"
        report += f"Unique Waste Types: {stats.get('unique_waste_types', 0)}\n"
        report += f"Unique Categories: {stats.get('unique_waste_categories', 0)}\n"
        report += f"Unique Bins: {stats.get('unique_bins', 0)}\n"

        # Waste type distribution
        report += "\n--- WASTE TYPE DISTRIBUTION ---\n"
        waste_dist = self.get_waste_type_distribution()
        for waste_type, count in sorted(waste_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats.get("total_records", 1)) * 100
            report += f"  {waste_type:<20} : {count:>4} ({percentage:>5.1f}%)\n"

        # Waste category distribution
        report += "\n--- WASTE CATEGORY DISTRIBUTION ---\n"
        cat_dist = self.get_waste_category_distribution()
        for category, count in sorted(cat_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats.get("total_records", 1)) * 100
            report += f"  {category:<35} : {count:>4} ({percentage:>5.1f}%)\n"

        # Bin distribution
        report += "\n--- BIN RECOMMENDATION DISTRIBUTION ---\n"
        bin_dist = self.get_bin_distribution()
        for bin_color, count in sorted(bin_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats.get("total_records", 1)) * 100
            report += f"  {bin_color:<25} : {count:>4} ({percentage:>5.1f}%)\n"

        # Confidence statistics
        report += "\n--- CONFIDENCE STATISTICS ---\n"
        conf_stats = self.get_confidence_statistics()
        report += f"  Average Confidence: {conf_stats.get('avg_confidence', 0)}%\n"
        report += f"  Min Confidence: {conf_stats.get('min_confidence', 0)}%\n"
        report += f"  Max Confidence: {conf_stats.get('max_confidence', 0)}%\n"
        report += f"  Median Confidence: {conf_stats.get('median_confidence', 0)}%\n"
        report += f"  High Confidence (>90%): {conf_stats.get('high_confidence_count', 0)}\n"
        report += f"  Low Confidence (<80%): {conf_stats.get('low_confidence_count', 0)}\n"

        # Top waste items
        report += "\n--- TOP 5 WASTE ITEMS ---\n"
        top_items = self.get_top_waste_items(5)
        for rank, (waste_type, count) in enumerate(top_items, 1):
            report += f"  {rank}. {waste_type:<20} : {count} detections\n"

        # Peak hours
        report += "\n--- PEAK HOURS ---\n"
        peak = self.get_peak_hours(5)
        for hour, count in peak:
            report += f"  {hour:02d}:00 - {hour:02d}:59 : {count} detections\n"

        report += "\n" + "=" * 70 + "\n"

        return report

    def export_summary_to_file(self, output_path: str = "waste_report.txt") -> bool:
        """
        Export summary report to text file.

        Args:
            output_path (str): Output file path

        Returns:
            bool: True if successful
        """
        try:
            report = self.generate_summary_report()
            with open(output_path, "w") as f:
                f.write(report)
            print(f"✓ Report exported to: {output_path}")
            return True
        except Exception as e:
            print(f"✗ Error exporting report: {e}")
            return False


def main():
    """Main analysis pipeline."""
    print("\n" + "=" * 70)
    print("BIOMEDICAL WASTE ANALYSIS & REPORTING TOOL")
    print("=" * 70)

    # Initialize analyzer
    analyzer = WasteAnalyzer("waste_log.csv")

    if analyzer.df is None:
        print("✗ Failed to load waste log. Please run inference first.")
        return

    # Generate and print report
    report = analyzer.generate_summary_report()
    print(report)

    # Export report
    analyzer.export_summary_to_file("waste_report.txt")

    # Show low confidence detections
    low_conf = analyzer.get_low_confidence_detections(threshold=80)
    if len(low_conf) > 0:
        print("\n⚠ LOW CONFIDENCE DETECTIONS (<80%):")
        print(f"Found {len(low_conf)} detections below 80% confidence threshold")
        print("\nTop 5 low confidence detections:")
        for idx, row in low_conf.head(5).iterrows():
            print(
                f"  - {row['Waste_Type']}: {row['Confidence']} "
                f"({row['Image_Name']})"
            )


if __name__ == "__main__":
    main()
