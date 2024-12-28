import pygame
import random
import sys
import math
import os

# Инициализация Pygame и звуковой системы
pygame.init()
try:
    # Пробуем разные частоты дискретизации
    for frequency in [44100, 22050, 48000]:
        try:
            pygame.mixer.quit()  # Сначала закроем микшер если он был открыт
            pygame.mixer.init(frequency, -16, 2, 512)  # Уменьшенный размер буфера
            if pygame.mixer.get_init():
                print(f"Mixer initialized with frequency {frequency}")
                break
        except:
            continue
    
    if not pygame.mixer.get_init():
        print("Failed to initialize mixer with any frequency")
        sounds_loaded = False
except Exception as e:
    print(f"Ошибка инициализации микшера: {str(e)}")
    sounds_loaded = False

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (100, 149, 237)
SNOW_COLOR = (240, 240, 255)
BROWN = (139, 69, 19)

# Настройка окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Новогодняя Змейка')
clock = pygame.time.Clock()

# Загрузка звуков и настройка громкости
sounds_loaded = False
try:
    if pygame.mixer.get_init():
        # Используем абсолютные пути для всех звуковых файлов
        base_path = '/Users/raddayurieva/Downloads/snake'
        sound_files = {
            'bell': os.path.join(base_path, 'sounds', 'bell.wav'),
            'game_over': os.path.join(base_path, 'sounds', 'game_over.mp3'),
            'music': os.path.join(base_path, 'sounds', 'jingle_bells.mp3')
        }
        
        # Создаем директорию sounds если её нет
        sounds_dir = os.path.join(base_path, 'sounds')
        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)
            print(f"Создана директория: {sounds_dir}")
        
        for name, path in sound_files.items():
            if not os.path.exists(path):
                print(f"Файл {name} не найден: {path}")
                raise FileNotFoundError(f"Файл {path} не существует")
        
        # Загружаем звуки
        collect_sound = pygame.mixer.Sound(sound_files['bell'])
        print("Bell sound loaded successfully")
        game_over_sound = pygame.mixer.Sound(sound_files['game_over'])
        print("Game over sound loaded successfully")
        
        # Загружаем музыку
        pygame.mixer.music.load(sound_files['music'])
        print("Music loaded successfully")
        
        # Настройка громкости
        collect_sound.set_volume(0.5)  # Увеличиваем громкость
        game_over_sound.set_volume(0.6)  # Увеличиваем громкость
        pygame.mixer.music.set_volume(0.4)  # Увеличиваем громкость фоновой музыки
        
        # Пробуем воспроизвести музыку
        try:
            pygame.mixer.music.play(-1)
            print("Music started playing")
            # Проверяем, действительно ли музыка играет
            if pygame.mixer.music.get_busy():
                print("Music is actually playing")
            else:
                print("Music not playing despite successful play() call")
            sounds_loaded = True
        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {str(e)}")
    else:
        print("Микшер не был инициализирован")
except Exception as e:
    print(f"Ошибка при загрузке звуков: {str(e)}")
    import traceback
    traceback.print_exc()  # Печатаем полный стек ошибки

GREETING = "С НОВЫМ 2025 ГОДОМ"
LETTERS = list(GREETING.replace(" ", "_"))  # Заменяем пробелы на подчеркивания для отображения

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(-50, 0)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(2, 4)

    def fall(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, WINDOW_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, SNOW_COLOR, (int(self.x), int(self.y)), self.size)

# Создаем список снежинок
snowflakes = [Snowflake() for _ in range(100)]

