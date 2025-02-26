import pandas as pd
import time
import sys
from find_pattern import predict
df = pd.read_csv('./dataset./levels.csv', header=None)


def print_output(sec):
    sys.stdout.write('\r' + ' ' + '\r')
    print(sec, end='', flush=True)


def count_down(sec):
    print(sec, end='', flush=True)
    while int(sec) > 0:
        time.sleep(1)
        sec = str(int(sec) - 1)
        # Clear the 'Thank you' message (move cursor to start of line, print spaces to overwrite)
        print_output(sec)


def train_dataset():
    for index, row in df.iterrows():
        # row = df.iloc[-1]
        row_list = row.dropna().tolist()
        pattern_length = len(row_list) + 1
        print(f' - {row_list[:10]}')
        while pattern_length - 5 > 0:
            pattern_length -= 1
            pattern_list = row_list[pattern_length - 5:]
            # print(pattern_list)
            predict(pattern_list, drop_index=index)
            length = len(pattern_list) - 5
            print(f'{length}/{len(row_list)}', end='', flush=True)
            print_output(f'{length}/{len(row_list) - 5}')
        print()
        count_down(2)


def train():
    while True:
        train_dataset()


if __name__ == "__main__":
    train_dataset()
