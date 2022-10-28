from __init__ import app, db, bcrypt, login_manager, Word, User, Student, Y200004, Y200042, Y200051, Y200062, Y200065, Y200078, Y200080, Y200089, Y200090, roles_required, record
import re, regex, pytz, random, collections
from datetime import datetime
from flask import render_template, request, url_for, redirect, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, Length, EqualTo, ValidationError
from sqlalchemy import or_, func

# Blueprint（他のPythonファイルのモジュール化）を登録
from create_questions import api_creator
from operate_database import api_operator
app.register_blueprint(api_creator)
app.register_blueprint(api_operator)

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
    password = PasswordField('password', validators=[DataRequired()])
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

# ログイン用コントローラーの登録
class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('LOGIN')

# プロフィール用コントローラーの登録
class ProfileForm(FlaskForm):
    username = StringField(validators=[Optional(strip_whitespace=False)])
    email = EmailField(validators=[Email(), Optional(strip_whitespace=False)])
    submit = SubmitField('UPDATE')

    # 既存のメールアドレスと同じものが入力されたらエラー判定を出す関数
    def validate_email(self, email):
        used_email = User.query.filter_by(email=email.data).first()
        if used_email:
            raise ValidationError('このメールアドレスは既に使用されています。')

    # 既存のユーザー名と同じものが入力されたらエラー判定を出す関数
    # 正規表現以外の文字もエラー対象
    def validate_username(self, username):
        used_username = User.query.filter_by(username=username.data).first()
        if used_username:
            raise ValidationError('このユーザー名は既に使用されています。')
            
        regular_word = regex.compile(r'^[0-9a-zA-Z０-９Ａ-Ｚａ-ｚ\p{Hiragana}\p{Katakana}\p{Han}]+$')
        if not regular_word.match(username.data):
            raise ValidationError('使用できない文字が含まれています。')

