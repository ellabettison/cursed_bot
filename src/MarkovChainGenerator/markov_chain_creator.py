import pandas as pd
import csv
from numpy.random import choice, randint
import sqlite3 as db

from message_generator import CommentType

end_words = []


def write_to_file(data, num):
    file_name = 'reddit_sarcastic' + num + '.csv'
    file = open(file_name, "w")
    file.close()

    data.to_csv(r'reddit_sarcastic' + num + '.csv')


def read_from_file(path):
    data = pd.read_csv(path)
    return data


def combine_files(path1, path2, num):
    data1 = pd.read_csv(path1)
    data2 = pd.read_csv(path2)
    data_comb = pd.concat([data1, data2])
    write_to_file(data_comb, num)


def clean_data(data):
    print(len(data))
    i = 0
    while i < len(data):
        try:
            if len(data[i]) == 0:
                data.pop(i)
            elif data[i][0] in ['@', '.', '&']:
                data.pop(i)
            elif 'http' in data[i]:
                data.pop(i)
            elif '&' in data[i]:
                ind = data[i].find('&')
                data[i] = data[i][ind:]
            else:
                i += 1
        except:
            print(i)
            print(data[i])
    return data


def generate_pol(start):
    conn = db.connect('MarkovChainGenerator/pol/database.sqlite')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    bodys = c.execute('SELECT body FROM 129419703').fetchall()
    print(bodys)


def generate_sexism(start):
    all_words = []
    df = pd.read_excel('MarkovChainGenerator/sexism/sexist_data.xlsx', sheet_name=0)
    words_list = df['Sentences'].tolist()
    list_values = df['Label'].tolist()
    line_count = 0
    word_count = 0
    print("~~~~~~~~~~##     DOING")
    while line_count < len(words_list):
        row = words_list[line_count]
        if list_values[line_count] == 0:
            words_list.pop(line_count)
            list_values.pop(line_count)
            continue
        else:
            # print(row)
            # print(row[1])
            for word in row.split(' '):
                word_count += 1
                all_words.append(word)
                try:
                    if word[-1] in ['.', '?', '!'] and word != '.':
                        end_words.append(word)
                except IndexError:
                    pass

            all_words.append('.')
            line_count += 1
    print("\n\nLINES ANALYSED: " + str(line_count))
    print("\n\nWORDS ANALYSED: " + str(word_count))
    print(all_words)
    return generate_words(all_words, start)



def generate_hate_speech(start):
    all_words = []
    with open('MarkovChainGenerator/hate_speech/labeled_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        word_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(row[1])
                for word in row[6].split(' '):
                    word_count += 1
                    all_words.append(word)
                    try:
                        if word[-1] in ['.', '?', '!'] and word != '.':
                            end_words.append(word)
                    except IndexError:
                        pass

                all_words.append('.')
                line_count += 1
    print("\n\nLINES ANALYSED: " + str(line_count))
    print("\n\nWORDS ANALYSED: " + str(word_count))
    all_words = clean_data(all_words)
    return generate_words(all_words, start)


def generate_sarcasm(start):
    all_words = []
    with open('MarkovChainGenerator/sarcasm/train-balanced-sarcasm.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        word_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(row[1])
                for word in row[1].split(' '):
                    word_count += 1
                    all_words.append(word)
                    try:
                        if word[-1] in ['.', '?', '!'] and word != '.':
                            end_words.append(word)
                    except IndexError:
                        pass

                all_words.append('.')
                line_count += 1
    print("\n\nLINES ANALYSED: " + str(line_count))
    print("\n\nWORDS ANALYSED: " + str(word_count))
    return generate_words(all_words, start)


def generate_words(all_words, start):

    # print(end_words)

    # num = 100000
    num = 7455
    # for i in range(start, 105):

    print("START: " + str(start * num) + " END: " + str((start * num) + num))
    words = all_words[start * num:(start * num) + num]
    # words = all_words

    dict_df = pd.DataFrame(columns=['lead', 'follow', 'freq'])
    dict_df['lead'] = words
    follow = words[1:]
    follow.append('EndWord')
    dict_df['follow'] = follow
    print(0)
    dict_df['freq'] = dict_df.groupby(by=['lead', 'follow'])['lead', 'follow'].transform('count').copy()
    print(1)
    dict_df = dict_df.drop_duplicates()
    pivot_df = dict_df.pivot(index='lead', columns='follow', values='freq')
    print(2)
    sum_words = pivot_df.sum(axis=1)
    pivot_df = pivot_df.apply(lambda x: x / sum_words)
    print(3)

    # total_dict_df = pd.concat([total_dict_df, pivot_df], axis=0)

    print(pivot_df)

    return pivot_df

    # file_name = 'reddit_sarcastic' + str(i) + '.csv'
    # file = open(file_name, "w")
    # file.close()
    #
    # pivot_df.to_csv(r'reddit_sarcastic' + str(i) + '.csv', index=False)


def generate_sentence(pivot_df, start, length):
    current_word = start
    sentence = [current_word]
    while len(sentence) < length:
        next_word = choice(a=list(pivot_df.columns), p=
        pivot_df.iloc[pivot_df.index == current_word].fillna(0).values[0])
        if next_word == 'EndWord':
            continue
        elif next_word in end_words:
            if len(sentence) > 2:
                sentence.append(next_word)
                break
            else:
                continue
        else:
            sentence.append(next_word)
        current_word = next_word
    sentence = ' '.join(sentence)
    return sentence


def get_pivot(type):
    if type == CommentType.HATE:
        return generate_hate_speech(randint(0, 3))
    elif type == CommentType.SARCASTIC:
        return generate_sarcasm(randint(0,105))
