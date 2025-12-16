# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from bs4 import BeautifulSoup
# import time
# import math

# def get_board(driver):
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, 'div[data-testid="interactive-grid"]')
#         )
#     )
#     print(element)

#     # Get direct children count
#     children = element.find_elements(By.XPATH, "./*")
#     total_cells = len(children) + 1  # child + 1 as requested

#     size = int(math.sqrt(total_cells))

#     if size * size != total_cells:
#         raise ValueError(
#             f"Total cells ({total_cells}) is not a perfect square"
#         )

#     rows = cols = size

#     return rows, cols, element.get_attribute("outerHTML")

# def build_board_matrix(rows, cols, board_html):
#     """
#     Build a matrix of (color, data-cell-idx) using computed background color
#     from the root node of each cell.
#     """
#     soup = BeautifulSoup(board_html, "html.parser")
#     matrix = [[None for _ in range(cols)] for _ in range(rows)]

    
#     cells = soup.find_all(attrs={"data-cell-idx": True})

#     for cell in cells:
#         idx = int(cell["data-cell-idx"])
#         r = idx // cols
#         c = idx % cols
        
#         style = cell.get("style", "")
#         color = None
#         if "background-color" in style:
#             color = style.split("background-color:")[1].split(";")[0].strip()
#         else:
#             classes = cell.get("class", [])
#             if classes:
#                 color = classes[-1]  

#         matrix[r][c] = (color, idx)

#     return matrix
    
# def solve(color_idx_board):
#     n = len(color_idx_board)
#     queens = []
#     used_rows = set()
#     used_cols = set()
#     used_colors = set()

#     def is_touching(r, c):
#         for qr, qc in queens:
#             if abs(qr - r) <= 1 and abs(qc - c) <= 1:
#                 return True
#         return False

#     def backtrack():
#         if len(queens) == n:
#             return True

#         for r in range(n):
#             if r in used_rows:
#                 continue
#             for c in range(n):
#                 color, _ = color_idx_board[r][c]

#                 if (
#                     c in used_cols
#                     or color in used_colors
#                     or is_touching(r, c)
#                 ):
#                     continue

#                 queens.append((r, c))
#                 used_rows.add(r)
#                 used_cols.add(c)
#                 used_colors.add(color)

#                 if backtrack():
#                     return True

#                 queens.pop()
#                 used_rows.remove(r)
#                 used_cols.remove(c)
#                 used_colors.remove(color)
#         return False

#     backtrack()
#     return [color_idx_board[r][c][1] for r, c in queens]


# def place_queens(driver, queen_indices):
#     actions = ActionChains(driver)
    
#     for idx in queen_indices:
#         try:
#             cell = driver.find_element(By.CSS_SELECTOR, f'div[data-cell-idx="{idx}"]')
#         except Exception as e:
#             print(f"Error finding cell {idx}: {e}")
#             continue
#         print(f"Double-clicking cell {idx}")
#         ActionChains(driver).double_click(cell).perform()
#         print(f"Placed queen at cell {idx}")
#         time.sleep(0.2)


from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


def get_board(driver):
    element = driver.find_element(By.ID, "queens-grid")
    style = element.get_attribute("style")

    rows = int(style.split("--rows:")[1].split(";")[0].strip())
    cols = int(style.split("--cols:")[1].split(";")[0].strip())

    return rows, cols, element.get_attribute("outerHTML")


def build_board_matrix(rows, cols, board_html):
    soup = BeautifulSoup(board_html, "html.parser")
    matrix = [[None for _ in range(cols)] for _ in range(rows)]

    cells = soup.find_all(attrs={"data-cell-idx": True})

    for cell in cells:
        idx = int(cell["data-cell-idx"])
        r = idx // cols
        c = idx % cols

        classes = cell.get("class", [])
        color = classes[1] if len(classes) > 1 else None

        matrix[r][c] = (color, idx)

    return matrix


def solve(color_idx_board):
    n = len(color_idx_board)

    queens = []
    used_rows = set()
    used_cols = set()
    used_colors = set()

    def is_touching(r, c):
        for qr, qc in queens:
            if abs(qr - r) <= 1 and abs(qc - c) <= 1:
                return True
        return False

    def backtrack():
        if len(queens) == n:
            return True

        for r in range(n):
            if r in used_rows:
                continue

            for c in range(n):
                color, _ = color_idx_board[r][c]

                if (
                    c in used_cols
                    or color in used_colors
                    or is_touching(r, c)
                ):
                    continue

                queens.append((r, c))
                used_rows.add(r)
                used_cols.add(c)
                used_colors.add(color)

                if backtrack():
                    return True

                queens.pop()
                used_rows.remove(r)
                used_cols.remove(c)
                used_colors.remove(color)

        return False

    backtrack()

    return [color_idx_board[r][c][1] for r, c in queens]


def get_cells_by_idx(driver, indices):
    print(indices)
    elements = []

    for idx in indices:
        el = driver.find_element(
            By.CSS_SELECTOR,
            f'div[data-cell-idx="{idx}"]'
        )
        elements.append(el)

    return elements


def place_queens(driver, queen_indices):
    queen_elements = get_cells_by_idx(driver, queen_indices)
    actions = ActionChains(driver)

    for el in queen_elements:
        actions.double_click(el).perform()
