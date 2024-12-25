import os
import json
import re
from pathlib import Path


def parse_results_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Extract day number from path
    day = int(re.search(r"day_(\d+)", str(file_path)).group(1))

    # Parse results for each model
    results = {}
    current_model = None

    for line in content.split("\n"):
        # Find model name
        if line.startswith("##"):
            current_model = line.strip("# ").strip(".py")
        # Find part results
        elif line.strip().startswith("- Part"):
            if current_model:
                part = int(re.search(r"Part (\d+)", line).group(1))

                # Check for exact matches and print mismatches
                if "Success" not in line and "Failed" not in line:
                    print(
                        f"WARNING: Inconsistent result format in {file_path}, model {current_model}, Part {part}"
                    )
                    print(f"Line content: {line.strip()}")

                success = 1 if "Success" in line else 0

                if current_model not in results:
                    results[current_model] = {}
                results[current_model][f"part{part}"] = success

    # Sort models alphabetically
    results = dict(sorted(results.items()))
    return day, results


def main():
    workspace_path = Path(os.getcwd())
    all_results = {}

    # Find all results.md files
    for day_dir in sorted(workspace_path.glob("day_*")):
        results_file = day_dir / "results.md"
        if results_file.exists():
            day, results = parse_results_file(results_file)
            day_key = f"day{day:02d}"
            all_results[day_key] = results

    # Sort days by number
    all_results = dict(sorted(all_results.items()))

    # Save to JSON file
    with open("model_performance.json", "w") as f:
        json.dump(all_results, f, indent=2)


if __name__ == "__main__":
    main()
