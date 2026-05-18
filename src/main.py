import pygame
from Field import *
from Snake import *
from Population import *


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
    field = Field()
    population = Population(100, field)

    best_snakes = []
    global_mutatin_rate = 0.01

    generations = 50

    while population.gen < generations:
        population.update()
        
        if population.is_done():
            population.calculate_fintess()
            best_snakes.append(population.get_best_snake())
            population.natural_selection()
            population.mutate(global_mutatin_rate)

    fps = 10
    clock = pygame.time.Clock()
    best_snake_ind = max([(best_snakes[i].fitness, i) for i in range(len(best_snakes))])[1]
    best_snake = best_snakes[best_snake_ind]

    # for i in range(len(best_snakes)):
    #     print(best_snakes[i].fitness)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                
        if best_snake.alive:
            best_snake.look()
            best_snake.change_direction_ai()
            best_snake.move()
            field.update(best_snake)
        else:
            field.screen.fill((0, 0, 0))
            pygame.display.flip()

            best_snake.reset()
            best_snake.food.respawn(field, best_snake)

        clock.tick(fps)
            

if __name__ == "__main__":
    main_ai()