from __init__ import db, Word, User, Student, Y200004, Y200042, Y200051, Y200062, Y200065, Y200078, Y200080, Y200089, Y200090, roles_required, record
import pytz, os, shutil
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file, redirect, url_for
from flask_login import login_required, current_user
import pandas as pd

api_operator = Blueprint('operate_database', __name__, url_prefix='/api')

# 英単語全検索API
@api_operator.route('/word-all-search')
@login_required
def word_all_search():
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
    return jsonify(params)

# 英単語ID検索API
@api_operator.route('/word-id-search/<word_id>', methods=['GET', 'POST'])
@login_required
def word_id_search(word_id):
    if request.method == 'GET':
        # word_idに合致するwordsテーブルのデータを単一取得
        data = Word.query.get(word_id)
        return jsonify({
            'word_id': data.id,
            'word': data.word,
            'translation': data.translation,
            'part_en': data.part_en,
            'part_jp': data.part_jp,
            'rank': data.rank,
            'freq_rank': data.freq_rank,
            'response': data.response,
            'correct': data.correct
        })
    
    if request.method == 'POST':
        # POSTリクエストでJSONを取得
        get_request = request.get_json()
        new_translation = get_request['new_translation']

        # word_idに合致するwordsテーブルのデータを単一取得
        data = Word.query.get(word_id)
        # 英単語データの日本語訳を更新
        data.translation = new_translation

        # データベースを更新する
        db.session.commit()
        return jsonify('finish')

# 英単語ランク検索API
@api_operator.route('/word-rank-search/<rank>')
@login_required
def word_rank_search(rank):    
    # rankと合致するwordsテーブルのデータを全取得
    datas = Word.query.filter_by(rank=rank).all()

    params = []
    for i in range(len(datas)):
        params.append({
            'word_id': datas[i].id,
            'word': datas[i].word,
            'translation': datas[i].translation,
            'part_en': datas[i].part_en,
            'part_jp': datas[i].part_jp,
            'rank': datas[i].rank,
            'freq_rank': datas[i].freq_rank,
            'response': datas[i].response,
            'correct': datas[i].correct
        })
    return jsonify(params)

