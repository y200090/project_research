from __init__ import db, bcrypt, Word, User
import json, pytz, random
from datetime import datetime

# データベースを削除
db.drop_all()

# データベースを作成
db.create_all()

# wordsテーブルにデータを登録する関数
def insert_words():
    # 英単語データファイルの読み込み
    with open('./alldata-Freq.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i in range(len(data)):
        while True:
            response_number = random.randint(1, 100)
            correct_number = random.randint(1, 100)
            if response_number > correct_number:
                break
        # 読み込んだ英単語データをwordsテーブルに登録
        set_db = Word(id=data[i]["ID"], word=data[i]["word"], translation=data[i]["translation"], part_en=data[i]["part"], part_jp=data[i]["partJP"], rank=data[i]["rank"], response=response_number, correct=correct_number, freq_rank=data[i]["FreqRank"])

        # データベースに追加
        db.session.add(set_db)
        db.session.commit()
    
    print('\033[32m' + f'{len(data)}単語をデータベースに登録しました。' + '\033[0m')
insert_words()

# usersテーブルにテスターを登録する関数
def insert_testers():
    # testers = ['y200004', 'y200042', 'y200051', 'y200062', 'y200065', 'y200078', 'y200080', 'y200089', 'y200090']
    testers = ['Admin']
    for tester in testers:
        # 重複しないユーザー固有のIDを作成
        while True:
            user_id = random.randint(100000, 999999)
            if not user_id == User.query.filter_by(id=user_id).first():
                break

        print('\033[32m' + f'{tester}のIDは{user_id}' + '\033[0m')
        email = f'{tester}@admin.com'
        username = f'{tester}'
        password = 'abcdefg'
        hashed_password = bcrypt.generate_password_hash(password)
        tester = User(id=user_id, email=email, username=username, password=hashed_password, role='Admin', login_state='inactive', signup_date=datetime.now(pytz.timezone('Asia/Tokyo')), total_remembered=0)

        # データベースに追加
        db.session.add(tester)
        db.session.commit()
insert_testers()

# usersテーブルに登録されているユーザーのユーザー権限をアップグレードする関数
def upgrade_user():
    admin = User.query.filter_by(username='y200090').first()
    admin.role = 'Admin'

    # データベースを更新する
    db.session.commit()
# upgrade_user()
