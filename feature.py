from __init__ import db, Word, User, Student, Y200004, Y200042, Y200051, Y200062, Y200065, Y200078, Y200080, Y200089, Y200090, record
import random, collections
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, func

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

def check_movepoint(Record):
    # 現在ログイン中のユーザーのIDと合致するusersテーブルのデータを単一取得
    users_data = User.query.filter_by(id=current_user.id).first()

    if not current_user.role == 'Student':
        # “復習待ち”と合致するy2000*テーブルのデータを全取得
        records = Record.query.filter_by(word_state='review_state').all()
    else:
        # 現在ログイン中のユーザーIDかつ“復習待ち”と合致するstudentsテーブルのデータを全取得
        records = Record.query.filter_by(user_id=current_user.id, word_state='review_state').all()

    if not records == []:
        # 重複しないy2000*テーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # 同一の英単語IDを持つ複数のレコードの中から、idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 同一の英単語IDを持つ複数のレコードの中から、現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

            # max_orderと合致するy2000* or studentsテーブルのデータを単一取得
            records_data = Record.query.get(max_order)
            if records_data.constant_test_correct >= (users_data.total_remembered + 50 * records_data.constant_test_correct ** 2):
                # “復習待ち”から“テスト待ち”へ更新
                records_data.word_state = 'test_state'
        
        # データベースを更新する
        db.session.commit()

def quiz_candidate(rank, Record):
    # rnakと合致するwordsテーブルのデータを全取得
    words_datas = Word.query.filter_by(rank=rank).all()

    if not current_user.role == 'Student':
        # rankかつ“テスト待ち”または“復習待ち”と合致するy2000*テーブルのデータを全取得
        records = Record.query.filter_by(rank=rank).filter(or_(Record.word_state=='test_state', Record.word_state=='review_state')).all()
    else:
        # 現在ログイン中のユーザーIDかつrankかつ“テスト待ち”または“復習待ち”と合致するstudentsテーブルのデータを全取得
        records = Record.query.filter_by(user_id=current_user.id, rank=rank).filter(or_(Record.word_state=='test_state', Record.word_state=='review_state')).all()

    records_datas = []
    if not records == []:
        # 重複しないy2000* or studentsテーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        # 同一の英単語IDを持つ複数のレコードの中から最新のデータを取得
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

            # max_orderと合致するy2000* or studentsテーブルのデータを単一取得
            records_datas.append(Record.query.get(max_order))
    
    params = []
    for i in range(len(words_datas)):
        check = 0
        # “テスト待ち”または“復習待ち”状態の英単語を除外
        for j in range(len(records_datas)):
            if words_datas[i].id == records_datas[j].word_id:
                check = 1
                break            
        if check == 1:
            continue

        params.append({
            'ID': words_datas[i].id,
            'word': words_datas[i].word,
            'translation': words_datas[i].translation,
            'part_en': words_datas[i].part_en,
            'part_jp': words_datas[i].part_jp,
            'rank': words_datas[i].rank,
            'freq_rank': words_datas[i].freq_rank,
            'response': words_datas[i].response,
            'correct': words_datas[i].correct
        })
    return params

def test_candidate(rank, Record):
    if not current_user.role == 'Student':
        # rankかつ“テスト待ち”と合致するy2000*テーブルのデータを全取得
        records = Record.query.filter_by(rank=rank, word_state='test_state').all()
    else:
        # 現在ログイン中のユーザーIDかつrankかつ“テスト待ち”と合致するstudentsテーブルのデータを全取得
        records = Record.query.filter_by(user_id=current_user.id, rank=rank, word_state='test_state').all()

    # 重複しないy2000* or studentsテーブルの英単語IDを取得
    word_id_list = list(map(lambda x: x.word_id, records))
    dedupe_keys = list(collections.Counter(word_id_list).keys())

    params = []
    for id in dedupe_keys:
        if not current_user.role == 'Student':
            # 同一の英単語IDを持つ複数のレコードの中から、idと合致するy2000*テーブルの最新のorderを取得
            max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
        else:
            # 同一の英単語IDを持つ複数のレコードの中から、現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
            max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

        # max_orderと合致するy2000* or studentsテーブルのデータを単一取得
        records_data = Record.query.get(max_order)
        # 上で取得した英単語IDと合致するwordsテーブルのデータを単一取得
        words_data = Word.query.filter_by(id=records_data.word_id).first()

        params.append({
            'ID': words_data.id,
            'word': words_data.word,
            'translation': words_data.translation,
            'part_en': words_data.part_en,
            'part_jp': words_data.part_jp,
            'rank': words_data.rank,
            'freq_rank': words_data.freq_rank,
            'response': words_data.response,
            'correct': words_data.correct
        })
    return params

