
import random
from datetime import datetime, timedelta, timezone

from database import db

random.seed(42)

print_jobs = db["print_jobs"]
printers = db["printers"]

def generate_print_jobs(count=300):
    jobs = []

    for i in range(1, count + 1):
        page_count = random.randint(1, 200)
        copies = random.randint(1, 5)
        print_mode = random.choice(["black_white", "color"])
        binding_type = random.choice(["none", "staple", "spiral"])

        # Generate a realistic sample duration.
        # These are synthetic values, not real shop measurements.
        printer_speed = random.choice([15, 20, 25, 30])

        pages_to_print = page_count * copies
        mode_factor = 1.0 if print_mode == "black_white" else 1.7
        binding_minutes = {
            "none": 0,
            "staple": 1.0,
            "spiral": 4.0,
        }[binding_type]

        actual_minutes = (
            pages_to_print / printer_speed * mode_factor
            + binding_minutes
            + random.uniform(0.2, 2.0)
        )

        created_at = datetime.now(timezone.utc) - timedelta(
            days=random.randint(0, 60),
            minutes=random.randint(0, 1440),
        )

        jobs.append({
            "job_id": f"JOB{i:04d}",
            "page_count": page_count,
            "copies": copies,
            "print_mode": print_mode,
            "binding_type": binding_type,
            "printer_speed_ppm": printer_speed,
            "created_at": created_at,
            "actual_duration_minutes": round(actual_minutes, 2),
            "status": "completed",
        })

    return jobs


def seed_printers():
    printer_documents = [
        {
            "printer_id": "PRN01",
            "name": "Printer A",
            "speed_ppm": 15,
            "supported_modes": ["black_white", "color"],
            "supports_binding": False,
            "status": "available",
        },
        {
            "printer_id": "PRN02",
            "name": "Printer B",
            "speed_ppm": 25,
            "supported_modes": ["black_white", "color"],
            "supports_binding": True,
            "status": "available",
        },
        {
            "printer_id": "PRN03",
            "name": "Printer C",
            "speed_ppm": 30,
            "supported_modes": ["black_white"],
            "supports_binding": True,
            "status": "available",
        },
    ]

    for printer in printer_documents:
        printers.update_one(
            {"printer_id": printer["printer_id"]},
            {"$set": printer},
            upsert=True,
        )

    print(f"Printer records ready: {printers.count_documents({})}")


def main():
    # Insert jobs only if the collection is empty.
    if print_jobs.count_documents({}) == 0:
        jobs = generate_print_jobs(300)
        print_jobs.insert_many(jobs)
        print(f"Inserted {len(jobs)} synthetic print jobs.")
    else:
        print(
            f"Existing print jobs found: "
            f"{print_jobs.count_documents({})}. Skipping insertion."
        )

    seed_printers()


if __name__ == "__main__":
    main()