# パスワード変更用コントローラーの登録
class ChangePasswordForm(FlaskForm):
    curpwd = PasswordField(validators=[DataRequired()])
    chgpwd = PasswordField(validators=[DataRequired(), EqualTo('cfmpwd', message='パスワードが一致しません。')])
    cfmpwd = PasswordField(validators=[DataRequired(message='入力してください。')])
    submit = SubmitField('CHANGE PASSWORD')

    # パスワードの長さが４よりも少ない場合にエラー判定を出す関数
    # 正規表現以外の文字もエラー対象
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('パスワードは4文字以上で入力してください。')

        regular_word = re.compile('^[0-9a-zA-Z]+$')
        if not regular_word.match(password.data):
            raise ValidationError('使用できない文字が含まれています。')

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
        
        # formに入力されたユーザー名を取得
        username = form.username.data
        # フォームに入力されたパスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # 新規ユーザー情報をusersテーブルに登録
        new_user = User(
            id=user_id, 
            username=username, 
            password=hashed_password, 
            email='未登録', 
            role="Student", 
            login_state='inactive', 
            signup_date=datetime.now(pytz.timezone('Asia/Tokyo')),
            total_quiz_response = 0,
            total_quiz_correct = 0,
            total_test_response = 0,
            total_test_correct = 0,
            quiz_challenge_number = 0,
            test_challenge_number = 0,
            remembering = 0
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
                login_user(now_user, remember=True)
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

            # max_orderかつ“テスト待ち”と合致するy2000* or studentsテーブルのデータを単一取得
            records_data = Record.query.filter_by(order=max_order, word_state='test_state').first()
            if records_data is None:
                continue
        
            records_datas.append(records_data)
        
        task = len(records_datas) // 20     # テストを受験できる回数を計算
        params.append(task)
    
    return render_template('home.html', stacks=params)

# ダッシュボードページ
@app.route('/mypage/dashboard')
@login_required
def dashboard():
    params = []
    counts = []
    remembereds = []
    answereds = []
    ranks = ['A1', 'A2', 'B1', 'B2']
    Record = record(current_user.id)
    users_data = User.query.filter_by(id=current_user.id).first()

    for rank in ranks:
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

            records_datas.append(records_data)

        # wordsテーブルのレコード数を取得
        words_length = Word.query.filter_by(rank=rank).count()

        diff = round((len(records_datas) * 100 / words_length), 1)    # クイズの達成度（四捨五入したパーセンテージ）を計算
        params.append(diff)

        count = 0
        for i in range(users_data.quiz_challenge_number):
            if not current_user.role == 'Student':
                challenge_data = Record.query.filter_by(rank=rank, quiz_challenge_index=(i+1)).first()
            else:
                challenge_data = Record.query.filter_by(user_id=current_user.id, rank=rank, quiz_challenge_index=(i+1)).first()

            if challenge_data:
                count += 1
        
        counts.append(count)

        remembered= []
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()
            
            remembering_data = Record.query.filter_by(order=max_order, word_state='review_state').first()
            if remembering_data is None:
                continue

            remembered.append(remembering_data)
        
        remembereds.append(len(remembered))

        answered = []
        for i in reversed(range(users_data.quiz_challenge_number)):
            if not current_user.role == 'Student':
                answer_data = Record.query.filter_by(rank=rank, quiz_response=1, test_response=-1, quiz_challenge_index=(i+1)).count()
            else:
                answer_data = Record.query.filter_by(user_id=current_user.id, rank=rank, quiz_response=1, test_response=-1, quiz_challenge_index=(i+1)).count()

            if len(answered) > 10:
                break

            if answer_data == 0:
                continue
            
            answered.append(answer_data)
        
        answereds.append(answered)

    
    return render_template(
        'dashboard.html', 
        params=params, 
        counts=counts,
        remembereds=remembereds,
        answereds=answereds,
        user_role=current_user.role
    )

# ライブラリページ
@app.route('/mypage/library')
@login_required
def library():
    return render_template('library.html', user_role=current_user.role)

# クイズコースページ
@app.route('/mypage/learnings')
@login_required
def learnings():
    return render_template('learnings.html')

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
    count = request.args.get('count')
    return render_template('quiz_result.html', rank=rank, score=score, count=count)

# テストコースページ
@app.route('/mypage/tasks')
@login_required
def tasks():
    params = []
    counts = []
    ranks = ['A1', 'A2', 'B1', 'B2']
    Record = record(current_user.id)
    users_data = User.query.filter_by(id=current_user.id).first()

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

            # max_orderかつ“テスト待ち”と合致するy2000* or studentsテーブルのデータを単一取得
            records_data = Record.query.filter_by(order=max_order, word_state='test_state').first()
            if records_data is None:
                continue
        
            records_datas.append(records_data)
        
        task = len(records_datas) // 20     # テストを受験できる回数を計算
        params.append(task)

        count = 0
        for i in range(users_data.test_challenge_number):
            if not current_user.role == 'Student':
                records = Record.query.filter_by(rank=rank, test_challenge_index=(i+1)).first()
            else:
                records = Record.query.filter_by(user_id=current_user.id, rank=rank, test_challenge_index=(i+1)).first()

            if records:
                count += 1
        
        counts.append(count)
        
    return render_template(
        'tasks.html', 
        stacks=params, 
        counts=counts,
        user_role=current_user.role
    )

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
    count = request.args.get('count')

    # 現在ログイン中のユーザーのIDと合致するusersテーブルのデータを単一取得
    users_data = User.query.filter_by(id=current_user.id).first()

    Record = record(current_user.id)
    if not current_user.role == 'Student':
        # y2000*テーブルのデータを全取得
        records = Record.query.all()
    else:
        # 現在ログイン中のユーザーIDと合致するstudentsテーブルのデータを全取得
        records = Record.query.filter_by(user_id=current_user.id).all()

    if records:
        # 重複しないy2000*テーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        remembering_data = []
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # 同一の英単語IDを持つ複数のレコードの中から、idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 同一の英単語IDを持つ複数のレコードの中から、現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()

            # max_orderかつ“復習待ち”と合致するy2000* or studentsテーブルのデータを単一取得
            records_data = Record.query.filter_by(order=max_order, word_state='review_state').first()
            if records_data is None:
                continue

            remembering_data.append(records_data)
        
        # 覚えている英単語の総数
        users_data.remembering = len(remembering_data)
        # データベースを更新する
        db.session.commit()
    
    return render_template('test_result.html', rank=rank ,score=score, count=count)

# FAQページ
@app.route('/mypage/faq')
@login_required
def faq():
    return render_template('faq.html')

# 設定ページ
@app.route('/mypage/settings')
@login_required
def settings():
    ranks = ['A1', 'A2', 'B1', 'B2']
    remembereds = 0
    Record = record(current_user.id)

    for rank in ranks:
        if not current_user.role == 'Student':
            # rankと合致するy2000*テーブルのデータを全取得
            records = Record.query.filter_by(rank=rank).all()
        else:
            # 現在ログイン中のユーザーIDかつrankと合致するstudentsテーブルのデータを全取得
            records = Record.query.filter_by(user_id=current_user.id, rank=rank).all()

        # 重複しないy2000*テーブルの英単語IDを取得
        word_id_list = list(map(lambda x: x.word_id, records))
        dedupe_keys = list(collections.Counter(word_id_list).keys())

        remembered = []
        for id in dedupe_keys:
            if not current_user.role == 'Student':
                # idと合致するy2000*テーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.word_id==id).scalar()
            else:
                # 現在ログイン中のユーザーIDかつidと合致するstudentsテーブルの最新のorderを取得
                max_order = db.session.query(func.max(Record.order)).filter(Record.user_id==current_user.id, Record.word_id==id).scalar()
            
            remembering_data = Record.query.filter_by(order=max_order, word_state='review_state').first()
            if remembering_data is None:
                continue

            remembered.append(remembering_data)

        remembereds += len(remembered)
    
    return render_template(
        'settings.html', 
        user_id=current_user.id, 
        username=current_user.username, 
        user_role=current_user.role,
        remembered=remembereds
    )

# プロフィールページ
@app.route('/mypage/settings/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    # バリデーションチェック
    if form.validate_on_submit():
        # formに入力されたユーザー名を取得
        if form.username.data == '':
            same_username = User.query.get(current_user.id).username
            username = same_username
        else:
            username = form.username.data

        # formに入力されたメールアドレスを取得
        # if form.email.data == '':
        #     same_email = User.query.get(current_user.id).email
        #     email = same_email
        # else :
        #     email = form.email.data

        update_user = User.query.get(current_user.id)
        # 新しいユーザー名・メールアドレスに変更
        update_user.username = username
        # update_user.email = email
        # データベースを更新
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template(
        'profile.html', 
        form=form, 
        ID=current_user.id,
        username=current_user.username,
        role=current_user.role,
        signup_date=current_user.signup_date
    )

# パスワード変更ページ
@app.route('/mypage/settings/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    # バリデーションチェック
    if form.validate_on_submit():
        # 現在ログイン中のユーザーのIDと合致するusersテーブルのデータを単一取得
        update_user = User.query.get(current_user.id)
        # ハッシュ化された現在のパスワードのチェック
        if bcrypt.check_password_hash(update_user.password, form.curpwd.data):
            # フォームに入力された新しいパスワードをハッシュ化
            hashed_password = bcrypt.generate_password_hash(form.chgpwd.data)
            # 新しいパスワードに変更
            update_user.password = hashed_password
            # データベースを更新
            db.session.commit()
            return redirect(url_for('change_password'))
        # パスワードが合致しなかった場合
        else :
            flash('パスワードが間違っています。', 'curpwd')

    return render_template('change_password.html', form=form)

# ログアウト
@app.route('/logout')
@login_required
def logout():
    # “ログイン中”を“ログアウト中”へ更新
    current_user.login_state = 'inactive'
    # データベースを更新
    db.session.commit()
    logout_user()
    session.pop('remember_token', None)
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
        # if datas[i].is_authenticated:
        #     datas[i].login_state = 'active'
        # else:
        #     datas[i].login_state = 'inactive'
        
        params.append({
            'ID': datas[i].id,
            'username': datas[i].username,
            'email': datas[i].email,
            'role': datas[i].role,
            'login_state': datas[i].login_state,
            'signup_date': str(datas[i].signup_date),
            'login_date': str(datas[i].login_date)
        })
    return render_template('admin.html', users=params)

if __name__ == '__main__':
    app.run()
