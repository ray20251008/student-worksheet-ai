import re

html_file = 'C:/Users/acer/.gemini/antigravity/scratch/student-worksheet-ai/worksheet_01.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Zhuyin
content = content.replace('<div class="zhuyin">${d.z}</div>', '')

# 2. Replace math section
new_math = '''<div class="math-grid">
    <div class="m-card"><div class="m-q">1. &nbsp;&nbsp; 350 × 8 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">2. &nbsp;&nbsp; 300 × 2 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">3. &nbsp;&nbsp; 1200 ÷ 2 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">4. &nbsp;&nbsp; 50 × 4 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">5. &nbsp;&nbsp; 500 - 125 - 175 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">6. &nbsp;&nbsp; 800 - 600 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">7. &nbsp;&nbsp; 20 + 50 + 30 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">8. &nbsp;&nbsp; 210 × 4 - 50 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">9. &nbsp;&nbsp; (250 - 100) ÷ 50 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">10. &nbsp; 600 ÷ 3 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">11. &nbsp; 500 - (120 + 130) = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">12. &nbsp; 890 - 650 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">13. &nbsp; 1500 ÷ 3 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">14. &nbsp; 64 - 2 - 15 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">15. &nbsp; 5 × 3 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">16. &nbsp; 15 × 30 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">17. &nbsp; 280 - (20 × 3) = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">18. &nbsp; 50 - 20 + 100 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">19. &nbsp; 20 × 15 = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
    <div class="m-card"><div class="m-q">20. &nbsp; 900 - (250 + 600) = ( &nbsp;&nbsp;&nbsp;&nbsp; )</div></div>
  </div>'''
content = re.sub(r'<div class="math-grid">.*?</div>', new_math, content, flags=re.DOTALL)

# 3. Replace answers
new_answers = '''<div class="answer-key">
    <h2>🔑 數學解答區 (列印時會自動隱藏)</h2>
    <ol>
      <li>2800</li>
      <li>600</li>
      <li>600</li>
      <li>200</li>
      <li>200</li>
      <li>200</li>
      <li>100</li>
      <li>790</li>
      <li>3</li>
      <li>200</li>
      <li>250</li>
      <li>240</li>
      <li>500</li>
      <li>47</li>
      <li>15</li>
      <li>450</li>
      <li>220</li>
      <li>130</li>
      <li>300</li>
      <li>50</li>
    </ol>
  </div>'''
content = re.sub(r'<div class="answer-key">.*?</div>', new_answers, content, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
