from __init__ import app, db, bcrypt, login_manager, Word, User, Record, roles_required
import re, regex, pytz, random
from datetime import datetime
from flask import render_template, render_template_string, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from feature import feature
from api import api

# Blueprint（他のPythonファイルのモジュール化）を登録
app.register_blueprint(feature)
app.register_blueprint(api)

# Flaskアプリと紐づけ
login_manager.init_app(app)

# ログインする際に実行される処理関数を登録
# login_requiredでリダイレクトされた場合に実行したい関数を登録する
login_manager.login_view = "login"

# 取得したユーザーIDからユーザー情報を返し、ログイン済みユーザーであることを確認
# Cookieのセッション情報を利用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# login_requiredでリダイレクトされた場合のメッセージを設定
@login_manager.unauthorized_handler
def unauthorized():
    flash('これより先のページへのアクセスにはログインが必要です。', 'unauthorized')
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
            if not user_id == User.query.filter_by(id=user_id).first():
                break
        
        # フォームに入力されたパスワードをハッシュ化
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # フォームに入力された情報をusersテーブルに登録
        new_user = User(id=user_id, username=form.username.data, password=hashed_password, role="Student", login_state='inactive', signup_date=datetime.now(pytz.timezone('Asia/Tokyo')))

        # データベースに追加
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
        
    return render_template('signup.html', form=form)

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ログイン状態を確認し、ログイン済みであればバリデーションチェックを飛ばす
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    # バリデーションチェック
    if form.validate_on_submit():

        # フォームに入力されたユーザー名と合致するユーザー名をusersテーブルから検索し、あれば取得
        now_user = User.query.filter_by(username=form.username.data).first()
        if now_user:
            
            # ハッシュ化されたパスワードのチェック
            if bcrypt.check_password_hash(now_user.password, form.password.data):
                # 実際にログインを行う関数
                # 第二引数にremember=Trueを渡すことで、Cookieにセッション情報を残している
                login_user(now_user, remember=form.remember.data)

                # ユーザー状態をアクティブに更新
                now_user.login_state = 'active'
                # ログイン日時を更新
                now_user.login_date = datetime.now(pytz.timezone('Asia/Tokyo'))
                db.session.commit()

                if now_user.role == 'Admin':
                    return redirect(url_for('admin'))

                return redirect(url_for('home'))
            else :
                flash('パスワードが間違っています。', 'password')
        else :
            flash('ユーザー名が間違っています。', 'username')

    return render_template('login.html', form=form)

# マイページ
@app.route('/mypage/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/mypage/home/library')
@login_required
def library():
    return render_template('library.html')

@app.route('/mypage/learnings')
@login_required
def learnings():
    return render_template('learnings.html')

@app.route('/mypage/learnings/quiz')
@login_required
def quiz():
    rank = request.args.get('rank')
    return render_template('quiz.html', rank=rank)

# クイズリザルトページ
@app.route('/mypage/learnings/quiz/result', methods=['POST'])
@login_required
def quiz_result():
    word_id = []
    for i in range(10):
        data = request.form.get(f'word_id{i}')
        word_id.append(data)
    
    answer_state = []
    for i in range(10):
        data = request.form.get(f'answer_state{i}')
        answer_state.append(data)
    
    rank = request.form.get('rank')
    score = request.form.get('score')
    
    return render_template('quiz_result.html', userId=current_user.id, wordId=word_id, answerState=answer_state, rank=rank, score=score)

@app.route('/mypage/tasks')
@login_required
def tasks():
    ranks = ['A1', 'A2', 'B1', 'B2']
    params = []
    for rank in ranks:
        # テスト待ちの英単語群を取得
        datas = Record.query.filter_by(user_id=current_user.id, rank=rank, test_correct=0, test_state='active').all()
        task = len(datas) // 20
        params.append(task)
    return render_template('tasks.html', tasks=params)

@app.route('/mypage/tasks/test')
@login_required
def test():
    rank = request.args.get('rank')
    return render_template('test.html', rank=rank)

# テストリザルトページ
@app.route('/mypage/tasks/test/result', methods=['POST'])
@login_required
def test_result():
    word_id = []
    for i in range(20):
        data = request.form.get(f'word_id{i}')
        word_id.append(data)
    
    answer_state = []
    for i in range(20):
        data = request.form.get(f'answer_state{i}')
        answer_state.append(data)
    
    score = request.form.get('score')

    return render_template('test_result.html', userId=current_user.id, wordId=word_id, answerState=answer_state, score=score)

@app.route('/mypage/settings')
@login_required
def settings():
    return render_template('settings.html', 
    user_id=current_user.id, username=current_user.username, user_role=current_user.role)

@app.route('/mypage/settings/profile')
@login_required
def profile():
    return render_template('profile.html', user_id=current_user.id, username=current_user.username, user_role=current_user.role, signup_date=current_user.signup_date)

# ログアウト処理
@app.route('/logout')
@login_required
def logout():
    # ユーザー状態を非アクティブに更新
    current_user.login_state = 'inactive'
    db.session.commit()

    # 実際にログアウトを行う関数
    logout_user()
    return redirect(url_for('homepage'))

# 管理者ページ
@app.route('/admin')
@login_required
@roles_required
def admin():
    params = []
    datas = User.query.all()
    for i in range(len(datas)):
        params.append({
            'user_id': datas[i].id,
            'username': datas[i].username,
            'role': datas[i].role,
            'login_state': datas[i].login_state,
            'signup_date': str(datas[i].signup_date),
            'login_date': str(datas[i].login_date),
            'total_remembered': datas[i].total_remembered
        })
    return render_template('admin.html', users=params)

if __name__ == '__main__':
    app.run()
