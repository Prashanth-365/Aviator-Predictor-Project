import pandas as pd

# Set the length of columns
col_len = 100

#Create a DataFrame with the first row as 100, and the second row as 'a'
data = {
    i: [100, 'a'] for i in range(col_len)
}
df = pd.DataFrame(data)
# Convert the dictionary to a DataFrame
# df = pd.read_csv('./dataset/score.csv', header=None)
# df.iloc[1, 105] = 50
# df.iloc[2, 105] = 'b'
# Save the DataFrame to a CSV file
df.to_csv('./dataset/score.csv')
