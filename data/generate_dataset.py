# CODE 1
# 
# import random
# import pandas as pd
# from data.juliet_loader import load_juliet_dataset

# NOISE_RATE = 0.15


# # ================= SAFE TEMPLATES =================
# SAFE_TEMPLATES = [
#     # basic
#     "int a = 0; if(a == 1) return 1;",
#     "for(int i=0;i<n;i++){ sum += i; }",
#     "int *p = NULL; if(p != NULL) *p = 5;",
#     "int x = 10; int y = x + 5;",
#     "if(x > 0) x--;",
#     "while(n > 0) { n--; }",

#     # arrays
#     "int arr[10]; for(int i=0;i<10;i++){ arr[i]=i; }",
#     "int arr[5]; arr[0] = 1;",
#     "for(int i=0;i<5;i++){ arr[i] = i*i; }",

#     # pointers
#     "int x = 5; int *p = &x; *p = 10;",
#     "int *p = malloc(sizeof(int)); if(p) { *p = 5; free(p); }",

#     # conditions
#     "if(a > b) a = b;",
#     "if(a < b) b = a;",
#     "if(x != 0) y = 10/x;",

#     # loops
#     "for(int i=0;i<10;i++){ printf(\"%d\", i); }",
#     "while(i < n) i++;",

#     # functions
#     "int add(int a,int b){ return a+b; }",
#     "int square(int x){ return x*x; }",

#     # memory safe
#     "char buf[10]; strncpy(buf, \"hi\", 9);",
#     "char *p = malloc(10); if(p) { strcpy(p, \"ok\"); free(p); }",

#     # misc
#     "int flag = 0; if(flag) return 1;",
#     "int count = 0; count += 1;",
# ]


# # ================= BUGGY TEMPLATES =================
# BUGGY_TEMPLATES = [
#     # uninitialized
#     "int a; if(a == 1) return 1;",
#     "int x; printf(\"%d\", x);",

#     # null pointer
#     "int *p = NULL; *p = 5;",
#     "char *p = NULL; strcpy(p, \"hello\");",

#     # overflow
#     "int arr[5]; arr[10] = 1;",
#     "for(int i=0;i<=n;i++){ arr[i]=0; }",

#     # divide by zero
#     "int x = 10 / 0;",
#     "int y = a / (b - b);",

#     # double free
#     "int *p = malloc(sizeof(int)); free(p); free(p);",

#     # use after free
#     "int *p = malloc(sizeof(int)); free(p); *p = 10;",

#     # buffer overflow
#     "char buf[5]; strcpy(buf, \"this is long\");",

#     # pointer issues
#     "int *p; *p = 10;",

#     # off by one
#     "for(int i=0;i<=10;i++){ arr[i]=i; }",

#     # missing check
#     "int *p = malloc(sizeof(int)); *p = 5;",

#     # incorrect free
#     "int x; free(&x);",

#     # recursion overflow
#     "void f(){ f(); }",

#     # logic bug
#     "if(x = 5) printf(\"bug\");",

#     # format string
#     "printf(user_input);",

#     # misc
#     "int x; x = x + 1;",
#     "int arr[3]; arr[3] = 10;",
# ]


# # ================= COMPLEX WRAPPERS =================
# def complex_safe():
#     template = random.choice(SAFE_TEMPLATES)
#     return f"""
#     int func(int n) {{
#         {template}
#         return n;
#     }}
#     """


# def complex_buggy():
#     template = random.choice(BUGGY_TEMPLATES)
#     return f"""
#     int func(int x) {{
#         {template}
#         return x;
#     }}
#     """


# def simple_safe():
#     return random.choice(SAFE_TEMPLATES)


# def simple_buggy():
#     return random.choice(BUGGY_TEMPLATES)


# # ================= VARIATIONS =================
# def add_variation(code):
#     vars = ["x", "temp", "count", "val", "num", "idx", "ptr"]
#     for v in ["a", "i", "x"]:
#         code = code.replace(v, random.choice(vars))
#     return code


# def random_spacing(code):
#     if random.random() < 0.5:
#         code = code.replace(";", ";\n")
#     return code


