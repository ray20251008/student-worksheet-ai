import json
import re
import os

base_dir = 'C:/Users/acer/.gemini/antigravity/scratch/student-worksheet-ai'
hw_file = os.path.join(base_dir, 'homework_01/homework_01.html')
demo_file = os.path.join(base_dir, 'worksheet_demo.html')

# 1. Get 40 chars from worksheet_demo.html
with open(demo_file, 'r', encoding='utf-8') as f:
    demo_content = f.read()

match = re.search(r'const charsData = (\[.*?\]);', demo_content)
if match:
    data = json.loads(match.group(1))
    # remove 'z' and take 40
    data = [{k:v for k,v in item.items() if k != 'z'} for item in data[:40]]
    new_data_str = json.dumps(data, ensure_ascii=False)

# 2. Update homework_01.html
with open(hw_file, 'r', encoding='utf-8') as f:
    hw_content = f.read()

# Update title
hw_content = hw_content.replace('生字簿甲乙本練習 (共20字)', '生字簿甲乙本練習 (共40字)')
hw_content = hw_content.replace('數學練習：混合算術 (共20題)', '數學練習：混合算術 (共30題)')

# Replace charsData
hw_content = re.sub(r'const charsData = \[.*?\];', f'const charsData = {new_data_str};', hw_content)

# Add 10 math questions
new_math = """    <div class="m-card"><div class="m-q">21. 300 × 5 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">22. 2500 ÷ 5 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">23. 450 + 150 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">24. 820 - 320 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">25. 150 × 4 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">26. 80 × 50 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">27. 480 ÷ 4 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">28. 600 - (150 + 200) = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">29. 180 + 320 - 100 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">30. 1000 ÷ 8 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>"""

hw_content = hw_content.replace('</div>\n\n  <div class="answer-key">', f'{new_math}\n  </div>\n\n  <div class="answer-key">')

# Add 10 answers
new_answers = """      <li>1500</li>
      <li>500</li>
      <li>600</li>
      <li>500</li>
      <li>600</li>
      <li>4000</li>
      <li>120</li>
      <li>250</li>
      <li>400</li>
      <li>125</li>"""

hw_content = hw_content.replace('</ol>', f'{new_answers}\n    </ol>')

with open(hw_file, 'w', encoding='utf-8') as f:
    f.write(hw_content)
print("Success")
