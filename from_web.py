from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys

auto_buttons = [
    '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]',
    '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher',
    '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[2]/div/app-navigation-switcher/div/button[2]',
    '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[2]/div/div[4]/div[2]/div[1]/app-ui-switcher'
]

input_paths = {
    "bets": [
        '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input',
        '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[2]/div/div[2]/div[1]/app-spinner/div/div[2]/input'
    ],
    "cash_outs": [
        '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[2]/div/app-spinner/div/div[2]/input',
        '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[2]/div/div[4]/div[2]/div[2]/div/app-spinner/div/div[2]/input'
    ]
}
# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Or use Firefox, Edge, etc.
driver.get("https://playinexch247.com")

# Wait for manual login
input("Press Enter after logging in and navigating to the page.")


def print_output(list):
    sys.stdout.write('\r' + ' ' + '\r')
    for x in list:
        print(x, flush=True)


def enter_bets(input_values):
    for key in input_values:
        for path, value in zip(input_paths[key], input_values[key]):
            try:
                entry = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, path))
                )
                entry.click()  # Focus on the input field
                entry.send_keys(Keys.CONTROL + "a")  # Select all text
                entry.send_keys(Keys.BACKSPACE)  # Delete selected text
                entry.send_keys(f"{value}")  # Enter the new value
                print(f"{key}: {value}")
            except Exception as e:
                print(f"Error interacting with element at {path}: {e}")


def press_buttons(button_paths):
    """
    Presses a list of buttons given their XPath locations.

    :param button_paths: A list of XPath strings representing the locations of the buttons to be pressed.
    :return: None
    """
    for button_path in button_paths:
        press_button(button_path)


def press_button(path):
    """
    Presses a button given their XPath location.

    :param path: XPath strings representing the locations of the button to be pressed.
    :return: None
    """
    button = driver.find_element(By.XPATH, path)
    button.click()


def init_auto(values):
    press_buttons(auto_buttons)
    enter_bets(values)


def convert_to_number(number_str):
    number = float(number_str.replace(",", ""))  # Remove the comma and convert to float
    return int(number)  # Convert to integer


def bets_count():
    # Define the XPath for the element
    bets_count_xpath = ("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[1]/app-bets-widget/div/app-all-bets-tab"
                        "/div/app-header/div[1]/div[1]/div[2]")

    # Find the element using XPath
    count = driver.find_element(By.XPATH, bets_count_xpath)
    if count:
        try:
            return int(count.text)
        except:
            print(count)
            print(count.text)


def get_multiplier_from_button():
    press_button()
    while True:
        try:
            # Define the XPath for the element
            multiplier_path = ("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[1]/app-bets-widget/div/app-all-bets-tab"
                               "/div/app-header/div[1]/div[2]/app-bubble-multiplier/div")

            # Find the element using XPath
            multiplier_element = driver.find_element(By.XPATH, multiplier_path)
            if multiplier_element:
                multiplier = float(multiplier_element.text.replace("x", ""))
                press_button()
                return multiplier
        except:
            continue


def get_multipliers():
    # Locate the div container by its class name
    payouts_block = driver.find_element(By.CLASS_NAME, "payouts-block")

    # Get all text inside the div
    payouts_text = payouts_block.text

    # Optionally, split the text into a list of lines or items
    payouts_list = [x.replace("x", "") for x in payouts_text.split("\n")]
    return payouts_list


def next_bet():
    bets_start = bets_count()
    bets_end = bets_count()
    if bets_end < 100 or bets_start < 100:
        return 1
    return 0


def close_window():
    # Close the driver
    driver.quit()
