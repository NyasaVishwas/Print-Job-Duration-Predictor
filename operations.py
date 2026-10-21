
from datetime import datetime, timezone

from database import db

print_jobs = db["print_jobs"]


def create_job():
    job_id = input("Enter job ID: ").strip()

    if not job_id:
        print("Job ID cannot be empty.")
        return

    if print_jobs.find_one({"job_id": job_id}):
        print("A job with this ID already exists.")
        return

    try:
        page_count = int(input("Number of pages: "))
        copies = int(input("Number of copies: "))
        print_mode = input(
            "Print mode (black_white/color): "
        ).strip().lower()
        binding_type = input(
            "Binding (none/staple/spiral): "
        ).strip().lower()
        printer_speed = int(input("Printer speed (pages/min): "))

        job = {
            "job_id": job_id,
            "page_count": page_count,
            "copies": copies,
            "print_mode": print_mode,
            "binding_type": binding_type,
            "printer_speed_ppm": printer_speed,
            "created_at": datetime.now(timezone.utc),
            "actual_duration_minutes": 0.0,
            "status": "queued",
        }

        result = print_jobs.insert_one(job)
        print("Job created successfully:", result.inserted_id)

    except (ValueError, TypeError):
        print("Invalid input. Enter valid numeric values.")


def read_jobs():
    jobs = print_jobs.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1).limit(10)

    print("\n--- Latest 10 Print Jobs ---")

    found = False

    for job in jobs:
        found = True
        print(
            f"{job.get('job_id')} | "
            f"Pages: {job.get('page_count')} | "
            f"Mode: {job.get('print_mode')} | "
            f"Status: {job.get('status')}"
        )

    if not found:
        print("No print jobs found.")


def update_job():
    job_id = input("Enter job ID to update: ").strip()

    print("Available statuses: queued, printing, completed, failed")
    new_status = input("Enter new status: ").strip().lower()

    valid_statuses = [
        "queued", "printing", "completed", "failed"
    ]

    if new_status not in valid_statuses:
        print("Invalid status.")
        return

    result = print_jobs.update_one(
        {"job_id": job_id},
        {"$set": {"status": new_status}}
    )

    if result.matched_count:
        print("Job updated successfully.")
    else:
        print("Job ID not found.")


def delete_job():
    job_id = input("Enter job ID to delete: ").strip()

    confirm = input(
        f"Delete job {job_id}? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        return

    result = print_jobs.delete_one({"job_id": job_id})

    if result.deleted_count:
        print("Job deleted successfully.")
    else:
        print("Job ID not found.")


def main():
    while True:
        print("\n===== PrintPulse CRUD Menu =====")
        print("1. Create print job")
        print("2. Read print jobs")
        print("3. Update job status")
        print("4. Delete print job")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_job()
        elif choice == "2":
            read_jobs()
        elif choice == "3":
            update_job()
        elif choice == "4":
            delete_job()
        elif choice == "5":
            print("Exiting PrintPulse.")
            break
        else:
            print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()