# # ================= MAIN =================
# def create_dataset(size=10000, juliet_path=None):
#     data = []

#     # synthetic
#     for _ in range(int(size * 0.6)):
#         r = random.random()

#         if r < 0.25:
#             code = simple_safe()
#             label = 0
#         elif r < 0.5:
#             code = simple_buggy()
#             label = 1
#         elif r < 0.75:
#             code = complex_safe()
#             label = 0
#         else:
#             code = complex_buggy()
#             label = 1

#         code = add_variation(code)
#         code = random_spacing(code)

#         if random.random() < NOISE_RATE:
#             label = 1 - label

#         data.append((code, label))

#     df = pd.DataFrame(data, columns=["code", "label"])

#     # juliet
#     if juliet_path:
#         print("Loading Juliet dataset...")
#         juliet_df = load_juliet_dataset(juliet_path, max_samples=int(size * 0.4))
#         df = pd.concat([df, juliet_df], ignore_index=True)

#     df = df.sample(frac=1, random_state=42).reset_index(drop=True)

#     df.to_csv("dataset.csv", index=False)
#     print(f"Final dataset size: {len(df)}")


# if __name__ == "__main__":
#     create_dataset(
#         size=10000,
#         juliet_path="/Users/sauravsharma/Downloads/C/testcases"
#     )







# CODE 2
# 
# 
# import random
# import re
# import pandas as pd
# from data.juliet_loader import load_juliet_dataset

# NOISE_RATE = 0.05

# # =========================
# # 🔹 SUBTLE MUTATIONS
# # =========================

# def subtle_off_by_one(code):
#     return re.sub(r'<\s*(\w+)', r'<= \1', code)

# def shift_loop_start(code):
#     return re.sub(r'for\s*\(\s*int\s+(\w+)\s*=\s*0', r'for(int \1 = 1', code)

# def boundary_condition_change(code):
#     return code.replace("> 0", ">= 0").replace("< 0", "<= 0")

# def nested_logic_change(code):
#     return code.replace("&&", "||")

# def silent_divide_bug(code):
#     return re.sub(r'/\s*(\w+)', r'/ (\1 - \1 + 1)', code)

# def condition_dependency_bug(code):
#     return re.sub(r'if\s*\((.*?)\)', r'if(\1 && 1)', code)

# def reorder_statements(code):
#     lines = code.split("\n")
#     if len(lines) > 3:
#         i, j = random.sample(range(len(lines)), 2)
#         lines[i], lines[j] = lines[j], lines[i]
#     return "\n".join(lines)

# def redundant_logic(code):
#     return code.replace("if(", "if(1 && ")

# def subtle_pointer_bug(code):
#     return code.replace("*p", "*(p + 0)")

# def delayed_bug(code):
#     return code + "\nint dummy = 0;\ndummy = dummy;"

# MUTATIONS = [
#     subtle_off_by_one,
#     shift_loop_start,
#     boundary_condition_change,
#     nested_logic_change,
#     silent_divide_bug,
#     condition_dependency_bug,
#     reorder_statements,
#     redundant_logic,
#     subtle_pointer_bug,
#     delayed_bug
# ]

# # =========================
# # 🔹 DIVERSITY
# # =========================

# def rename_variables(code):
#     replacements = ["idx", "cnt", "val", "tmp", "num"]
#     return re.sub(r'\b[a-zA-Z_]\w*\b', lambda x: random.choice(replacements), code)

# def random_spacing(code):
#     if random.random() < 0.5:
#         code = code.replace(";", ";\n")
#     return code

# def diversify(code):
#     code = rename_variables(code)
#     code = random_spacing(code)
#     return code

# # =========================
# # 🔹 NORMALIZATION (DEDUP)
# # =========================

# def normalize(code):
#     code = re.sub(r'\s+', '', code)
#     code = re.sub(r'[a-zA-Z_]\w*', 'VAR', code)
#     return code

# # =========================
# # 🔹 APPLY MUTATIONS
# # =========================

