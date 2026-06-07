"""
YOLOv11 Nano Model Training Script

This script trains a YOLOv11 Nano model on the biomedical waste dataset
using transfer learning from the pretrained yolo11n.pt weights.

The trained model is saved as best.pt in the runs/detect/train/weights/ directory.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import os
from pathlib import Path
from typing import Optional

from ultralytics import YOLO


class BiomedicalWasteModelTrainer:
    """Handles training of YOLO model for biomedical waste detection."""

    def __init__(
        self,
        dataset_path: str = "Biomedical_Waste",
        epochs: int = 20,
        imgsz: int = 416,
        batch: str = "auto",
    ):
        """
        Initialize the trainer.

        Args:
            dataset_path (str): Path to the dataset root directory
            epochs (int): Number of training epochs
            imgsz (int): Input image size
            batch (str): Batch size (use "auto" for automatic)
        """
        self.dataset_path = dataset_path
        self.data_yaml = os.path.join(dataset_path, "data.yaml")
        self.epochs = epochs
        self.imgsz = imgsz
        self.batch = batch
        self.model = None
        self.best_model_path = None

    def validate_dataset(self) -> bool:
        """
        Validate that the dataset exists and has required structure.

        Returns:
            bool: True if dataset is valid, False otherwise
        """
        print("\n" + "=" * 60)
        print("VALIDATING DATASET STRUCTURE")
        print("=" * 60)

        if not os.path.exists(self.dataset_path):
            print(f"✗ Dataset path not found: {self.dataset_path}")
            return False

        if not os.path.exists(self.data_yaml):
            print(f"✗ data.yaml not found: {self.data_yaml}")
            return False

        required_dirs = ["train", "valid", "test"]
        for dir_name in required_dirs:
            dir_path = os.path.join(self.dataset_path, dir_name)
            if not os.path.exists(dir_path):
                print(f"✗ Missing directory: {dir_name}")
                return False
            print(f"✓ Found directory: {dir_name}")

        print("\n✓ Dataset structure is valid")
        return True

    def load_pretrained_model(self) -> None:
        """Load the pretrained YOLOv11 Nano model."""
        print("\n" + "=" * 60)
        print("LOADING PRETRAINED MODEL")
        print("=" * 60)

        try:
            print("Loading yolo11n.pt (YOLOv11 Nano - pretrained)...")
            self.model = YOLO("yolo11n.pt")
            print("✓ Pretrained model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading pretrained model: {e}")
            raise

    def train(self) -> Optional[str]:
        """
        Train the model on the biomedical waste dataset.

        Returns:
            Optional[str]: Path to best model if successful, None otherwise
        """
        if self.model is None:
            print("✗ Model not loaded. Call load_pretrained_model() first.")
            return None

        print("\n" + "=" * 60)
        print("STARTING MODEL TRAINING")
        print("=" * 60)
        print(f"Dataset YAML: {self.data_yaml}")
        print(f"Epochs: {self.epochs}")
        print(f"Image Size: {self.imgsz}")
        print(f"Batch Size: {self.batch}")
        print("=" * 60)

        try:
            # Convert batch to int if it's "auto"
            # For CPU: use smaller batch size
            batch_size = 4 if self.batch == "auto" else int(self.batch)

            # Train the model
            results = self.model.train(
                data=self.data_yaml,
                epochs=self.epochs,
                imgsz=self.imgsz,
                batch=batch_size,
                device="cpu",  # Use CPU (no CUDA GPU available)
                patience=5,  # Early stopping patience (reduced for CPU)
                save=True,
                save_period=5,
                verbose=False,
                project="runs/detect",
                name="train",
                exist_ok=True,
                cache=False,  # Disable cache for CPU
                workers=0,  # Single worker for CPU
            )

            print("\n✓ Training completed successfully")
            return results

        except Exception as e:
            print(f"✗ Error during training: {e}")
            return None

    def validate(self) -> Optional[dict]:
        """
        Validate the trained model on validation dataset.

        Returns:
            Optional[dict]: Validation results if successful, None otherwise
        """
        if self.model is None:
            print("✗ Model not loaded.")
            return None

        print("\n" + "=" * 60)
        print("VALIDATING MODEL ON VALIDATION SET")
        print("=" * 60)

        try:
            results = self.model.val()
            print("✓ Validation completed")
            return results
        except Exception as e:
            print(f"✗ Error during validation: {e}")
            return None

    def test(self) -> Optional[dict]:
        """
        Test the trained model on test dataset.

        Returns:
            Optional[dict]: Test results if successful, None otherwise
        """
        if self.model is None:
            print("✗ Model not loaded.")
            return None

        print("\n" + "=" * 60)
        print("TESTING MODEL ON TEST SET")
        print("=" * 60)

        try:
            results = self.model.val(data=self.data_yaml, split="test")
            print("✓ Testing completed")
            return results
        except Exception as e:
            print(f"✗ Error during testing: {e}")
            return None

    def find_and_save_best_model(self) -> Optional[str]:
        """
        Find the best trained model and save it locally as best.pt.

        Returns:
            Optional[str]: Path to best.pt if found, None otherwise
        """
        print("\n" + "=" * 60)
        print("LOCATING BEST MODEL")
        print("=" * 60)

        # Look for best.pt in the runs directory
        possible_paths = [
            "runs/detect/train/weights/best.pt",
            "runs/detect/train/weights/last.pt",
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"✓ Found best model at: {path}")

                # Copy to project root as best.pt
                destination = "best.pt"
                try:
                    with open(path, "rb") as src:
                        with open(destination, "wb") as dst:
                            dst.write(src.read())
                    print(f"✓ Saved best model to: {destination}")
                    self.best_model_path = os.path.abspath(destination)
                    return self.best_model_path
                except IOError as e:
                    print(f"✗ Error copying model: {e}")
                    return path

        print("✗ Best model not found in expected locations")
        return None

    def print_training_summary(self) -> None:
        """Print a summary of training results."""
        print("\n" + "=" * 60)
        print("TRAINING SUMMARY")
        print("=" * 60)

        if self.best_model_path:
            print(f"✓ Best Model Path: {self.best_model_path}")
            print(f"  Absolute: {os.path.abspath(self.best_model_path)}")
        else:
            print("✗ Best model path not available")

        print("\nTo use the trained model for inference:")
        print("  from ultralytics import YOLO")
        print('  model = YOLO("best.pt")')
        print('  results = model.predict(source="image.jpg", conf=0.5)')

        print("\n" + "=" * 60)


def main():
    """Main training pipeline."""
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█  BIOMEDICAL WASTE SEGREGATION - YOLOv11 TRAINING" + " " * 7 + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)

    # Initialize trainer
    trainer = BiomedicalWasteModelTrainer(
        dataset_path="Biomedical_Waste",
        epochs=100,
        imgsz=640,
        batch="auto",
    )

    # Step 1: Validate dataset
    if not trainer.validate_dataset():
        print("\n✗ Dataset validation failed. Exiting.")
        return

    # Step 2: Load pretrained model
    try:
        trainer.load_pretrained_model()
    except Exception as e:
        print(f"\n✗ Failed to load pretrained model: {e}")
        return

    # Step 3: Train the model
    training_results = trainer.train()
    if training_results is None:
        print("\n✗ Training failed. Exiting.")
        return

    # Step 4: Validate the model
    validation_results = trainer.validate()

    # Step 5: Test the model
    test_results = trainer.test()

    # Step 6: Find and save best model
    best_model_path = trainer.find_and_save_best_model()

    # Step 7: Print summary
    trainer.print_training_summary()

    print("\n✓ Training pipeline completed successfully!")
    print("\nNext steps:")
    print("  1. Use inference.py for detection on images or video")
    print("  2. Check waste_log.csv for logged detections")
    print("  3. Import waste_log.csv into Power BI for dashboards")


if __name__ == "__main__":
    main()
