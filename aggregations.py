
from database import db

print_jobs = db["print_jobs"]


def average_duration_by_mode():
    pipeline = [
        {"$match": {"status": "completed"}},
        {
            "$group": {
                "_id": "$print_mode",
                "average_duration": {
                    "$avg": "$actual_duration_minutes"
                },
                "total_jobs": {"$sum": 1},
            }
        },
        {"$sort": {"average_duration": -1}},
    ]

    print("\n--- Average Duration by Print Mode ---")

    for result in print_jobs.aggregate(pipeline):
        print(
            f"Mode: {result['_id']} | "
            f"Average: {result['average_duration']:.2f} min | "
            f"Jobs: {result['total_jobs']}"
        )


def job_count_by_status():
    pipeline = [
        {
            "$group": {
                "_id": "$status",
                "job_count": {"$sum": 1},
            }
        },
        {"$sort": {"job_count": -1}},
    ]

    print("\n--- Job Count by Status ---")

    for result in print_jobs.aggregate(pipeline):
        print(
            f"Status: {result['_id']} | "
            f"Jobs: {result['job_count']}"
        )


def total_pages_by_binding():
    pipeline = [
        {"$match": {"status": "completed"}},
        {
            "$group": {
                "_id": "$binding_type",
                "total_pages": {
                    "$sum": {
                        "$multiply": [
                            "$page_count",
                            "$copies",
                        ]
                    }
                },
                "total_jobs": {"$sum": 1},
            }
        },
        {"$sort": {"total_pages": -1}},
    ]

    print("\n--- Total Pages by Binding Type ---")

    for result in print_jobs.aggregate(pipeline):
        print(
            f"Binding: {result['_id']} | "
            f"Pages: {result['total_pages']} | "
            f"Jobs: {result['total_jobs']}"
        )


def slowest_jobs():
    pipeline = [
        {"$match": {"status": "completed"}},
        {"$sort": {"actual_duration_minutes": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 0,
                "job_id": 1,
                "page_count": 1,
                "copies": 1,
                "actual_duration_minutes": 1,
                "print_mode": 1,
            }
        },
    ]

    print("\n--- Five Slowest Completed Jobs ---")

    for result in print_jobs.aggregate(pipeline):
        print(
            f"Job: {result['job_id']} | "
            f"Pages: {result['page_count']} | "
            f"Copies: {result['copies']} | "
            f"Mode: {result['print_mode']} | "
            f"Duration: {result['actual_duration_minutes']} min"
        )


def main():
    average_duration_by_mode()
    job_count_by_status()
    total_pages_by_binding()
    slowest_jobs()


if __name__ == "__main__":
    main()
