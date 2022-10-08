from __init__ import app, db, bcrypt, login_manager, Word, User, Student, Y200004, Y200042, Y200051, Y200062, Y200065, Y200078, Y200080, Y200089, Y200090, roles_required, record
import os, re, regex, pytz, random, collections, shutil
from datetime import datetime
from flask import render_template, request, url_for, redirect, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from sqlalchemy import or_, func

# Blueprint（他のPythonファイルのモジュール化）を登録
from feature import feature
from api import api
app.register_blueprint(feature)
app.register_blueprint(api)

# Flaskアプリと紐づけ
login_manager.init_app(app)

# login_requiredでリダイレクトされた場合に実行したい関数を登録
login_manager.login_view = "login"

# Cookieのセッション情報を利用して、current_userに情報を渡す
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# login_requiredでリダイレクトされた場合のメッセージを設定
@login_manager.unauthorized_handler
def unauthorized():
    flash("これより先のページへのアクセスにはログインが必要です。", "unauthorized")
    return redirect(url_for('login'))

# サインアップ用コントローラーの登録
class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=50)])
    privacypolicy = BooleanField()
    submit = SubmitField('SIGNUP')

    # 既存のユーザー名と同じものが入力されたらエラー判定を出す関数
    # 正規表現以外の文字もエラー対象
    def validate_username(self, username):
        used_username = User.query.filter_by(username=username.data).first()
        if used_username:
            raise ValidationError('このユーザー名は既に使用されています。')
            
        regular_word = regex.compile(r'^[0-9a-zA-Z０-９Ａ-Ｚａ-ｚ\p{Hiragana}\p{Katakana}\p{Han}]+$')
        if not regular_word.match(username.data):
            raise ValidationError('使用できない文字が含まれています。')

    # パスワードの長さが４よりも少ない場合にエラー判定を出す関数
    # 正規表現以外の文字もエラー対象
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('パスワードは4文字以上で入力してください。')

        regular_word = re.compile('^[0-9a-zA-Z]+$')
        if not regular_word.match(password.data):
            raise ValidationError('使用できない文字が含まれています。')

    # 利用規約に同意しない場合にエラー判定を出す関数
    def validate_privacypolicy(self, privacypolicy):
        if privacypolicy.data == False:
            raise ValidationError('利用規約に同意してください。')

# ログイン用コントローラーの登録
class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField()
    submit = SubmitField('LOGIN')

# ホームページ
@app.route('/')
def homepage():
    return render_template('homepage.html')

# サインアップページ
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # バリデーションチェック
    if form.validate_on_submit():
        # 重複しないユーザー固有のIDを作成
        while True:
            user_id = random.randint(100000, 999999)
            if not user_id == User.query.get(user_id):
                break
        
        # foamに入力されたユーザー名を取得
        username = form.username.data
        # フォームに入力されたパスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # 新規ユーザー情報をusersテーブルに登録
        new_user = User(
            id=user_id, 
            username=username, 
            password=hashed_password, 
            role="Student", 
            login_state='inactive', 
            signup_date=datetime.now(pytz.timezone('Asia/Tokyo')),
            total_quiz_response = 0,
            total_quiz_correct = 0,
            total_test_response = 0,
            total_remembered = 0,
            quiz_challenge_number = 0,
            test_challenge_number = 0
        )
        # データベースに追加
        db.session.add(new_user)
        # データベースを更新
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template('signup.html', form=form)

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ログイン済みであればバリデーションチェックを飛ばす
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    # バリデーションチェック
    if form.validate_on_submit():
        # フォームに入力されたユーザー名と合致するusersテーブルのデータを単一取得
        now_user = User.query.filter_by(username=form.username.data).first()
        if now_user:
            # ハッシュ化されたパスワードのチェック
            if bcrypt.check_password_hash(now_user.password, form.password.data):
                # 第二引数にremember=Trueを渡すことで、Cookieにセッション情報を残している
                login_user(now_user, remember=form.remember.data)
                # ユーザーのログイン状態をアクティブに更新
                now_user.login_state = 'active'
                # ログイン日時を更新
                now_user.login_date = datetime.now(pytz.timezone('Asia/Tokyo'))
                # データベースを更新
                db.session.commit()
                return redirect(url_for('home'))
            # パスワードが合致しなかった場合
            else :
                flash('パスワードが間違っています。', 'password')
        # ユーザー名が合致しなかった場合
        else :
            flash('ユーザー名が間違っています。', 'username')

    return render_template('login.html', form=form)

# マイページ
@app.route('/mypage/home')
@login_required
def home():
    return render_template('home.html')

# ライブラリページ
@app.route('/mypage/home/library')
@login_required
def library():
    return render_template('library.html')

