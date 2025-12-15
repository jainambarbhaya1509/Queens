from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


from solve_queens import get_board, build_board_matrix, solve, place_queens

import os
from dotenv import load_dotenv

load_dotenv()

def login(url):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 40)

    driver.get(url)

    try:
        # Login fields
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))

        username.send_keys(os.getenv("EMAIL"))
        password.send_keys(os.getenv("PASSWORD"))
        password.submit()

        # Wait for successful login
        wait.until(
            EC.any_of(
                EC.url_contains("/feed"),
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
        )

        print("Login successful")

    except TimeoutException:
        print("Login failed or CAPTCHA detected")
        return driver

    # Keep browser open for next commands
    return driver


def solve_queens(driver):
    driver.get("https://www.linkedin.com/games/queens/")

    try:
        rows, cols, board = get_board(driver)
        matrix = build_board_matrix(rows, cols, board)
        idx = solve(matrix)
        place_queens(driver, idx)
        print("Queens Solved!")


    except NoSuchElementException:
        print("Could not find the game board.")
        return


driver = login("https://www.linkedin.com/checkpoint/lg/sign-in-another-account")

input("Logged in -> Press ENTER to open Queens")
solve_queens(driver)
input("Done. Press ENTER to close browser...")

driver.quit()

# [0, 10, 20, 30, 33, 45, 51, 63]