from random import randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)

STONE_COLOR = (158, 158, 158)

POISON_COLOR = (139, 69, 19)

SPEED = 20


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    """Создание класса GameObject"""

    def draw(self):
        """Создание виртуального метода,появляющегося у каждого наследника"""
        raise NotImplementedError

    def __init__(self):
        self.body_color = None
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))


class Stone(GameObject):
    """Создание класса Камень"""

    def draw_cell(self):
        """Метод для отображения камня"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def __init__(self):
        self.body_color = STONE_COLOR
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Poison(GameObject):
    """Создание класса Неправильная еда"""

    def __init__(self):
        self.body_color = POISON_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод для измнения позиции яда"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw_cell(self):
        """Метод для отображения яда"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Создание класса Яблоко"""

    def draw(self):
        """Метод для отображения яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def __init__(self):
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод для измнения позиции яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """Создание класса Змейка"""

    def __init__(self):
        self.direction = UP
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.positions = []
        self.reset()

    def draw(self):
        """Метод для отображения змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод для обновления направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения змейки"""
        self.update_direction()
        if self.direction == RIGHT:
            new_position = (
                self.get_head_position()[0] + GRID_SIZE,
                self.get_head_position()[1]
            )
        elif self.direction == LEFT:
            new_position = (
                self.get_head_position()[0] - GRID_SIZE,
                self.get_head_position()[1]
            )
        elif self.direction == UP:
            new_position = (
                self.get_head_position()[0],
                self.get_head_position()[1] - GRID_SIZE
            )
        elif self.direction == DOWN:
            new_position = (
                self.get_head_position()[0],
                self.get_head_position()[1] + GRID_SIZE
            )

        if self.positions:
            self.last = self.positions[-1]

        self.positions.insert(0, new_position)

        if self.length < len(self.positions[1:]):
            self.positions.pop()

        if new_position[0] < 0 or new_position[0] >= SCREEN_WIDTH:
            self.reset()
        elif new_position[1] < 0 or new_position[1] >= SCREEN_HEIGHT:
            self.reset()

    def get_head_position(self):
        """Метод для возвращения головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод для сбрасывания направления и длины змейки"""
        self.length = 1
        self.positions.clear()
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions.append(self.position)


def handle_keys(game_object):
    """Функция, реализующий функционал игры"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, создающая необходимые объекты для запуска игры"""
    pygame.init()
    apple = Apple()
    snake = Snake()
    stone1 = Stone()
    stone2 = Stone()
    stone3 = Stone()
    poison = Poison()
    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if apple.position == snake.get_head_position():
            apple.randomize_position()
            poison.randomize_position()
            if apple.position in snake.positions:
                apple.randomize_position()
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        if snake.get_head_position() == stone1.position:
            snake.reset()
        if snake.get_head_position() == stone2.position:
            snake.reset()
        if snake.get_head_position() == stone3.position:
            snake.reset()
        if snake.get_head_position() == poison.position:
            poison.randomize_position()
            if snake.length != 1:
                snake.length -= 1
                snake.positions.pop()
            else:
                snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        poison.draw_cell()
        stone1.draw_cell()
        stone2.draw_cell()
        stone3.draw_cell()
        pygame.display.update()


if __name__ == '__main__':
    main()
