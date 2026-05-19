import pygame
import sys
from World import World
from Field import Field
from Snake import Snake


def main_human():
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
            # Show game over message
            field.screen.fill((0, 0, 0))
            pygame.display.flip()

        clock.tick(fps)
        
def main_ai():
    """Режим генетического алгоритма"""
    
    # 1. Создаем мир (настраиваем гиперпараметры)
    world = World(
        width=320, 
        height=240, 
        cell_size=20, 
        pop_size=200, 
        mutation_rate=0.05, 
        max_generations=150
    )

    # Можно добавить уже умную змейку в начальную популяцию
    # world.population.snakes[0].read_from_file()

    # 2. Быстро обучаем (без отрисовки графики для скорости)
    world.train()

    # 3. Сохраняем мозг лучшей змейки
    world.all_time_best_snake.save_to_file()

    # 3.5 Загружаем готовую змейку (необязательно)
    # world.all_time_best_snake.read_from_file()

    # 4. Визуализируем самую успешную змейку
    world.play_best(fps=15)
            

if __name__ == "__main__":
    main_ai()