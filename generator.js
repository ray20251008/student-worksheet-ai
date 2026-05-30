document.addEventListener('DOMContentLoaded', () => {
  const apiKeyInput = document.getElementById('apiKey');
  const articleTextInput = document.getElementById('articleText');
  const generateBtn = document.getElementById('generateBtn');
  const loader = document.getElementById('loader');
  const statusMsg = document.getElementById('statusMsg');
  const worksheetContainer = document.getElementById('worksheetContainer');
  
  // 讀取儲存的 API Key
  const savedKey = localStorage.getItem('gemini_api_key');
  if (savedKey) {
    apiKeyInput.value = savedKey;
  }

  generateBtn.addEventListener('click', async () => {
    const apiKey = apiKeyInput.value.trim();
    const article = articleTextInput.value.trim();

    if (!apiKey) {
      statusMsg.textContent = '請輸入 Gemini API Key！';
      return;
    }
    if (!article) {
      statusMsg.textContent = '請輸入文章內容！';
      return;
    }

    // 儲存 API Key
    localStorage.setItem('gemini_api_key', apiKey);

    // 更新 UI 狀態
    generateBtn.disabled = true;
    loader.style.display = 'inline-block';
    statusMsg.style.color = '#2D6A4F';
    statusMsg.textContent = '正在請 AI 產生學習單，請稍候 (約需 10-20 秒)...';
    worksheetContainer.style.display = 'none';

    try {
      const data = await fetchWorksheetData(apiKey, article);
      renderWorksheet(data, article);
      
      statusMsg.textContent = '✨ 學習單產生成功！';
      worksheetContainer.style.display = 'block';
      // 滾動到學習單區域
      worksheetContainer.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
      console.error(err);
      statusMsg.style.color = '#b74b4b';
      statusMsg.textContent = '發生錯誤：' + err.message;
    } finally {
      generateBtn.disabled = false;
      loader.style.display = 'none';
    }
  });
});

async function fetchWorksheetData(apiKey, article) {
  const prompt = `
你是一位專業的國小國語與數學老師。我將給你一篇短文，請根據這篇短文，為學生設計一份學習單。
請輸出嚴格的 JSON 格式，不要包含任何其他說明文字或 Markdown 標記 (\`\`\`json 等)。

需包含以下欄位：
1. "title": 根據文章內容產生一個合適的標題 (例如 "每週學習單：存錢大作戰")
2. "reading_questions": 3 題閱讀測驗題目 (Array of strings)
3. "reading_answers": 閱讀測驗的解答 (Array of strings)
4. "vocab": 從文章中挑選 10 到 20 個適合國小學生的生字。每個生字需要是一個物件，包含：
   - "c": 生字本身 (一個字)
   - "z": 該生字的注音符號 (例如 "ㄐㄧㄣˋ")
   - "r": 部首 (例如 "辵")
   - "s": 總筆畫數 (字串格式，例如 "8")
5. "math_questions": 根據文章情境，設計 5 到 10 題適合國小程度的數學應用題 (Array of strings)
6. "math_answers": 數學題的算式與解答 (Array of strings)

文章內容如下：
${article}
`;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseMimeType: "application/json"
      }
    })
  });

  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.error?.message || 'API 請求失敗');
  }

  const result = await response.json();
  let text = result.candidates[0].content.parts[0].text;
  
  // 移除 markdown 代碼區塊標記
  text = text.replace(/^```json/i, '').replace(/```$/i, '').trim();
  
  return JSON.parse(text);
}

function renderWorksheet(data, article) {
  // 1. 標題與文章
  document.getElementById('wsTitle').textContent = data.title;
  // 將換行符號轉為 <br>
  document.getElementById('wsArticle').innerHTML = article.replace(/\n/g, '<br>');

  // 2. 閱讀測驗
  const readingContainer = document.getElementById('wsReading');
  readingContainer.innerHTML = '';
  data.reading_questions.forEach((q, i) => {
    const li = document.createElement('li');
    li.innerHTML = `${i + 1}. ${q}<br><input type="text">`;
    readingContainer.appendChild(li);
  });

  // 3. 生字簿
  const vocabContainer = document.getElementById('vocab-container');
  vocabContainer.innerHTML = '';
  
  data.vocab.forEach((d, i) => {
    const col = document.createElement('div');
    col.className = 'v-col';

    // 訂正區
    col.innerHTML += `<div class="v-box box-empty"><div class="box-title">訂正</div></div>`;
    
    // 生字與注音
    col.innerHTML += `<div class="v-box box-char">
      <div class="ruby-text">
        <span>${d.c}</span>
        <div class="zhuyin">${d.z}</div>
      </div>
    </div>`;

    // 部首筆畫
    col.innerHTML += `<div class="v-box box-meta">部首：${d.r}<br>筆畫：${d.s}</div>`;

    // 造詞空白區
    col.innerHTML += `<div class="v-box box-word">
      <div class="word-label">造詞</div>
      <div class="word-line"></div>
    </div>`;

    // 田字格 (1 個描寫 + 3 個空白)
    for(let j=0; j<4; j++) {
      const tianzi = document.createElement('div');
      tianzi.className = 'v-box tianzi';
      
      if (j === 0) {
        // 第一個格子放 Hanzi Writer 描寫字
        const hwTarget = document.createElement('div');
        hwTarget.className = 'hw-target';
        hwTarget.id = `hw-${i}`;
        tianzi.appendChild(hwTarget);
        col.appendChild(tianzi);
        
        // 初始化 Hanzi Writer
        setTimeout(() => {
          try {
            HanziWriter.create(`hw-${i}`, d.c, {
              width: 55,
              height: 55,
              padding: 5,
              strokeColor: '#ffb3b3', // 粉紅色示範字
              showOutline: false
            });
          } catch(e) { console.error("HanziWriter Error:", e); }
        }, 300);
      } else {
        col.appendChild(tianzi);
      }
    }
    vocabContainer.appendChild(col);
  });

  // 4. 數學題
  const mathContainer = document.getElementById('wsMath');
  mathContainer.innerHTML = '';
  data.math_questions.forEach((q, i) => {
    const card = document.createElement('div');
    card.className = 'm-card';
    card.innerHTML = `
      <div class="m-q">${i + 1}. ${q}</div>
      <div class="m-ans">算式：<span></span> = <span></span></div>
    `;
    mathContainer.appendChild(card);
  });

  // 5. 解答區
  const answersContainer = document.getElementById('wsAnswers');
  answersContainer.innerHTML = '';
  
  // 閱讀測驗解答
  const rTitle = document.createElement('h3');
  rTitle.style.color = '#d4a373';
  rTitle.textContent = '【閱讀測驗解答】';
  answersContainer.appendChild(rTitle);
  
  const rOl = document.createElement('ol');
  data.reading_answers.forEach((ans) => {
    const li = document.createElement('li');
    li.textContent = ans;
    rOl.appendChild(li);
  });
  answersContainer.appendChild(rOl);

  // 數學解答
  const mTitle = document.createElement('h3');
  mTitle.style.color = '#d4a373';
  mTitle.textContent = '【數學解答】';
  answersContainer.appendChild(mTitle);
  
  const mOl = document.createElement('ol');
  data.math_answers.forEach((ans) => {
    const li = document.createElement('li');
    li.textContent = ans;
    mOl.appendChild(li);
  });
  answersContainer.appendChild(mOl);
}
