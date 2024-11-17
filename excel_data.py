import pandas as pd

# Read the Excel file, specifying that the data starts from B2
excel_file = r'C:\Users\Roopa Eshwar\PycharmProjects\aviator_predictor\resources\data_set.xlsx'  # Replace with your file name
df = pd.read_excel(excel_file, sheet_name='Values', header=None)

# Select the data starting from B2 (i.e., all rows from the second row onward, and all columns from the second column onward)
data = df.iloc[1:, 1:]

# Transpose the DataFrame
transposed_df = data.T

# Write the transposed DataFrame to a CSV file
transposed_df.to_csv('./dataset/values.csv', header=False, index=False)

print("Data has been transposed and saved to 'output.csv'")