# クイズコースページ
@app.route('/mypage/learnings')
@login_required
def learnings():
    params = []
    ranks = ['A1', 'A2', 'B1', 'B2']
    Record = record(current_user.id)

    for rank in ranks:
        # wordsテーブルのレコード数を取得
        words_length = Word.query.filter_by(rank=rank).count()

        if not current_user.role == 'Student':
            # rankと合致するy2000*テーブルのデータを全取得
            records = Record.query.filter_by(rank=rank).all()
        else:
            # 現在ログイン中のユーザーIDかつrankと合致するstudentsテーブルのデータを全取得
            records = Record.query.filter_by(user_id=current_user.id, rank=rank).all()

        # 重複しないy2000*テーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        records_datas = []
        # 同一の英単語IDを持つ複数のレコードの中から最新のデータを取得
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

            # max_orderかつ“テスト待ち”または“復習待ち”と合致するy2000*テーブルのデータを単一取得
            records_data = Record.query.filter_by(order=max_order).filter(or_(Record.word_state=='test_state', Record.word_state=='review_state')).first()
            if records_data is None:
                continue
            records_datas.append(max_order)

        diff = round((len(records_datas) * 100 / words_length), 1)    # クイズの達成度（四捨五入したパーセンテージ）を計算
        params.append(diff)
    
    return render_template('learnings.html', params=params)

# クイズページ
@app.route('/mypage/learnings/quiz/<rank>')
@login_required
def quiz(rank):
    # 現在ログイン中のユーザーIDと合致するusersテーブルのデータを単一取得
    data = User.query.get(current_user.id)
    # “クイズに挑戦した累計”の更新
    data.quiz_challenge_number += 1
    # データベースを更新
    db.session.commit()
    return render_template('quiz.html', rank=rank)

# クイズリザルトページ
@app.route('/mypage/learnings/quiz/<rank>/result')
@login_required
def quiz_result(rank):
    # クエリパラメータを取得
    score = request.args.get('score')        
    return render_template('quiz_result.html', rank=rank, score=score)

# テストコースページ
@app.route('/mypage/tasks')
@login_required
def tasks():
    params = []
    ranks = ['A1', 'A2', 'B1', 'B2']
    Record = record(current_user.id)

    for rank in ranks:
        if not current_user.role == 'Student':
            # rankと合致するy2000*のテーブルのデータを全取得
            records = Record.query.filter_by(rank=rank).all()
        else:
            # 現在ログイン中のユーザーIDかつrankと合致するstudentsテーブルのデータを全取得
            records = Record.query.filter_by(user_id=current_user.id, rank=rank).all()

        # 重複しないy2000*テーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        records_datas = []
        # 同一の英単語IDを持つ複数のレコードの中から最新のデータを取得
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

            # max_orderと合致するy2000* or studentsテーブルのデータを単一取得
            records_data = Record.query.filter_by(order=max_order, word_state='test_state').first()
            if records_data is None:
                continue
            records_datas.append(records_data)
        
        task = len(records_datas) // 20     # テストを受験できる回数を計算
        params.append(task)
        
    return render_template('tasks.html', tasks=params)

# テストページ
@app.route('/mypage/tasks/test/<rank>')
@login_required
def test(rank):
    # 現在ログイン中のユーザーのIDと合致するusersテーブルのデータを単一取得
    data = User.query.get(current_user.id)
    # “テストに挑戦した累計”の更新
    data.test_challenge_number += 1
    # データベースを更新
    db.session.commit()
    return render_template('test.html', rank=rank)

# テストリザルトページ
@app.route('/mypage/tasks/test/<rank>/result')
@login_required
def test_result(rank):
    # クエリパラメータを取得
    score = request.args.get('score')
    return render_template('test_result.html', rank=rank ,score=score)

# 設定ページ
@app.route('/mypage/settings')
@login_required
def settings():
    return render_template(
        'settings.html', 
        user_id=current_user.id, 
        username=current_user.username, 
        user_role=current_user.role
    )

# プロフィールページ
@app.route('/mypage/settings/profile')
@login_required
def profile():
    return render_template(
        'profile.html', 
        user_id=current_user.id, 
        username=current_user.username, 
        user_role=current_user.role, 
        signup_date=current_user.signup_date
    )

# ログアウト
@app.route('/logout')
@login_required
def logout():
    # “ログイン中”を“ログアウト中”へ更新
    current_user.login_state = 'inactive'
    # データベースを更新
    db.session.commit()
    logout_user()
    return redirect(url_for('homepage'))

# 管理者ページ
@app.route('/admin')
@login_required
@roles_required
def admin():
    # usersテーブルのデータを全取得
    datas = User.query.all()

    params = []
    for i in range(len(datas)):
        params.append({
            'ID': datas[i].id,
            'username': datas[i].username,
            'role': datas[i].role,
            'login_state': datas[i].login_state,
            'signup_date': str(datas[i].signup_date),
            'login_date': str(datas[i].login_date),
            'total_quiz_response': datas[i].total_quiz_response,
            'total_quiz_correct': datas[i].total_quiz_correct,
            'total_test_response': datas[i].total_test_response,
            'total_remembered': datas[i].total_remembered,
            'quiz_challenge_number': datas[i].quiz_challenge_number,
            'test_challenge_number': datas[i].test_challenge_number
        })
    return render_template('admin.html', users=params)

if __name__ == '__main__':
    app.run(debug=True)
