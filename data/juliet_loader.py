import os
import pandas as pd


def load_juliet_dataset(root_dir, max_samples=3000):
    data = []
    count = 0

    for subdir, _, files in os.walk(root_dir):
        for file in files:

            # only C/C++ files
            if not file.endswith((".c", ".cpp")):
                continue

            filename = file.lower()

            # ✅ FIXED labeling (CRITICAL)
            if "_bad" in filename:
                label = 1
            elif "_good" in filename:
                label = 0
            else:
                continue

            path = os.path.join(subdir, file)

            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()

                data.append((code, label))
                count += 1

                # 🔥 Debug progress
                if count % 200 == 0:
                    print(f"Loaded {count} Juliet samples...")

                # ✅ Early stop (important for speed)
                if count >= max_samples:
                    print(f"Stopping at {count} samples")
                    return pd.DataFrame(data, columns=["code", "label"])

            except:
                continue

    print(f"Finished scanning. Total collected: {count}")
    return pd.DataFrame(data, columns=["code", "label"])