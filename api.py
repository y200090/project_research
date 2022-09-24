from __init__ import db, Word, User, Record, roles_required
import pytz, json
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

api = Blueprint('api', __name__, url_prefix='/api')

# View All Words API
@api.route('/view-all-words')
def view_all_words():
    params = []
    datas = Word.query.all()
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

# Word ID Search API
@api.route('/word-id-search/<word_id>')
@login_required
def word_id_search(word_id):
    words_data = Word.query.filter_by(id=word_id).first()
    if words_data:
        return jsonify({
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
    else:
        return "このIDの英単語データは存在しません。"

# Words Rank Belt Search API
@api.route('/words-rank-belt-search/<rank>')
@login_required
def words_rank_belt_search(rank):
    params = []
    words_datas = Word.query.filter_by(rank=rank).all()
    if words_datas:
        for i in range(len(words_datas)):
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
        return jsonify(params)
    else:
        return "このランク帯の英単語データは存在しません。"

# Quiz Achievement Calculation API
@api.route('/quiz-achivement-calculation')
@login_required
def quiz_achievement_Calculation():
    ranks = ['A1', 'A2', 'B1', 'B2']
    params = []
    for rank in ranks:
        words_datas = Word.query.filter_by(rank=rank).all()
        records_datas = Record.query.filter_by(user_id=current_user.id, rank=rank, test_state='active').all()
        diff = len(records_datas) * 100 // len(words_datas)
        params.append(diff)
    return jsonify(params)

# Update by Quiz API
@api.route('/update-by-quiz/<rank>', methods=['POST'])
@login_required
def update_by_quiz(rank):
    # POSTリクエストを受け取る
    get_request = request.get_json()

    word_id = get_request['word_id']
    answer_state = get_request['answer_state']

    # wordsテーブルの出題数・正解数を更新
    words_data = Word.query.filter_by(id=word_id).first()
    words_data.response += 1
    if answer_state == 'correct':
        words_data.correct += 1
    
    # recordsテーブルを検索
    records_data = Record.query.filter_by(user_id=current_user.id, word_id=word_id).first()

    # 既出の場合
    if records_data:
        if answer_state == 'correct':
            # 学習待ちからテスト待ちへ
            records_data.test_state = 'active'
        elif answer_state == 'incorrect':
            # 再度学習待ちへ
            records_data.test_state = 'inactive'
    # 初出の場合
    else:
        # recordsテーブルにデータを登録
        if answer_state == 'correct':
            # テスト待ちへ
            test_state = 'active'
        elif answer_state == 'incorrect':
            # 学習待ちへ
            test_state = 'inactive'
        
        set_db = Record(user_id=current_user.id, word_id=word_id, rank=rank, test_correct=0, test_state=test_state)
        # データベースに追加
        db.session.add(set_db)
    
    # データベースを更新する
    db.session.commit()

    return jsonify('finish')

# Update by Test API
@api.route('/update-by-test', methods=['POST'])
@login_required
def update_by_test():
    # POSTリクエストを受け取る
    get_request = request.get_json()

    word_id = get_request['word_id']
    answer_state = get_request['answer_state']

    words_data = Word.query.filter_by(id=word_id).first()
    records_data = Record.query.filter_by(user_id=current_user.id, word_id=word_id).first()
    users_data = User.query.filter_by(id=current_user.id).first()

    words_data.response += 1                     # 全体の解答数を更新
    
    # テスト正解時の場合
    if answer_state == 'correct':
        words_data.correct += 1                  # 全体の正解数を更新
        records_data.test_correct += 1           # テストの正解数を更新
        records_data.test_state = 'review'       # テスト待ちから復習待ちへ
        users_data.total_remembered += 1         # ユーザーの”覚えた”判定の累計を更新

    # テスト不正解時の場合
    elif answer_state == 'incorrect':
        records_data.test_correct = 0            # テストの正解数をリセット
        records_data.test_state = 'inactive'     # テスト待ちから学習待ちへ
    
    # データベースを更新する
    db.session.commit()
    
    return jsonify('finish')

# Record API
@api.route('/user/<user_id>')
def user_id_search(user_id):
    temp = []
    datas = Record.query.filter_by(user_id=user_id).all()
    if datas:
        for i in range(len(datas)):
            temp.append({
                'user_id': datas[i].user_id,
                'word_id': datas[i].word_id,
                'response': datas[i].response,
                'correct': datas[i].correct,
                'responseDate': str(datas[i].response_date)
            })
        return jsonify(temp)
    return "このIDのユーザーは存在しません。"

# Record WordID API
@api.route('/user/<user_id>/word/<word_id>', methods=['GET', 'POST'])
def two_ids_search(user_id, word_id):
    # ユーザーの成績データから英単語IDと合致する英単語データを検索する
    if request.method == 'GET':

        data = Record.query.filter_by(user_id=user_id, word_id=word_id).first()
        if data:
            return jsonify({
                'user_id': data.user_id,
                'word_id': data.word_id,
                'response': data.response,
                'correct': data.correct,
                'responseDate': str(data.response_date)
            })
        return "このIDのユーザー、または英単語データは存在しません。"
        
    # # ユーザーの成績データの出題数・正解数・解答日時を更新する
    # elif request.method == 'POST':
    #     # POSTリクエストを受け取る
    #     get_request = request.get_json()
    #     new_response = get_request["newUserResponse"]
    #     new_correct = get_request["newUserCorrect"]

    #     data = Record.query.filter_by(user_id=user_id, word_id=word_id).first()
    #     data.response = new_response
    #     data.correct = new_correct
    #     data.response_date = datetime.now(pytz.timezone('Asia/Tokyo'))

    #     # データベースを更新する
    #     db.session.commit()
    #     return jsonify({
    #         'user_id': data.user_id,
    #         'word_id': data.word_id,
    #         'response': data.response,
    #         'correct': data.correct,
    #         'responseDate': str(data.response_date)
    #     })

# User API
@api.route('/admin')
@login_required
@roles_required
def admin():
    params = []
    datas = User.query.all()
    for i in range(len(datas)):
        params.append({
            'user_id': datas[i].id,
            'email': datas[i].email,
            'username': datas[i].username,
            'role': datas[i].role,
            'login_state': datas[i].login_state,
            'signup_date': str(datas[i].signup_date),
            'login_date': str(datas[i].login_date),
            'total_remembered': datas[i].total_remembered
        })
    return jsonify(params)
