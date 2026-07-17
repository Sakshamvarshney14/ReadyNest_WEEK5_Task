import os
import subprocess
import time

print("=" * 70)
print("CUSTOMER PURCHASE ANALYTICS - ETL PIPELINE")
print("=" * 70)

scripts = [

    "src/preprocessing/dataset_audit.py",

    "src/preprocessing/data_validation.py",

    "src/preprocessing/data_consistency_check.py",

    "src/preprocessing/data_cleaning.py",

    "src/preprocessing/feature_engineering.py"

]

start_time = time.time()

success = []
failed = []

for script in scripts:

    print("\n" + "-" * 70)
    print(f"Running : {script}")
    print("-" * 70)

    try:

        result = subprocess.run(
            ["python", script],
            check=True
        )

        success.append(script)

        print(f"\nSUCCESS : {script}")

    except subprocess.CalledProcessError:

        failed.append(script)

        print(f"\nFAILED : {script}")

end_time = time.time()

print("\n" + "=" * 70)
print("ETL PIPELINE SUMMARY")
print("=" * 70)

print(f"\nTotal Scripts : {len(scripts)}")
print(f"Successful    : {len(success)}")
print(f"Failed        : {len(failed)}")
print(f"Execution Time: {round(end_time-start_time,2)} Seconds")

print("\nExecuted Modules")

for module in success:

    print(f"✓ {module}")

if failed:

    print("\nFailed Modules")

    for module in failed:

        print(f"✗ {module}")

print("\nETL Pipeline Completed")

print("=" * 70)