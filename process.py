import datetime
import os
import json

DATA_DIR = "/app/data"
OUTPUT_DIR = "/app/output"

def process():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read input file
    input_file = os.path.join(DATA_DIR, "input.json")
    if not os.path.exists(input_file):
        print(f"No input file found at {input_file}")
        return

    with open(input_file, "r") as f:
        data = json.load(f)

    # Process data
    result = {
        "processed_at": datetime.datetime.now().isoformat(),
        "record_count": len(data),
        "summary": {
            "total_value": sum(item.get("value", 0) for item in data),
            "avg_value": sum(item.get("value", 0) for item in data) / len(data),
        },
    }

    # Write output
    output_file = os.path.join(OUTPUT_DIR, "result.json")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Processed {result['record_count']} records")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    process()
