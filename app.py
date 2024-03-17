# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, Markup
import numpy as np
import pandas as pd
import joblib
# 予測モデルの読み込み
price = joblib.load('data/lunch3.pkl')

app = Flask(__name__)
# Routing
@app.route('/')
def index():
    return render_template('index3_1.html')

@app.route('/yosoku', methods=['POST'])
def yosoku():
    try:
        if request.method == 'POST':
            x1 = int(request.form['x1'])
            x2 = int(request.form['x2'])
            x3 = int(request.form['x3'])
            x4 = int(request.form['x4'])

            # dummy用表示
            week = [0,0,0,0,0,0]
            weat = [0,0,0,0,0,0]
            week[x3] = 1
            weat[x1] = 1

            # DataFrame用
            df = pd.DataFrame([[x2,x4,week[1],week[2],week[3],week[4],week[5],weat[1],weat[2],weat[3],weat[4],weat[5]]],
                columns=['temperature','remarks','week_月','week_木','week_水','week_火','week_金','weather_快晴','weather_晴れ','weather_曇','weather_薄曇','weather_雨'],
                index=['1'])
            
            # 予測
            yoso = int(price.predict(df)[0])
           
            # リスト表示処理           
            x1_moji = {1:"快晴", 2:"晴れ", 3:"曇", 4:"薄曇", 5:"雨"}
            if x1 in x1_moji:
                xx1 = x1_moji[x1]
            else:
                xx1 = x1
            
            x3_moji = {1:"月曜日", 2:"火曜日", 3:"水曜日", 4:"木曜日", 5:"金曜日"}
            if x3 in x3_moji:
                xx3 = x3_moji[x3]
            else:
                xx1 = x3
            
            x4_moji = {0:"その他", 1:"お楽しみメニュー"}
            if x4 in x4_moji:
                xx4 = x4_moji[x4]
            else:
                xx4 = x4

            #結果のHTML書き出し
            return render_template('index3_2.html',
                x1=xx1, x2=x2, x3=xx3, x4=xx4, yoso=yoso)
        else:
            return redirect(url_for('index'))
    except Exception as e:
        return str(e)

# if __name__ == '__main__':
#    app.run('0.0.0.0', 5500, debug=True)
