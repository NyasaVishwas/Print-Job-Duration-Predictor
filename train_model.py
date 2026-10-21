
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from database import db


MODEL_PATH = Path("models/linear_regression.joblib")

def main():
    # 1. Load completed print jobs from MongoDB.
    records = list(
        db["print_jobs"].find(
            {"status": "completed"},
            {
                "_id": 0,
                "page_count": 1,
                "copies": 1,
                "print_mode": 1,
                "binding_type": 1,
                "printer_speed_ppm": 1,
                "actual_duration_minutes": 1,
            },
        )
    )

    if len(records) < 20:
        raise ValueError(
            "At least 20 completed print jobs are required for training."
        )

    df = pd.DataFrame(records).dropna()

    # 2. Engineer features that reflect the printing workload.
    df["effective_pages"] = (
        df["page_count"] * df["copies"] / df["printer_speed_ppm"]
    )

    df["color_pages"] = np.where(
        df["print_mode"] == "color",
        df["effective_pages"],
        0.0,
    )

    feature_columns = [
        "effective_pages",
        "color_pages",
        "binding_type",
    ]

    X = df[feature_columns]
    y = df["actual_duration_minutes"]

    # 3. Split before training to evaluate on unseen records.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    # 4. Encode binding type and train Linear Regression.
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "binding",
                OneHotEncoder(handle_unknown="ignore"),
                ["binding_type"],
            ),
        ],
        remainder="passthrough",
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", LinearRegression()),
        ]
    )

    model.fit(X_train, y_train)

    # 5. Evaluate on the held-out test set.
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    # 6. Save the trained pipeline.
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("\n--- PrintPulse Model Evaluation ---")
    print(f"Training records: {len(X_train)}")
    print(f"Testing records:  {len(X_test)}")
    print(f"MAE:  {mae:.3f} minutes")
    print(f"RMSE: {rmse:.3f} minutes")
    print(f"R²:   {r2:.4f}")
    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
