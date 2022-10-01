from __init__ import app, db, Word, User, roles_required
import random
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import or_

feature = Blueprint('create_quiz', __name__, url_prefix='/feature')

partToJP ={'verb':"動詞",'noun':"名詞",'adjective':"形容詞",'adverb':"副詞",'preposition':"前置詞",'conjunction':"接続詞",'determiner':"限定詞",'pronoun':"代名詞",'be-verb':"be動詞",'modal auxiliary':"修飾助動詞",'interjection':"間投詞",'do-verb':"do動詞",'number':"数",'have-verb':"have動詞",'infinitive-to':"不定詞to"}
# rankdict = {'A1':"1", 'A2':"2", 'B1':"3", 'B2':"4"}
partdict ={'verb':"00",'noun':"01",'adjective':"02",'adverb':"03",'preposition':"04",'conjunction':"05",'determiner':"06",'pronoun':"07",'be-verb':"08",'modal auxiliary':"09",'interjection':"10",'do-verb':"11",'number':"12",'have-verb':"13",'infinitive-to':"14"}

def partcompare(ans, wrong): #品詞が同じかどうかの評価関数、〇〇-verb系は統一。同じなら1、違うなら0を返す
    if ans == wrong:
        return 1
    elif partdict[ans] == "00" or partdict[ans] == "08" or partdict[ans] == "11" or partdict[ans] == "13":
        if partdict[wrong] == "00" or partdict[wrong] == "08" or partdict[wrong] == "11" or partdict[wrong] == "13":
            return 1
        else:
            return 0
    else:
        return 0

def check_period():
    users_data = User.query.filter_by(id=current_user.id).first()
    # 復習待ち英単語群を取得
    # records_datas = Record.query.filter_by(id=current_user.id, test_state='review').all()

    # for i in range(len(records_datas)):
    #     if records_datas[i].test_correct >= (users_data.total_remembered + 50 * records_datas[i].test_correct**2):
    #         print('\033[32m' + f'{records_datas[i].word_id}:{records_datas[i].test_state} -> active' + '\033[0m')    # 確認用
    #         # 復習待ちからテスト待ちへ
    #         records_datas[i].test_state = 'active'

def for_quiz(rank):
    params = []
    words_datas = Word.query.filter_by(rank=rank).all()
    # テスト待ち・復習待ち英単語を検索
    # records_datas = Record.query.filter(Record.user_id==current_user.id, Record.rank==rank).filter(or_(Record.test_state=='active', Record.test_state=='review')).all()
    # print('\033[32m' + f'{records_datas}' + '\033[0m')    # 確認用
    # for i in range(len(words_datas)):
    #     check = 0
    #     # テスト待ち・復習待ち英単語を避けて出力する
    #     for j in range(len(records_datas)):
    #         if words_datas[i].id == records_datas[j].word_id:
    #             check = 1
    #             break
    #     if check == 1:
    #         continue

    #     params.append({
    #         'ID': words_datas[i].id,
    #         'word': words_datas[i].word,
    #         'translation': words_datas[i].translation,
    #         'part_en': words_datas[i].part_en,
    #         'part_jp': words_datas[i].part_jp,
    #         'rank': words_datas[i].rank,
    #         'freq_rank': words_datas[i].freq_rank,
    #         'response': words_datas[i].response,
    #         'correct': words_datas[i].correct
    #     })
    # return params

# def for_test(rank):
#     params = []
#     # テスト待ち英単語を検索
#     records_datas = Record.query.filter_by(user_id=current_user.id, rank=rank, test_state='active').all()
#     # print('\033[32m' + f'{records_datas}' + '\033[0m')     # 確認用
#     for i in range(len(records_datas)):
#         words_data = Word.query.filter_by(id=records_datas[i].word_id).first()
#         # print('\033[34m' + f'{words_data}' + '\033[0m')    # 確認用
#         params.append({
#             'ID': words_data.id,
#             'word': words_data.word,
#             'translation': words_data.translation,
#             'part_en': words_data.part_en,
#             'part_jp': words_data.part_jp,
#             'rank': words_data.rank,
#             'freq_rank': words_data.freq_rank,
#             'response': words_data.response,
#             'correct': words_data.correct
#         })
#     return params