# クイズ解答時更新API
@api_operator.route('/quiz-update/<rank>', methods=['POST'])
@login_required
def quiz_update(rank):
    # POSTリクエストでJSONを取得
    get_request = request.get_json()
    word_id = get_request['word_id']
    answer_state = get_request['answer_state']
    response_span = get_request['response_span']

    # word_idに合致するwordsテーブルのデータを単一取得
    words_data = Word.query.get(word_id)
    # 現在ログイン中のユーザーIDと合致するusersテーブルのデータを単一取得
    users_data = User.query.get(current_user.id)
    
    # “解答された累計”を更新
    words_data.response += 1
    # “クイズの解答数の累計”を更新
    users_data.total_quiz_response += 1

    # クイズ正解時の場合
    if answer_state == 'correct':
        # “正解された累計”を更新
        words_data.correct += 1
        # “クイズの正解数の累計”を更新
        users_data.total_quiz_correct += 1

    Record = record(current_user.id)
    if not current_user.role == 'Student':
        # word_idと合致するy2000*テーブルのデータを全取得
        records = Record.query.filter_by(word_id=word_id).all()
    else:
        # 現在ログイン中のユーザーIDかつword_idと合致するstudentsテーブルのデータを全取得
        records = Record.query.filter_by(user_id=current_user.id, word_id=word_id).all()
    
    # 解答した英単語が既出の場合
    if records:
        print('\033[31m' + ' >> 既出です。' + '\033[0m')      # 確認用

        if not current_user.role == 'Student':
            # 同一の英単語IDを持つ複数のレコードの中から、word_idと合致するy2000*テーブルの最新のorderを取得
            x = Record.query.filter_by(word_id=word_id).all()
        else:
            # 同一の英単語IDを持つ複数のレコードの中から、現在ログイン中のユーザーIDかつword_idと合致するstudentsテーブルの最新のorderを取得
            x = Record.query.filter_by(user_id=current_user.id, word_id=word_id).all()

        max_order = x[-1].order
        # max_orderと合致するy2000*テーブルのデータを単一取得
        records_data = Record.query.get(max_order)

        # クイズ正解時の場合
        if answer_state == 'correct':
            # “学習待ち”から“テスト待ち”へ更新
            word_state = 'test_state'
            # “クイズでの解答結果”を格納
            quiz_response = 1

        # クイズ不正解時の場合
        elif answer_state == 'incorrect':
            # “学習待ち”状態を継承
            word_state = 'quiz_state'
            # “クイズでの解答結果”を格納
            quiz_response = 0

        # 初期値継承
        test_response = records_data.test_response
        constant_test_correct = records_data.constant_test_correct
        test_challenge_index = records_data.test_challenge_index

    # 解答した英単語が初出の場合
    else:
        print('\033[31m' + ' >> 初出です。' + '\033[0m')      # 確認用

        # クイズ正解時の場合
        if answer_state == 'correct':
            # “テスト待ち”として登録
            word_state = 'test_state'
            # “クイズでの解答結果”を格納
            quiz_response = 1

        # クイズ不正解時の場合
        elif answer_state == 'incorrect':
            # “学習待ち”として登録
            word_state = 'quiz_state'
            # “クイズでの解答結果”を格納
            quiz_response = 0

        # 初期値設定
        test_response = -1
        constant_test_correct = 0
        test_challenge_index = -1
    
    if not current_user.role == 'Student':
        # 上記のデータをy2000*テーブルに新規登録
        set_db = Record(
            word_id=word_id, 
            rank=rank, 
            quiz_response=quiz_response, 
            test_response=test_response, 
            constant_test_correct=constant_test_correct, 
            word_state=word_state, 
            response_date=datetime.now(pytz.timezone('Asia/Tokyo')), 
            response_span=response_span,
            quiz_challenge_index=users_data.quiz_challenge_number, 
            test_challenge_index=test_challenge_index
        )
    else:
        # 上記のデータをstudentsテーブルに新規登録
        set_db = Record(
            user_id=current_user.id,
            word_id=word_id, 
            rank=rank, 
            quiz_response=quiz_response, 
            test_response=test_response, 
            constant_test_correct=constant_test_correct, 
            word_state=word_state, 
            response_date=datetime.now(pytz.timezone('Asia/Tokyo')), 
            response_span=response_span,
            quiz_challenge_index=users_data.quiz_challenge_number, 
            test_challenge_index=test_challenge_index
        )

    # データベースに追加
    db.session.add(set_db)
    # データベースを更新
    db.session.commit()
    return jsonify('更新完了')

# テスト更新API
@api_operator.route('/test-update/<rank>', methods=['POST'])
@login_required
def test_update(rank):
    # POSTリクエストを受け取る
    get_request = request.get_json()
    word_id = get_request['word_id']
    answer_state = get_request['answer_state']
    response_span = get_request['response_span']
    
    # word_idに合致するwordsテーブルのデータを単一取得
    words_data = Word.query.get(word_id)
    # 現在ログイン中のユーザーIDと合致するusersテーブルのデータを単一取得
    users_data = User.query.get(current_user.id)

    Record = record(current_user.id)
    if not current_user.role == 'Student':
        # 同一の英単語IDを持つ複数のレコードの中から、word_idと合致するy2000*テーブルの最新のorderを取得
        x = Record.query.filter_by(word_id=word_id).all()
    else:
        # 同一の英単語IDを持つ複数のレコードの中から、現在ログイン中のユーザーIDかつword_idと合致するstudentsテーブルの最新のorderを取得
        x = Record.query.filter_by(user_id=current_user.id, word_id=word_id).all()

    max_order = x[-1].order
    # max_orderと合致するy2000*テーブルのデータを単一取得
    records_data = Record.query.get(max_order)

    # “解答された累計”を更新
    words_data.response += 1
    # “テストの解答数の累計”を更新
    users_data.total_test_response += 1
    
    # テスト正解時の場合
    if answer_state == 'correct':
        # “正解された累計”を更新
        words_data.correct += 1
        # “テストの正解数の累計”を更新
        users_data.total_test_correct += 1

        # “テスト待ち”から“復習待ち”へ更新
        word_state = 'review_state'
        # “テストでの解答結果”を格納
        test_response = 1
        # “テストにおける連続正解数”を更新
        constant_test_correct = records_data.constant_test_correct + 1

    # テスト不正解時の場合
    elif answer_state == 'incorrect':
        # “テスト待ち”から“学習待ち”へ更新
        word_state = 'quiz_state'
        # “テストでの解答結果”を格納
        test_response = 0
        # “テストにおける連続正解数”をリセット
        constant_test_correct = 0

    if not current_user.role == 'Student':
        # 上記のデータをy2000*テーブルに新規登録
        set_db = Record(
            word_id=word_id, 
            rank=rank, 
            quiz_response=records_data.quiz_response, 
            test_response=test_response, 
            constant_test_correct=constant_test_correct, 
            word_state=word_state, 
            response_date=datetime.now(pytz.timezone('Asia/Tokyo')), 
            response_span=response_span,
            quiz_challenge_index=records_data.quiz_challenge_index, 
            test_challenge_index=users_data.test_challenge_number
        )
    else:
        # 上記のデータをstudentsテーブルに新規登録
        set_db = Record(
            user_id=current_user.id,
            word_id=word_id, 
            rank=rank, 
            quiz_response=records_data.quiz_response, 
            test_response=test_response, 
            constant_test_correct=constant_test_correct, 
            word_state=word_state, 
            response_date=datetime.now(pytz.timezone('Asia/Tokyo')), 
            response_span=response_span,
            quiz_challenge_index=records_data.quiz_challenge_index, 
            test_challenge_index=users_data.test_challenge_number
        )

    # データベースに追加
    db.session.add(set_db)
    # データベースを更新
    db.session.commit()    
    return jsonify('finish')

