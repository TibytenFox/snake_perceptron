import pygame
import sys
from World import World
from Field import Field
from Snake import Snake


def main_human():
    """Режим игры для человека (ручное управление клавишами)."""
    field = Field()
    snake = Snake(field)

    fps = 10
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not snake.alive:
                    snake.reset()
                    snake.food.respawn(field, snake)
                else:
                    snake.change_direction(event.key)

        if snake.alive:
            snake.move()
            field.update(snake)
        else:
            field.screen.fill((0, 0, 0))
            pygame.display.flip()

        clock.tick(fps)
        
def main_ai():
    """Режим генетического алгоритма (нейроэволюция)."""
    
    # Создание мира и настройка гиперпараметров
    world = World(
        width=640, 
        height=480, 
        cell_size=20, 
        pop_size=200, 
        mutation_rate=0.01, 
        max_generations=500
    )

    # Продолжение эволюции из файла
    # world.population.read_population()

    # Запуск быстрого обучения без графики
    world.train()

    # Сохранение весов лучшего поколения
    world.population.save_population()

    # Демонстрация игры финального чемпиона
    world.play_best(fps=15)
            

if __name__ == "__main__":
    main_ai()