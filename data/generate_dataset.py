import random
import pandas as pd
from data.juliet_loader import load_juliet_dataset

NOISE_RATE = 0.15


# ================= SAFE TEMPLATES =================
SAFE_TEMPLATES = [
    # basic
    "int a = 0; if(a == 1) return 1;",
    "for(int i=0;i<n;i++){ sum += i; }",
    "int *p = NULL; if(p != NULL) *p = 5;",
    "int x = 10; int y = x + 5;",
    "if(x > 0) x--;",
    "while(n > 0) { n--; }",

    # arrays
    "int arr[10]; for(int i=0;i<10;i++){ arr[i]=i; }",
    "int arr[5]; arr[0] = 1;",
    "for(int i=0;i<5;i++){ arr[i] = i*i; }",

    # pointers
    "int x = 5; int *p = &x; *p = 10;",
    "int *p = malloc(sizeof(int)); if(p) { *p = 5; free(p); }",

    # conditions
    "if(a > b) a = b;",
    "if(a < b) b = a;",
    "if(x != 0) y = 10/x;",

    # loops
    "for(int i=0;i<10;i++){ printf(\"%d\", i); }",
    "while(i < n) i++;",

    # functions
    "int add(int a,int b){ return a+b; }",
    "int square(int x){ return x*x; }",

    # memory safe
    "char buf[10]; strncpy(buf, \"hi\", 9);",
    "char *p = malloc(10); if(p) { strcpy(p, \"ok\"); free(p); }",

    # misc
    "int flag = 0; if(flag) return 1;",
    "int count = 0; count += 1;",
]


# ================= BUGGY TEMPLATES =================
BUGGY_TEMPLATES = [
    # uninitialized
    "int a; if(a == 1) return 1;",
    "int x; printf(\"%d\", x);",

    # null pointer
    "int *p = NULL; *p = 5;",
    "char *p = NULL; strcpy(p, \"hello\");",

    # overflow
    "int arr[5]; arr[10] = 1;",
    "for(int i=0;i<=n;i++){ arr[i]=0; }",

    # divide by zero
    "int x = 10 / 0;",
    "int y = a / (b - b);",

    # double free
    "int *p = malloc(sizeof(int)); free(p); free(p);",

    # use after free
    "int *p = malloc(sizeof(int)); free(p); *p = 10;",

    # buffer overflow
    "char buf[5]; strcpy(buf, \"this is long\");",

    # pointer issues
    "int *p; *p = 10;",

    # off by one
    "for(int i=0;i<=10;i++){ arr[i]=i; }",

    # missing check
    "int *p = malloc(sizeof(int)); *p = 5;",

    # incorrect free
    "int x; free(&x);",

    # recursion overflow
    "void f(){ f(); }",

    # logic bug
    "if(x = 5) printf(\"bug\");",

    # format string
    "printf(user_input);",

    # misc
    "int x; x = x + 1;",
    "int arr[3]; arr[3] = 10;",
]


# ================= COMPLEX WRAPPERS =================
def complex_safe():
    template = random.choice(SAFE_TEMPLATES)
    return f"""
    int func(int n) {{
        {template}
        return n;
    }}
    """


def complex_buggy():
    template = random.choice(BUGGY_TEMPLATES)
    return f"""
    int func(int x) {{
        {template}
        return x;
    }}
    """


def simple_safe():
    return random.choice(SAFE_TEMPLATES)


def simple_buggy():
    return random.choice(BUGGY_TEMPLATES)


# ================= VARIATIONS =================
def add_variation(code):
    vars = ["x", "temp", "count", "val", "num", "idx", "ptr"]
    for v in ["a", "i", "x"]:
        code = code.replace(v, random.choice(vars))
    return code


def random_spacing(code):
    if random.random() < 0.5:
        code = code.replace(";", ";\n")
    return code


# ================= MAIN =================
def create_dataset(size=10000, juliet_path=None):
    data = []

    # synthetic
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

    # juliet
    if juliet_path:
        print("Loading Juliet dataset...")
        juliet_df = load_juliet_dataset(juliet_path, max_samples=int(size * 0.4))
        df = pd.concat([df, juliet_df], ignore_index=True)

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    df.to_csv("dataset.csv", index=False)
    print(f"Final dataset size: {len(df)}")


if __name__ == "__main__":
    create_dataset(
        size=10000,
        juliet_path="/Users/sauravsharma/Downloads/C/testcases"
    )