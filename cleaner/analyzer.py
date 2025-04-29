import ast

class DeadCodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.defined_funcs = set()
        self.called_funcs = set()
        self.imports = set()
        self.used_names = set()

    def visit_FunctionDef(self, node):
        self.defined_funcs.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.called_funcs.add(node.func.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

def analyze_code(source_code):
    tree = ast.parse(source_code)
    analyzer = DeadCodeAnalyzer()
    analyzer.visit(tree)

    unused_funcs = analyzer.defined_funcs - analyzer.called_funcs
    unused_imports = analyzer.imports - analyzer.used_names

    return {
        "unused_funcs": unused_funcs,
        "unused_imports": unused_imports,
    }
