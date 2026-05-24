import re
import json

html_file = 'C:/Users/acer/.gemini/antigravity/scratch/student-worksheet-ai/worksheet_01.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the title
content = content.replace('生字簿甲乙本練習 (共50字)', '生字簿甲乙本練習 (共20字)')

# Find charsData array and truncate it
match = re.search(r'const charsData = (\[.*?\]);', content)
if match:
    data_str = match.group(1)
    data = json.loads(data_str)
    # keep only first 20
    data = data[:20]
    new_data_str = json.dumps(data, ensure_ascii=False)
    content = content.replace(f'const charsData = {data_str};', f'const charsData = {new_data_str};')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
