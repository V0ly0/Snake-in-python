import pygame
import random
import time
import logging
import requests

print("Snake game e-sport version by Volyo <3")
pygame.init()

DISCORD_WEBHOOK_URL = "Your Webhook url"

WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

logging.basicConfig(filename='snake_game.log', level=logging.INFO)

def get_system(self) -> bool:
        global username

        username = os.getenv("UserName")
        get_system()

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if new_head in self.body or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            return False

        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

        logging.info(f"Snake moved to {new_head} in direction {self.direction}")
        return True

    def change_direction(self, new_direction):
        if (
            (new_direction == UP and not self.direction == DOWN)
            or (new_direction == DOWN and not self.direction == UP)
            or (new_direction == LEFT and not self.direction == RIGHT)
            or (new_direction == RIGHT and not self.direction == LEFT)
        ):
            self.direction = new_direction

    def check_collision_with_food(self, food):
        collision = self.body[0] == food
        if collision:
            logging.info("Snake eat food.")
        return collision

    def grow_snake(self):
        self.grow = True

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def reposition(self):
        self.position = self.random_position()

def display_scores():
    scores = []
    with open("scores.txt", "r") as score_file:
        scores = score_file.readlines()

    font = pygame.font.Font(None, 36)
    y_offset = 120

    best_score = 0

    for i, line in enumerate(scores):
        score_text = font.render(line.strip(), True, WHITE)
        screen.blit(score_text, (WIDTH // 4, HEIGHT // 3 + y_offset * i))

        score = int(line.strip().split(": ")[1])
        if score > best_score:
            best_score = score

    pygame.display.flip()

    return best_score

def display_logs_window():
    log_window_width = 600
    log_window_height = 400
    log_window = pygame.display.set_mode((log_window_width, log_window_height))
    pygame.display.set_caption("Logs")

    font = pygame.font.Font(None, 24)
    log_text = ""

    current_log_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_log_index = max(current_log_index - 1, 0)
                elif event.key == pygame.K_DOWN:
                    current_log_index = min(current_log_index + 1, len(log_lines) - 1)

        log_window.fill((255, 255, 255))

        with open("snake_game.log", "r") as log_file:
            log_text = log_file.read()

        log_lines = log_text.split("\n")
        y_offset = 10

        for i, line in enumerate(log_lines):
            if i >= current_log_index and y_offset < log_window_height:
                log_line = font.render(line, True, (0, 0, 0))
                log_window.blit(log_line, (10, y_offset))
                y_offset += 30

        pygame.display.flip()

    pygame.quit()

def reset_logs():
    with open("snake_game.log", "w"):
         pass

def send_score_to_discord(score):
    data = {
        "content": f"New score: {score}",
        "username": "Snake Game",
    }

    result = requests.post(DISCORD_WEBHOOK_URL, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Score sent to Discord successfully, code {}.".format(result.status_code))

def main():
    reset_logs()
    snake = Snake()
    food = Food()

    score = 0

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    game_over = False
    restart_button = None

    last_frame_time = time.time()

    paused = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_l:
                    display_logs_window()
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if not game_over and not paused:
            if not snake.move():
                logging.info("Snake died.")
                game_over = True

            if snake.check_collision_with_food(food.position):
                snake.grow_snake()
                food.reposition()
                score += 1

            screen.fill(BLACK)

            if not paused:
                for segment in snake.body:
                    pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

                pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))

            current_time = time.time()
            elapsed_time = current_time - last_frame_time
            last_frame_time = current_time

            if elapsed_time > 0:
                fps = 1 / elapsed_time
            else:
                fps = 0

            reaction_time_ms = elapsed_time * 1000

            fps_text = font.render(f"FPS: {int(fps)}", True, WHITE)
            screen.blit(fps_text, (10, 40))

            reaction_time_text = font.render(f"React: {int(reaction_time_ms)} ms", True, WHITE)
            screen.blit(reaction_time_text, (10, 70))

            pygame.display.flip()

            clock.tick(12)

        elif paused:
            pause_text = font.render("Paused", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
            pygame.display.flip()

    screen.fill(BLACK)
    final_score_text = font.render(f"Score final: {score}", True, WHITE)
    screen.blit(final_score_text, (WIDTH // 4, HEIGHT // 3))

    restart_button = pygame.draw.rect(screen, GREEN, (WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))
    restart_text = font.render("Redémarrer", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2.9, HEIGHT // 1.90))

    send_score_to_discord(score)
    
    pygame.display.flip()

    score_file = open("scores.txt", "a")
    score_file.write(f"Score: {score}\n")
    score_file.close()

    pygame.display.flip()

    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_x, mouse_y):
                    main()



if __name__ == "__main__":
    main()