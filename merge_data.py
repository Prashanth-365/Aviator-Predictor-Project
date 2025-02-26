import pandas as pd

# Load the CSV file into a DataFrame
file_path = './dataset/values.csv'
df = pd.read_csv(file_path, header=None)


def find_common(row_i, row_j):
    for i in range(len(row_i)):
        for j in range(len(row_j)):
            if len(row_i) > i+4 and len(row_j) > j+4:
                if row_i[i] == row_j[j] and row_i[i+1] == row_j[j+1] and row_i[i+2] == row_j[j+2] and row_i[i+3] == row_j[j+3] and row_i[i+4] == row_j[j+4]:
                    if i == 0:
                        return row_j[j:]
                    elif j == 0:
                        return row_i[i:]
    return ' '


# Function to merge two rows if they have 3 or more common values
def merge_two_rows(row_i, row_j):
    common_values = find_common(row_i, row_j)
    new_row = False
    # If 3 or more common values, merge rows
    if len(common_values) >= 5:
        common_values_str = ','.join(map(str, common_values))
        row_i_str = ','.join(map(str, row_i))
        row_j_str = ','.join(map(str, row_j))
        if common_values_str in row_i_str and common_values_str in row_j_str:
            if row_i[0] == common_values[0]:
                new_row = row_j + [value for value in row_i if value not in row_j]
            elif row_j[0] == common_values[0]:
                new_row = row_i + [value for value in row_j if value not in row_i]
    return new_row


# Function to check and merge rows with 3 or more common values
def merge():
    global df
    merged = False
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            # Find common values between two rows in the order they appear
            row_i = df.iloc[i].dropna().tolist()
            row_j = df.iloc[j].dropna().tolist()

            # Try to merge two rows
            new_row = merge_two_rows(row_i, row_j)
            if new_row:
                # Drop the two rows and add the merged row
                df = df.drop([i, j]).reset_index(drop=True)
                new_row_df = pd.Series(new_row).to_frame().T
                df = pd.concat([df, new_row_df], ignore_index=True)

                merged = True
                break

        if merged:
            break

    return df, merged



def merge_all_rows():
    # Repeat the merging process until no rows can be merged
    while True:
        df, merged = merge()
        if not merged:
            break
    df.to_csv(file_path, index=False, header=False)
    print("Rows merged successfully.")
