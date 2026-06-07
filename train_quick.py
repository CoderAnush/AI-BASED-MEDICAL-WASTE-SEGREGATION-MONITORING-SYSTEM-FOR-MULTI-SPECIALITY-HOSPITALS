"""Quick training script for CPU - minimal configuration"""

from ultralytics import YOLO

# Load pretrained model
print("Loading YOLOv11 Nano...")
model = YOLO("yolo11n.pt")

# Train with minimal settings
print("Starting training (5 epochs, quick test)...")
results = model.train(
    data="Biomedical_Waste/data.yaml",
    epochs=5,
    imgsz=320,
    batch=2,
    device="cpu",
    patience=3,
    save=True,
    workers=0,
    cache=False,
    verbose=False,
)

print("\n✓ Training complete!")
print("Best model saved to: runs/detect/train/weights/best.pt")
