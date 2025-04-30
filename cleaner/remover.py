import ast
import astor

class DeadCodeRemover(ast.NodeTransformer):
    def __init__(self, unused_funcs, unused_imports, source_code=None, interactive=False):
        self.unused_funcs = set(unused_funcs)
        self.unused_imports = set(unused_imports)
        self.source_code = source_code
        self.interactive = interactive

    def visit_FunctionDef(self, node):
        if node.name in self.unused_funcs:
            if self.interactive and self.source_code:
                func_code = ast.get_source_segment(self.source_code, node)
                ans = input(f"\n🗑️ Delete unused function '{node.name}'?\n{func_code}\n[y/N] ").strip().lower()
                if ans != "y":
                    return node  # skip deletion
            return None  # delete this node
        return self.generic_visit(node)

    def visit_Import(self, node):
        if self.interactive:
            keep_names = []
            for alias in node.names:
                if alias.name not in self.unused_imports:
                    keep_names.append(alias)
                else:
                    ans = input(f"🗑️ Delete unused import '{alias.name}'? [y/N] ").strip().lower()
                    if ans != "y":
                        keep_names.append(alias)
            if keep_names:
                node.names = keep_names
                return node
            return None
        else:
            node.names = [alias for alias in node.names if alias.name not in self.unused_imports]
            return node if node.names else None

    def visit_ImportFrom(self, node):
        # Same as visit_Import — for `from x import y` style
        if self.interactive:
            keep_names = []
            for alias in node.names:
                full_name = f"{node.module}.{alias.name}" if node.module else alias.name
                if full_name not in self.unused_imports:
                    keep_names.append(alias)
                else:
                    ans = input(f"🗑️ Delete unused import '{full_name}'? [y/N] ").strip().lower()
                    if ans != "y":
                        keep_names.append(alias)
            if keep_names:
                node.names = keep_names
                return node
            return None
        else:
            node.names = [
                alias for alias in node.names
                if f"{node.module}.{alias.name}" not in self.unused_imports
            ]
            return node if node.names else None


def remove_dead_code(source_code, analysis, interactive=False):
    tree = ast.parse(source_code)
    cleaner = DeadCodeRemover(
        analysis["unused_funcs"],
        analysis["unused_imports"],
        source_code=source_code,
        interactive=interactive
    )
    cleaned_tree = cleaner.visit(tree)
    return astor.to_source(cleaned_tree)

