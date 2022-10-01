import os, functools
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user
from flask_bcrypt import Bcrypt

# Flaskインスタンスを作成
app = Flask(__name__)

# データベースの接続先を登録
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

# セッションの変更の追跡を無効
# データベースのメモリ消費を回避のため
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ターミナルにデータベースのログを出力
app.config['SQLALCHEMY_ECHO'] = True

# シークレットキーの登録
# セッション情報の暗号化のために必要、簡易な文字列は危険
app.config['SECRET_KEY'] = os.urandom(24)

# 日本語の文字化けを回避
app.config['JSON_AS_ASCII'] = False

# SQLAlchemyインスタンスを作成
db = SQLAlchemy(app)

# Bcryptインスタンスを作成
bcrypt = Bcrypt(app)

# LoginManagerインスタンスを作成
login_manager = LoginManager()

# 英単語データモデルの定義
class Word(db.Model):
    __tablename__ ="words"                          # テーブル名をwordsに再設定
    id = db.Column(db.Integer, primary_key=True)    # 英単語の固有ID
    word = db.Column(db.String(50))                 # 英単語
    translation = db.Column(db.String(50))          # 日本語訳
    part_en = db.Column(db.String(20))              # 品詞（英語）
    part_jp = db.Column(db.String(20))              # 品詞（日本語）
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    freq_rank = db.Column(db.String(100))           # 頻出度
    response = db.Column(db.Integer)                # 全ユーザーの解答数
    correct = db.Column(db.Integer)                 # 全ユーザーの正解数

    def __repr__(self):
        params = {
            'ID': self.id,
            'word': self.word,
            'translation': self.translation,
            'part_en': self.part_en,
            'part_jp': self.part_jp,
            'rank': self.rank,
            'freq_rank': self.freq_rank,
            'response': self.response,
            'correct': self.correct
        }
        return f"{params}\n"

# ユーザーモデルの定義
class User(db.Model, UserMixin):
    __tablename__ = "users"                               # テーブル名をusersに再設定
    id = db.Column(db.String(20), primary_key=True)       # ユーザーの固有ID
    username = db.Column(db.String(50), unique=True)      # ユーザー名
    password = db.Column(db.String(100))                  # パスワード
    role = db.Column(db.String(20))                       # ユーザー権限（Admin=管理者, Student=生徒）
    login_state = db.Column(db.String(20))                # ユーザー状態（active=ログイン中, inactive=ログアウト中）
    signup_date = db.Column(db.DateTime)                  # サインアップ日時
    login_date = db.Column(db.DateTime)                   # 最終ログイン日時
    total_answered = db.Column(db.Integer)                # クイズを解いた累計
    total_remembered = db.Column(db.Integer)              # ”覚えた”判定を出した累計

    def __repr__(self):
        params = {
            'ID': self.id,
            'username': self.username,
            'rolel': self.role,
            'login_state': self.login_state,
            'signup_date': self.signup_date,
            'login_date': self.login_date,
            'total_answered': self.total_answered,
            'total_remembered': self.total_remembered
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200004(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200042(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200051(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200062(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200065(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200078(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200080(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーの成績データモデルの定義
class y200089(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"
        
# ユーザーの成績データモデルの定義
class y200090(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                 # 英単語固有のID
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)           # クイズにおける解答数の累計
    quiz_correct = db.Column(db.Integer)            # クイズにおける正解数の累計
    test_correct = db.Column(db.Integer)            # テストにおける連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))           # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)          # 解答した日時

    def __repr__(self):
        params = {
            'order': self.id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date
        }
        return f"{params}\n"

# ユーザーロールでアクセス制限をかける関数デコレータ
def roles_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role == 'Student':
            return 'アクセス権限がありません。'
        elif current_user.role == 'Admin':
            return view(**kwargs)
    return wrapped_view
