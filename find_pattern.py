import pandas as pd
from score_board import score_board


VALUES = {10: 'H', 2: 'M', 0: 'L'}
score_board_path = 'dataset/score.csv'


def convert_to_str(row):
    string = ''
    for i in row:
        if pd.notna(i):
            string += i
    return string


def match_pattern(dataset, pattern):
    result = {}
    for index, row in dataset.iloc[:-1].iterrows():
        string = convert_to_str(row)
        for i in range(1, len(pattern)+1):
            # i = len(pattern)#6
            current_pattern = pattern[:i]
            if current_pattern in string[1:]:
                if len(current_pattern) > 1:
                    if current_pattern not in result:
                        result[current_pattern] = {'L': 0, 'M': 0, 'H': 0}
                    for d in range(1, len(string)):
                        a = string[d:d+i]
                        if current_pattern == a:
                            match = string[d-1]
                            result[current_pattern][match] += 1
        # else:
        #     break
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
    result, patt, length = predict(last_row, drop_index='')
    # for pat, values in result.items():
    #     print(f"{pat} : {values}")
    pattern_len = 0
    for pat, values in result.items():
        if len(pat) > pattern_len:
            pattern_len = len(pat)
        max_key = max(values, key=values.get)
        print(f"{pat}({len(pat)}) : {max_key}")
    print()
    print(f"{patt[:pattern_len]}-({pattern_len})\n")
    print('\ndataset length -', length)


def predict(last_row, drop_index):
    data = pd.read_csv('dataset/levels.csv', header=None)
    if drop_index:
        data = data.drop(index=drop_index)
    counts = {'L': 0, 'M': 0, 'H': 0}

    for index, row in data.iterrows():
        for key in row:
            if key in counts:
                counts[key] += 1
    data_len = sum(counts.values())

    if not last_row:
        last_row = data.iloc[-1]

    keyword = last_row[0]

    pattern = convert_to_str(last_row)

    sum_dict = {'L': 0, 'M': 0, 'H': 0}
    result_without_scores = match_pattern(data, pattern)

    for pat, values in result_without_scores.items():
        for sub_key, value in values.items():
            probability = ((value * len(pat)) / counts[sub_key])
            result_without_scores[pat][sub_key] = probability
    for pat, values in result_without_scores.items():
        values_sum = sum(values.values())
        for sub_key, value in values.items():
            result_without_scores[pat][sub_key] = round(value / values_sum, 6)
    result_with_scores, q = score_board(result_without_scores, keyword, score_board_path, mode='multiply')
    for key, values in result_with_scores.items():
        for sub_key, value in values.items():
            sum_dict[sub_key] += value
    result_with_scores['sum'] = sum_dict
    highest = {'L': 0, 'M': 0, 'H': 0}
    result = {'L': 0, 'M': 0, 'H': 0}
    for key, values in result_with_scores.items():
        max_key = max(values, key=values.get)
        if values[max_key] >= highest[max_key] and key != 'sum':
            highest[max_key] = values[max_key]
            result[max_key] = len(key)
        # for sub_key, value in values.items():
        #     if value > highest[sub_key] and key != 'sum':
        #         highest[sub_key] = value
        #         result[sub_key] = len(key)
    # for pat, values in result_with_scores.items():
    #     if pat != 'sum':
    #         max_key = max(values, key=values.get)
    #         if max_key in highest:
    #             highest[max_key] += values[max_key]
    #         else:
    #             highest[max_key] = values[max_key]
    result_with_scores['highest'] = highest
    result_with_scores['result'] = result
    r, max_score_index = score_board(result_with_scores, keyword, score_board_path, mode='insert')
    for key, value in result_with_scores['result'].items():
        # print(value, max_score_index)
        if value == max_score_index:
            # print("**********There is a high chance of getting********** \n----", key, max_score_index, "----")
            pass
    return result_with_scores, pattern, data_len


# while pattern != 'close':
#     pattern = input('Enter pattern: ')
#     predicted_report(pattern)
