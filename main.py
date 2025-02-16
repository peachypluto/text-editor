import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import font as tkFont
from docx import Document
from docx.shared import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовый редактор/процессор")

        self.text_area = tk.Text(root, wrap='word', font=("Arial", 12))
        self.text_area.pack(expand=1, fill='both')

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Файл", menu=self.file_menu)
        self.file_menu.add_command(label="Создать", command=self.new_file)
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        self.file_menu.add_command(label="Сохранить", command=self.save_file)
        self.file_menu.add_command(label="Сохранить как DOCX", command=self.save_as_docx)
        self.file_menu.add_command(label="Сохранить как PDF", command=self.save_as_pdf)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход", command=root.quit)

        self.format_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Формат", menu=self.format_menu)
        self.format_menu.add_command(label="Шрифт", command=self.change_font)
        self.format_menu.add_command(label="Выравнивание", command=self.align_text)
        self.format_menu.add_command(label="Создать список", command=self.create_list)
        self.format_menu.add_command(label="Создать таблицу", command=self.create_table)
        self.format_menu.add_command(label="Добавить ссылку", command=self.add_link)
        self.format_menu.add_command(label="Добавить изображение", command=self.add_image)
        self.format_menu.add_command(label="Создать график", command=self.create_chart)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def save_as_docx(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                 filetypes=[("Word files", "*.docx"),
                                                            ("All files", "*.*")])
        if file_path:
            doc = Document()
            content = self.text_area.get(1.0, tk.END).strip().split('\n')
            for line in content:
                doc.add_paragraph(line)
            doc.save(file_path)

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf"),
                                                            ("All files", "*.*")])
        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            text = self.text_area.get(1.0, tk.END).strip().split('\n')
            y = height - 40

            for line in text:
                c.drawString(40, y, line)
                y -= 15

            c.save()

    def change_font(self):
        font_name = simpledialog.askstring("Шрифт", "Введите название шрифта:")
        font_size = simpledialog.askinteger("Размер шрифта", "Введите размер шрифта:")

        if font_name and font_size:
            new_font = (font_name, font_size)
            self.text_area.config(font=new_font)

    def align_text(self):
        alignment = simpledialog.askstring("Выравнивание", "Введите выравнивание (left/center/right):")

        if alignment == "left":
            self.text_area.tag_configure("left", justify='left')
            self.text_area.tag_add("left", 1.0, "end")
        elif alignment == "center":
            self.text_area.tag_configure("center", justify='center')
            self.text_area.tag_add("center", 1.0, "end")
        elif alignment == "right":
            self.text_area.tag_configure("right", justify='right')
            self.text_area.tag_add("right", 1.0, "end")

    def create_list(self):
        list_items = simpledialog.askstring("Создать список", "Введите элементы списка через запятую:")
        if list_items:
            items = list_items.split(',')
            for item in items:
                self.text_area.insert(tk.END, f"• {item.strip()}\n")

    def create_table(self):
        rows = simpledialog.askinteger("Создать таблицу", "Введите количество строк:")
        cols = simpledialog.askinteger("Создать таблицу", "Введите количество столбцов:")

        if rows and cols:
            table_str = ""
            for r in range(rows):
                row_data = []
                for c in range(cols):
                    cell_data = simpledialog.askstring("Таблица", f"Введите данные для ячейки ({r + 1}, {c + 1}):")
                    row_data.append(cell_data if cell_data else "")
                table_str += '\t'.join(row_data) + '\n'
            self.text_area.insert(tk.END, table_str + "\n")

    def add_link(self):
        link_text = simpledialog.askstring("Добавить ссылку", "Введите текст ссылки:")
        link_url = simpledialog.askstring("Добавить ссылку", "Введите URL:")

        if link_text and link_url:
            self.text_area.insert(tk.END, f"{link_text} ({link_url})\n")

    def add_image(self):
        img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])

        if img_path:
            img = Image.open(img_path)
            img.thumbnail((100, 100))
            img.save("temp_image.png")
            self.text_area.image_create(tk.END, image=ImageTk.PhotoImage(img))

    def create_chart(self):
        plt.plot([1, 2, 3], [4, 5, 6])
        plt.title('Простой график')

        chart_path = 'chart.png'
        plt.savefig(chart_path)
        plt.close()

        img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])

        if img_path:
            img = Image.open(chart_path)
            img.thumbnail((100, 100))
            img.save("temp_chart.png")
            self.text_area.image_create(tk.END, image=ImageTk.PhotoImage(img))


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
