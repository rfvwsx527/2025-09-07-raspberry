import pygame
import sys
import random

# 階段一：基礎設定與環境建置
# ==========================================================================================

# 初始化 Pygame
pygame.init()

# --- 定義常數 ---
# 螢幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# 遊戲區域尺寸 (10x20 的格子)
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

# 遊戲區域在螢幕上的左上角位置
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


# --- 建立遊戲視窗 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# --- 設定遊戲時脈 (FPS) ---
clock = pygame.time.Clock()
FPS = 60

# ==========================================================================================

# 階段二：遊戲核心物件
# ==========================================================================================

# --- 方塊形狀定義 ---
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# 形狀列表與對應顏色
shapes = [S, Z, I, O, J, L, T]
shape_colors = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, MAGENTA]


class Piece:
    """
    代表一個正在掉落的俄羅斯方塊
    """
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    """
    建立遊戲區的網格資料結構
    - 網格是一個 20x10 的二維列表
    - (0,0,0) 代表空格
    - 其他顏色值代表有方塊佔據
    """
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def convert_shape_format(piece):
    """
    將方塊的形狀定義轉換為實際的網格座標
    """
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    # 調整位移
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(piece, grid):
    """
    檢查方塊是否在有效的位置
    """
    # 建立一個包含所有空格座標的集合
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    """
    檢查是否遊戲結束 (方塊堆到頂部)
    """
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    """
    隨機回傳一個新的方塊物件
    """
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color):
    """
    在視窗中央繪製文字
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2),
                         TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    """
    在視窗上繪製網格線
    """
    for i in range(len(grid)):
        # 繪製水平線
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE),
                         (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(len(grid[0])):
            # 繪製垂直線
            pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y),
                             (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def clear_rows(grid, locked):
    """
    清除已填滿的行，並回傳消除的行數
    """
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(piece, surface):
    """
    繪製下一個方塊的預覽
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 10, sy - 30))

    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)


def draw_window(surface, grid, score=0, level=0, next_piece=None):
    """
    繪製遊戲主視窗的所有內容
    """
    surface.fill(BLACK)  # 將背景填充為黑色

    # 繪製標題
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))

    # 顯示分數
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))

    # 顯示等級
    label = font.render('Level: ' + str(level), 1, WHITE)
    surface.blit(label, (sx + 20, sy + 200))


    # 繪製已固定的方塊
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # 繪製遊戲區域的框線
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    # 繪製網格線
    draw_grid(surface, grid)

    # 繪製下一個方塊
    if next_piece:
        draw_next_shape(next_piece, surface)


# ==========================================================================================


def main():
    """
    遊戲主函式
    """
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    fall_time = 0
    score = 0
    level = 0
    total_lines_cleared = 0
    fall_speed = 0.27 # 初始掉落速度

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # --- 等級與速度控制 ---
        if total_lines_cleared >= (level + 1) * 10:
            level += 1
            fall_speed = max(0.1, 0.27 - level * 0.02)


        # --- 方塊自動掉落 ---
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # --- 事件處理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    # 加速下降並加分
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                    else:
                        score += 1 # 按下加速可以得 1 分
                elif event.key == pygame.K_UP:
                    # 旋轉方塊
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        # --- 遊戲邏輯 ---
        shape_pos = convert_shape_format(current_piece)

        # 如果方塊觸底，則鎖定位置並生成新方塊
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
            # 計算分數
            lines_cleared = clear_rows(grid, locked_positions)
            total_lines_cleared += lines_cleared
            if lines_cleared == 1:
                score += 40 * (level + 1)
            elif lines_cleared == 2:
                score += 100 * (level + 1)
            elif lines_cleared == 3:
                score += 300 * (level + 1)
            elif lines_cleared >= 4:
                score += 1200 * (level + 1)


        # --- 畫面繪製 ---
        draw_window(screen, grid, score, level, next_piece)

        # 繪製正在掉落的方塊
        for pos in shape_pos:
            pygame.draw.rect(screen, current_piece.color,
                             (TOP_LEFT_X + pos[0] * BLOCK_SIZE, TOP_LEFT_Y + pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.update()

        # 檢查是否遊戲結束
        if check_lost(locked_positions):
            run = False

    draw_text_middle(screen, "You Lost! Score: " + str(score), 60, WHITE)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    """
    遊戲主選單
    """
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle(screen, 'Press Any Key To Play', 60, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

    pygame.display.quit()


if __name__ == "__main__":
    main_menu()
