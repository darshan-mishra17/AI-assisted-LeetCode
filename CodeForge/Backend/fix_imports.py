"""
Fix import statements in all Python files to use relative imports
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace app.* imports with relative imports
        patterns = [
            (r'from app\.models\.models import', 'from models.models import'),
            (r'from app\.schemas\.schemas import', 'from schemas.schemas import'),
            (r'from app\.auth\.auth import', 'from auth.auth import'),
            (r'from app\.database import', 'from database import'),
            (r'from app\.utils\.helpers import', 'from utils.helpers import'),
            (r'from app\.routes import', 'from routes import'),
        ]
        
        for old_pattern, new_pattern in patterns:
            content = re.sub(old_pattern, new_pattern, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    """Fix imports in all Python files in the app directory"""
    app_dir = Path("c:/Users/HP/OneDrive/Desktop/CodeForge/Backend/app")
    
    if not app_dir.exists():
        print("App directory not found!")
        return
    
    python_files = list(app_dir.rglob("*.py"))
    
    for py_file in python_files:
        fix_imports_in_file(py_file)
    
    print(f"\nProcessed {len(python_files)} Python files")

if __name__ == "__main__":
    main()
