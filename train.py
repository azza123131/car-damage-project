import mlflow
import mlflow.pytorch
from ultralytics import YOLO
import yaml
import os
from ultralytics import settings as ultralytics_settings
ultralytics_settings.update({"mlflow": False})

# ── Load params ──────────────────────────────────────────
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

train_params = params["train"]
data_params  = params["data"]

# ── MLflow setup ─────────────────────────────────────────
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("car-damage-detection")

# ── Train ─────────────────────────────────────────────────
with mlflow.start_run():

    # Log all hyperparameters
    mlflow.log_params(train_params)
    mlflow.log_params(data_params)

    # Train YOLOv8m
    model = YOLO("yolov8m.pt")
    results = model.train(
        data=data_params["yaml_path"],
        epochs=train_params["epochs"],
        imgsz=train_params["imgsz"],
        batch=train_params["batch_size"],
        project="runs/train",
        name="yolov8m_cardd",
        exist_ok=True,
    )

    # ── Log metrics ──────────────────────────────────────
    metrics = results.results_dict
    mlflow.log_metric("mAP50",      metrics.get("metrics/mAP50(B)",    0))
    mlflow.log_metric("mAP50_95",   metrics.get("metrics/mAP50-95(B)", 0))
    mlflow.log_metric("precision",  metrics.get("metrics/precision(B)", 0))
    mlflow.log_metric("recall",     metrics.get("metrics/recall(B)",    0))
    mlflow.log_metric("box_loss",   metrics.get("train/box_loss",       0))
    mlflow.log_metric("cls_loss",   metrics.get("train/cls_loss",       0))

    # ── Log model ────────────────────────────────────────
    best_model_path = "runs/train/yolov8m_cardd/weights/best.pt"
    if os.path.exists(best_model_path):
        mlflow.log_artifact(best_model_path, artifact_path="model")
        print("✅ Model logged to MLflow")

    print("✅ Training complete and logged to MLflow")