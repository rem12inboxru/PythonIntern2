import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        #self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.palette_color = 'white'  # начальный цвет палитры
        self.fon_color = 'white'

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # привязка функции выбора цвета с палитры к правой кнопке мыши.
        self.canvas.bind('<Button-1>', self.motion)      # кнопка фиксирует расположение текста на холсте

        self.root.bind('<Control-s>', self.save_image)  # горячая клавиша для сохранения
        self.root.bind('<Control-c>', self.choose_color)  # горячая клавиша вызова меню выбора цвета

        self.memory_color = []  # список - ячейка памяти - сохраняет цвет кисти
        self.memory_text = ['',]   # список - ячейка памяти - сохраняет текст

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Метка рядом с кнопкой выбора размера кисти
        size_brush_button = tk.Label(control_frame, text="Размер кисти")
        size_brush_button.pack(side=tk.LEFT)
        self.brush_size_menu(control_frame)

        #self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        #self.brush_size_scale.pack(side=tk.LEFT)

        rubber_button = tk.Label(control_frame, text="Ластик")  # Метка рядом с ячейкой состояния ластика
        rubber_button.pack(side=tk.LEFT)
        self.var = tk.BooleanVar()  # Вспомогательная переменная для описания состояния ластика
        #   Ячейка состояния ластика - включено или выключено
        rubber_button = tk.Checkbutton(control_frame, text="", variable=self.var, command=self.rubber)
        rubber_button.pack(side=tk.LEFT)

        # Кнопка для вызова меню выбора размеров холста
        win_size_button = tk.Button(control_frame, text="Размер холста", command=self.window_size)
        win_size_button.pack(side=tk.LEFT)

        # Кнопка для вызова диалогового окна для ввода текста
        text_button = tk.Button(control_frame, text='Текст', command=self.input_text)
        text_button.pack(side=tk.LEFT)

        # Кнопка выбора цвета фона
        fon_button = tk.Button(control_frame, text='Выбрвть фон', command=self.choice_fon)
        fon_button.pack(side=tk.LEFT)

        # палитра расположена в нижней части "холста"
        self.palette = tk.Label(self.root, text='Палитра для просмотра цвета кисти', bg=self.palette_color, width=90,
                                height=2)
        self.palette.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        # Запоминаем значение цвета кисти, к нему можно вернуться после выключения ластика
        self.memory_color.append(self.pen_color)
        self.update_palette()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def brush_size_menu(self, x):
        '''
        Функция создает меню для выбора ширины кисти
        '''
        sizes = [1, 2, 3, 5, 7, 10, 15]
        self.brush_size = tk.IntVar(value=1)
        self.menu = tk.OptionMenu(x, self.brush_size, *sizes, command=self.update_brush_size)
        self.menu.pack(side=tk.LEFT)

    def update_brush_size(self, value):
        '''
        Вспомогательная функция обновляет размер кисти
        '''
        self.brush_size.set(value)

    def rubber(self):
        '''
        Режим ластика
        Если ластик "включен" вспомогательная переменная возвращает True, цвету кисти приваивается
        значение белого цвета, как общий фон. Если ластик "выключен", цвету кисти присваивается
        последнее значение, которое было перед использованием ластика - из списка - ячейки памяти
        '''
        if self.var.get():
            self.pen_color = 'white'
        else:
            self.pen_color = self.memory_color[-1]

    def pick_color(self, event):
        '''
        Функциональный инструмент в виде пипетки для выбора цвета из любой точки на палитре.
        '''
        z = self.image.getpixel((event.x, event.y))  # определяем цвет в нужной точке палитры
        self.pen_color = self.rgb_to_hex(z)
        # присваиваем цвету кисти цвет нужной точки на палитре в шестнадцатеричном коде.

    # Вспомогательная функция для преобразования кода цвета из RGB в шестнадцатеричный
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    # функция согласования цвета на палитре с выбранным цветом
    def update_palette(self):
        self.palette_color = self.palette.config(bg=self.pen_color)

    def window_size(self):
        '''
        Функция открывает последовательно два диалоговых окна в которых
        запрашивает у пользователя желаемые размеры высоты и ширины холста.
        Потом создает новый холст с указанными размерами.
        '''
        new_height = simpledialog.askinteger('Размер холста', 'Введите высоту холста: ')
        new_width = simpledialog.askinteger('Размер холста', 'Введите ширину холста:  ')
        self.canvas.config(width=new_width, height=new_height)
        self.image = Image.new("RGB", (new_width, new_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def input_text(self):
        '''
        Функция вызова диалогового окна и сохранения текста
        '''
        self.text_user = simpledialog.askstring('Ввод текста', 'Текст: ')
        self.memory_text.append(self.text_user)


    def motion(self, event):
        '''
        Функция добавляет текст в выбранное место
        '''
        x, y = event.x, event.y
        self.canvas.create_text(x, y, text=self.memory_text[-1], fill=self.pen_color)
        self.draw.text((x, y), self.memory_text[-1], fill=self.pen_color)


    def choice_fon(self):
        '''
        Функция позволяет выбрать цвет фона
        '''
        self.fon_color = colorchooser.askcolor(color=self.fon_color)[1]
        self.canvas.config(background=self.fon_color)

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
