import argparse
from cleaner.analyzer import analyze_code
from cleaner.remover import remove_dead_code

def main():
    parser = argparse.ArgumentParser(description="🧹 Dead Code Cleaner")
    parser.add_argument("--file", required=True, help="Path to the Python file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    analysis = analyze_code(code)
    print(f"🧠 Unused functions: {analysis['unused_funcs']}")
    print(f"📦 Unused imports: {analysis['unused_imports']}")

    cleaned_code = remove_dead_code(code, analysis)

    if args.overwrite:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
        print("✅ File cleaned and overwritten.")
    else:
        out_path = args.file.replace(".py", "_cleaned.py")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
        print(f"✅ Cleaned version saved to {out_path}")

if __name__ == "__main__":
    main()