def draw_christmas_tree(surface, x, y, size):
    # Ствол
    pygame.draw.rect(surface, BROWN, (x + size//3, y + size - size//4, size//3, size//4))
    # Ёлка (три треугольника)
    for i in range(3):
        points = [
            (x + size//2, y + i * size//3),
            (x, y + size//3 * (i + 1)),
            (x + size, y + size//3 * (i + 1))
        ]
        pygame.draw.polygon(surface, DARK_GREEN, points)
        # Украшения на ёлке
        for _ in range(3):
            dec_x = random.randint(int(x), int(x + size))
            dec_y = random.randint(int(y + i * size//3), int(y + size//3 * (i + 1)))
            pygame.draw.circle(surface, RED, (dec_x, dec_y), 3)

def draw_santa_hat(surface, x, y, size):
    # Основная часть шапки
    pygame.draw.rect(surface, RED, (x, y, size, size-5))
    # Белая опушка
    pygame.draw.rect(surface, WHITE, (x, y + size-7, size, 7))
    # Помпон
    pygame.draw.circle(surface, WHITE, (x + size//2, y), size//3)

def draw_letter(surface, x, y, size, letter):
    # Рисуем букву на черном фоне
    bg_rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(surface, BLACK, bg_rect)
    pygame.draw.rect(surface, WHITE, bg_rect, 1)
    
    # Отрисовка буквы
    font = pygame.font.Font(None, size)
    text = font.render(letter, True, WHITE)
    text_rect = text.get_rect(center=(x + size//2, y + size//2))
    surface.blit(text, text_rect)

def draw_background():
    # Рисуем фон в виде зимнего неба
    screen.fill(BLUE)
    
    # Добавляем звезды
    for _ in range(50):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT//2)
        size = random.randint(1, 3)
        pygame.draw.circle(screen, WHITE, (x, y), size)
    
    # Рисуем ёлки по краям
    for i in range(5):
        draw_christmas_tree(screen, 50, 100 + i * 100, 60)
        draw_christmas_tree(screen, WINDOW_WIDTH - 110, 100 + i * 100, 60)
    
    # Обновляем и рисуем падающий снег
    for snowflake in snowflakes:
        snowflake.fall()
        snowflake.draw(screen)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.current_letter_index = 0
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))
    
    def get_current_letter(self):
        return LETTERS[self.current_letter_index]
    
    def next_letter(self):
        self.current_letter_index = (self.current_letter_index + 1) % len(LETTERS)

def draw_snowman(surface, x, y, size):
    # Нижний шар (самый большой)
    pygame.draw.circle(surface, WHITE, (x, y), size)
    # Средний шар
    pygame.draw.circle(surface, WHITE, (x, y - size*0.8), size*0.7)
    # Голова
    pygame.draw.circle(surface, WHITE, (x, y - size*1.5), size*0.5)
    
    # Глаза
    eye_color = BLACK
    pygame.draw.circle(surface, eye_color, (x - size*0.2, y - size*1.6), size*0.08)
    pygame.draw.circle(surface, eye_color, (x + size*0.2, y - size*1.6), size*0.08)
    
    # Морковка-нос
    nose_points = [(x, y - size*1.5),
                   (x + size*0.3, y - size*1.45),
                   (x, y - size*1.4)]
    pygame.draw.polygon(surface, (255, 165, 0), nose_points)  # Оранжевый цвет
    
    # Пуговицы
    for i in range(3):
        pygame.draw.circle(surface, BLACK, (x, y - size*0.3 - i*0.4*size), size*0.08)

def draw_gifts(surface, x, y, size):
    # Рисуем несколько подарков разных цветов
    gift_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0)]
    for i, color in enumerate(gift_colors):
        # Коробка подарка
        gift_x = x + (i - len(gift_colors)/2) * size * 1.2
        pygame.draw.rect(surface, color, (gift_x, y, size, size))
        # Ленточка
        ribbon_color = WHITE
        pygame.draw.rect(surface, ribbon_color, (gift_x + size/2 - size*0.1, y, size*0.2, size))
        pygame.draw.rect(surface, ribbon_color, (gift_x, y + size/2 - size*0.1, size, size*0.2))
        # Бант
        pygame.draw.circle(surface, ribbon_color, (int(gift_x + size/2), int(y + size/2)), int(size*0.2))

def main():
    snake = Snake()
    food = Food()
    score = 0
    game_active = True
    show_victory_screen = False  # Добавляем новую переменную
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active:
                    # Перезапуск игры
                    snake.reset()
                    food.randomize_position()
                    score = 0
                    game_active = True
                    show_victory_screen = False  # Сбрасываем флаг
                    pygame.mixer.music.play(-1)
                elif game_active:  # Обрабатываем управление только при активной игре
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if game_active:
            if not snake.update():
                game_active = False
                if sounds_loaded:
                    pygame.mixer.music.stop()
                    game_over_sound.play()
            
            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food.next_letter()
                food.randomize_position()
                if sounds_loaded:
                    collect_sound.play()
            
                # Проверка победы
                if score == len(LETTERS):
                    game_active = False
                    show_victory_screen = True  # Устанавливаем флаг победы
                    if sounds_loaded:
                        pygame.mixer.music.stop()
                        game_over_sound.play()

        # Отрисовка
        if show_victory_screen:
            # Рисуем победный экран
            screen.fill(BLUE)
            
            # Рисуем падающий снег
            for snowflake in snowflakes:
                snowflake.fall()
                snowflake.draw(screen)
            
            # Рисуем снеговика в центре
            snowman_size = 80  # Увеличим размер снеговика
            draw_snowman(screen, WINDOW_WIDTH//2, WINDOW_HEIGHT//2, snowman_size)
            
            # Рисуем подарки под снеговиком
            gift_size = 50  # Увеличим размер подарков
            draw_gifts(screen, WINDOW_WIDTH//2 - gift_size*2, WINDOW_HEIGHT//2 + snowman_size + 20, gift_size)
            
            # Победное сообщение
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render('С Новым 2025 Годом!', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/4))
            screen.blit(game_over_text, text_rect)
            
            restart_text = game_over_font.render('Нажмите пробел для новой игры', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4))
            screen.blit(restart_text, restart_rect)
        else:
            # Обычная отрисовка игры
            draw_background()
            
            # Отрисовка змейки
            for i, pos in enumerate(snake.positions):
                x, y = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE
                pygame.draw.rect(screen, DARK_GREEN, (x, y, GRID_SIZE-2, GRID_SIZE-2))
                if i == 0:  # Если это голова
                    draw_santa_hat(screen, x, y-10, GRID_SIZE)
            
            # Отрисовка буквы
            draw_letter(screen, 
                       food.position[0] * GRID_SIZE,
                       food.position[1] * GRID_SIZE,
                       GRID_SIZE,
                       food.get_current_letter())
            
            # Отображение собранных букв
            collected_text = ''.join(LETTERS[:score]).replace("_", " ")
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Собрано: {collected_text}', True, WHITE)
            screen.blit(score_text, (10, 10))
            
            # Сообщение о проигрыше
            if not game_active and not show_victory_screen:
                game_over_font = pygame.font.Font(None, 48)
                game_over_text = game_over_font.render('Игра окончена! Нажмите пробел для рестарта', True, WHITE)
                text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                screen.blit(game_over_text, text_rect)
        
        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main() 