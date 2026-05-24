import re

html_file = 'C:/Users/acer/.gemini/antigravity/scratch/student-worksheet-ai/worksheet_demo.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS for Tianzige and Answer Key
css_to_add = '''
  /* Tianzige */
  .v-char-section { display: flex; padding: 10px; border-right: 2px solid #c8e6c9; align-items: center; }
  .tianzi { width: 50px; height: 50px; border: 1px solid #2D6A4F; position: relative; display: inline-block; margin-right: 5px; }
  .tianzi::before, .tianzi::after { content: ''; position: absolute; border: 1px dashed #c8e6c9; }
  .tianzi::before { top: 50%; left: 0; right: 0; transform: translateY(-50%); }
  .tianzi::after { left: 50%; top: 0; bottom: 0; transform: translateX(-50%); }
  .tianzi span { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; font-family: 'Kaiti', 'DFKai-sb', serif; font-size: 35px; color: #ccc; z-index: 1; }
  
  .answer-key { margin-top: 40px; padding: 20px; background: #fdf5e6; border: 1px dashed #d4a373; border-radius: 8px; }
  .answer-key h2 { color: #d4a373; margin-top: 0; }
  @media print { .answer-key { display: none; } } /* Hide answers when printing */
'''
content = content.replace('/* Math */', css_to_add + '\n  /* Math */')

# 2. Modify Vocab Cards
def replace_card(match):
    char = match.group(1)
    info = match.group(2)
    new_char = f'<div class="v-char-section"><div class="tianzi"><span>{char}</span></div><div class="tianzi"></div><div class="tianzi"></div></div>'
    return f'<div class="v-card">{new_char}<div class="v-info">{info}</div></div>'

content = re.sub(r'<div class="v-card"><div class="v-char">(.*?)</div><div class="v-info">(.*?)</div></div>', replace_card, content)

# 3. Add Math Answers
math_answers = [
    "350 × 0.8 = 280, 280 - 50 = 230",
    "300 × 2 = 600, 600 - 450 = 150",
    "1200 ÷ 2 = 600",
    "50 × 4 = 200",
    "500 - 125 - 175 = 200",
    "800 - 600 = 200",
    "20 + 50 + 0 + 30 = 100",
    "210 × 4 = 840, 840 - 50 = 790",
    "250 - 100 = 150, 150 ÷ 50 = 3",
    "600 ÷ 3 = 200",
    "120 + 130 = 250, 500 - 250 = 250",
    "890 - 650 = 240",
    "1500 ÷ 3 = 500",
    "64 - 2 - 15 = 47",
    "5 × 3 = 15",
    "15 × 30 = 450",
    "280 - (20 × 3) = 220",
    "50 - 20 + 100 = 130",
    "20 × 15 = 300",
    "250 + 600 = 850, 900 - 850 = 50 (不夠，相差50元)"
]

answers_html = '<div class="answer-key"><h2>🔑 數學解答區 (列印時會自動隱藏)</h2><ol>'
for ans in math_answers:
    answers_html += f'<li>{ans}</li>'
answers_html += '</ol></div>'

content = content.replace('</body>', answers_html + '\n</body>')

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
