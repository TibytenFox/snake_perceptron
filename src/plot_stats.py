import os
import matplotlib.pyplot as plt

def plot_learning_curves(filename="./stats.txt"):
    if not os.path.exists(filename):
        print(f"Ошибка: Файл данных '{filename}' не найден. Сначала запустите обучение змейки!")
        return

    # Списки для чтения данных
    generations = []
    max_fitness = []
    avg_fitness = []
    max_scores = []

    # Читаем данные из файла
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            if not line.strip():
                continue
            gen, idx_fit, avg_fit, score = line.strip().split(",")
            generations.append(int(gen))
            max_fitness.append(float(idx_fit))
            avg_fitness.append(float(avg_fit))
            max_scores.append(int(score))

    # Настраиваем стиль
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    
    # Создаем 3 подграфика по вертикали (изменили figsize для вместительности)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    fig.suptitle("Анализ результатов нейроэволюции змейки", fontsize=16, fontweight='bold')

    # --- График 1: Метрика МАКСИМАЛЬНОГО Фитнеса ---
    ax1.plot(generations, max_fitness, label="Макс. Фитнес поколения (Рекорд)", color="crimson", linewidth=2)
    ax1.set_ylabel("Max Fitness", fontsize=11)
    ax1.set_title("Абсолютная приспособленность (лучшая особь)", fontsize=12)
    ax1.legend(loc="upper left")
    ax1.grid(True, linestyle=":", alpha=0.6)

    # --- График 2: Метрика СРЕДНЕГО Фитнеса (теперь на своей шкале!) ---
    ax2.plot(generations, avg_fitness, label="Ср. Фитнес поколения", color="royalblue", linewidth=1.5, linestyle="--")
    ax2.set_ylabel("Avg Fitness", fontsize=11)
    ax2.set_title("Средняя приспособленность всей популяции", fontsize=12)
    ax2.legend(loc="upper left")
    ax2.grid(True, linestyle=":", alpha=0.6)

    # --- График 3: Максимальный счет (Яблоки) ---
    ax3.plot(generations, max_scores, label="Рекорд съеденных яблок", color="forestgreen", linewidth=2)
    ax3.set_xlabel("Номер поколения (Generation)", fontsize=12)
    ax3.set_ylabel("Количество яблок (Score)", fontsize=11)
    ax3.set_title("Максимальный игровой счет", fontsize=12)
    ax3.legend(loc="upper left")
    ax3.grid(True, linestyle=":", alpha=0.6)

    # Оптимизируем расположение элементов
    plt.tight_layout()
    
    print("Графики успешно разделены и построены. Отображение окна...")
    plt.show()

if __name__ == "__main__":
    plot_learning_curves()