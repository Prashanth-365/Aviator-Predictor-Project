import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Sample data (replace this with your actual dataset)
data = [
    "L,M,M,M,L,L,L,M,L,L,M,L,M,L,M,M,M,L,L,M,L,L,H,M,M,M,L,L",
    "L,M,H,L,L,H,L,L,M,L,L,L,L,L,M,M,M,L,L,L,L,M,H,L,L,M,L,M,M,M,M",
    "M,M,L,L,M,L,M,L,M,M,M,L,M,L,L,M,L,M,M,M,L,L,L,L,M,M",
    "M,M,L,L,L,L,M,L,M,L,L,L,L,M,M,M,L,M,M,M,L,H,H,M,M,L,M,M,M,M,H"
]

# Convert the string data to a DataFrame
df = pd.DataFrame([x.split(',') for x in data])

# Flatten the DataFrame into a single column (representing your categorical values)
df = df.stack().reset_index(drop=True)

# Map categories 'L', 'M', 'H' to numerical values
category_map = {'L': 0, 'M': 1, 'H': 2}
df = df.map(category_map)

# Now, you need to create a feature (X) and target (y). For simplicity, let's predict based on the previous value.
X = df[:-1].values.reshape(-1, 1)  # Features are the previous value
y = df[1:].values  # Target is the next value

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Detailed classification report
print(classification_report(y_test, y_pred))
