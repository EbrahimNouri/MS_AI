"""
Snake Game
----------
Classic Snake game built with pygame.

Controls:
    Arrow keys / WASD - move
    P                 - pause / unpause
    R                 - restart after game over
    Esc / close window - quit

Run with:
    pip install pygame
    python snake_game.py
"""

import random
import sys
import pygame

# ----------------------------- Config ----------------------------- #

CELL_SIZE = 24
GRID_WIDTH = 25
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + 60  # extra space for score bar

FPS_START = 8
FPS_MAX = 20
SPEED_STEP_EVERY = 5  # increase speed every N food eaten

# Colors
BG_COLOR = (18, 18, 24)
GRID_COLOR = (28, 28, 36)
SNAKE_HEAD_COLOR = (98, 214, 122)
SNAKE_BODY_COLOR = (60, 170, 90)
FOOD_COLOR = (230, 90, 90)
TEXT_COLOR = (240, 240, 240)
SUBTEXT_COLOR = (170, 170, 180)
PANEL_COLOR = (26, 26, 34)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("consolas", 42, bold=True)
        self.font_med = pygame.font.SysFont("consolas", 24, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 18)
        self.reset()

    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.snake = [(cx - 1, cy), (cx - 2, cy), (cx - 3, cy)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.high_score = getattr(self, "high_score", 0)
        self.speed = FPS_START
        self.game_over = False
        self.paused = False

    def spawn_food(self):
        occupied = set(self.snake) if hasattr(self, "snake") else set()
        while True:
            pos = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if pos not in occupied:
                return pos

    # ------------------------- Input handling ------------------------- #

    def handle_keydown(self, key):
        if key in (pygame.K_ESCAPE,):
            pygame.quit()
            sys.exit()

        if self.game_over:
            if key == pygame.K_r:
                self.reset()
            return

        if key == pygame.K_p:
            self.paused = not self.paused
            return

        if self.paused:
            return

        direction_map = {
            pygame.K_UP: UP,
            pygame.K_w: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_s: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_a: LEFT,
            pygame.K_RIGHT: RIGHT,
            pygame.K_d: RIGHT,
        }
        if key in direction_map:
            new_dir = direction_map[key]
            # prevent reversing directly into itself
            if OPPOSITE[new_dir] != self.direction:
                self.pending_direction = new_dir

    # ------------------------------ Update ------------------------------ #

    def update(self):
        if self.game_over or self.paused:
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Wall collision
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            self.end_game()
            return

        # Self collision
        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.high_score = max(self.high_score, self.score)
            self.food = self.spawn_food()
            if self.score % SPEED_STEP_EVERY == 0:
                self.speed = min(FPS_MAX, self.speed + 1)
        else:
            self.snake.pop()

    def end_game(self):
        self.game_over = True

    # ------------------------------ Drawing ------------------------------ #

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(
                    x * CELL_SIZE, y * CELL_SIZE + 60, CELL_SIZE, CELL_SIZE
                )
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, GRID_COLOR, rect)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(
                x * CELL_SIZE + 1, y * CELL_SIZE + 60 + 1, CELL_SIZE - 2, CELL_SIZE - 2
            )
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def draw_food(self):
        x, y = self.food
        rect = pygame.Rect(
            x * CELL_SIZE + 3, y * CELL_SIZE + 60 + 3, CELL_SIZE - 6, CELL_SIZE - 6
        )
        pygame.draw.rect(self.screen, FOOD_COLOR, rect, border_radius=8)

    def draw_top_bar(self):
        pygame.draw.rect(self.screen, PANEL_COLOR, pygame.Rect(0, 0, WIDTH, 60))
        score_surf = self.font_med.render(f"Score: {self.score}", True, TEXT_COLOR)
        high_surf = self.font_small.render(
            f"Best: {self.high_score}", True, SUBTEXT_COLOR
        )
        self.screen.blit(score_surf, (16, 16))
        self.screen.blit(high_surf, (16, 40))

        hint = "P: pause" if not self.game_over else "R: restart"
        hint_surf = self.font_small.render(hint, True, SUBTEXT_COLOR)
        self.screen.blit(hint_surf, (WIDTH - hint_surf.get_width() - 16, 22))

    def draw_center_message(self, title, subtitle=None):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title_surf = self.font_big.render(title, True, TEXT_COLOR)
        self.screen.blit(
            title_surf, title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        )

        if subtitle:
            sub_surf = self.font_small.render(subtitle, True, SUBTEXT_COLOR)
            self.screen.blit(
                sub_surf, sub_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            )

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_top_bar()

        if self.paused and not self.game_over:
            self.draw_center_message("PAUSED", "Press P to resume")
        elif self.game_over:
            self.draw_center_message(
                "GAME OVER", f"Score: {self.score}   |   Press R to restart"
            )

        pygame.display.flip()

    # ------------------------------- Loop ------------------------------- #

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)

            self.update()
            self.draw()
            self.clock.tick(self.speed)


if __name__ == "__main__":
    SnakeGame().run()
