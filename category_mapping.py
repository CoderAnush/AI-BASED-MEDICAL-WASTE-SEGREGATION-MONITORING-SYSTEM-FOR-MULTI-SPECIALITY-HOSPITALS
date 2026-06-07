"""
Biomedical Waste Category and Bin Mapping Module

This module provides functions to map detected waste items to their biomedical
waste categories and recommended disposal bins according to the Biomedical
Waste Management Rules.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

from typing import Dict, Tuple


class WasteCategoryMapper:
    """Maps detected waste items to categories and bin recommendations."""

    # Waste type to category mapping
    WASTE_CATEGORY_MAP: Dict[str, str] = {
        "needle": "Sharps Waste",
        "syringe": "Sharps Waste",
        "glove": "Contaminated Recyclable Waste",
        "mask": "Contaminated Recyclable Waste",
        "iv_tube": "Contaminated Recyclable Waste",
        "cotton": "Infectious Waste",
        "medicine_bottle": "Glass Waste",
        "general_waste": "Non-Biomedical Waste",
    }

    # Waste category to bin color mapping
    CATEGORY_BIN_MAP: Dict[str, str] = {
        "Sharps Waste": "White Bin",
        "Contaminated Recyclable Waste": "Red Bin",
        "Infectious Waste": "Yellow Bin",
        "Glass Waste": "Blue Bin",
        "Non-Biomedical Waste": "General Waste Bin",
    }

    # Waste type to bin color mapping (direct mapping for convenience)
    WASTE_BIN_MAP: Dict[str, str] = {
        "needle": "White Bin",
        "syringe": "White Bin",
        "glove": "Red Bin",
        "mask": "Red Bin",
        "iv_tube": "Red Bin",
        "cotton": "Yellow Bin",
        "medicine_bottle": "Blue Bin",
        "general_waste": "General Waste Bin",
    }

    @staticmethod
    def get_waste_category(waste_type: str) -> str:
        """
        Get the biomedical waste category for a detected waste item.

        Args:
            waste_type (str): The detected waste item class name
                             (e.g., 'needle', 'syringe', 'glove')

        Returns:
            str: The biomedical waste category (e.g., 'Sharps Waste')

        Raises:
            ValueError: If waste_type is not recognized
        """
        waste_type_lower = waste_type.lower().strip()

        if waste_type_lower not in WasteCategoryMapper.WASTE_CATEGORY_MAP:
            raise ValueError(
                f"Unknown waste type: '{waste_type}'. "
                f"Valid types: {list(WasteCategoryMapper.WASTE_CATEGORY_MAP.keys())}"
            )

        return WasteCategoryMapper.WASTE_CATEGORY_MAP[waste_type_lower]

    @staticmethod
    def get_recommended_bin(waste_type: str) -> str:
        """
        Get the recommended disposal bin for a detected waste item.

        Args:
            waste_type (str): The detected waste item class name
                             (e.g., 'needle', 'syringe', 'glove')

        Returns:
            str: The recommended disposal bin (e.g., 'White Bin', 'Red Bin')

        Raises:
            ValueError: If waste_type is not recognized
        """
        waste_type_lower = waste_type.lower().strip()

        if waste_type_lower not in WasteCategoryMapper.WASTE_BIN_MAP:
            raise ValueError(
                f"Unknown waste type: '{waste_type}'. "
                f"Valid types: {list(WasteCategoryMapper.WASTE_BIN_MAP.keys())}"
            )

        return WasteCategoryMapper.WASTE_BIN_MAP[waste_type_lower]

    @staticmethod
    def get_complete_mapping(waste_type: str) -> Tuple[str, str]:
        """
        Get both the waste category and recommended bin for a waste item.

        Args:
            waste_type (str): The detected waste item class name

        Returns:
            Tuple[str, str]: A tuple of (waste_category, recommended_bin)

        Raises:
            ValueError: If waste_type is not recognized
        """
        waste_type_lower = waste_type.lower().strip()

        if waste_type_lower not in WasteCategoryMapper.WASTE_CATEGORY_MAP:
            raise ValueError(
                f"Unknown waste type: '{waste_type}'. "
                f"Valid types: {list(WasteCategoryMapper.WASTE_CATEGORY_MAP.keys())}"
            )

        category = WasteCategoryMapper.get_waste_category(waste_type)
        bin_color = WasteCategoryMapper.get_recommended_bin(waste_type)

        return category, bin_color

    @staticmethod
    def get_all_waste_types() -> list:
        """Get a list of all recognized waste types."""
        return list(WasteCategoryMapper.WASTE_CATEGORY_MAP.keys())

    @staticmethod
    def validate_waste_type(waste_type: str) -> bool:
        """
        Check if a waste type is valid.

        Args:
            waste_type (str): The waste type to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return waste_type.lower().strip() in WasteCategoryMapper.WASTE_CATEGORY_MAP


# Module-level convenience functions
def get_waste_category(waste_type: str) -> str:
    """Get waste category. Wrapper for WasteCategoryMapper.get_waste_category()"""
    return WasteCategoryMapper.get_waste_category(waste_type)


def get_recommended_bin(waste_type: str) -> str:
    """Get recommended bin. Wrapper for WasteCategoryMapper.get_recommended_bin()"""
    return WasteCategoryMapper.get_recommended_bin(waste_type)


def get_complete_mapping(waste_type: str) -> Tuple[str, str]:
    """Get complete mapping. Wrapper for WasteCategoryMapper.get_complete_mapping()"""
    return WasteCategoryMapper.get_complete_mapping(waste_type)


if __name__ == "__main__":
    # Test the mapping functions
    print("=" * 60)
    print("BIOMEDICAL WASTE CATEGORY MAPPING - TEST")
    print("=" * 60)

    test_waste_types = [
        "needle",
        "syringe",
        "glove",
        "mask",
        "iv_tube",
        "cotton",
        "medicine_bottle",
        "general_waste",
    ]

    for waste_type in test_waste_types:
        try:
            category = get_waste_category(waste_type)
            bin_color = get_recommended_bin(waste_type)
            print(f"\nWaste Type: {waste_type}")
            print(f"  → Category: {category}")
            print(f"  → Bin: {bin_color}")
        except ValueError as e:
            print(f"Error processing {waste_type}: {e}")

    print("\n" + "=" * 60)