# def apply_mutations(code):
#     k = random.choice([1, 2, 3])  # combine mutations
#     rules = random.sample(MUTATIONS, k)

#     new_code = code

#     for r in rules:
#         temp = r(new_code)
#         if temp != new_code:
#             new_code = temp

#     return new_code

# # =========================
# # 🔹 MAIN PIPELINE
# # =========================

# def create_dataset(size=20000, juliet_path=None):
#     if not juliet_path:
#         raise ValueError("Juliet path required")

#     print("Loading Juliet dataset...")
#     juliet_df = load_juliet_dataset(juliet_path, max_samples=size // 2)

#     print(f"Loaded {len(juliet_df)} Juliet samples")

#     data = []
#     seen = set()

#     for _, row in juliet_df.iterrows():
#         code = row["code"]
#         label = row["label"]

#         # Original
#         key = normalize(code)
#         if key not in seen:
#             seen.add(key)
#             data.append((code, label))

#         # Augmented versions
#         for _ in range(2):
#             new_code = apply_mutations(code)
#             new_code = diversify(new_code)

#             # flip label probabilistically (not deterministic)
#             new_label = label
#             if random.random() < 0.5:
#                 new_label = 1 - label

#             if random.random() < NOISE_RATE:
#                 new_label = 1 - new_label

#             key = normalize(new_code)
#             if key not in seen:
#                 seen.add(key)
#                 data.append((new_code, new_label))

#         if len(data) >= size:
#             break

#     df = pd.DataFrame(data, columns=["code", "label"])
#     df = df.sample(frac=1, random_state=42).reset_index(drop=True)

#     df.to_csv("dataset.csv", index=False)
#     print(f"Final dataset size: {len(df)}")


# if __name__ == "__main__":
#     create_dataset(
#         size=20000,
#         juliet_path="/Users/sauravsharma/Downloads/C/testcases"
#     )


# CODE 3
# 
# import random
# import re
# import pandas as pd
# from data.juliet_loader import load_juliet_dataset

# NOISE_RATE = 0.01

# # =========================
# # 🔹 SUBTLE BUG MUTATIONS
# # =========================

# def subtle_off_by_one(code):
#     return re.sub(r'<\s*(\w+)', r'<= \1', code)

# def shift_loop_start(code):
#     return re.sub(r'for\s*\(\s*int\s+(\w+)\s*=\s*0', r'for(int \1 = 1', code)

# def boundary_condition_change(code):
#     return code.replace("> 0", ">= 0").replace("< 0", "<= 0")

# def nested_logic_change(code):
#     return code.replace("&&", "||")

# def silent_divide_bug(code):
#     return re.sub(r'/\s*(\w+)', r'/ (\1 - \1 + 1)', code)

# # =========================
# # 🔹 SAFE / SEMANTIC CHANGES
# # =========================

# def reorder_statements(code):
#     lines = code.split("\n")

#     if len(lines) > 5:
#         i, j = random.sample(range(len(lines)), 2)
#         lines[i], lines[j] = lines[j], lines[i]

#     return "\n".join(lines)

# def redundant_logic(code):
#     return code.replace("if(", "if(1 && ")

# def subtle_pointer_change(code):
#     return code.replace("*p", "*(p + 0)")

# def formatting_noise(code):
#     if random.random() < 0.5:
#         code = code.replace(";", ";\n")
#     return code

# # =========================
# # 🔹 MUTATION LISTS
# # =========================

# BUG_MUTATIONS = [
#     subtle_off_by_one,
#     shift_loop_start,
#     boundary_condition_change,
#     nested_logic_change,
#     silent_divide_bug,
# ]

# SAFE_MUTATIONS = [
#     reorder_statements,
#     redundant_logic,
#     subtle_pointer_change,
#     formatting_noise,
# ]

# ALL_MUTATIONS = BUG_MUTATIONS + SAFE_MUTATIONS

# # =========================
# # 🔹 VARIABLE RENAMING
# # =========================

# def rename_variables(code):
#     replacements = ["idx", "cnt", "tmp", "val", "num"]

#     return re.sub(
#         r'\b[a-zA-Z_]\w*\b',
#         lambda x: random.choice(replacements),
#         code
#     )

