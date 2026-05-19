import pygame
import sys
from Field import Field
from Population import Population

class World:
    def __init__(self, width=320, height=240, cell_size=20, pop_size=100, mutation_rate=0.05, max_generations=500):
        self.field = Field(width, height, cell_size)
        self.population = Population(pop_size, self.field)
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        
        # Храним глобального победителя за все поколения
        self.all_time_best_snake = None
        self.historical_best_fitness = 0

        self.history_generations = []
        self.history_max_fitness = []
        self.history_avg_fitness = []
        self.history_max_score = []

    def train(self):
        """Проводит симуляцию генетического алгоритма без отрисовки (для скорости)."""
        print(f"[{'='*40}]")
        print(f" НАЧАЛО ОБУЧЕНИЯ")
        print(f" Поколений: {self.max_generations} | Размер популяции: {len(self.population.snakes)}")
        print(f" Мутация: {self.mutation_rate * 100}%")
        print(f"[{'='*40}]\n")

        while self.population.gen <= self.max_generations:
            # Обрабатываем события Pygame, чтобы окно не "зависало" (Not Responding) в ОС
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Обновляем всех змеек в текущем поколении
            self.population.update()
            
            # Когда все змейки погибли
            if self.population.is_done():
                self.population.calculate_fintess()
                
                # Сбор статистики
                current_best_snake = self.population.get_best_snake()
                avg_fitness = sum(s.fitness for s in self.population.snakes) / len(self.population.snakes)
                max_score = max(s.score for s in self.population.snakes)
                
                # Сохраняем абсолютного чемпиона
                if current_best_snake.fitness > self.historical_best_fitness:
                    self.historical_best_fitness = current_best_snake.fitness
                    # Ссылка безопасна, т.к. natural_selection создает новые объекты змеек
                    self.all_time_best_snake = current_best_snake 
                    
                # Красивый вывод в консоль
                print(f"Поколение: {self.population.gen:03d}/{self.max_generations} | "
                      f"Топ Фитнес: {current_best_snake.fitness:8.2f} | "
                      f"Ср. Фитнес: {avg_fitness:8.2f} | "
                      f"Рекорд яблок: {max_score}")
                
                # Сохранение метрик
                self.history_generations.append(self.population.gen)
                self.history_max_fitness.append(current_best_snake.fitness)
                self.history_avg_fitness.append(avg_fitness)
                self.history_max_score.append(max_score)
                
                # Эволюция
                self.population.natural_selection()
                self.population.mutate(self.mutation_rate)
                
        print(f"\n[{'='*40}]")
        print(f" ОБУЧЕНИЕ ЗАВЕРШЕНО")
        print(f" Абсолютный рекорд Fitness: {self.historical_best_fitness:.2f}")
        print(f"[{'='*40}]\n")

        self.save_history_to_file()

    def save_history_to_file(self, filename="./stats.txt"):
        """Сохраняет собранные метрики в текстовый файл для последующего построения графиков."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                # Записываем заголовки колонок
                f.write("generation,max_fitness,avg_fitness,max_score\n")
                for i in range(len(self.history_generations)):
                    f.write(f"{self.history_generations[i]},"
                            f"{self.history_max_fitness[i]},"
                            f"{self.history_avg_fitness[i]},"
                            f"{self.history_max_score[i]}\n")
            print(f"Статистика успешно сохранена в файл {filename}")
        except Exception as e:
            print(f"Не удалось сохранить статистику: {e}")

    def play_best(self, fps=15):
        """Запускает визуальную симуляцию лучшей найденной змейки."""
        if not self.all_time_best_snake:
            print("Ошибка: Сначала запустите обучение (.train())!")
            return
            
        print("Запуск нейросети чемпиона...")
        print("Управление: 'R' - перезапустить чемпиона, 'Q' - выход.")
        
        clock = pygame.time.Clock()
        best = self.all_time_best_snake
        
        # Сбрасываем её состояние перед показом
        best.reset()
        best.food.respawn(self.field, best)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        best.reset()
                        best.food.respawn(self.field, best)
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            
            if best.alive:
                best.look()
                best.change_direction_ai()
                best.move()
                self.field.update(best)
            else:
                # Если чемпион случайно врезался, просто перезапускаем его
                self.field.screen.fill((0, 0, 0))
                pygame.display.flip()
                best.reset()
                best.food.respawn(self.field, best)

            clock.tick(fps)