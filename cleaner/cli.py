import argparse
import ast
import difflib
from pathlib import Path

from cleaner.analyzer import analyze_code
from cleaner.remover import remove_dead_code
from cleaner.ai_client import DeadCodeAIExplainer


def main():
    parser = argparse.ArgumentParser(description="🧹 Dead Code Cleaner with AI")
    parser.add_argument("--file", required=True, help="Path to the Python file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file")
    parser.add_argument("--explain-only", action="store_true", help="Only explain unused code, don't remove it")
    parser.add_argument("--patch", action="store_true", help="Generate a .patch file instead of saving cleaned file")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    # Analyze code to find unused functions and imports
    analysis = analyze_code(code)
    unused_funcs = analysis["unused_funcs"]
    unused_imports = analysis["unused_imports"]

    # 🤖 AI-based explanation of unused functions
    explainer = DeadCodeAIExplainer()

    for func_name in unused_funcs:
        func_node = next(
            (node for node in ast.walk(ast.parse(code)) if isinstance(node, ast.FunctionDef) and node.name == func_name),
            None,
        )
        if func_node:
            func_code = ast.get_source_segment(code, func_node)
            start_line = func_node.lineno - 1
            end_line = start_line + len(func_code.splitlines())

            surrounding_code = code

            full_context = f"""
### Here is the surrounding code:
{surrounding_code}

Here is the dead Function code:
{func_code}
"""
            explanation = explainer.explain_dead_code(full_context)
            print(f"\n🤖 Why is function '{func_name}' considered dead code?\n{explanation.strip()}\n")
        else:
            print(f"❗ Function {func_name} not found in the code!")

    if args.explain_only:
        print("🧹 Explanations completed. No code has been removed.")
        return

    # ✂️ Remove dead code
    cleaned_code = remove_dead_code(code, analysis)

    if args.patch:
        original_lines = code.splitlines(keepends=True)
        cleaned_lines = cleaned_code.splitlines(keepends=True)
        diff = difflib.unified_diff(
            original_lines,
            cleaned_lines,
            fromfile=args.file,
            tofile=args.file.replace(".py", "_cleaned.py"),
        )
        patch_path = Path(args.file).with_suffix(".deadcode.patch")
        with open(patch_path, "w", encoding="utf-8") as f:
            f.writelines(diff)
        print(f"✅ Patch saved to {patch_path}. Apply with: git apply {patch_path}")
    elif args.overwrite:
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
