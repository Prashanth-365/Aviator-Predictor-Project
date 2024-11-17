import pandas as pd
import os


class WriteToCsv:
    def __init__(self, values_dir, levels_dir, values_list):
        self.values_dir = values_dir
        self.letters_dir = levels_dir
        self.values_list = values_list

    def write_data(self, data, path, merge):
        if merge:
            df = pd.read_csv(path, header=None)
            df = df.drop(df.index[-1]).reset_index(drop=True)
            new_row_df = pd.Series(data).to_frame().T
            df = pd.concat([df, new_row_df], ignore_index=True)
            df.to_csv(path, index=False, header=False)
        else:
            df = pd.DataFrame([data])
            df.to_csv(path, index=False, mode='a', header=False)
        return data

    def convert_all_values_to_levels(self):
        df = pd.DataFrame()
        df.to_csv(self.letters_dir, header=False)
        data = pd.read_csv(self.values_dir, header=None, on_bad_lines='skip')
        for i, row in data.iterrows():
            self.convert_row_value_to_level(row, merge=False)

    def convert_row_value_to_level(self, data, merge):
        letters = []
        for value in data:
            letter = ''
            for key in self.values_list:
                if float(value) >= key:
                    letter = self.values_list[key]
                    break
            letters.append(letter)
        self.write_data(letters, self.letters_dir, merge)

    def insert_values(self, data, merge):
        data = self.write_data(data, self.values_dir, merge)
        self.convert_row_value_to_level(data, merge)
        print("Values inserted Successfully")
