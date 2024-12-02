
# Aviator Predictor

**!! Warning !!**  
This project is for informational purposes only. Do not trust this project to invest your money or make financial decisions. It is a personal project created in free time, and I am not responsible for any losses incurred.

## Project Description

The **Aviator Predictor** project aims to forecast the next possible multiplier in the online game *Aviator*. In this game, players predict the optimal moment to cash out before the plane "takes off." The multiplier starts at 1x and steadily increases as the plane ascends.

This project predicts whether the next multiplier will be:
- **L** (less than 2x)
- **M** (between 2x and 10x)
- **H** (greater than 10x)

## How to Use the Project

1. **Download and Extract**
   - Download the zip file of this repository and extract it.
   - Open the project folder in your preferred Python code editor.

2. **Set Up Environment**
   - Create a virtual environment (recommended).
   - Install the required libraries using the following command:

     ```bash
     pip3 install pandas opencv-python pytesseract
     ```

3. **Run the Code**
   - Open `main.py` in your editor and run the file.
   - Place the *Aviator* game page and the program output (window or terminal) side by side.

4. **Predict the Multiplier**
   - Enter the latest multiplier shown in the Aviator game when prompted.
   - The program will predict the next multiplier.

### Sample Output

If you input a multiplier value of `1.9`, the output might look like this:

```plaintext
Image saved as ./dataset/Captured_image.png  
Start DroidCam  
moDbierd hote  

4  
Start DroidCam  
moDbierd hote  
count = 4  
count = 0 []  
Image Error! - Couldn't scan the image properly  

C - capture image from screen  
S - To scan multiple images from the folder  
A - To arrange and formulate dataSet  
I - To predict instantly  
or input value manually  
close - To stop the program  
Select what action you need to perform: 1.9  

LL(2) : M  
LLM(3) : L  
LLMM(4) : L  
LLMMM(5) : L  
LLMMMM(6) : L  
LLMMMMH(7) : M  
LLMMMMHM(8) : L  
LLMMMMHMH(9) : L  
sum(3) : L  
highest(7) : L  
result(6) : L  

LLMMMMHMH-(9)  

Dataset length: 9031  
1.9 - L
```

In this example:
- The predicted value is **L** (less than 2x), as all metrics (`sum(3)`, `highest(7)`, `result(6)`) indicate the same value, **L**.

---

## Troubleshooting

1. **Webcam or Image Capture Errors**
   - If you encounter an error related to the webcam or image capture, update the `webcam_id` value in `main.py`:
     - Change `webcam_id = 1` to `webcam_id = 0` (line 11).

2. **Contact**
   - For queries or support, feel free to contact me.
