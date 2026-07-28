"""
Tetris - Classic Edition
-------------------------
A faithful recreation of classic (NES/Game Boy style) Tetris using pygame.

Controls:
    Left / Right (or A / D) - move piece
    Down (or S)              - soft drop
    Space                    - hard drop
    Up / Z (or W)            - rotate clockwise
    X                        - rotate counter-clockwise
    C                        - hold piece
    P                        - pause
    R                        - restart after game over
    Esc / close window       - quit

Run with:
    pip install pygame
    python tetris.py
"""

import random
import sys
import pygame

# ----------------------------- Config ----------------------------- #

CELL = 30
COLS = 10
ROWS = 20

BOARD_W = CELL * COLS
BOARD_H = CELL * ROWS

SIDE_PANEL = 200
MARGIN = 20
WIDTH = BOARD_W + SIDE_PANEL + MARGIN * 3
HEIGHT = BOARD_H + MARGIN * 2

BOARD_X = MARGIN
BOARD_Y = MARGIN

# Classic Game Boy-ish dark palette with NES-bright piece colors
BG_COLOR = (15, 15, 20)
BOARD_BG = (10, 10, 14)
GRID_LINE = (30, 30, 38)
PANEL_COLOR = (22, 22, 30)
TEXT_COLOR = (235, 235, 235)
SUBTEXT_COLOR = (150, 150, 160)
GHOST_ALPHA = 70

# Gravity speed table (frames per row drop) approximated from NES Tetris, by level
LEVEL_SPEEDS_MS = [
  800,
  720,
  630,
  550,
  470,
  380,
  300,
  220,
  130,
  100,
  80,
  80,
  80,
  70,
  70,
  70,
  50,
  50,
  50,
  30,
]

SCORE_TABLE = {
  1: 40,
  2: 100,
  3: 300,
  4: 1200,
}  # single, double, triple, tetris (x level+1)

# ------------------------------ Pieces ------------------------------ #

# Each shape defined as a list of rotation states; each state is a list of (x, y) cells
# on a 4x4 grid, matching classic SRS-ish layouts but simplified (no wall-kick table,
# just simple rotation with basic bounds/collision check).

