from __init__ import Word, User, record
import pandas as pd

testers = ['Y200004', 'Y200042', 'Y200051', 'Y200062', 'Y200065', 'Y200078', 'Y200080', 'Y200089']

def test_record():
    for tester in testers:
        users_data = User.query.filter_by(id=tester).first()
        words_datas = Word.query.filter_by(rank='B2').all()
        Record = record(tester)

        csv_data = []
        data_index = []
        for i in range(len(words_datas)):
            data_line = {}
            for j in range(users_data.test_challenge_number):
                records_data = Record.query.filter_by(word_id=words_datas[i].id, test_challenge_index=(j+1)).first()

                if records_data is None:
                    data_line[f'テスト{j + 1}'] = -1
                else:
                    data_line[f'テスト{j + 1}'] = records_data.test_response

            csv_data.append(data_line)
            data_index.append(words_datas[i].word)

        # データフレーム作成
        df = pd.DataFrame(data=csv_data, index=data_index)
        df.to_csv(f'{tester}_B2_test_record.csv', encoding='shift-jis')

def quiz_record():
    for tester in testers:
        users_data = User.query.filter_by(id=tester).first()
        words_datas = Word.query.filter_by(rank='B2').all()
        Record = record(tester)

        csv_data = []
        data_index = []
        for i in range(len(words_datas)):
            data_line = {}
            for j in range(users_data.quiz_challenge_number):
                records_data = Record.query.filter_by(word_id=words_datas[i].id, quiz_challenge_index=(j+1)).first()

                if records_data is None:
                    data_line[f'クイズ{j + 1}'] = -1
                else:
                    data_line[f'クイズ{j + 1}'] = records_data.quiz_response

            csv_data.append(data_line)
            data_index.append(words_datas[i].word)

        # データフレーム作成
        df = pd.DataFrame(data=csv_data, index=data_index)
        df.to_csv(f'{tester}_B2_quiz_record.csv', encoding='shift-jis')

def test_span():
    for tester in testers:
        users_data = User.query.filter_by(id=tester).first()
        words_datas = Word.query.filter_by(rank='B2').all()
        Record = record(tester)

        csv_data = []
        data_index = []
        for i in range(len(words_datas)):
            data_line = {}
            for j in range(users_data.test_challenge_number):
                records_data = Record.query.filter_by(word_id=words_datas[i].id, test_challenge_index=(j+1)).first()

                if records_data is None:
                    data_line[f'テスト{j + 1}'] = -1
                else:
                    data_line[f'テスト{j + 1}'] = records_data.response_span

            csv_data.append(data_line)
            data_index.append(words_datas[i].word)

        # データフレーム作成
        df = pd.DataFrame(data=csv_data, index=data_index)
        df.to_csv(f'{tester}_B2_test_span.csv', encoding='shift-jis')

def quiz_span():
    for tester in testers:
        users_data = User.query.filter_by(id=tester).first()
        words_datas = Word.query.filter_by(rank='B2').all()
        Record = record(tester)

        csv_data = []
        data_index = []
        for i in range(len(words_datas)):
            data_line = {}
            for j in range(users_data.quiz_challenge_number):
                records_data = Record.query.filter_by(word_id=words_datas[i].id, quiz_challenge_index=(j+1)).first()

                if records_data is None:
                    data_line[f'クイズ{j + 1}'] = -1
                else:
                    data_line[f'クイズ{j + 1}'] = records_data.response_span

            csv_data.append(data_line)
            data_index.append(words_datas[i].word)

        # データフレーム作成
        df = pd.DataFrame(data=csv_data, index=data_index)
        df.to_csv(f'{tester}_B2_quiz_span.csv', encoding='shift-jis')

# test_record()
# quiz_record()
test_span()
quiz_span()
