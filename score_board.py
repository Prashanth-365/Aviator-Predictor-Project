import pandas as pd
# 2706,6415,42.18
# 143,247,57.89

pattern = {
    'dsa': {'l': 0, 'L': 2, 'M': 3, 'h': 2, 'H': 0, 'X': 0},
    'da': {'l': 9, 'L': 2, 'M': 3, 'h': 2, 'H': 0, 'X': 0},
    'a': {'l': 0, 'L': 0, 'M': 0, 'h': 1, 'H': 9, 'X': 0},
    'sum': {'l': 0, 'L': 0, 'M': 7, 'h': 1, 'H': 0, 'X': 7}
}


def score_board(result, key, path, mode):
    df = pd.read_csv(path)

    score = df.iloc[0, 1:].tolist()
    if '0' in score:
        # Add 100 to the entire second row (except the first column)
        for i in range(1, len(df.columns)):
            df.iloc[0, i] = int(df.iloc[0, i]) + 100
        df.to_csv(path, index=False)
    # col = 50
    # if col >= len(df.columns):
    #     # Add columns until we reach the desired column
    #     for _ in range(col - len(df.columns) + 1):
    #         df[len(df.columns)] = 1
    row = 1
    max_score_index = 0
    if mode == 'insert':
        prob = pd.read_csv('./dataset/probability.csv')
        a = []
        num = []
        for i in range(len(df.columns)):
            a.append(df.iloc[1, i])
            num.append(int(df.iloc[0, i]))
            df.iloc[1, i] = 'a'
        max_score_index = num.index(max(num)) + 3
        # for letter, col in result['result'].items():
        # for pat, values in result.items():
        #     col = len(pat)
        for col in range(1, len(a)):
            letter = 'a'
            # print(letter, col, a[col], end=' - ')
            if a[col] == key or (a[col] != 'L' and key != 'L' and a[col] != 'a'):
                df.iloc[row - 1, col] = int(df.iloc[row - 1, col]) + 1
                prob.loc[0, 'right_count'] += 1
                prob.loc[0, 'total'] += 1
                break
                # print('plus')
            elif a[col] != 'a':
                df.iloc[row - 1, col] = int(df.iloc[row - 1, col]) - 1
                prob.loc[0, 'total'] += 1
            #     print('minus')
            # else:
            #     print('No')
            # max_key = max(values, key=values.get)
        max_key = max(result['highest'], key=result['highest'].get)
        df.iloc[row, result['result'][max_key]] = max_key  # If it exists, increment the value;
        prob.loc[0, 'probability'] = round(prob.loc[0, 'right_count'] / prob.loc[0, 'total'] * 100, 2)
        prob.to_csv('./dataset/probability.csv', index=False, mode='w')
    else:
        for pat, values in result.items():
            col = len(pat)
            if pat != 'sum' and pat != 'highest' and pat != 'result':
                multiplier = df.iloc[row - 1, col]
                for k in values:
                    result[pat][k] *= int(multiplier)
    df.to_csv(path, index=False)
    return result, max_score_index
