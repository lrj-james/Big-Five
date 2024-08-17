import sqlite3
from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio
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
def make_qlist(traits):
    
    import random
    qlist = []
    
    # 取出字典中的人格縮寫，與題號共同組成4位編號
    for trait in traits:  
        randlist = random.sample(range(1, 51), 5)
        for num in randlist:
            item = trait + "0" + str(num) if num <= 9 else trait + str(num)
            qlist.append(item)
            
    random.shuffle(qlist)  
    return qlist  


# 生成雷達圖
def generate_radar_chart(traits):
    
    categories = [
        '開放性 (Openness)', 
        '盡責性 (Conscientiousness)', 
        '外向性 (Extraversion)', 
        '親和性 (Agreeableness)', 
        '神經質 (Neuroticism)'
    ]
    categories = [*categories, categories[0]]

    user_results = [traits['op'], traits['cs'], traits['ex'], traits['ag'], traits['nu']]
    user_results = [min(max(value, -5), 5) for value in user_results]
    user_results = [*user_results, user_results[0]]

    fig = go.Figure(
        data = [
            go.Scatterpolar(r=user_results, theta=categories, fill='toself', name='User Results'),
        ],
        layout = go.Layout(
            title = go.layout.Title(text='五大性格中的占比'),
            polar = {'radialaxis': {'range': [-5, 5], 'visible': True}},
            showlegend = True,
            font = dict(
                family = "SimHei, Arial",
                size = 14
            )
        )
    )

    # 將圖片保存為 BytesIO 對象
    img_buffer = BytesIO()
    pio.write_image(fig, img_buffer, format='png')
    img_buffer.seek(0)

    # 將圖片轉換為 Base64 字串
    img_str = base64.b64encode(img_buffer.read()).decode('utf-8')

    return img_str

 
@app.route("/", methods=['GET', 'POST'])
def index():
    
    global questions
    
    if request.method == "GET":
    
        # 歸零變數
        for trait in traits:
            traits[trait] = 0

        # 隨機挑選題目
        global qlist
        qlist = make_qlist(traits)  
        
        # 匯入題庫
        con = sqlite3.connect("questions.db")
        cur = con.cursor()
        
        rows = []
        for index_code in qlist:
            rows.append(cur.execute(
                'SELECT index_code, question, score FROM questions WHERE index_code = (?)', (index_code,)
            ).fetchone())
        
        con.close()
        
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

        return render_template("index.html", questions=questions)
    
    # 傳送表單則計算測驗結果
    else:
        
        for i in range(1, 26):
            questions[i-1]['choice'] = (request.form.get('q' + str(i) + '_choice'))
            
        for row in questions:
            if (
                row['score'] == '+' and row['choice'] == 'y'
            ) or (
                row['score'] == '-' and row['choice'] == 'n'
                
            ):
                traits[row['index_code'][:2]] += 1
            else:
                traits[row['index_code'][:2]] -= 1
                
        src = generate_radar_chart(traits)
        
        return render_template('result.html', traits=traits, src=src)
    