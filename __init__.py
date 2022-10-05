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
# データベースのメモリ消費を回避
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
    __tablename__ = "words"                          # テーブル名をwordsに再設定
    id = db.Column(db.Integer, primary_key=True)    # 英単語の固有ID
    word = db.Column(db.String(50))                 # 英単語
    translation = db.Column(db.String(50))          # 日本語訳
    part_en = db.Column(db.String(20))              # 品詞（英語）
    part_jp = db.Column(db.String(20))              # 品詞（日本語）
    rank = db.Column(db.String(10))                 # A1, A2, B1, B2
    freq_rank = db.Column(db.String(100))           # 頻出度
    response = db.Column(db.Integer)                # 解答された累計
    correct = db.Column(db.Integer)                 # 正解された累計

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
    role = db.Column(db.String(20))                       # ユーザー権限（Admin=管理者, Tester=テスター, Student=生徒）
    login_state = db.Column(db.String(20))                # ログイン状態（active=ログイン中, inactive=ログアウト中）
    signup_date = db.Column(db.DateTime)                  # サインアップ日時
    login_date = db.Column(db.DateTime)                   # 最終ログイン日時
    total_quiz_response = db.Column(db.Integer)           # クイズの解答数の累計
    total_quiz_correct = db.Column(db.Integer)            # クイズの正解数の累計
    total_test_response = db.Column(db.Integer)           # テストの解答数の累計
    total_remembered = db.Column(db.Integer)              # “覚えた”判定を出した累計（テストの正解数の累計）
    quiz_challenge_number = db.Column(db.Integer)         # クイズに挑戦した累計
    test_challenge_number = db.Column(db.Integer)         # テストに挑戦した累計

    def __repr__(self):
        params = {
            'ID': self.id,
            'username': self.username,
            'role': self.role,
            'login_state': self.login_state,
            'signup_date': self.signup_date,
            'login_date': self.login_date,
            'total_quiz_response': self.total_quiz_response,
            'total_quiz_correct': self.total_quiz_correct,
            'total_test_response': self.total_test_response,
            'total_remembered': self.total_remembered,
            'quiz_challenge_number': self.quiz_challenge_number,
            'test_challenge_number': self.test_challenge_number
        }
        return f"{params}\n"

# 生徒の成績データモデルの定義
class Student(db.Model):
    __tablename__ = "students"                         # テーブル名をstudentsに再設定
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    user_id = db.Column(db.Integer)                    # ユーザー固有のID
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'user_id': self.user_id,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200004(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200042(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200051(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200062(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200065(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200078(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200080(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200089(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# テスターの成績データモデルの定義
class Y200090(db.Model):
    order = db.Column(db.Integer, primary_key=True)    # テーブルに追加された順番
    word_id = db.Column(db.Integer)                    # 英単語固有のID
    rank = db.Column(db.String(10))                    # A1, A2, B1, B2
    quiz_response = db.Column(db.Integer)              # クイズでの解答数の累計
    quiz_correct = db.Column(db.Integer)               # クイズでの正解数の累計
    test_response = db.Column(db.Integer)              # テストでの解答数の累計
    test_correct = db.Column(db.Integer)               # テストでの連続正解数（一度でも間違えれば0に）
    word_state = db.Column(db.String(20))              # 英単語の状態（test_state=テスト待ち, quiz_state=学習待ち, review_state=復習待ち）
    response_date = db.Column(db.DateTime)             # 解答した日時
    quiz_challenge_index = db.Column(db.Integer)       # ユーザーが解答したクイズのタイミング
    test_challenge_index = db.Column(db.Integer)       # ユーザーが解答したテストのタイミング

    def __repr__(self):
        params = {
            'order': self.order,
            'word_id': self.word_id,
            'rank': self.rank,
            'quiz_response': self.quiz_response,
            'quiz_correct': self.quiz_correct,
            'test_response': self.test_response,
            'test_correct': self.test_correct,
            'word_state': self.word_state,
            'response_date': self.response_date,
            'quiz_challenge_index': self.quiz_challenge_index,
            'test_challenge_index': self.test_challenge_index
        }
        return f"{params}\n"

# ユーザーロールでアクセス制限をかける関数デコレータ
def roles_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if current_user.role == 'Student' or current_user.role == 'Tester':
            return 'アクセス権限がありません。'
        elif current_user.role == 'Admin':
            return view(**kwargs)
    return wrapped_view

# ユーザーの成績データモデルを返す関数
def record(id):
    testers = [Y200004, Y200042, Y200051, Y200062, Y200065, Y200078, Y200080, Y200089, Y200090]

    for tester in testers:
        if tester.__name__ == id:
            return tester
    else:
        return Student