# # =========================
# # 🔹 NORMALIZATION FOR DEDUP
# # =========================

# def normalize(code):
#     code = re.sub(r'\s+', '', code)
#     code = re.sub(r'[a-zA-Z_]\w*', 'VAR', code)
#     return code

# # =========================
# # 🔹 APPLY MUTATIONS
# # =========================

# def apply_mutations(code):
#     k = random.choice([1, 2])

#     rules = random.sample(ALL_MUTATIONS, k)

#     new_code = code
#     applied = []

#     for r in rules:
#         temp = r(new_code)

#         if temp != new_code:
#             new_code = temp
#             applied.append(r.__name__)

#     return new_code, applied

# # =========================
# # 🔹 LABEL INFERENCE
# # =========================

# BUG_RULE_NAMES = {
#     "subtle_off_by_one",
#     "shift_loop_start",
#     "boundary_condition_change",
#     "nested_logic_change",
#     "silent_divide_bug",
# }

# def infer_label(original_label, applied_rules):

#     # if any bug mutation applied → buggy
#     if any(r in BUG_RULE_NAMES for r in applied_rules):
#         return 1

#     return original_label

# # =========================
# # 🔹 MAIN DATASET CREATION
# # =========================

# def create_dataset(size=20000, juliet_path=None):

#     if not juliet_path:
#         raise ValueError("Juliet path required")

#     print("Loading Juliet dataset...")

#     juliet_df = load_juliet_dataset(
#         juliet_path,
#         max_samples=10000
#     )

#     print(f"Loaded {len(juliet_df)} Juliet samples")

#     data = []
#     seen = set()

#     for _, row in juliet_df.iterrows():

#         code = row["code"]
#         label = row["label"]

#         # -------------------------
#         # ORIGINAL SAMPLE
#         # -------------------------

#         key = normalize(code)

#         if key not in seen:
#             seen.add(key)
#             data.append((code, label))

#         # -------------------------
#         # AUGMENTED SAMPLES
#         # -------------------------

#         for _ in range(2):

#             new_code, applied_rules = apply_mutations(code)

#             new_code = rename_variables(new_code)

#             new_label = infer_label(label, applied_rules)

#             # very small label noise
#             if random.random() < NOISE_RATE:
#                 new_label = 1 - new_label

#             key = normalize(new_code)

#             if key not in seen:
#                 seen.add(key)
#                 data.append((new_code, new_label))

#         if len(data) >= size:
#             break

#     # =========================
#     # FINAL DATAFRAME
#     # =========================

#     df = pd.DataFrame(data, columns=["code", "label"])

#     df = df.sample(
#         frac=1,
#         random_state=42
#     ).reset_index(drop=True)

#     df.to_csv("dataset.csv", index=False)

#     print(f"Final dataset size: {len(df)}")

# # =========================
# # 🔹 ENTRY POINT
# # =========================

# if __name__ == "__main__":

#     create_dataset(
#         size=20000,
#         juliet_path="/Users/sauravsharma/Downloads/C/testcases"
#     )


import os
import random
import pandas as pd


JULIET_PATH = "/Users/sauravsharma/Downloads/C/testcases"

MAX_SAMPLES = 20000


def mutate_code(code):
    mutations = []

    lines = code.split("\n")

    # Remove bounds checks
    for i, line in enumerate(lines):
        if "if" in line and ("<" in line or ">" in line):
            modified = lines[:i] + lines[i + 1 :]
            mutations.append("\n".join(modified))

    # Replace safe functions
    replacements = {
        "strncpy": "strcpy",
        "snprintf": "sprintf",
        "memcpy": "strcpy",
        "fgets": "gets",
    }

    for safe, unsafe in replacements.items():
        if safe in code:
            mutations.append(code.replace(safe, unsafe))

    # Remove NULL checks
    if "NULL" in code:
        mutations.append(code.replace("!= NULL", ""))

    # Integer overflow style mutation
    if "+" in code:
        mutations.append(code.replace("+", "*", 1))

    # Array boundary mutation
    if "[" in code and "]" in code:
        mutations.append(code.replace("[i]", "[i+100]", 1))

    return mutations