def all_words():
    params = []
    datas = Word.query.all()
    for i in range(len(datas)):
        params.append({
            'ID': datas[i].id,
            'word': datas[i].word,
            'translation': datas[i].translation,
            'part_en': datas[i].part_en,
            'part_jp': datas[i].part_jp,
            'rank': datas[i].rank,
            'freq_rank': datas[i].freq_rank,
            'response': datas[i].response,
            'correct': datas[i].correct
        })
    return params

# Create Questions API
@feature.route('/create-questions/<category>/<rank>')
@login_required
def create_questions(category, rank):       #問題を作成し、辞書型変数で返す

    check_period()

    learningList = []

    if category == 'quiz':
        fp = for_quiz(rank)
        # print('\033[31m' + f'{fp}' + '\033[0m')      # 確認用
        Qcount = 10 #問題数

        random.shuffle(fp)        

        ###learninglist.jsonに10単語追加するコード。重み調整済み。
        j = 0
        while True:
                l = random.randrange(len(fp))
                i = random.randrange(1,1500)
                x = int(fp[l]["freq_rank"])
                threshold = 1000 * (0.5) ** (x / 1000) + 500         # 重み付け部分
                if threshold >= i:
                    # learningList.append({"ID":fp[l]['ID']})

                    learningList.append(l)   # クイズに出題する英単語IDの配列番号を記憶
                    
                    # print(f"QUALIFIED >> rand:{i}, FreqRank:{fp[l]['freq_rank']}, Freqvalue:{threshold}")
                    j+=1
                else:
                    # print(f"CONTINUED >> rand:{i}, FreqRank:{fp[l]['freq_rank']}, Freqvalue:{threshold}")
                    continue
                if j >= Qcount:
                    break
    
    if category == 'test':
        # fp = for_test(rank)
        # print('\033[31m' + f'{fp}' + '\033[0m')      # 確認用
        Qcount = 20
        for q in range(Qcount):
            learningList.append(q)

    op = all_words()      # 誤答選択肢用の英単語データを取得
    linecount = len(op)         #データファイルの行数をカウント
    # print('\033[32m' + f'{linecount}' + '\033[0m')

    obj = [] #出力用リスト

    for _ in range(Qcount):
        QuestionLine = [] #出題用の問題保存リスト

        # while True:
        # a = int(learningList[_]["ID"])%10000-1  # 1~行数の乱数を生成        
        ansline = list(fp[learningList[_]].values()) # fp(辞書)のa要素目の値をリストとして取得

        # for b in range(6):
        #     ansline[b] = ansline[b].rstrip('\n') #読み込んだデータの余分な空白などを削除(以下クリーンアップ)

        QuestionLine.append(ansline) #出題用の問題保存リストにアペンド

        wrongline = []  # 誤答選択肢用のリストを用意
            # break

        i = 0
        while i < 3:  # 3回だけ
            a = random.randrange(1, linecount)
            imp = list(op[a].values()) # fp(辞書)のa要素目の値をリストとして取得

            # for j in range(6):
            #     imp[j] = imp[j].rstrip('\n') #読み込んだデータをクリーンアップ

            if partcompare(imp[3], ansline[3]) == 0: #品詞が正答と違ったら60%の確率でやり直し
                if random.randrange(1,100) <= 60:
                    #print("continued : parts")
                    continue

            wrongline.append(imp)  #impに読み込んだデータをwronglineにアペンド
            
            QuestionLine.append(wrongline[i]) #出題用の問題保存リストにアペンド

            i+=1 #ここまで来たらi+1してwhile続行

        random.shuffle(QuestionLine) #問題のシャッフル

        opt = []
        for i in range(4):
            opt.append(QuestionLine[i][2]) #optに日本語訳の選択肢をアペンド

        obj.append({
            "ID": ansline[0], 
            "word": f"{ansline[1]}", 
            "option": [f"{opt[0]}", f"{opt[1]}", f"{opt[2]}", f"{opt[3]}"], 
            "answer": f"{ansline[2]}",
            "correct": ansline[8], 
            "response": ansline[7]
        }) #出力内容をobjにアペンド

    return jsonify(obj)
    # return obj
