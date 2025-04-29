import argparse
from cleaner.analyzer import analyze_code
from cleaner.remover import remove_dead_code
from cleaner.ai_client import DeadCodeAIExplainer
import ast

def main():
    parser = argparse.ArgumentParser(description="🧹 Dead Code Cleaner with AI")
    parser.add_argument("--file", required=True, help="Path to the Python file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file")
    parser.add_argument("--explain-only", action="store_true", help="Only explain unused code, don't remove it")

    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    # Analyze the code to get unused functions and imports
    analysis = analyze_code(code)
    unused_funcs = analysis["unused_funcs"]
    unused_imports = analysis["unused_imports"]

    # print(f"🧠 Unused functions: {unused_funcs}")
    # print(f"📦 Unused imports: {unused_imports}")

    # 🔥 Call AI for explanations
    explainer = DeadCodeAIExplainer()

    # If unused_funcs contains function names (strings), get their line numbers and code
    for func_name in unused_funcs:
        # Extract the function code using the function name and the line number
        func_node = next((node for node in ast.walk(ast.parse(code)) if isinstance(node, ast.FunctionDef) and node.name == func_name), None)

        if func_node:
            func_code = ast.get_source_segment(code, func_node)

            # Get the lines surrounding the function definition to add more context
            start_line = func_node.lineno - 1  # Line numbers are 1-indexed
            end_line = start_line + len(func_code.splitlines())

            # Include some context from the surrounding code (e.g., imports, class definitions)
            surrounding_code = "\n".join(code.splitlines()[max(0, start_line - 5):min(end_line + 5, len(code.splitlines()))])

            # Include the full context for the AI model to understand why the function is "dead code"
            full_context = f"""
### Task: Explain why this function is considered dead code in the following script.
Here is the code where this function is defined and not used:

{surrounding_code}

The function is not called anywhere else in the script. Please provide a detailed explanation of why it is considered dead code and how it can be removed or refactored.

Function code:
{func_code}

Explanation:
"""
            # Pass the full context to the AI explainer
            explanation = explainer.explain_dead_code(full_context)
            print(f"\n🤖 Why is function '{func_name}' considered dead code?\n{explanation}\n")
        else:
            print(f"❗ Function {func_name} not found in the code!")

    # Only remove dead code if the user didn't opt for explain-only mode
    if not args.explain_only:
        # ✂️ Remove dead code
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
    else:
        print("🧹 Explanations completed. No code has been removed.")

if __name__ == "__main__":
    main()