# バックアップ作成API
@api_operator.route('/database/create_backup')
@login_required
@roles_required
def create_backup():
    src = './database.db'
    # コピー元ファイルの存在を判定
    if os.path.isfile(src):
        now = datetime.now(pytz.timezone('Asia/Tokyo'))
        filename = now.strftime('%Y%m%d_%H%M%S') + '.db'
        os.makedirs('./backup', exist_ok=True)
        dst = f'./backup/{filename}'
        # ファイルをコピー
        shutil.copy(src, dst)

        print('\033[31m' + f'{filename} の作成が完了しました。\nデータベースのバックアップに成功しました。' + '\033[0m')      # 確認用

        return send_file(dst)
    else:
        return jsonify('Failure')

# テストデータCSV出力API
@api_operator.route('/database/create_csv/<type>/<user_id>/<rank>')
@login_required
@roles_required
def create_csv(type, user_id, rank):
    users_data = User.query.filter_by(id=user_id).first()
    words_datas = Word.query.filter_by(rank=rank).all()
    Record = record(user_id)

    csv_data = []
    data_index = []
    for i in range(len(words_datas)):
        data_line = {}
        for j in range(users_data.test_challenge_number):
            if not users_data.role == 'Student':
                records_data = Record.query.filter_by(word_id=words_datas[i].id, test_challenge_index=(j+1)).first()
            else:
                records_data = Record.query.filter_by(user_id=user_id, word_id=words_datas[i].id, test_challenge_index=(j+1)).first()
                        
            if records_data is None:
                if type == 'record':
                    data_line[f'テスト{j + 1}'] = -1

                if type == 'datetime':
                    data_line[f'テスト{j + 1}'] = '1999-1-1 12:12:12'
            else:
                if type == 'record':
                    data_line[f'テスト{j + 1}'] = records_data.test_response
                
                if type == 'datetime':
                    data_line[f'テスト{j + 1}'] = records_data.response_date

        csv_data.append(data_line)
        data_index.append(words_datas[i].word)

    # データフレーム作成
    df = pd.DataFrame(data=csv_data, index=data_index)
    if type == 'datetime':
        for i in range(len(df.columns)):
            df[f'テスト{i + 1}'] = pd.to_datetime(df[f'テスト{i + 1}'])
            
    os.makedirs('./export', exist_ok=True)
    if type == 'record':
        output = f'./export/{user_id}_{rank}_record.csv'

    elif type == 'datetime':
        output = f'./export/{user_id}_{rank}_datetime.csv'
    # CSVファイルをエクスポート
    df.to_csv(f'{output}', encoding='shift-jis')

    print('\033[31m' + f'{user_id}_{rank}_record.csv の作成が完了しました。\nCSVファイルの出力に成功しました。' + '\033[0m')      # 確認用

    return send_file(output)
    
# ユーザー削除API
@api_operator.route('/database/delete/<id>')
@login_required
@roles_required
def delete(id):
    # 削除するユーザーのIDを取得
    delete_user = User.query.get(id)
    # データベースを削除
    db.session.delete(delete_user)
    # データベースを更新
    db.session.commit()
    return redirect(url_for('admin'))
