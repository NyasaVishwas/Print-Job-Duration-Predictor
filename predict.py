
import joblib
import pandas as pd

from database import db

MODEL_PATH = "models/linear_regression.joblib"

model = joblib.load(MODEL_PATH)

prediction_history = db["prediction_history"]


def predict_duration(
    page_count,
    copies,
    print_mode,
    binding_type,
    printer_speed_ppm,
):
    if page_count < 1 or copies < 1 or printer_speed_ppm < 1:
        raise ValueError("Page count, copies, and printer speed must be positive.")

    if print_mode not in ["black_white", "color"]:
        raise ValueError("Invalid print mode.")

    if binding_type not in ["none", "staple", "spiral"]:
        raise ValueError("Invalid binding type.")

    effective_pages = (
        page_count * copies / printer_speed_ppm
    )

    color_pages = (
        effective_pages if print_mode == "color" else 0.0
    )

    input_data = pd.DataFrame([{
        "effective_pages": effective_pages,
        "color_pages": color_pages,
        "binding_type": binding_type,
    }])

    predicted_minutes = max(
        0.0,
        float(model.predict(input_data)[0])
    )

    record = {
        "page_count": page_count,
        "copies": copies,
        "print_mode": print_mode,
        "binding_type": binding_type,
        "printer_speed_ppm": printer_speed_ppm,
        "predicted_duration_minutes": round(
            predicted_minutes, 2
        ),
    }

    result = prediction_history.insert_one(record)

    print("\n--- PrintPulse Prediction ---")
    print(f"Pages: {page_count}")
    print(f"Copies: {copies}")
    print(f"Mode: {print_mode}")
    print(f"Binding: {binding_type}")
    print(f"Printer speed: {printer_speed_ppm} pages/min")
    print(f"Predicted duration: {predicted_minutes:.2f} minutes")
    print(f"Saved prediction ID: {result.inserted_id}")

    return predicted_minutes


if __name__ == "__main__":
    predict_duration(
        page_count=50,
        copies=2,
        print_mode="color",
        binding_type="spiral",
        printer_speed_ppm=25,
    )
