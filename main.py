import pandas as pd
from data_handler import WriteToCsv
from scan_image import extract_numbers_from_image, capture_image
from merge_data import *
from find_pattern import predicted_report
from train_data import train_dataset
VALUES = {10: 'H', 2: 'M', 0: 'L'}
values_dir = './dataset/values.csv'
levels_dir = './dataset/levels.csv'
image_folder = './dataset/images'
webcam_id = 1
captured_image_path = './dataset/Captured_image.png'

data_handler = WriteToCsv(values_dir, levels_dir, VALUES)


def arrange_data():
    merge_all_rows()
    data_handler.convert_all_values_to_levels()


def capture_data():
    data = capture_image(webcam_id, captured_image_path)
    # data = [1.96,1.12,1.4,1.59,1.52,10.08,9.37,1.69]
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


if __name__ == "__main__":
    # arrange_data()
    capture_data()
    end_program = True
    while end_program:
        action = input("""
        C - capture image from screen
        S - To scan multiple images from the folder
        A - To arrange and formulate dataSet
        I - To predict instantly
        or input value manually
        close - To stop the program
        Select what action you need to perform: """).lower()
        if action == "close":
            end_program = False
        elif action == "c":
            capture_data()

        elif action == "s":
            pass

        elif action == "a":
            arrange_data()
        elif action == "i":
            pass

        else:
            if action is not None:
                action = float(action)
                df = pd.read_csv(values_dir, header=None)
                last_row = df.iloc[-1].tolist()
                last_row.insert(0, action)
                df.iloc[-1] = last_row[:len(df.columns)]
                df.to_csv(values_dir, header=False, index=False)
                letter = ''
                for key in VALUES:
                    if action >= key:
                        letter = VALUES[key]
                        break
                df = pd.read_csv(levels_dir, header=None)
                last_row = df.iloc[-1].tolist()
                last_row.insert(0, letter)
                df.iloc[-1] = last_row[:len(df.columns)]
                df.to_csv(levels_dir, header=False, index=False)
                # letter = ''
                predicted_report(last_row='')
                print(action, '-', letter)
            else:
                print("Error! enter a input")