SHAPES = {
  "I": {
    "color": (49, 199, 239),
    "rotations": [
      [(0, 1), (1, 1), (2, 1), (3, 1)],
      [(2, 0), (2, 1), (2, 2), (2, 3)],
      [(0, 2), (1, 2), (2, 2), (3, 2)],
      [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
  },
  "O": {
    "color": (247, 211, 8),
    "rotations": [
                   [(1, 0), (2, 0), (1, 1), (2, 1)],
                 ]
                 * 4,
  },
  "T": {
    "color": (173, 77, 156),
    "rotations": [
      [(1, 0), (0, 1), (1, 1), (2, 1)],
      [(1, 0), (1, 1), (2, 1), (1, 2)],
      [(0, 1), (1, 1), (2, 1), (1, 2)],
      [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
  },
  "S": {
    "color": (66, 182, 66),
    "rotations": [
      [(1, 0), (2, 0), (0, 1), (1, 1)],
      [(1, 0), (1, 1), (2, 1), (2, 2)],
      [(1, 1), (2, 1), (0, 2), (1, 2)],
      [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
  },
  "Z": {
    "color": (239, 32, 41),
    "rotations": [
      [(0, 0), (1, 0), (1, 1), (2, 1)],
      [(2, 0), (1, 1), (2, 1), (1, 2)],
      [(0, 1), (1, 1), (1, 2), (2, 2)],
      [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
  },
  "J": {
    "color": (90, 101, 206),
    "rotations": [
      [(0, 0), (0, 1), (1, 1), (2, 1)],
      [(1, 0), (2, 0), (1, 1), (1, 2)],
      [(0, 1), (1, 1), (2, 1), (2, 2)],
      [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
  },
  "L": {
    "color": (237, 129, 40),
    "rotations": [
      [(2, 0), (0, 1), (1, 1), (2, 1)],
      [(1, 0), (1, 1), (1, 2), (2, 2)],
      [(0, 1), (1, 1), (2, 1), (0, 2)],
      [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
  },
}

SHAPE_KEYS = list(SHAPES.keys())


class Piece:
  def __init__(self, kind):
    self.kind = kind
    self.color = SHAPES[kind]["color"]
    self.rotation = 0
    self.x = 3
    self.y = -2 if kind != "I" else -2

  def cells(self, rotation=None, x=None, y=None):
    rotation = self.rotation if rotation is None else rotation
    x = self.x if x is None else x
    y = self.y if y is None else y
    shape = SHAPES[self.kind]["rotations"][rotation % 4]
    return [(x + cx, y + cy) for cx, cy in shape]


class SevenBag:
  """Classic 7-bag randomizer: shuffles one of each piece, no long droughts."""

  def __init__(self):
    self.bag = []

  def next(self):
    if not self.bag:
      self.bag = SHAPE_KEYS[:]
      random.shuffle(self.bag)
    return self.bag.pop()


class Tetris:
  def __init__(self):
    pygame.init()
    pygame.display.set_caption("Tetris - Classic Edition")
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    self.clock = pygame.time.Clock()
    self.font_big = pygame.font.SysFont("consolas", 34, bold=True)
    self.font_med = pygame.font.SysFont("consolas", 22, bold=True)
    self.font_small = pygame.font.SysFont("consolas", 16)
    self.reset()

  def reset(self):
    self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    self.bag = SevenBag()
    self.current = Piece(self.bag.next())
    self.next_piece = Piece(self.bag.next())
    self.hold_kind = None
    self.hold_used = False
    self.score = 0
    self.high_score = getattr(self, "high_score", 0)
    self.lines_cleared = 0
    self.level = 0
    self.game_over = False
    self.paused = False
    self.fall_timer = 0.0
    self.das_timer = 0.0  # delayed auto shift for held movement
    self.das_dir = 0
    self.line_clear_flash = []
    self.flash_timer = 0.0

  # ------------------------- Collision helpers ------------------------- #

  def valid(self, cells):
    for x, y in cells:
      if x < 0 or x >= COLS or y >= ROWS:
        return False
      if y >= 0 and self.grid[y][x] is not None:
        return False
    return True

  def lock_piece(self):
    for x, y in self.current.cells():
      if y < 0:
        self.game_over = True
        return
      self.grid[y][x] = self.current.color
    self.clear_lines()
    self.spawn_next()

  def spawn_next(self):
    self.current = self.next_piece
    self.current.x, self.current.y = 3, -2
    self.next_piece = Piece(self.bag.next())
    self.hold_used = False
    if not self.valid(self.current.cells()):
      self.game_over = True

  def clear_lines(self):
    full_rows = [
      y
      for y in range(ROWS)
      if all(self.grid[y][x] is not None for x in range(COLS))
    ]
    if not full_rows:
      return
    for y in full_rows:
      del self.grid[y]
      self.grid.insert(0, [None] * COLS)

    n = len(full_rows)
    self.lines_cleared += n
    self.score += SCORE_TABLE.get(n, 0) * (self.level + 1)
    self.high_score = max(self.high_score, self.score)
    self.level = self.lines_cleared // 10

  # ------------------------------ Actions ------------------------------ #

  def try_move(self, dx, dy):
    new_cells = self.current.cells(x=self.current.x + dx, y=self.current.y + dy)
    if self.valid(new_cells):
      self.current.x += dx
      self.current.y += dy
      return True
    return False

  def try_rotate(self, direction):
    new_rotation = (self.current.rotation + direction) % 4
    new_cells = self.current.cells(rotation=new_rotation)
    if self.valid(new_cells):
      self.current.rotation = new_rotation
      return
    # simple wall-kick attempts (left, right, up)
    for kick_x, kick_y in [(-1, 0), (1, 0), (0, -1), (-2, 0), (2, 0)]:
      kicked = self.current.cells(
        rotation=new_rotation,
        x=self.current.x + kick_x,
        y=self.current.y + kick_y,
      )
      if self.valid(kicked):
        self.current.rotation = new_rotation
        self.current.x += kick_x
        self.current.y += kick_y
        return

  def hard_drop(self):
    drop_distance = 0
    while self.try_move(0, 1):
      drop_distance += 1
    self.score += drop_distance * 2
    self.lock_piece()

  def soft_drop(self):
    if not self.try_move(0, 1):
      self.lock_piece()
    else:
      self.score += 1

  def hold(self):
    if self.hold_used:
      return
    self.hold_used = True
    if self.hold_kind is None:
      self.hold_kind = self.current.kind
      self.spawn_next()
    else:
      self.hold_kind, new_kind = self.current.kind, self.hold_kind
      self.current = Piece(new_kind)
      self.current.x, self.current.y = 3, -2

  def ghost_y(self):
    ghost = Piece(self.current.kind)
    ghost.rotation = self.current.rotation
    ghost.x, ghost.y = self.current.x, self.current.y
    while self.valid(ghost.cells(y=ghost.y + 1)):
      ghost.y += 1
    return ghost.y

  # ------------------------- Input handling ------------------------- #

  def handle_keydown(self, key):
    if key == pygame.K_ESCAPE:
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

    if key in (pygame.K_LEFT, pygame.K_a):
      self.try_move(-1, 0)
      self.das_dir = -1
      self.das_timer = 0.0
    elif key in (pygame.K_RIGHT, pygame.K_d):
      self.try_move(1, 0)
      self.das_dir = 1
      self.das_timer = 0.0
    elif key in (pygame.K_DOWN, pygame.K_s):
      self.soft_drop()
    elif key == pygame.K_SPACE:
      self.hard_drop()
    elif key in (pygame.K_UP, pygame.K_z, pygame.K_w):
      self.try_rotate(1)
    elif key == pygame.K_x:
      self.try_rotate(-1)
    elif key == pygame.K_c:
      self.hold()

  def handle_keyup(self, key):
    if key in (pygame.K_LEFT, pygame.K_a) and self.das_dir == -1:
      self.das_dir = 0
    elif key in (pygame.K_RIGHT, pygame.K_d) and self.das_dir == 1:
      self.das_dir = 0

  # ------------------------------ Update ------------------------------ #

  def update(self, dt_ms):
    if self.game_over or self.paused:
      return

    # Delayed auto-shift for held direction keys
    if self.das_dir != 0:
      self.das_timer += dt_ms
      if self.das_timer > 160:
        self.try_move(self.das_dir, 0)
        self.das_timer -= 40

    self.fall_timer += dt_ms
    speed = LEVEL_SPEEDS_MS[min(self.level, len(LEVEL_SPEEDS_MS) - 1)]
    if self.fall_timer >= speed:
      self.fall_timer = 0
      if not self.try_move(0, 1):
        self.lock_piece()

  # ------------------------------ Drawing ------------------------------ #

  def draw_cell(self, surface, px, py, color, alpha=255):
    rect = pygame.Rect(px, py, CELL, CELL)
    if alpha < 255:
      s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
      pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=4)
      pygame.draw.rect(
        s,
        (*color, min(255, alpha + 60)),
        s.get_rect(),
        width=2,
        border_radius=4,
      )
      surface.blit(s, (px, py))
    else:
      pygame.draw.rect(surface, color, rect, border_radius=4)
      highlight = tuple(min(255, c + 40) for c in color)
      pygame.draw.rect(surface, highlight, rect, width=2, border_radius=4)

  def draw_board(self):
    board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_W, BOARD_H)
    pygame.draw.rect(self.screen, BOARD_BG, board_rect)

    for x in range(COLS + 1):
      xpos = BOARD_X + x * CELL
      pygame.draw.line(
        self.screen, GRID_LINE, (xpos, BOARD_Y), (xpos, BOARD_Y + BOARD_H)
      )
    for y in range(ROWS + 1):
      ypos = BOARD_Y + y * CELL
      pygame.draw.line(
        self.screen, GRID_LINE, (BOARD_X, ypos), (BOARD_X + BOARD_W, ypos)
      )

    # Locked cells
    for y in range(ROWS):
      for x in range(COLS):
        color = self.grid[y][x]
        if color:
          self.draw_cell(
            self.screen, BOARD_X + x * CELL, BOARD_Y + y * CELL, color
          )

    if not self.game_over and not self.paused:
      # Ghost piece
      ghost_y = self.ghost_y()
      for x, y in self.current.cells(y=ghost_y):
        if y >= 0:
          self.draw_cell(
            self.screen,
            BOARD_X + x * CELL,
            BOARD_Y + y * CELL,
            self.current.color,
            alpha=GHOST_ALPHA,
          )
      # Current piece
      for x, y in self.current.cells():
        if y >= 0:
          self.draw_cell(
            self.screen,
            BOARD_X + x * CELL,
            BOARD_Y + y * CELL,
            self.current.color,
          )

    pygame.draw.rect(self.screen, (60, 60, 70), board_rect, width=2)

  def draw_mini_piece(self, kind, center_x, center_y, scale=20):
    if kind is None:
      return
    shape = SHAPES[kind]["rotations"][0]
    color = SHAPES[kind]["color"]
    xs = [c[0] for c in shape]
    ys = [c[1] for c in shape]
    w = (max(xs) - min(xs) + 1) * scale
    h = (max(ys) - min(ys) + 1) * scale
    start_x = center_x - w // 2
    start_y = center_y - h // 2
    for cx, cy in shape:
      px = start_x + (cx - min(xs)) * scale
      py = start_y + (cy - min(ys)) * scale
      rect = pygame.Rect(px, py, scale - 2, scale - 2)
      pygame.draw.rect(self.screen, color, rect, border_radius=3)

  def draw_panel(self):
    panel_x = BOARD_X + BOARD_W + MARGIN
    panel_rect = pygame.Rect(panel_x, BOARD_Y, SIDE_PANEL, BOARD_H)
    pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect, border_radius=8)

    y = BOARD_Y + 20

    title = self.font_med.render("NEXT", True, TEXT_COLOR)
    self.screen.blit(title, (panel_x + 20, y))
    y += 40
    box = pygame.Rect(panel_x + 20, y, SIDE_PANEL - 40, 80)
    pygame.draw.rect(self.screen, BOARD_BG, box, border_radius=6)
    self.draw_mini_piece(self.next_piece.kind, box.centerx, box.centery)
    y += 100

    title = self.font_med.render("HOLD", True, TEXT_COLOR)
    self.screen.blit(title, (panel_x + 20, y))
    y += 40
    box = pygame.Rect(panel_x + 20, y, SIDE_PANEL - 40, 80)
    pygame.draw.rect(self.screen, BOARD_BG, box, border_radius=6)
    self.draw_mini_piece(self.hold_kind, box.centerx, box.centery)
    y += 110

    for label, value in [
      ("SCORE", self.score),
      ("HIGH", self.high_score),
      ("LINES", self.lines_cleared),
      ("LEVEL", self.level),
    ]:
      label_surf = self.font_small.render(label, True, SUBTEXT_COLOR)
      value_surf = self.font_med.render(str(value), True, TEXT_COLOR)
      self.screen.blit(label_surf, (panel_x + 20, y))
      self.screen.blit(value_surf, (panel_x + 20, y + 20))
      y += 60

    hint_lines = [
      "P  pause",
      "Space  hard drop",
      "C  hold",
      "R  restart",
    ]
    y = BOARD_Y + BOARD_H - 20 * len(hint_lines) - 10
    for line in hint_lines:
      hint_surf = self.font_small.render(line, True, SUBTEXT_COLOR)
      self.screen.blit(hint_surf, (panel_x + 20, y))
      y += 20

  def draw_center_message(self, title, subtitle=None):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
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
    self.draw_board()
    self.draw_panel()

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
      dt_ms = self.clock.tick(60)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.KEYDOWN:
          self.handle_keydown(event.key)
        if event.type == pygame.KEYUP:
          self.handle_keyup(event.key)

      self.update(dt_ms)
      self.draw()


if __name__ == "__main__":
  Tetris().run()
