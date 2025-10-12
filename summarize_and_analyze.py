import os
import ast
import json

def analyze_code(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
        tree = ast.parse(code)

    analysis = {
        'imports': [],
        'functions': [],
        'classes': [],
        'variables': []
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                analysis['imports'].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            analysis['imports'].append(node.module)
        elif isinstance(node, ast.FunctionDef):
            analysis['functions'].append(node.name)
        elif isinstance(node, ast.ClassDef):
            analysis['classes'].append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    analysis['variables'].append(target.id)

    return analysis

def summarize_directory(directory):
    summary = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                summary[filepath] = analyze_code(filepath)
    return summary

if __name__ == '__main__':
    src_summary = summarize_directory('src/provide/foundation')
    with open('src_summary.json', 'w') as f:
        json.dump(src_summary, f, indent=4)

    docs_summary = summarize_directory('docs')
    with open('docs_summary.json', 'w') as f:
        json.dump(docs_summary, f, indent=4)

    print("Summaries generated: src_summary.json, docs_summary.json")