import random
import pandas as pd
from data.juliet_loader import load_juliet_dataset

NOISE_RATE = 0.15


# -------- SIMPLE --------
def simple_safe():
    return random.choice([
        "int a = 0; if(a == 1) return 1;",
        "for(int i=0;i<n;i++){ sum += i; }",
        "int *p = NULL; if(p != NULL) *p = 5;",
    ])


def simple_buggy():
    return random.choice([
        "int a; if(a == 1) return 1;",
        "int *p = NULL; *p = 5;",
        "for(int i=0;i<=n;i++){ arr[i]=0; }",
    ])


# -------- COMPLEX --------
def complex_safe():
    return """
    int sum_array(int *arr, int n) {
        int sum = 0;
        for(int i = 0; i < n; i++) {
            if(arr[i] > 0) {
                sum += arr[i];
            }
        }
        return sum;
    }
    """


def complex_buggy():
    return """
    int compute(int x) {
        int y = x * 2;
        int z = y - x;
        if(z > 10) {
            x = z / (x - x);
        }
        return x;
    }
    """


# -------- NOISE --------
def add_variation(code):
    vars = ["x", "temp", "count", "val", "num"]
    for v in ["a", "i", "x"]:
        code = code.replace(v, random.choice(vars))
    return code


def random_spacing(code):
    if random.random() < 0.5:
        code = code.replace(";", ";\n")
    return code


# -------- MAIN --------
def create_dataset(size=10000, juliet_path=None):
    data = []

    # --- synthetic ---
    for _ in range(int(size * 0.6)):
        r = random.random()

        if r < 0.25:
            code = simple_safe()
            label = 0
        elif r < 0.5:
            code = simple_buggy()
            label = 1
        elif r < 0.75:
            code = complex_safe()
            label = 0
        else:
            code = complex_buggy()
            label = 1

        code = add_variation(code)
        code = random_spacing(code)

        if random.random() < NOISE_RATE:
            label = 1 - label

        data.append((code, label))

    df = pd.DataFrame(data, columns=["code", "label"])

    # --- juliet ---
    if juliet_path:
        print("Loading Juliet dataset...")
        juliet_df = load_juliet_dataset(juliet_path, max_samples=int(size * 0.4))
        df = pd.concat([df, juliet_df], ignore_index=True)

    # shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    df.to_csv("dataset.csv", index=False)
    print(f"Final dataset size: {len(df)}")


if __name__ == "__main__":
    create_dataset(
        size=10000,
        juliet_path="/Users/sauravsharma/Downloads/C/testcases"
    )