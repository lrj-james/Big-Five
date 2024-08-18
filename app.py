from flask import Flask, render_template, request
import sqlite3
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import base64
from io import BytesIO


app = Flask(__name__)


# 公域變數
traits = {
    "op": 0,  # openness
    "cs": 0,  # conscientiousness
    "ex": 0,  # extraversion
    "ag": 0,  # agreeableness
    "nu": 0   # neuroticism
}


# 製作題目列表，共25題隨機排列
def make_qlist():
    
    qlist = []
    
    # 取出字典中的人格縮寫，與題號共同組成4位編號
    for trait in traits:  
        randlist = random.sample(range(1, 51), 5)
        for num in randlist:
            item = trait + "0" + str(num) if num <= 9 else trait + str(num)
            qlist.append(item)
            
    random.shuffle(qlist)  
    return qlist  


def generate_questions():

    qlist = make_qlist()  
    
    # 依據隨機的題目列表從資料庫匯入題庫
    con = sqlite3.connect("questions.db")
    cur = con.cursor()
    
    rows = []
    for index_code in qlist:
        rows.append(cur.execute(
            'SELECT index_code, question, score FROM questions WHERE index_code = (?)', (index_code,)
        ).fetchone())
    
    con.close()
    
    # 將題庫從串列型態轉為字典
    # count為題號
    # index_code 為題目的4位編號
    # questions為題目字串本身
    # score表示該題表示該人格的加分或減分
    global questions
    questions = []
    count = 1
    for row in rows:
        new_row = {}
        new_row['count'] = count
        new_row['index_code'] = row[0]
        new_row['question'] = row[1]
        new_row['score'] = row[2]
        questions.append(new_row)
        count += 1
        
    return questions


# 計算測驗結果
def calc_result():
    
    # 接收使用者的回答
    for i in range(1, 26):
        questions[i-1]['choice'] = (request.form.get('q' + str(i) + '_choice'))
        
    # 計分
    for row in questions:
        if (
            row['score'] == '+' and row['choice'] == 'y'
        ) or (
            row['score'] == '-' and row['choice'] == 'n'
            
        ):
            traits[row['index_code'][:2]] += 1
        else:
            traits[row['index_code'][:2]] -= 1


# 生成雷達圖
## TODO: 中文字型顯示錯誤
def generate_radar_chart():
    
    # 手動設置字型路徑
    font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'  # 替換為你的字型文件路徑
    font_prop = fm.FontProperties(fname=font_path)
    
    # 設置全局字型
    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
    # 解決負號顯示問題
    plt.rcParams['axes.unicode_minus'] = False  
    
    categories = [
        '開放性 (Openness)', 
        '盡責性 (Conscientiousness)', 
        '外向性 (Extraversion)', 
        '親和性 (Agreeableness)', 
        '神經質 (Neuroticism)'
    ]
    N = len(categories)
    
    user_results = [traits['op'], traits['cs'], traits['ex'], traits['ag'], traits['nu']]
    user_results = [min(max(value, -5), 5) for value in user_results]
    user_results += user_results[:1]  # 閉合多邊形

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)

    ax.plot(angles, user_results, linewidth=1, linestyle='solid')
    ax.fill(angles, user_results, 'b', alpha=0.1)

    # 將圖片保存為 BytesIO 對象
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    # 將圖片轉換為 Base64 字串
    src = base64.b64encode(img_buffer.read()).decode('utf-8')

    return src

 
@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == "GET":
    
        # 歸零人格特質變數
        for trait in traits:
            traits[trait] = 0

        questions = generate_questions()

        return render_template("index.html", questions=questions)
    
    # 傳送表單則計算測驗結果
    else:
        
        calc_result()
                
        src = generate_radar_chart()
        
        return render_template('result.html', traits=traits, src=src)
    