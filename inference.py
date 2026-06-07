"""
Biomedical Waste Detection - Main Inference Pipeline

Supports:
1. Single Image Inference: Performs detection on an image, logs to CSV, saves annotated image.
2. Folder Inference: Scans a folder for all images, runs inference sequentially, logs results, saves outputs.
3. Webcam Inference: Runs real-time video capture, detects waste, draws bounding boxes, shows live FPS and annotations, logs detections.

Author: AI-Based Medical Waste Segregation System
Version: 1.1
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

from config import SystemConfig
from category_mapping import WasteCategoryMapper
from csv_logger import WasteCSVLogger
from utils import ImageUtils, VisualizationUtils, FileUtils


class BiomedicalWasteInferencePipeline:
    """Performs YOLOv11 inference for biomedical waste segregation monitoring."""

    def __init__(self, confidence_threshold: Optional[float] = None):
        """Initialize pipeline, configure paths, and load the YOLO model."""
        # Ensure directory structure exists
        SystemConfig.setup_directories()

        # Overwrite confidence threshold if specified, else use config
        self.conf_threshold = confidence_threshold or SystemConfig.MODEL_CONFIG["confidence_threshold"]
        self.model_path = SystemConfig.MODEL_PATH
        self.csv_path = SystemConfig.CSV_LOG_PATH
        self.output_dir = SystemConfig.OUTPUT_IMAGES_DIR

        self.model = None
        self.logger = None
        self.class_names = {}

        self._load_components()

    def _load_components(self) -> None:
        """Load the YOLO model weights and initialize the CSV logger."""
        print("\n" + "=" * 60)
        print("SYSTEM INITIALIZATION")
        print("=" * 60)

        # 1. Check if model weights exist
        if not self.model_path.exists():
            print(f"✗ CRITICAL ERROR: Model weight file not found at: {self.model_path}")
            print("  Please ensure 'best.pt' is placed in the 'weights/' directory.")
            sys.exit(1)

        # 2. Load the YOLO model
        try:
            print(f"Loading YOLO model weights: {self.model_path} ...")
            self.model = YOLO(str(self.model_path))
            self.class_names = self.model.names
            print("✓ YOLO model loaded successfully.")
            print(f"✓ Detected classes in model: {list(self.class_names.values())}")
        except Exception as e:
            print(f"✗ CRITICAL ERROR: Failed to load YOLO model: {e}")
            sys.exit(1)

        # 3. Load CSV Logger
        try:
            self.logger = WasteCSVLogger(self.csv_path)
            print("✓ CSV logging system initialized.")
        except Exception as e:
            print(f"✗ CRITICAL ERROR: Failed to initialize CSV logger: {e}")
            sys.exit(1)

        print("=" * 60 + "\n")

    def run_inference_on_frame(self, frame: np.ndarray, source_name: str, log_results: bool = True) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Perform model prediction and post-processing on a single image frame.

        Args:
            frame (np.ndarray): Input image frame in BGR format.
            source_name (str): Identifier/file name for logging.
            log_results (bool): If True, commits detections to the CSV file.

        Returns:
            Tuple[np.ndarray, List[Dict[str, Any]]]: (Annotated image frame, List of detections)
        """
        detections = []
        
        try:
            results = self.model.predict(
                source=frame,
                conf=self.conf_threshold,
                iou=SystemConfig.MODEL_CONFIG["iou_threshold"],
                verbose=False
            )
        except Exception as e:
            print(f"✗ Error during model prediction: {e}")
            return frame, []

        if results and len(results) > 0:
            boxes = results[0].boxes
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    # Extract coordinates, confidence and class index
                    xyxy = box.xyxy[0].cpu().numpy().astype(int)
                    conf = float(box.conf[0].cpu().numpy())
                    cls_idx = int(box.cls[0].cpu().numpy())

                    # Map class index to class name
                    waste_type = self.class_names.get(cls_idx, "general_waste")

                    # Map class name to category and bin recommendation
                    try:
                        category, bin_recommendation = WasteCategoryMapper.get_complete_mapping(waste_type)
                    except ValueError:
                        category = "Non-Biomedical Waste"
                        bin_recommendation = "General Waste Bin"

                    # Log to CSV if required
                    waste_id = "N/A"
                    if log_results:
                        try:
                            waste_id = self.logger.log_detection(
                                waste_type=waste_type,
                                waste_category=category,
                                recommended_bin=bin_recommendation,
                                confidence=conf,
                                image_name=source_name
                            )
                        except Exception as e:
                            print(f"✗ CSV Logging failed for {waste_type}: {e}")

                    detections.append({
                        "box": (xyxy[0], xyxy[1], xyxy[2], xyxy[3]),
                        "waste_id": waste_id,
                        "waste_type": waste_type,
                        "waste_category": category,
                        "recommended_bin": bin_recommendation,
                        "confidence": conf
                    })

        # Draw annotations using the custom OpenCV draw utility
        annotated_frame = VisualizationUtils.draw_detections(frame, detections)
        return annotated_frame, detections

    def process_single_image(self, image_path_str: str) -> None:
        """
        Mode 1: Single image inference. Reads, predicts, logs to CSV, saves annotated image.

        Args:
            image_path_str (str): Path to input image file.
        """
        img_path = Path(image_path_str)
        if not img_path.exists():
            print(f"✗ Error: Image file does not exist at {image_path_str}")
            return

        if not ImageUtils.validate_image_file(img_path):
            print(f"✗ Error: Invalid or corrupted image file: {image_path_str}")
            return

        # Load image
        img = ImageUtils.load_image(img_path)
        if img is None:
            return

        print(f"Processing image '{img_path.name}'...")
        annotated_img, detections = self.run_inference_on_frame(img, img_path.name, log_results=True)

        # Print detection results to the console
        if detections:
            print(f"✓ Detected {len(detections)} waste item(s):")
            for idx, det in enumerate(detections, 1):
                print(f"  [{idx}] {det['waste_id']} | Type: {det['waste_type'].capitalize()} | "
                      f"Category: {det['waste_category']} | Bin: {det['recommended_bin']} | "
                      f"Confidence: {det['confidence']*100:.1f}%")
        else:
            print("⊘ No waste items detected above the confidence threshold.")

        # Save annotated image
        output_filename = f"{img_path.stem}_annotated{img_path.suffix}"
        output_path = self.output_dir / output_filename
        
        if ImageUtils.save_image(annotated_img, output_path):
            print(f"✓ Annotated image saved to: {output_path}")

    def process_folder(self, folder_path_str: str) -> None:
        """
        Mode 2: Folder/Batch inference. Scans folder, processes all images.

        Args:
            folder_path_str (str): Path to directory containing images.
        """
        folder_path = Path(folder_path_str)
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"✗ Error: Directory does not exist: {folder_path_str}")
            return

        # Find image files
        image_files = FileUtils.get_image_files_in_folder(folder_path)
        if not image_files:
            print(f"✗ Error: No valid images found in folder: {folder_path_str}")
            return

        print(f"Found {len(image_files)} image(s) in folder. Starting batch inference...")
        
        total_detections = 0
        start_time = time.time()

        for idx, img_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] processing '{img_path.name}'")
            img = ImageUtils.load_image(img_path)
            if img is None:
                continue

            annotated_img, detections = self.run_inference_on_frame(img, img_path.name, log_results=True)
            total_detections += len(detections)

            # Save annotated image
            output_filename = f"{img_path.stem}_annotated{img_path.suffix}"
            output_path = self.output_dir / output_filename
            ImageUtils.save_image(annotated_img, output_path)

        elapsed = time.time() - start_time
        print("\n" + "=" * 60)
        print("BATCH PROCESSING COMPLETED")
        print("=" * 60)
        print(f"Processed: {len(image_files)} image(s)")
        print(f"Total waste items detected and logged: {total_detections}")
        print(f"Time taken: {elapsed:.2f} seconds")
        print(f"All annotated images saved to: {self.output_dir}")
        print("=" * 60)

    def process_webcam(self) -> None:
        """
        Mode 3: Live webcam inference.
        Shows bounding boxes, categories, recommended bins, confidence, and real-time FPS.
        Press 'Q' to exit.
        Saves annotated frames and logs to CSV automatically upon detection with debouncing.
        """
        print("\n" + "=" * 60)
        print("STARTING REAL-TIME WEBCAM MONITORING")
        print("=" * 60)
        print("• Press 'Q' to quit and stop the stream.")
        print("• Detections are logged and saved automatically.")
        print("=" * 60 + "\n")

        # Open webcam video stream (default 0)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("✗ ERROR: Webcam is unavailable, disconnected, or blocked by another process.")
            return

        # Attempt to set HD resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        prev_time = time.time()
        frame_counter = 0
        
        # Debounce logic to prevent logging the exact same class every single frame.
        # Tracks last time a class was logged. Allow logging again after 2 seconds.
        last_logged_time: Dict[str, float] = {}
        log_cooldown_seconds = 2.0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("✗ Error: Failed to retrieve video frame from webcam.")
                    break

                frame_counter += 1
                
                # Perform inference, but wait: do we log immediately?
                # We perform inference with log_results=False, and log selectively based on debouncing.
                annotated_frame, detections = self.run_inference_on_frame(frame, "webcam_live", log_results=False)

                current_time = time.time()
                
                # Handle debounced logging and frame saving for webcam mode
                webcam_detections_logged = False
                for det in detections:
                    w_type = det["waste_type"]
                    # If this class has not been logged recently, log it
                    if w_type not in last_logged_time or (current_time - last_logged_time[w_type] > log_cooldown_seconds):
                        last_logged_time[w_type] = current_time
                        
                        # Generate structured frame filename
                        waste_id = self.logger.get_next_waste_id()
                        webcam_image_name = f"webcam_frame_{waste_id}.jpg"
                        
                        # Log to CSV
                        self.logger.log_detection(
                            waste_type=w_type,
                            waste_category=det["waste_category"],
                            recommended_bin=det["recommended_bin"],
                            confidence=det["confidence"],
                            image_name=webcam_image_name
                        )
                        
                        # Save the annotated frame to output_images
                        frame_save_path = self.output_dir / webcam_image_name
                        ImageUtils.save_image(annotated_frame, frame_save_path)
                        print(f"✓ Auto-Logged: {waste_id} | {w_type.capitalize()} detected. Frame saved: {webcam_image_name}")
                        webcam_detections_logged = True

                # Calculate FPS
                fps = 1.0 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
                prev_time = current_time

                # Draw FPS overlay
                cv2.putText(
                    annotated_frame,
                    f"FPS: {fps:.1f}",
                    (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                    lineType=cv2.LINE_AA
                )
                
                # Draw status info
                cv2.putText(
                    annotated_frame,
                    "LIVE MONITORING | Press 'Q' to Exit",
                    (15, annotated_frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    lineType=cv2.LINE_AA
                )

                # Show live window
                cv2.imshow("AI Medical Waste Segregation System", annotated_frame)

                # Wait for Q key to exit
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    print("\nWebcam session ended by operator.")
                    break
        except KeyboardInterrupt:
            print("\nWebcam session interrupted.")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Webcam stream release complete. Live window closed.")


def main():
    """Main program entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Based Medical Waste Segregation Monitoring System for Multi-Speciality Hospitals"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--image", type=str, help="Path to single image file for inference")
    group.add_argument("--folder", type=str, help="Path to folder containing images for inference")
    group.add_argument("--webcam", action="store_true", help="Launch live webcam inference mode")
    
    parser.add_argument("--conf", type=float, help="Override default confidence threshold (0.5)")

    args = parser.parse_args()

    try:
        pipeline = BiomedicalWasteInferencePipeline(confidence_threshold=args.conf)
        
        if args.image:
            pipeline.process_single_image(args.image)
        elif args.folder:
            pipeline.process_folder(args.folder)
        elif args.webcam:
            pipeline.process_webcam()
            
    except Exception as e:
        print(f"✗ Critical runtime error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
