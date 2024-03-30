import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def restart_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, draw_id
    # Reset game state
    snake.x = 5 * TILE_SIZE
    snake.y = 5 * TILE_SIZE
    food.x = 10 * TILE_SIZE
    food.y = 10 * TILE_SIZE
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    canvas.delete("all")
    draw_id = window.after(100, draw)


# game window
window = tkinter.Tk()
window.title("snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()

# initialize game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0
draw_id = None


def change_direction(e):
    global velocityX, velocityY, game_over

    if game_over:
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    global snake, food, snake_body, game_over, score
    if game_over:
        return

    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return

    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    # collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # update snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score, draw_id
    move()

    canvas.delete("all")

    # draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")
    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over : {score}",
                           fill="white")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 30, font="Arial 20", text="Press 'R' to Restart",
                           fill="white")
    else:
        canvas.create_text(60, 20, font="Arial 20", text=f"Score : {score}", fill="white")
    draw_id = window.after(100, draw)


draw_id = window.after(100, draw)
window.bind("<KeyPress>", change_direction)
window.bind("r", lambda event: restart_game())  # Bind 'r' key to restart the game
window.mainloop()
