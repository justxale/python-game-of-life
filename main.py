import enum
import tkinter as tk
import random

# Параметры поля
WIDTH = 50
HEIGHT = 50
CELL_SIZE = 12
UPDATES_PER_SECOND = 20


class ButtonText(enum.StrEnum):
    """
    Значения текста кнопок
    """
    START = 'Запустить автообновление'
    STOP = 'Остановить автообновление'
    CLEAR = "Очистить поле"
    NEXT_FRAME = "Следующий кадр"


class CellStatus(enum.IntEnum):
    """
    Значения состояния клетки
    """
    ALIVE = 1
    DEAD = 0


def initialize_board() -> list[list[CellStatus]]:
    """
    Инициализатор поля случайными значениями
    :return: Рандомно сгенерированное поле
    """
    return [[random.choice([CellStatus.DEAD, CellStatus.ALIVE]) for _ in range(WIDTH)] for _ in range(HEIGHT)]


# Count live neighbors of a given cell
def count_neighbors(board: list[list[CellStatus]], x: int, y: int) -> int:
    """
    Функция подсчёта соседей данной клетки
    :param board: Текущее поле
    :param x: Координата клетки по оси X
    :param y: Координата клетки по оси Y
    :return: Количество соседей
    """
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:  # пропускаем себя же
                continue
            board_x = x + i
            board_y = y + j  # координаты на поле
            neighbors += board[board_x % WIDTH][board_y % HEIGHT]
    return neighbors


def update_board(board: list[list[CellStatus]]) -> list[list[CellStatus]]:
    """
    Функция обновления поля
    :param board: Текущее поле
    :return: Обновлённое поле
    """
    board_copy = [[CellStatus.DEAD for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(HEIGHT):
        for y in range(WIDTH):
            neighbors = count_neighbors(board, x, y)
            match board[x][y]:
                case 1:  # Живая клетка
                    if neighbors < 2 or neighbors > 3:
                        board_copy[x][y] = CellStatus.DEAD  # Клетка умирает из-за перенаселения или одиночества
                    else:
                        board_copy[x][y] = CellStatus.ALIVE  # Клетка выживает
                case 0:  # Мёртвая клетка
                    if neighbors == 3:
                        board_copy[x][y] = CellStatus.ALIVE  # В клетке зарождается жизнь
    return board_copy


class GameOfLifeApp:
    """
    Основной класс интерфейса симуляции
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.running = False
        self.root.title("Игра Жизнь")

        self.start_button = tk.Button(root, text=ButtonText.START, command=self.toggle_auto_update)
        self.start_button.pack()

        self.next_frame_button = tk.Button(root, text=ButtonText.NEXT_FRAME, command=self.next_frame)
        self.next_frame_button.pack()

        self.clear_button = tk.Button(root, text=ButtonText.CLEAR, command=self.clear_grid)
        self.clear_button.pack()

        self.canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.board = initialize_board()

        self.draw_grid()

        self.auto_update_game()

    def draw_grid(self) -> None:
        """
        Метод отрисовки поля
        :return: None
        """
        self.canvas.delete("all")
        for x in range(HEIGHT):
            for y in range(WIDTH):
                color = 'blue' if self.board[x][y] == 1 else 'white'
                self.canvas.create_rectangle(
                    y * CELL_SIZE, x * CELL_SIZE,
                    (y + 1) * CELL_SIZE, (x + 1) * CELL_SIZE,
                    fill=color, outline='gray'
                )

    def next_frame(self) -> None:
        """
        Метод обновления кадра
        :return: None
        """
        self.board = update_board(self.board)
        self.draw_grid()

    def toggle_cell(self, event) -> None:
        """
        Метод переключения состояния клетки
        :param event: События нажатия кнопки
        :return: None
        """
        x, y = event.y // CELL_SIZE, event.x // CELL_SIZE
        self.board[x][y] = 1 - self.board[x][y]
        self.draw_grid()

    def toggle_auto_update(self) -> None:
        """
        Метод переключения статуса автообновления
        :return: None
        """
        self.running = not self.running
        if self.running:
            self.start_button.config(text=ButtonText.STOP)
        else:
            self.start_button.config(text=ButtonText.START)

    def clear_grid(self) -> None:
        """
        Метод очистки поля
        :return: None
        """
        self.board = [[CellStatus.DEAD] * WIDTH for _ in range(HEIGHT)]
        self.draw_grid()

    def auto_update_game(self) -> None:
        """
        Метод для автообновления игры
        :return:
        """
        if self.running:
            self.next_frame()
        self.root.after(1000 // UPDATES_PER_SECOND, self.auto_update_game)


def main() -> None:
    try:
        root = tk.Tk()
        app = GameOfLifeApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

