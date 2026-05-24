import json
import re
import os
import subprocess

base_dir = 'C:/Users/acer/.gemini/antigravity/scratch/student-worksheet-ai'
hw_file = os.path.join(base_dir, 'homework_01/homework_01.html')

# Get the original 50 chars from commit 4ccb520
old_content = subprocess.check_output(['git', 'show', '4ccb520:worksheet_01.html'], cwd=base_dir, text=True, encoding='utf-8')

match = re.search(r'const charsData = (\[.*?\]);', old_content)
if match:
    data = json.loads(match.group(1))
    # slice the first 40
    data = data[:40]
    new_data_str = json.dumps(data, ensure_ascii=False)

# Update homework_01.html
with open(hw_file, 'r', encoding='utf-8') as f:
    hw_content = f.read()

hw_content = re.sub(r'const charsData = \[.*?\];', f'const charsData = {new_data_str};', hw_content)

with open(hw_file, 'w', encoding='utf-8') as f:
    f.write(hw_content)

print("Successfully updated with 40 characters")
