import os

print("Step 1: Generating dataset...")
os.system("python data/generate_dataset.py")

print("\nStep 2: Training models...")
os.system("python models/train.py")

print("\nDone. Run predict.py to test.")