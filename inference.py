"""
Biomedical Waste Inference Pipeline

This module provides inference capabilities for waste detection with support for:
- Single image inference
- Folder/batch inference
- Real-time webcam inference

Detected items are logged to CSV and displayed with annotations.

Author: AI-Based Medical Waste Segregation System
Version: 1.0
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from category_mapping import WasteCategoryMapper
from csv_logger import WasteCSVLogger


class BiomedicalWasteInference:
    """Performs waste detection and classification inference."""

    def __init__(
        self,
        model_path: str = "best.pt",
        output_dir: str = "output_images",
        csv_path: str = "waste_log.csv",
        confidence_threshold: float = 0.5,
    ):
        """
        Initialize the inference pipeline.

        Args:
            model_path (str): Path to the trained YOLO model
            output_dir (str): Directory to save annotated images
            csv_path (str): Path to CSV log file
            confidence_threshold (float): Minimum confidence for detections
        """
        self.model_path = model_path
        self.output_dir = output_dir
        self.csv_path = csv_path
        self.confidence_threshold = confidence_threshold

        # Initialize model and logger
        self.model = None
        self.logger = None
        self.class_names = None

        self._initialize()

    def _initialize(self) -> None:
        """Initialize model and logger."""
        print("\n" + "=" * 60)
        print("INITIALIZING INFERENCE PIPELINE")
        print("=" * 60)

        # Load model
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        try:
            print(f"Loading model: {self.model_path}")
            self.model = YOLO(self.model_path)
            print("✓ Model loaded successfully")

            # Get class names
            self.class_names = self.model.names
            print(f"✓ Detected {len(self.class_names)} classes")
            for idx, name in self.class_names.items():
                print(f"  {idx}: {name}")

        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise

        # Initialize CSV logger
        try:
            self.logger = WasteCSVLogger(self.csv_path)
            print(f"✓ CSV logger initialized")
        except Exception as e:
            print(f"✗ Error initializing CSV logger: {e}")
            raise

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"✓ Output directory ready: {self.output_dir}")

    def _format_output(self, detection: dict) -> str:
        """
        Format detection result for console display.

        Args:
            detection (dict): Detection information

        Returns:
            str: Formatted output string
        """
        output = "\n" + "=" * 50 + "\n"
        output += f"Detected Waste : {detection['waste_type']}\n"
        output += f"Waste Category : {detection['waste_category']}\n"
        output += f"Recommended Bin : {detection['recommended_bin']}\n"
        output += f"Confidence : {detection['confidence']:.1f}%\n"
        output += f"Image : {detection['image_name']}\n"
        output += "=" * 50 + "\n"
        return output

    def infer_image(self, image_path: str, save_output: bool = True) -> List[dict]:
        """
        Run inference on a single image.

        Args:
            image_path (str): Path to the image
            save_output (bool): Whether to save annotated image

        Returns:
            List[dict]: List of detections
        """
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            return []

        print(f"\n✓ Processing image: {image_path}")

        try:
            # Run inference
            results = self.model.predict(
                source=image_path,
                conf=self.confidence_threshold,
                verbose=False,
            )

            detections = []
            image_name = os.path.basename(image_path)

            if results and len(results) > 0:
                result = results[0]
                image = result.orig_img.copy()
                h, w = image.shape[:2]

                # Process detections
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        # Extract box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                        confidence = float(box.conf[0].cpu().numpy())
                        class_id = int(box.cls[0].cpu().numpy())

                        # Get class name
                        waste_type = self.class_names[class_id]

                        # Get category and bin
                        try:
                            waste_category = WasteCategoryMapper.get_waste_category(
                                waste_type
                            )
                            recommended_bin = (
                                WasteCategoryMapper.get_recommended_bin(waste_type)
                            )
                        except ValueError as e:
                            print(f"✗ Error mapping waste type: {e}")
                            continue

                        # Log to CSV
                        waste_id = self.logger.log_detection(
                            waste_type=waste_type,
                            waste_category=waste_category,
                            recommended_bin=recommended_bin,
                            confidence=confidence * 100,
                            image_name=image_name,
                        )

                        # Store detection
                        detection_data = {
                            "waste_id": waste_id,
                            "waste_type": waste_type,
                            "waste_category": waste_category,
                            "recommended_bin": recommended_bin,
                            "confidence": confidence * 100,
                            "image_name": image_name,
                            "box": (x1, y1, x2, y2),
                        }
                        detections.append(detection_data)

                        # Print console output
                        print(
                            self._format_output(
                                {
                                    "waste_type": waste_type,
                                    "waste_category": waste_category,
                                    "recommended_bin": recommended_bin,
                                    "confidence": confidence * 100,
                                    "image_name": image_name,
                                }
                            )
                        )

                        # Draw on image
                        color = (0, 255, 0)  # Green
                        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

                        # Create label
                        label = f"{waste_type} ({confidence*100:.1f}%)"
                        label_size, _ = cv2.getTextSize(
                            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                        )
                        cv2.rectangle(
                            image,
                            (x1, y1 - label_size[1] - 8),
                            (x1 + label_size[0], y1),
                            color,
                            -1,
                        )
                        cv2.putText(
                            image,
                            label,
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 0),
                            2,
                        )

                        # Add category and bin info
                        info_text = f"Category: {waste_category} | Bin: {recommended_bin}"
                        cv2.putText(
                            image,
                            info_text,
                            (10, h - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )

                    # Save annotated image
                    if save_output:
                        output_path = os.path.join(
                            self.output_dir,
                            f"annotated_{image_name}",
                        )
                        cv2.imwrite(output_path, image)
                        print(f"✓ Saved annotated image: {output_path}")

                else:
                    print(f"⊘ No waste items detected in image")

            return detections

        except Exception as e:
            print(f"✗ Error processing image: {e}")
            return []

    def infer_folder(
        self,
        folder_path: str,
        file_extensions: Optional[List[str]] = None,
        save_output: bool = True,
    ) -> List[dict]:
        """
        Run inference on all images in a folder.

        Args:
            folder_path (str): Path to the folder
            file_extensions (Optional[List[str]]): File extensions to process
            save_output (bool): Whether to save annotated images

        Returns:
            List[dict]: All detections
        """
        if file_extensions is None:
            file_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

        if not os.path.isdir(folder_path):
            print(f"✗ Folder not found: {folder_path}")
            return []

        print(f"\n✓ Processing folder: {folder_path}")

        # Get all image files
        image_files = []
        for ext in file_extensions:
            image_files.extend(
                Path(folder_path).glob(f"*{ext}"),
            )
            image_files.extend(
                Path(folder_path).glob(f"*{ext.upper()}"),
            )

        image_files = sorted(set(str(f) for f in image_files))

        if not image_files:
            print(f"✗ No images found in folder")
            return []

        print(f"Found {len(image_files)} images to process")

        all_detections = []
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}]", end=" ")
            detections = self.infer_image(image_path, save_output)
            all_detections.extend(detections)

        print(f"\n✓ Folder processing complete")
        return all_detections

    def infer_webcam(
        self,
        webcam_id: int = 0,
        confidence_display: bool = True,
    ) -> None:
        """
        Run real-time inference from webcam.

        Args:
            webcam_id (int): Webcam device ID (usually 0)
            confidence_display (bool): Whether to display confidence
        """
        print(f"\n✓ Starting webcam inference (ID: {webcam_id})")
        print("Press 'q' to quit, 's' to save frame, 'c' to capture detection")

        cap = cv2.VideoCapture(webcam_id)

        if not cap.isOpened():
            print(f"✗ Could not open webcam {webcam_id}")
            return

        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)

        frame_count = 0
        saved_count = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("✗ Error reading frame from webcam")
                    break

                frame_count += 1

                # Run inference
                results = self.model.predict(
                    source=frame,
                    conf=self.confidence_threshold,
                    verbose=False,
                )

                if results and len(results) > 0:
                    result = results[0]
                    annotated_frame = result.plot()
                    h, w = annotated_frame.shape[:2]

                    # Process detections
                    if result.boxes is not None and len(result.boxes) > 0:
                        for box in result.boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                            confidence = float(box.conf[0].cpu().numpy())
                            class_id = int(box.cls[0].cpu().numpy())

                            waste_type = self.class_names[class_id]

                            try:
                                waste_category = (
                                    WasteCategoryMapper.get_waste_category(
                                        waste_type
                                    )
                                )
                                recommended_bin = (
                                    WasteCategoryMapper.get_recommended_bin(
                                        waste_type
                                    )
                                )

                                # Add info on frame
                                text = f"{waste_type} | {waste_category} | {recommended_bin}"
                                cv2.putText(
                                    annotated_frame,
                                    text,
                                    (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    (0, 255, 0),
                                    2,
                                )
                            except ValueError:
                                pass

                    # Display frame info
                    cv2.putText(
                        annotated_frame,
                        f"Frame: {frame_count} | Press 'q' to quit",
                        (10, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        1,
                    )

                    cv2.imshow("Biomedical Waste Detection", annotated_frame)
                else:
                    cv2.imshow("Biomedical Waste Detection", frame)

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print("\n✓ Exiting webcam inference")
                    break
                elif key == ord("s"):
                    filename = f"webcam_frame_{frame_count}.jpg"
                    output_path = os.path.join(self.output_dir, filename)
                    cv2.imwrite(output_path, frame)
                    saved_count += 1
                    print(f"✓ Saved frame: {output_path}")

        except KeyboardInterrupt:
            print("\n✓ Interrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"Processed {frame_count} frames, saved {saved_count}")


def main():
    """Main inference pipeline."""
    print("\n" + "=" * 60)
    print("BIOMEDICAL WASTE SEGREGATION - INFERENCE PIPELINE")
    print("=" * 60)

    # Check for command-line arguments
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python inference.py --image <image_path>")
        print("  python inference.py --folder <folder_path>")
        print("  python inference.py --webcam [device_id]")
        print("\nExamples:")
        print("  python inference.py --image sample_images/waste1.jpg")
        print("  python inference.py --folder sample_images/")
        print("  python inference.py --webcam 0")
        print("\n" + "=" * 60)
        return

    try:
        # Initialize inference pipeline
        inference = BiomedicalWasteInference(
            model_path="best.pt",
            output_dir="output_images",
            csv_path="waste_log.csv",
            confidence_threshold=0.5,
        )

        # Parse arguments
        if sys.argv[1] == "--image" and len(sys.argv) > 2:
            image_path = sys.argv[2]
            inference.infer_image(image_path)

        elif sys.argv[1] == "--folder" and len(sys.argv) > 2:
            folder_path = sys.argv[2]
            inference.infer_folder(folder_path)

        elif sys.argv[1] == "--webcam":
            webcam_id = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            inference.infer_webcam(webcam_id)

        else:
            print("✗ Invalid arguments")

        # Print summary
        print("\n" + "=" * 60)
        print("INFERENCE SUMMARY")
        print("=" * 60)
        print(f"Total records logged: {inference.logger.get_total_records()}")
        print(f"CSV location: {inference.logger.get_csv_path()}")
        print(f"Output directory: {os.path.abspath(inference.output_dir)}")

        # Print statistics
        stats = inference.logger.get_summary_statistics()
        if stats:
            print("\n--- Statistics ---")
            print(f"Average Confidence: {stats.get('average_confidence', 'N/A')}%")
            print(f"Most Common Waste: {stats.get('most_common_waste_type', 'N/A')}")
            print(f"Most Common Category: {stats.get('most_common_category', 'N/A')}")
            print(f"Most Common Bin: {stats.get('most_common_bin', 'N/A')}")

        print("\n" + "=" * 60)

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
