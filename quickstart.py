"""
Quick Start Guide for Biomedical Waste Detection System

This script provides guided setup and first-run instructions.
Run this to get started quickly.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import os
import sys
from pathlib import Path


def print_banner():
    """Print welcome banner."""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " BIOMEDICAL WASTE SEGREGATION SYSTEM - QUICK START".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)


def check_prerequisites():
    """Check if prerequisites are installed."""
    print("\n" + "=" * 70)
    print("CHECKING PREREQUISITES")
    print("=" * 70)

    prerequisites = {
        "Python 3.9+": sys.version_info >= (3, 9),
    }

    all_ok = True

    # Check Python version
    if prerequisites["Python 3.9+"]:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    else:
        print(
            f"✗ Python version too old: {sys.version_info.major}.{sys.version_info.minor}"
        )
        all_ok = False

    # Check required modules
    modules = ["cv2", "numpy", "pandas", "ultralytics"]
    print("\nChecking Python modules:")

    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} NOT INSTALLED")
            all_ok = False

    return all_ok


def check_directory_structure():
    """Check and create necessary directories."""
    print("\n" + "=" * 70)
    print("CHECKING DIRECTORY STRUCTURE")
    print("=" * 70)

    directories = [
        "sample_images",
        "output_images",
        "weights",
        "utils",
    ]

    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ {directory}/ exists")
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✓ Created {directory}/")
            except Exception as e:
                print(f"✗ Error creating {directory}/: {e}")


def check_dataset():
    """Check if dataset is available."""
    print("\n" + "=" * 70)
    print("CHECKING DATASET")
    print("=" * 70)

    dataset_path = "Biomedical_Waste"
    data_yaml = os.path.join(dataset_path, "data.yaml")

    if os.path.exists(dataset_path):
        print(f"✓ Dataset folder found: {dataset_path}/")

        if os.path.exists(data_yaml):
            print(f"✓ data.yaml found")
        else:
            print(f"✗ data.yaml NOT FOUND")
            print("  Please extract your Roboflow dataset to this folder")
            return False

        # Check subdirectories
        for subdir in ["train", "valid", "test"]:
            subdir_path = os.path.join(dataset_path, subdir)
            if os.path.exists(subdir_path):
                print(f"✓ {subdir}/ found")
            else:
                print(f"✗ {subdir}/ NOT FOUND")
                return False

        return True
    else:
        print(f"✗ Dataset folder NOT FOUND: {dataset_path}/")
        print("\n  Steps to add dataset:")
        print("  1. Download dataset from Roboflow")
        print("  2. Extract to: Biomedical_Waste/")
        print("  3. Verify structure:")
        print("     Biomedical_Waste/")
        print("     ├── train/")
        print("     ├── valid/")
        print("     ├── test/")
        print("     └── data.yaml")
        return False


def check_model():
    """Check if trained model exists."""
    print("\n" + "=" * 70)
    print("CHECKING TRAINED MODEL")
    print("=" * 70)

    model_path = "best.pt"

    if os.path.exists(model_path):
        print(f"✓ Trained model found: {model_path}")
        return True
    else:
        print(f"✗ Trained model NOT FOUND: {model_path}")
        print("\n  To train the model:")
        print("  1. Ensure dataset is in place")
        print("  2. Run: python train_model.py")
        print("  3. Training will take 1-2 hours (on GPU)")
        return False


def show_quick_start_guide():
    """Show quick start guide."""
    print("\n" + "=" * 70)
    print("QUICK START GUIDE")
    print("=" * 70)

    guide = """
STEP 1: Install Dependencies
  pip install -r requirements.txt

STEP 2: Prepare Dataset
  - Download dataset from Roboflow
  - Extract to: Biomedical_Waste/

STEP 3: Train Model (if needed)
  python train_model.py
  # This takes 1-2 hours on GPU

STEP 4: Run Inference on Single Image
  python inference.py --image sample_images/waste.jpg

STEP 5: Run Inference on Folder
  python inference.py --folder sample_images/

STEP 6: Run Real-Time Webcam Detection
  python inference.py --webcam 0

STEP 7: Analyze Results
  python analyze_csv.py
  # Shows statistics and insights

STEP 8: Import to Power BI
  - Open Power BI Desktop
  - Get Data → CSV
  - Select: waste_log.csv
  - Create dashboards
"""

    print(guide)


def show_next_steps():
    """Show next steps based on current state."""
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)

    prerequisites_ok = check_prerequisites()
    dataset_ok = check_dataset()
    model_ok = check_model()

    if not prerequisites_ok:
        print("\n❌ BLOCKING ISSUE: Missing Python modules")
        print("   Run: pip install -r requirements.txt")
        return False

    if not dataset_ok:
        print("\n⚠ WARNING: Dataset not found or incomplete")
        print("   Add Roboflow dataset before training")
        return False

    if not model_ok:
        print("\n⚠ ACTION REQUIRED: Model not trained")
        print("   Run: python train_model.py")
        print("   This is required for inference")
        return False

    print("\n✓ All checks passed!")
    print("   System is ready for inference")
    print("\n   Try this command:")
    print("   python inference.py --webcam 0")

    return True


def interactive_menu():
    """Show interactive menu."""
    print("\n" + "=" * 70)
    print("INTERACTIVE MENU")
    print("=" * 70)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Check system status")
        print("  2. View quick start guide")
        print("  3. Run inference on image")
        print("  4. Run inference on folder")
        print("  5. Run webcam detection")
        print("  6. Analyze results")
        print("  7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == "1":
            check_prerequisites()
            check_directory_structure()
            check_dataset()
            check_model()

        elif choice == "2":
            show_quick_start_guide()

        elif choice == "3":
            image_path = input("Enter image path: ").strip()
            if os.path.exists(image_path):
                print(f"Running: python inference.py --image {image_path}")
                os.system(f"python inference.py --image {image_path}")
            else:
                print(f"✗ Image not found: {image_path}")

        elif choice == "4":
            folder_path = input("Enter folder path: ").strip()
            if os.path.isdir(folder_path):
                print(f"Running: python inference.py --folder {folder_path}")
                os.system(f"python inference.py --folder {folder_path}")
            else:
                print(f"✗ Folder not found: {folder_path}")

        elif choice == "5":
            device_id = input("Enter webcam device ID (default 0): ").strip() or "0"
            print(f"Running: python inference.py --webcam {device_id}")
            os.system(f"python inference.py --webcam {device_id}")

        elif choice == "6":
            print("Running: python analyze_csv.py")
            os.system("python analyze_csv.py")

        elif choice == "7":
            print("\n✓ Goodbye!")
            break

        else:
            print("✗ Invalid choice")


def main():
    """Main entry point."""
    print_banner()

    # Automated checks
    check_directory_structure()
    prerequisites_ok = check_prerequisites()

    if not prerequisites_ok:
        print("\n✗ Prerequisites missing!")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    dataset_ok = check_dataset()
    model_ok = check_model()

    show_quick_start_guide()
    show_next_steps()

    # Show interactive menu
    try:
        response = input(
            "\nWould you like to use interactive mode? (y/n): "
        ).strip().lower()
        if response == "y":
            interactive_menu()
    except KeyboardInterrupt:
        print("\n\n✓ Exiting...")
        sys.exit(0)

    print("\n" + "=" * 70)
    print("For more information, see README.md")
    print("=" * 70)


if __name__ == "__main__":
    main()