def all_words():
   # wordsテーブルのデータを全取得
    datas = Word.query.all()

    params = []
    for i in range(len(datas)):
        params.append({
            'word_id': datas[i].id,
            'word': datas[i].word,
            'translation': datas[i].translation,
            'part_en': datas[i].part_en,
            'part_jp': datas[i].part_jp,
            'rank': datas[i].rank,
            'response': datas[i].response,
            'correct': datas[i].correct,
            'freq_rank': datas[i].freq_rank
        })

    return params

# Create Questions API
@feature.route('/create-questions/<category>/<rank>')
@login_required
def create_questions(category, rank):
    # 問題として出題する英単語IDを格納する配列
    learningList = []

    Record = record(current_user.id)

    # クイズリクエスト時の処理
    if category == 'quiz':
        # クイズに出題する候補の英単語データを取得
        fp = quiz_candidate(rank, Record)        
        random.shuffle(fp)

        Qcount = 10    # 問題数
        j = 0
        while True:
            l = random.randrange(len(fp))
            i = random.randrange(1,1500)
            x = int(fp[l]["freq_rank"])
            threshold = 1000 * (0.5) ** (x / 1000) + 500    # 重み付け部分
            if threshold >= i:
                # クイズに出題する英単語IDの配列番号（行数）を記憶
                learningList.append(l)
                j+=1
            else:
                continue
            if j >= Qcount:
                break
    
    # テストリクエスト時の処理
    if category == 'test':
        # “復習待ち”状態の英単語を“テスト待ち”へ更新する条件を満たしているかの判定を行う
        check_movepoint(Record)
        
        # テストに出題する候補の英単語データを取得
        fp = test_candidate(rank, Record)
        
        Qcount = 20    # 問題数
        for q in range(Qcount):
            # テストに出題する英単語IDの配列番号（行数）を記憶
            learningList.append(q)

    # 誤答選択肢用の英単語データを取得
    op = all_words()
    linecount = len(op)         #データファイルの行数をカウント

    obj = [] #出力用リスト
    for _ in range(Qcount):
        QuestionLine = [] #出題用の問題保存リスト    

        # fp(辞書)のa要素目の値をリストとして取得
        ansline = list(fp[learningList[_]].values())

        #出題用の問題保存リストにアペンド
        QuestionLine.append(ansline)

        # 誤答選択肢用のリストを用意
        wrongline = []

        i = 0
        while i < 3:
            a = random.randrange(1, linecount)
            # fp(辞書)のa要素目の値をリストとして取得
            imp = list(op[a].values())

            #品詞が正答と違ったら60%の確率でやり直し
            if partcompare(imp[3], ansline[3]) == 0:
                if random.randrange(1,100) <= 60:
                    continue

            #impに読み込んだデータをwronglineにアペンド
            wrongline.append(imp)
            #出題用の問題保存リストにアペンド
            QuestionLine.append(wrongline[i])

            i += 1

        random.shuffle(QuestionLine) #問題のシャッフル

        opt = []
        for i in range(4):
            #optに日本語訳の選択肢をアペンド
            opt.append(QuestionLine[i][2])

        obj.append({
            "ID": ansline[0], 
            "word": f"{ansline[1]}", 
            "options": [f"{opt[0]}", f"{opt[1]}", f"{opt[2]}", f"{opt[3]}"], 
            "answer": f"{ansline[2]}",
            "correct": ansline[8], 
            "response": ansline[7]
        })

    return jsonify(obj)
