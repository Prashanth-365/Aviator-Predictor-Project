import pandas as pd
from score_board import score_board
import re
import json
import sys

VALUES = {2: "H", 0: "L"}
score_board_path = 'dataset/score.csv'


def print_output(x):
    sys.stdout.write('\r' + ' ' + '\r')
    print(x,end='', flush=True)


def print_dict(dict):
    for key, value in dict.items():
        print(f"{key} : {value}")


def convert_to_str(row):
    string = ''
    for i in row:
        if pd.notna(i):
            string += i
    return string


def match_pattern(dataset, pattern):
    with open("dataset/patterns.json", "r") as file:
        patterns_counts = json.load(file)
        result = {}
        for i in range(2, len(pattern)+1):
            current_pattern = pattern[:i]
            if current_pattern in patterns_counts:
                if len(current_pattern) > 1:
                    result[current_pattern] = patterns_counts[current_pattern]
        return result


def update_score(df, row, col, path):
    if col >= len(df.columns):
        # Add columns until we reach the desired column
        for _ in range(col - len(df.columns) + 3):
            df[len(df.columns)] = 1

    # if pd.isna(df.iloc[row, col]):
    #     df.iloc[row, col] = 1  # If it doesn't exist, set it to 1
    else:
        df.iloc[row, col] += 1  # If it exists, increment the value

    # Save the updated DataFrame back to the CSV file
    df.to_csv(path, index=False)


def predicted_report(last_row):
    result, patt, length, key = predict(last_row, drop_index='')
    # for pat, val in result.items():
    #     print(f"{pat} : {val}")
    # for pat, val in result.items():
    #     print(f"{pat}({len(pat)}) : {val}")
    print(f"result - ({key} ", end="-")
    return key


def predict(last_row, drop_index):
    data = pd.read_csv('dataset/levels.csv', header=None)
    if drop_index:
        data = data.drop(index=drop_index)
    counts_init = {"L": 0, "H": 0}
    counts = counts_init.copy()
    for index, row in data.iterrows():
        for key in row:
            if key in counts:
                counts[key] += 1
    data_len = sum(counts.values())

    if not last_row:
        last_row = data.iloc[-1]

    keyword = last_row[0]

    pattern = convert_to_str(last_row)

    sum_dict = {"H": 0, "L": 0}
    result_without_scores = match_pattern(data, pattern)
    dif = {}
    for pat, values in result_without_scores.items():
        lst = []
        for val in values.values():
            lst.append(val)
        s = sum(lst)
        dif[pat] = round(lst[1]/s - lst[0]/s, 2)  # difference of probabilities
        # for sub_key, value in values.items():
        #     probability = (value / s)
        #     result_without_scores[pat][sub_key] = probability
    result_with_scores, q = score_board(dif, keyword, score_board_path, mode='multiply')

    result, key = score_board(result_with_scores, keyword, score_board_path, mode='insert')
    return result_with_scores, pattern, data_len, key


# while pattern != 'close':
#     pattern = input('Enter pattern: ')
#     predicted_report(pattern)