def load_juliet_dataset(max_samples=MAX_SAMPLES):
    dataset = []

    count = 0

    for root, dirs, files in os.walk(JULIET_PATH):

        for file in files:

            if not (
                file.endswith(".c")
                or file.endswith(".cpp")
                or file.endswith(".cc")
            ):
                continue

            filepath = os.path.join(root, file)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()

                if len(code.strip()) < 20:
                    continue

                label = 1 if "bad" in filepath.lower() else 0

                dataset.append((code, label))
                count += 1

                # Generate synthetic buggy variants ONLY from safe code
                if label == 0:

                    mutated_versions = mutate_code(code)

                    for mutated in mutated_versions:

                        if mutated != code and len(mutated.strip()) > 20:
                            dataset.append((mutated, 1))

                if count % 200 == 0:
                    print(f"Loaded {count} Juliet samples...")

                if count >= max_samples:
                    print(f"Stopping at {max_samples} samples")
                    return dataset

            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return dataset


def balance_dataset(dataset):
    safe = [x for x in dataset if x[1] == 0]
    buggy = [x for x in dataset if x[1] == 1]

    min_size = min(len(safe), len(buggy))

    safe = random.sample(safe, min_size)
    buggy = random.sample(buggy, min_size)

    combined = safe + buggy
    random.shuffle(combined)

    return combined


def generate_dataset():
    print("Loading Juliet dataset...")

    dataset = load_juliet_dataset()

    print(f"Loaded {len(dataset)} total samples before balancing")

    dataset = balance_dataset(dataset)

    print(f"Final balanced dataset size: {len(dataset)}")

    df = pd.DataFrame(dataset, columns=["code", "label"])

    df.to_csv("dataset.csv", index=False)

    print("Dataset saved to dataset.csv")


if __name__ == "__main__":
    generate_dataset()


# import os
# import pandas as pd
# from pathlib import Path
# from sklearn.utils import shuffle

# JULIET_PATH = "/Users/sauravsharma/Downloads/C/testcases"

# MAX_JULIET_SAMPLES = 10000

# SAFE_KEYWORDS = [
#     "good",
#     "fix",
# ]

# UNSAFE_KEYWORDS = [
#     "bad",
#     "vuln",
# ]

# dataset = []

# def load_juliet():
#     print("Loading Juliet dataset...")

#     count = 0

#     for root, dirs, files in os.walk(JULIET_PATH):
#         for file in files:

#             if not file.endswith((".c", ".cpp")):
#                 continue

#             path = os.path.join(root, file)

#             try:
#                 with open(path, "r", encoding="utf-8", errors="ignore") as f:
#                     code = f.read()

#                 filename = file.lower()

#                 label = None

#                 if any(k in filename for k in UNSAFE_KEYWORDS):
#                     label = 1

#                 elif any(k in filename for k in SAFE_KEYWORDS):
#                     label = 0

#                 if label is None:
#                     continue

#                 dataset.append({
#                     "code": code,
#                     "label": label
#                 })

#                 count += 1

#                 if count % 200 == 0:
#                     print(f"Loaded {count} Juliet samples...")

#                 if count >= MAX_JULIET_SAMPLES:
#                     print(f"Stopping at {MAX_JULIET_SAMPLES} samples")
#                     return

#             except Exception:
#                 continue


# def balance_dataset(df):

#     min_count = df["label"].value_counts().min()

#     balanced = pd.concat([
#         df[df["label"] == 0].sample(min_count, random_state=42),
#         df[df["label"] == 1].sample(min_count, random_state=42),
#     ])

#     return shuffle(balanced, random_state=42)


# def main():

#     load_juliet()

#     print(f"Loaded {len(dataset)} Juliet samples")

#     df = pd.DataFrame(dataset)

#     df = balance_dataset(df)

#     print(f"Final dataset size: {len(df)}")

#     df.to_csv("dataset.csv", index=False)

#     print("Dataset saved to dataset.csv")


# if __name__ == "__main__":
#     main()