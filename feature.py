from __init__ import db, Word, User, Student, roles_required
import random, requests
from flask import Blueprint, jsonify, request
from flask_login import login_required

feature = Blueprint('create_quiz', __name__, url_prefix='/api')

def makeid(i,r,p):                                      # id作成関数
    id = ""
    id += rankdict[r]
    id += partdict[p]
    id += str(format(i,'05'))
    return id

def partcompare(ans, wrong):      # 品詞が同じかどうかの評価関数、〇〇-verb系は統一。同じなら1、違うなら0を返す
    if ans == wrong:
        return 1
    elif partdict[ans] == "00" or partdict[ans] == "08" or partdict[ans] == "11" or partdict[ans] == "13":
        if partdict[wrong] == "00" or partdict[wrong] == "08" or partdict[wrong] == "11" or partdict[wrong] == "13":
            return 1
        else:
            return 0
    else:
        return 0

rankdict = {'A1':"1", 'A2':"2", 'B1':"3", 'B2':"4"}
partdict ={'verb':"00",'noun':"01",'adjective':"02",'adverb':"03",'preposition':"04",'conjunction':"05",'determiner':"06",'pronoun':"07",'be-verb':"08",'modal auxiliary':"09",'interjection':"10",'do-verb':"11",'number':"12",'have-verb':"13",'infinitive-to':"14"}

# Create Quiz API
@feature.route('/create-quiz')
def create_quiz():
    rank = request.args.get('rank')
    url = f"http://127.0.0.1:8000/api/word/rank/{rank}"
    res = requests.get(url).json()                       # レスポンスをJSON形式に変換
    linecount = len(res)
    count = 10                                          # 出題数
    obj = []
    for _ in range(count):
        QuestionLine = []                               # 出題用の問題保存リスト
        a = random.randrange(1, linecount)              # 1~行数の乱数を生成
        ansline = list(res[a].values())                  # res(辞書)のa要素目の値をリストとして取得
        QuestionLine.append(ansline)                    # 出題用の問題保存リストにアペンド
        wrongline = []                                  # 誤答選択肢用のリストを用意
        i = 0
        while i < 3:                                    # 3回だけ
            a = random.randrange(1, linecount)
            imp = list(res[a].values())                  # res(辞書)のa要素目の値をリストとして取得
            wrongline.append(imp)                       # impに読み込んだデータをwronglineにアペンド
            QuestionLine.append(wrongline[i])           # 出題用の問題保存リストにアペンド
            i+=1                                        # ここまで来たらi+1してwhile続行
        random.shuffle(QuestionLine)                    # 問題のシャッフル
        opt = []
        for i in range(4):
            opt.append(QuestionLine[i][4])              # optに日本語訳の選択肢をアペンド
        # id = makeid(a,ansline[4],ansline[3])            # 正答の行数、ランク、品詞からidを作成
        obj.append({
            "ID": ansline[6], 
            "word": f"{ansline[5]}", 
            "option": [f"{opt[0]}", f"{opt[1]}", f"{opt[2]}", f"{opt[3]}"], 
            "answer": f"{ansline[4]}", 
            "correct": ansline[0], 
            "response": ansline[3]
        })
    return jsonify(obj)
