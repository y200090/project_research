from __init__ import db, bcrypt, Word, User
import json, pytz, random, string
from datetime import datetime

# データベースを初期化する関数
def init_db():
    # データベースを削除
    db.drop_all()
    # データベースを作成
    db.create_all()

# wordsテーブルに英単語データを登録する関数
def insert_words():
    # 英単語データファイルの読み込み
    with open('./alldata-Freq.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        # ランダムで解答数と正解数を設定
        while True:
            response_number = random.randint(1, 100)
            correct_number = random.randint(1, 100)
            if response_number > correct_number:
                break
            
        # 読み込んだ英単語データをwordsテーブルに登録
        set_db = Word(id=data[i]["ID"], word=data[i]["word"], translation=data[i]["translation"], part_en=data[i]["part"], part_jp=data[i]["partJP"], rank=data[i]["rank"], freq_rank=data[i]["FreqRank"], response=response_number, correct=correct_number)

        # データベースに追加
        db.session.add(set_db)

    # データベースを更新
    db.session.commit()
    
    # ログ確認用
    print('\033[32m' + f'{Word.query.count()}単語をデータベースに登録しました。' + '\033[0m')

# 重複しないランダムな文字列を作成する関数
def generate_password(n):
    return ''.join(random.sample(string.ascii_letters + string.digits, k=n))

# usersテーブルに管理者ユーザーを追加する関数
def insert_admin():
    admins = {
        'Y200090': '森裕都'
    }

    for admin_id in admins.keys():
        id = f"{admin_id}"
        username = f"{admins[admin_id]}"
        password = 'abcdefg'
        hashed_password = bcrypt.generate_password_hash(password)
        role = 'Admin'
        login_state = 'inactive'
        signup_date = datetime.now(pytz.timezone('Asia/Tokyo'))
        total_quiz_response = 0
        total_quiz_correct = 0
        total_test_response = 0
        total_remembered = 0
        quiz_challenge_number = 0
        test_challenge_number = 0
    
        # 管理者ユーザーをusersテーブルに登録
        admin = User(
            id=id, 
            username=username, 
            password=hashed_password, 
            role=role, 
            login_state=login_state, 
            signup_date=signup_date, 
            total_quiz_response=total_quiz_response, 
            total_quiz_correct = 
            total_quiz_correct, 
            total_test_response=total_test_response, 
            total_remembered=total_remembered, 
            quiz_challenge_number = quiz_challenge_number, 
            test_challenge_number = test_challenge_number
        )

        # データベースに追加
        db.session.add(admin)

        # ログ確認用
        print('\033[32m' + f'{username} さんを“管理者”として登録しました。' + '\033[0m')

    # データベースを更新
    db.session.commit()

# usersテーブルにテスターを登録する関数
def insert_testers():
    testers = {
        'Y200004': '安部凌平',
        'Y200042': '小橋口純',
        'Y200051': '猿渡脩大',
        'Y200062': '竹本来生',
        'Y200065': '玉井信',
        'Y200078': '前川悠人',
        'Y200080': '松本⻁太郎',
        'Y200089': '森昂誠'
    }

    for tester_id in testers.keys():
        id = f"{tester_id}"
        username = f"{testers[tester_id]}"
        password = f"{tester_id}"
        hashed_password = bcrypt.generate_password_hash(password)
        role = 'Tester'
        login_state = 'inactive'
        signup_date = datetime.now(pytz.timezone('Asia/Tokyo'))
        total_quiz_response = 0
        total_quiz_correct = 0
        total_test_response = 0
        total_remembered = 0
        quiz_challenge_number = 0
        test_challenge_number = 0

        # usersテーブルにテスターを登録
        tester = User(
            id=id, 
            username=username, 
            password=hashed_password, 
            role=role, 
            login_state=login_state, 
            signup_date=signup_date, 
            total_quiz_response=total_quiz_response, 
            total_quiz_correct = total_quiz_correct, 
            total_test_response=total_test_response, 
            total_remembered=total_remembered, 
            quiz_challenge_number = quiz_challenge_number, 
            test_challenge_number = test_challenge_number
        )

        # データベースに追加
        db.session.add(tester)

        # ログ確認用
        print('\033[32m' + f'{username} さんを“テスター”として登録しました。' + '\033[0m')
    
    # データベースを更新
    db.session.commit()

init_db()
insert_words()
insert_admin()
insert_testers()
