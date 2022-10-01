from __init__ import app, db, bcrypt, login_manager, Word, User, y200004, y200042, y200051, y200062, y200065, y200078, y200080, y200089, y200090, roles_required
import re, regex, pytz, random
from datetime import datetime
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError

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
    flash("You don't have access permission.", "unauthorized")
    return redirect(url_for('login'))

# # サインアップ用コントローラーの登録
# class SignupForm(FlaskForm):
#     username = StringField('username', validators=[DataRequired()])
#     password = PasswordField('password', validators=[DataRequired(), Length(min=4, max=50)])
#     privacypolicy = BooleanField()
#     submit = SubmitField('SIGNUP')

#     # 既存のユーザー名と同じものが入力されたらエラー判定を出す関数
#     # 正規表現以外の文字もエラー対象
#     def validate_username(self, username):
#         used_username = User.query.filter_by(username=username.data).first()
#         if used_username:
#             raise ValidationError('このユーザー名は既に使用されています。')
            
#         regular_word = regex.compile(r'^[0-9a-zA-Z０-９Ａ-Ｚａ-ｚ\p{Hiragana}\p{Katakana}\p{Han}]+$')
#         if not regular_word.match(username.data):
#             raise ValidationError('使用できない文字が含まれています。')

#     # パスワードの長さが４よりも少ない場合にエラー判定を出す関数
#     # 正規表現以外の文字もエラー対象
#     def validate_password(self, password):
#         if len(password.data) < 4:
#             raise ValidationError('パスワードは4文字以上で入力してください。')

#         regular_word = re.compile('^[0-9a-zA-Z]+$')
#         if not regular_word.match(password.data):
#             raise ValidationError('使用できない文字が含まれています。')

#     # 利用規約に同意しない場合にエラー判定を出す関数
#     def validate_privacypolicy(self, privacypolicy):
#         if privacypolicy.data == False:
#             raise ValidationError('利用規約に同意してください。')

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

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ログイン済みであればバリデーションチェックを飛ばす
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    # バリデーションチェック
    if form.validate_on_submit():
        # フォームに入力されたユーザー名と合致するユーザー名をusersテーブルから検索
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
                flash('This password is incorrect', 'password')

        # ユーザー名が合致しなかった場合
        else :
            flash('This username is incorrect', 'username')

    return render_template('login.html', form=form)

# マイページ
@app.route('/mypage/home')
@login_required
def home():
    print('\033[34m' + f'{current_user.id, type(current_user.id)}' + '\033[0m')    # 確認用
    return render_template('home.html')

# ライブラリページ
@app.route('/mypage/home/library')
@login_required
def library():
    return render_template('library.html')

# 学習コースページ
@app.route('/mypage/learnings')
@login_required
def learnings():
    return render_template('learnings.html')

# クイズページ
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

# テストコースページ
@app.route('/mypage/tasks')
@login_required
def tasks():
    ranks = ['A1', 'A2', 'B1', 'B2']
    params = []
    tester = current_user.id
    for rank in ranks:
        # テスト待ちの英単語群を取得
        datas = tester.query.filter_by(rank=rank, test_state='active').all()
        task = len(datas) // 20
        params.append(task)
    return render_template('tasks.html', tasks=params)

# テストページ
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

# 設定ページ
@app.route('/mypage/settings')
@login_required
def settings():
    return render_template('settings.html', 
    user_id=current_user.id, username=current_user.username, user_role=current_user.role)

# プロフィールページ
@app.route('/mypage/settings/profile')
@login_required
def profile():
    return render_template('profile.html', user_id=current_user.id, username=current_user.username, user_role=current_user.role, signup_date=current_user.signup_date)

# ログアウト
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
