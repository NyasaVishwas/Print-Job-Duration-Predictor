
from pymongo.errors import OperationFailure

from database import db


def configure_validation():
    # Validation rules for print-job documents.
    print_job_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "job_id",
                "page_count",
                "copies",
                "print_mode",
                "binding_type",
                "printer_speed_ppm",
                "actual_duration_minutes",
                "status",
            ],
            "properties": {
                "job_id": {
                    "bsonType": "string",
                },
                "page_count": {
                    "bsonType": ["int", "long"],
                    "minimum": 1,
                },
                "copies": {
                    "bsonType": ["int", "long"],
                    "minimum": 1,
                },
                "print_mode": {
                    "enum": ["black_white", "color"],
                },
                "binding_type": {
                    "enum": ["none", "staple", "spiral"],
                },
                "printer_speed_ppm": {
                    "bsonType": ["int", "long"],
                    "minimum": 1,
                },
                "actual_duration_minutes": {
                    "bsonType": ["int", "double", "long", "decimal"],
                    "minimum": 0,
                },
                "status": {
                    "enum": [
                        "queued",
                        "printing",
                        "completed",
                        "failed",
                    ],
                },
            },
        }
    }

    collection_name = "print_jobs"

    if collection_name not in db.list_collection_names():
        db.create_collection(
            collection_name,
            validator=print_job_validator,
            validationLevel="strict",
            validationAction="error",
        )
        print("Created print_jobs with schema validation.")

    else:
        db.command({
            "collMod": collection_name,
            "validator": print_job_validator,
            "validationLevel": "strict",
            "validationAction": "error",
        })
        print("Updated print_jobs schema validation.")

    print("Schema validation configured successfully.")


def test_invalid_document():
    try:
        db["print_jobs"].insert_one({
            "job_id": "INVALID001",
            "page_count": -5,
            "copies": 1,
            "print_mode": "black_white",
            "binding_type": "none",
            "printer_speed_ppm": 25,
            "actual_duration_minutes": 2.0,
            "status": "completed",
        })

        print("Warning: invalid document was unexpectedly accepted.")

    except OperationFailure:
        print("Validation test passed: invalid document rejected.")


if __name__ == "__main__":
    configure_validation()
    test_invalid_document()
