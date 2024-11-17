import cv2
import pytesseract
import re


# Function to extract numbers from the image
def extract_numbers_from_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Preprocess the image to improve OCR accuracy
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply histogram equalization to improve contrast
    # equalized = cv2.equalizeHist(gray)

    # Alternatively, use adaptive contrast stretching
    contrast_stretched = cv2.convertScaleAbs(gray, alpha=2.5, beta=10)

    # You can choose to display or save the enhanced image for checking
    # cv2.imwrite('./dataset/contrast_enhanced.png', equalized)
    cv2.imwrite('./dataset/contrast_stretched.png', contrast_stretched)
    # cv2.imwrite('./dataset/grey.png', gray)
    blurred = cv2.GaussianBlur(contrast_stretched, (5, 5), 0)
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite('./dataset/thresh.png', thresh)
    # Use pytesseract to extract text
    config = "--psm 6"  # Use psm 6 to treat image as a single uniform block of text
    text = pytesseract.image_to_string(thresh, config=config)
    print(text)
    values_count = int(len(text) / 6)
    print(values_count)
    # Modify the regular expression to capture numbers (with or without decimals) followed by 'x'
    matches = re.findall(r'(\d+\.?\d*)[a-zA-Z%@#$&*]?', text)

    # Process the captured numbers and ensure they are formatted to two decimal places
    numbers = []
    for match in matches:
        match = match.replace('.', '')
        num = f"{match[:-2]}.{match[-2:]}"
        numbers.append(float(num))
    for num in numbers:
        if num < 1:
            numbers = 'Invalid'
    if numbers != 'Invalid':
        if values_count == len(numbers) or values_count - 1 == len(numbers) or values_count + 1 == len(numbers) or values_count - 2 == len(numbers) or values_count + 2 == len(numbers):
            print(numbers)
            return numbers
        else:
            print(text, 'count = ', values_count)
            print('count = ', len(numbers), numbers)
            print("Image Error! - Couldn't scan the image properly")
    else:
        print(text, 'count = ', values_count)
        print('count = ', len(numbers), numbers)
        print("Image Error! - Couldn't scan the image properly")


# extract_numbers_from_image('./dataset/Captured_image.png')

def capture_image(webcam_id, save_path):
    # Open a connection to the webcam
    cap = cv2.VideoCapture(webcam_id)

    if not cap.isOpened():
        print("Could not open webcam")
        return

    # Set the resolution to 1366 x 768
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1366)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    # Read a single frame from the webcam
    ret, frame = cap.read()

    if ret:
        # Save the captured frame as an image
        cv2.imwrite(save_path, frame)
        print(f"Image saved as {save_path}")
    else:
        print("Failed to capture image")

    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    return extract_numbers_from_image(save_path)


# Example usage
# numbers = capture_image(3, './dataset/Captured_image.png')
