import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # привязка функции выбора цвета с палитры к правой кнопке мыши.

        self.memory_color = []   # список - ячейка памяти - сохраняет цвет кисти


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

        rubber_button = tk.Label(control_frame, text="Ластик")   # Метка рядом с ячейкой состояния ластика
        rubber_button.pack(side=tk.LEFT)
        self.var = tk.BooleanVar()           # Вспомогательная переменная для описания состояния ластика
        #   Ячейка состояния ластика - включено или выключено
        rubber_button = tk.Checkbutton(control_frame, text="", variable=self.var, command=self.rubber)
        rubber_button.pack(side=tk.LEFT)

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

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        # Запоминаем значение цвета кисти, к нему можно вернуться после выключения ластика
        self.memory_color.append(self.pen_color)

    def save_image(self):
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
        self.brush_size = tk.IntVar(value= 1)
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
        self.pen_color = self.rgb_to_hex(z)          # присваиваем цвету кисти цвет нужной точки на палитре в шестнадцатеричном коде.

    # Вспомогательная функция для преобразования кода цвета из RGB в шестнадцатеричный
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb





def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()