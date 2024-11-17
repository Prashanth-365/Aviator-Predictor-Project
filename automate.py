from main import capture_data
from train_data import count_down

while True:
    capture_data()  # Call the function
    count_down(600)
