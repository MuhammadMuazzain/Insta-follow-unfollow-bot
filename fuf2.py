from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time

def sleep_for_period_of_time(a, b):
    time.sleep(random.randint(a, b))


def main():
    # Prompt for user credentials
    user = input("Enter your username: ")
    pwd = input("Enter your password: ")

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    options.add_argument("--start-maximized")  # optional
    # options.add_argument("--headless")  # uncomment to run in headless mode

    # Initialize the browser correctly
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    # Open Instagram
    browser.get("https://www.instagram.com")
    time.sleep(5)

    try:
        cookies_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Only allow essential cookies')]")
        cookies_button.click()
        sleep_for_period_of_time(3, 6)
    except NoSuchElementException:
        print("No cookie banner found.")

    # Login
    username_input = browser.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = browser.find_element(By.CSS_SELECTOR, "input[name='password']")

    username_input.send_keys(user)
    password_input.send_keys(pwd)
    sleep_for_period_of_time(2, 4)

    login_button = browser.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    sleep_for_period_of_time(5, 8)

    # Skip "Save Your Login Info?" or "Turn on Notifications"
    try:
        not_now = browser.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now.click()
        sleep_for_period_of_time(2, 4)
    except NoSuchElementException:
        pass

    # Navigate to target page
    page_ig = input("Enter page username to follow their followers: ")
    browser.get(f"https://www.instagram.com/{page_ig}")
    sleep_for_period_of_time(5, 8)

    num_follow = int(input("How many people do you want to follow? "))

    try:
        followers_link = browser.find_element(By.PARTIAL_LINK_TEXT, "followers")
        followers_link.click()
    except Exception as e:
        print("Error opening followers list:", e)
        browser.quit()
        return

    sleep_for_period_of_time(4, 6)

    wait = WebDriverWait(browser, 10)
    pop_up_window = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1dm5mii')]")))

    followed = 0

    while followed < num_follow:
        try:
            follow_buttons = browser.find_elements(By.XPATH, '//button/div/div[contains(text(), "Follow")]')
            print(f"Found {len(follow_buttons)} follow buttons.")

            for button_div in follow_buttons:
                try:
                    button = button_div.find_element(By.XPATH, "..")  # go to <button> parent
                    if button.text == "Follow":
                        button.click()
                        followed += 1
                        print(f"Followed {followed}/{num_follow}")
                        sleep_for_period_of_time(40, 60)

                        if followed >= num_follow:
                            break
                except ElementClickInterceptedException:
                    print("Click intercepted, scrolling slightly and retrying.")
                    browser.execute_script("arguments[0].scrollTop += 100;", pop_up_window)
                    time.sleep(2)

            # Scroll to load more
            browser.execute_script("arguments[0].scrollTop += arguments[0].offsetHeight;", pop_up_window)
            time.sleep(2)

        except Exception as e:
            print("Error during following loop:", e)
            break

    print("Follow automation complete.")
    input("Press Enter to exit...")
    browser.quit()


if __name__ == "__main__":
    main()
