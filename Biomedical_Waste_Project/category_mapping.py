"""
Biomedical Waste Category and Bin Mapping Module

This module provides functions to map detected waste items to their biomedical
waste categories and recommended disposal bins according to system design guidelines.

Author: AI-Based Medical Waste Segregation System
Version: 1.1
"""

from typing import Tuple, Dict, List
try:
    from config import SystemConfig
except ImportError:
    # Fallback to local dicts if config isn't importable (e.g. during standalone testing)
    class SystemConfig:
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
        BIN_RECOMMENDATION_MAP = {
            "Sharps Waste": "White Bin",
            "Contaminated Recyclable Waste": "Red Bin",
            "Infectious Waste": "Yellow Bin",
            "Glass Waste": "Blue Bin",
            "Non-Biomedical Waste": "General Waste Bin",
        }


class WasteCategoryMapper:
    """Class to map detected waste items to categories and bin recommendations."""

    @staticmethod
    def get_waste_category(waste_type: str) -> str:
        """
        Get the biomedical waste category for a detected waste item.

        Args:
            waste_type (str): The detected waste item class name (e.g. 'needle', 'glove')

        Returns:
            str: The biomedical waste category (e.g. 'Sharps Waste', 'Infectious Waste')
        """
        waste_type_lower = waste_type.lower().strip()
        if waste_type_lower in SystemConfig.WASTE_CATEGORY_MAP:
            return SystemConfig.WASTE_CATEGORY_MAP[waste_type_lower]
        else:
            raise ValueError(
                f"Unknown waste type '{waste_type}'. Valid types: "
                f"{list(SystemConfig.WASTE_CATEGORY_MAP.keys())}"
            )

    @staticmethod
    def get_recommended_bin(waste_category: str) -> str:
        """
        Get the recommended disposal bin for a waste category.

        Args:
            waste_category (str): The waste category (e.g. 'Sharps Waste')

        Returns:
            str: The recommended disposal bin (e.g. 'White Bin', 'Red Bin')
        """
        if waste_category in SystemConfig.BIN_RECOMMENDATION_MAP:
            return SystemConfig.BIN_RECOMMENDATION_MAP[waste_category]
        else:
            # Check if input is actually a waste type instead of category
            waste_type_lower = waste_category.lower().strip()
            if waste_type_lower in SystemConfig.WASTE_CATEGORY_MAP:
                cat = SystemConfig.WASTE_CATEGORY_MAP[waste_type_lower]
                return SystemConfig.BIN_RECOMMENDATION_MAP[cat]
            raise ValueError(
                f"Unknown waste category or type '{waste_category}'. Valid categories: "
                f"{list(SystemConfig.BIN_RECOMMENDATION_MAP.keys())}"
            )

    @staticmethod
    def get_complete_mapping(waste_type: str) -> Tuple[str, str]:
        """
        Get both the waste category and recommended bin for a waste item.

        Args:
            waste_type (str): The detected waste item class name

        Returns:
            Tuple[str, str]: A tuple of (waste_category, recommended_bin)
        """
        category = WasteCategoryMapper.get_waste_category(waste_type)
        bin_recommendation = WasteCategoryMapper.get_recommended_bin(category)
        return category, bin_recommendation

    @staticmethod
    def get_all_waste_types() -> List[str]:
        """Get a list of all recognized waste types."""
        return list(SystemConfig.WASTE_CATEGORY_MAP.keys())


# Module-level convenience functions
def get_waste_category(waste_type: str) -> str:
    """Convenience wrapper for WasteCategoryMapper.get_waste_category."""
    return WasteCategoryMapper.get_waste_category(waste_type)


def get_recommended_bin(waste_category: str) -> str:
    """Convenience wrapper for WasteCategoryMapper.get_recommended_bin."""
    return WasteCategoryMapper.get_recommended_bin(waste_category)


def get_complete_mapping(waste_type: str) -> Tuple[str, str]:
    """Convenience wrapper for WasteCategoryMapper.get_complete_mapping."""
    return WasteCategoryMapper.get_complete_mapping(waste_type)


if __name__ == "__main__":
    # Test the mapping functions
    print("=" * 60)
    print("BIOMEDICAL WASTE CATEGORY MAPPING - TEST")
    print("=" * 60)

    for w_type in WasteCategoryMapper.get_all_waste_types():
        cat, bin_color = get_complete_mapping(w_type)
        print(f"Waste Type: {w_type:<20} -> Category: {cat:<30} -> Bin: {bin_color}")
    print("=" * 60)
