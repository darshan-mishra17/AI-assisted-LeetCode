"""
Fix all Pydantic Config classes to use v2 format
"""

import re

def fix_pydantic_config():
    file_path = "c:/Users/HP/OneDrive/Desktop/CodeForge/Backend/app/models/models.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old Config class with new model_config
    pattern = r'    class Config:\s+populate_by_name = True\s+json_encoders = \{ObjectId: str\}'
    replacement = '    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)'
    
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed Pydantic Config classes")

if __name__ == "__main__":
    fix_pydantic_config()
