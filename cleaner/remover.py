import ast
import astor

class DeadCodeRemover(ast.NodeTransformer):
    def __init__(self, unused_funcs, unused_imports):
        self.unused_funcs = unused_funcs
        self.unused_imports = unused_imports

    def visit_FunctionDef(self, node):
        if node.name in self.unused_funcs:
            return None  # Remove the function
        return self.generic_visit(node)

    def visit_Import(self, node):
        node.names = [n for n in node.names if (n.asname or n.name) not in self.unused_imports]
        return node if node.names else None

def remove_dead_code(source_code, analysis):
    tree = ast.parse(source_code)
    cleaner = DeadCodeRemover(
        analysis["unused_funcs"],
        analysis["unused_imports"]
    )
    cleaned_tree = cleaner.visit(tree)
    return astor.to_source(cleaned_tree)
