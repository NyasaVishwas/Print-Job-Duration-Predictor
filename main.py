
from database import db
from predict import predict_duration
from operations import (
    create_job,
    read_jobs,
    update_job,
    delete_job,
)
from aggregations import (
    average_duration_by_mode,
    job_count_by_status,
    total_pages_by_binding,
    slowest_jobs,
)


def main():
    while True:
        print("\n===== Print Job Duration Predictor =====")
        print("1. Predict print duration")
        print("2. Create print job")
        print("3. View print jobs")
        print("4. Update job status")
        print("5. Delete print job")
        print("6. View aggregation reports")
        print("7. View prediction history")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                page_count = int(input("Number of pages: "))
                copies = int(input("Number of copies: "))
                print_mode = input(
                    "Print mode (black_white/color): "
                ).strip().lower()
                binding_type = input(
                    "Binding (none/staple/spiral): "
                ).strip().lower()
                speed = int(input("Printer speed (pages/min): "))

                predict_duration(
                    page_count,
                    copies,
                    print_mode,
                    binding_type,
                    speed,
                )

            elif choice == "2":
                create_job()

            elif choice == "3":
                read_jobs()

            elif choice == "4":
                update_job()

            elif choice == "5":
                delete_job()

            elif choice == "6":
                print("\n--- Aggregation Reports ---")
                average_duration_by_mode()
                job_count_by_status()
                total_pages_by_binding()
                slowest_jobs()

            elif choice == "7":
                history = db["prediction_history"].find(
                    {},
                ).sort("_id", -1).limit(10)

                print("\n--- Recent Predictions ---")
                found = False

                for record in history:
                    found = True
                    print(record)

                if not found:
                    print("No predictions found.")

            elif choice == "8":
                print("Exiting PrintPulse.")
                break

            else:
                print("Invalid choice. Enter a number from 1 to 8.")

        except ValueError as error:
            print("Invalid input:", error)

        except Exception as error:
            print("Operation failed:", error)


if __name__ == "__main__":
    main()
