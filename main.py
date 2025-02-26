import time
import json
import re

from data_handler import WriteToCsv
from scan_image import extract_numbers_from_image, capture_image
from merge_data import *
from find_pattern import predicted_report, convert_to_str, print_output
from train_data import train_dataset
from from_web import *

VALUES = {2: "H", 0: "L"}
values_dir = './dataset/values.csv'
levels_dir = './dataset/levels.csv'
image_folder = './dataset/images'
webcam_id = 1
captured_image_path = './dataset/Captured_image.png'
input_bets_1 = {"bets": [15, 10], "cash_outs": [1.67, 2]}
input_bets_2 = {"bets": [30, 20], "cash_outs": [1.67, 2]}

bets_button = [
    "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button",
    "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[2]/div/div[2]/div[2]/button"
]
prev_letter = ""
bal = 150

data_handler = WriteToCsv(values_dir, levels_dir, VALUES)


def arrange_data():
    merge_all_rows()
    data_handler.convert_all_values_to_levels()


def generate_patterns():
    patterns_counts = {}
    r = int(input("Enter Max Pattern Length: "))
    INIT = {"L": 0, "H": 0}
    data = pd.read_csv('dataset/levels.csv', header=None)
    for index, row in data.iloc[:-1].iterrows():
        string = convert_to_str(row)
        print_output(index)
        for n in range(2, r + 1):
            for i in range(2 ** n):
                num = f"{i:0{n}b}"  # Generate the binary representation
                num = num.replace('1', 'H').replace('0', 'L')  # Replace 1 with H and 0 with L
                current_pattern = num
                pat_len = len(current_pattern)
                if current_pattern in string[1:]:
                    if current_pattern not in patterns_counts:
                        patterns_counts[current_pattern] = INIT.copy()

                    # Use re.finditer with a lookahead to include overlapping matches
                    values = [string[match.start() - 1] for match in re.finditer(f"(?={current_pattern})", string) if
                              match.start() > 0]

                    # Count occurrences of each value
                    for key in INIT:
                        patterns_counts[current_pattern][key] += values.count(key)
    with open("dataset/patterns.json", "w") as file:
        json.dump(patterns_counts, file)
    print("\n Completed")


def capture_data():
    # data = capture_image(webcam_id, captured_image_path)
    # data = [1.96,1.12,1.4,1.59,1.52,10.08,9.37,1.69]
    data = get_multipliers()
    df = pd.read_csv(values_dir, header=None)
    last = df.iloc[-1].tolist()
    if data:
        merged = merge_two_rows(last, data)
        # print(merged)
        if merged:
            merge = True
            data = merged
        else:
            merge = False
        data_handler.insert_values(data, merge)
        # train_dataset()


def start(multiplier):
    output_df = pd.read_csv("output.csv")
    global prev_letter, bal
    multiplier = float(multiplier)
    df = pd.read_csv(values_dir, header=None)
    last_row = df.iloc[-1].tolist()
    last_row.insert(0, multiplier)
    df.iloc[-1] = last_row[:len(df.columns)]
    df.to_csv(values_dir, header=False, index=False)
    letter = ''
    for key in VALUES:
        if multiplier >= key:
            letter = VALUES[key]
            break
    df = pd.read_csv(levels_dir, header=None)
    last_row = df.iloc[-1].tolist()
    last_row.insert(0, letter)
    df.iloc[-1] = last_row[:len(df.columns)]
    df.to_csv(levels_dir, header=False, index=False)
    if prev_letter == 'H':
        bal -= 25  # bet
        if multiplier >= 2:
            bal += 45  # Equivalent to +25 and +20
        elif multiplier >= 1.67:
            bal += 25  # Equivalent to +25 - 10
    t = int(time.time())
    print(f" {letter}) - {multiplier}", end=" ")
    if prev_letter == letter:
        print("|", bal, t)
    else:
        print(" ", bal, t)
    length = len(output_df)
    output_df.loc[length, "predicted"] = prev_letter
    output_df.loc[length, "actual"] = letter
    output_df.loc[length, "multiplier"] = multiplier # f"{multiplier}"
    output_df.loc[length, "balance"] = bal # f"{bal}"
    output_df.loc[length, "time"] = t # f"{t}"
    prev_letter = predicted_report(last_row='')
    # output_df = output_df._append(new_row, ignore_index=True)
    output_df.to_csv("output.csv", index=False)
    # print(" - ", round(time.time() - a, 1))


if __name__ == "__main__":
    # arrange_data()
    capture_data()
    end_program = True
    while end_program:
        # action = input("""
        # C - capture image from screen
        # S - To scan multiple images from the folder
        # A - To arrange and formulate dataSet
        # I - To predict instantly
        # or input value manually
        # close - To stop the program
        # Select what action you need to perform: """).lower()
        action = input("Enter Input: ").lower()
        if action == "close":
            end_program = False
        elif action == "c":
            capture_data()

        elif action == "g":
            generate_patterns()

        elif action == "a":
            arrange_data()
        elif action == "i":
            pass

        elif action == "auto":
            while True:
                if next_bet():
                    multi = get_multipliers()[0]
                    start(multi)
                    time.sleep(2)
        elif action == "auto bet":
            init_auto(input_bets_1)
            while True:
                if next_bet():
                    # press_buttons(bets_button)
                    multi = get_multipliers()[0]
                    start(multi)
                    time.sleep(2)


        else:
            if action is not None:
                start(action)
            else:
                print("Error! enter a input")
