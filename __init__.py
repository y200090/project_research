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

# 英単語データの定義
class Word(db.Model):
    __tablename__ ="words"                                          # テーブル名をwordsに再設定
    id = db.Column(db.Integer, primary_key=True)                    # 英単語の固有ID
    word = db.Column(db.String(50), nullable=False)                 # 英単語
    translation = db.Column(db.String(50), nullable=False)          # 日本語訳
    part_en = db.Column(db.String(20), nullable=False)              # 品詞（英語）
    part_jp = db.Column(db.String(20), nullable=False)              # 品詞（日本語）
    rank = db.Column(db.String(10), nullable=False)                 # A1, A2, B1, B2
    freq_rank = db.Column(db.String(100))                           # 頻出ランク
    response = db.Column(db.Integer)                                # 全体の出題数
    correct = db.Column(db.Integer)                                 # 全体の正解数

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
    __tablename__ = "users"                                             # テーブル名をusersに再設定
    id = db.Column(db.Integer, primary_key=True)                        # ユーザーの固有ID
    # email = db.Column(db.String(100), unique=True, nullable=False)      # メールアドレス
    username = db.Column(db.String(50), unique=True, nullable=False)    # ユーザー名
    password = db.Column(db.String(100), nullable=False)                # パスワード
    role = db.Column(db.String(20), nullable=False)                     # ユーザー権限（Admin, Tester, Student）
    login_state = db.Column(db.String(20), nullable=False)              # ユーザー状態（active, inactive）
    signup_date = db.Column(db.DateTime, nullable=False)                # サインアップ日時
    login_date = db.Column(db.DateTime)                                 # ログイン日時
    total_remembered = db.Column(db.Integer)                            # ”覚えた”判定を出した累計

    def __repr__(self):
        params = {
            'ID': self.id,
            # 'email': self.email,
            'username': self.username,
            'role': self.role,
            'login_state': self.login_state,
            'signup_date': self.signup_date,
            'login_date': self.login_date,
            'total_remembered': self.total_remembered
        }
        return f"{params}\n"

# ユーザー個人の成績データの定義
class Record(db.Model):
    __tablename__ = "records"                                 # テーブル名をrecordsに再設定
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)           # ユーザーの固有ID
    word_id = db.Column(db.Integer, nullable=False)           # 英単語固有のID
    rank = db.Column(db.String(10), nullable=False)           # A1, A2, B1, B2
    test_correct = db.Column(db.Integer)                      # ユーザー個人のテストの正解数（test_correct > 0 : 復習待ち）
    test_state = db.Column(db.String(20), nullable=False)     # テスト待ち状態（active, inactive）

    def __repr__(self):
        params = {
            'user_id': self.user_id,
            'word_id': self.word_id,
            'rank': self.rank,
            'test_correct': self.test_correct,
            'test_state': self.test_state
        }
        return f"{params}\n"

# ユーザーロールでアクセス制限をかける関数デコレータ
def roles_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role == 'Student' or current_user.role == 'Tester':
            return 'null'
        elif current_user.role == 'Admin':
            return view(**kwargs)
    return wrapped_view
