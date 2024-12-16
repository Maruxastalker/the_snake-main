from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

STONE_COLOR = (158,158,158)
# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

my_game =False
# Тут опишите все классы игры.

class GameObject:
    body_color = None

    def draw(self):
        pass

    def __init__(self):
        self.position = ((SCREEN_WIDTH//2),(SCREEN_HEIGHT//2))

class Stone(GameObject):
    body_color = STONE_COLOR


    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def __init__(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

class Apple(GameObject):

    body_color = APPLE_COLOR


    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    
    def __init__(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        

class Snake(GameObject):

    length = 1
    positions = [] 
    direction = UP
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self):
        super().__init__()
        self.positions.append(self.position) 
        

    def draw(self):
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
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


    def move(self):
        self.update_direction() 
        if self.direction == RIGHT:
            new_position = (self.positions[0][0] + GRID_SIZE, self.positions[0][1])
        elif self.direction == LEFT:
            new_position = (self.positions[0][0] - GRID_SIZE, self.positions[0][1])
        elif self.direction == UP:
            new_position = (self.positions[0][0], self.positions[0][1] - GRID_SIZE)
        elif self.direction == DOWN:
            new_position = (self.positions[0][0], self.positions[0][1] + GRID_SIZE)

        
        if self.positions:
            self.last = self.positions[-1]
        
        self.positions.insert(0, new_position)
        
        if self.length<len(self.positions[1:]):
            self.positions.pop() 
        
        if new_position[0]<0 or new_position[0]>=SCREEN_WIDTH:
            self.reset()
        elif new_position[1]<0 or new_position[1]>=SCREEN_HEIGHT:
            self.reset()
        

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
    

    def get_head_position(self):
        return self.positions[0]
    

    def reset(self):    
        self.length = 1
        self.positions.clear()
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions.append(self.position)
            
            
        
            
def handle_keys(game_object):
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
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    stone1 = Stone()
    stone2 = Stone()
    stone3 = Stone()
    gameobject = GameObject()
    while True:

        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if apple.position == snake.get_head_position():
            apple.randomize_position()
            snake.length+=1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        if snake.get_head_position() == stone1.position:
            snake.reset()
        if snake.get_head_position() == stone2.position:
            snake.reset()
        if snake.get_head_position() == stone3.position:
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        stone1.draw()
        stone2.draw()
        stone3.draw()
        pygame.display.update()
        
        # Тут опишите основную логику игры.
        # ...
    

if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
