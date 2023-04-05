import tkinter as tk
import tkinter.font as tkFont 
from os import listdir, getcwd
from tkinter import ttk
from random import choice
from functools import partial
from Search import Search


class papan:
    def __init__(self, size=20, bg="orange", color="orange", file_name="kumpulan_kata.txt", words=None):
        assert size > 5
        root = tk.Tk()
        root.title("Permaianan Pencarian Kata") # judul dari program
        # root.resizable(width=False, height=True)

        self._word_grid = tk.Frame(root) #ukuran kata kata
        self._word_list = tk.Frame(root) #ukuran kumpulan kata
        self._menu = tk.Frame(root) # ukuran menu

        self._solution_shown = False
        self._size = size # fungsi untuk mengukur tata letak perkataan yang acak
        self._color = color # fungsi untuk memberikan waran pada satu kata kemudian diikuti pencarian kata contohnya PEN (P-E-N)
        self.bg = bg # fungsi ini untuk memberikan warna pada background sehingga mengetahui sesuai fitur pencaraian kata secara auto

        new_words_button = tk.DISABLED
        if file_name in listdir(getcwd()):
            new_words_button = tk.NORMAL
            with open(file_name, mode="r") as f:
                self._kumpulan_katatxt = filter(None, f.read().split("\n"))
                self._kumpulan_katatxt = list(
                    filter(lambda x: len(x) < self._size - 3, self._kumpulan_katatxt)
                )
        elif words is None:
            raise FileNotFoundError(
                f"""{file_name} terjadi error pada program. 
                tidak bisa dibuka karena ada problem pada beberapa file mohon dicek kembali."""
            )

        self._pushed = set()

        self._words = words
        if self._words is None:
            self._choose_random_words()
        else:
            self._words = list(set(map(str.upper, self._words)))

        self._buttons = []
        for i in range(self._size):
            row = []
            for j in range(self._size):
                row.append(
                    tk.Button(
                        self._word_grid, padx=6, command=partial(self._pressed, i, j)
                    )
                )
                row[-1].grid(row=i, column=j, sticky="ew")
            self._buttons.append(row)

        tk.Label(self._menu, text="Menu", pady=4, font=tkFont.Font(weight="bold")).grid(
            row=0, column=0, columnspan=4, sticky="ew"
        )
        tk.Button(
            self._menu,
            text="Buat Kata Baru",
            padx=1,
            pady=1,
            state=new_words_button,
            command=self._select_new,
        ).grid(row=2, column=0, sticky="ew")
        tk.Button(
            self._menu, text="Cari Kata", padx=1, pady=1, command=self._solution
        ).grid(row=2, column=2, sticky="ew")
        tk.Button(
            self._menu, text="Acak kata", padx=1, pady=1, command=self._reshuffle
        ).grid(row=2, column=1, sticky="ew")

        self._labels = {}
        self._Cari_kata = None
        self._create_labels()
        self._reshuffle()

        self._word_grid.pack(side=tk.BOTTOM)
        self._menu.pack(side=tk.RIGHT, pady=self._size)
        self._word_list.pack(side=tk.LEFT, padx=20, pady=40)

        tk.mainloop()

    def _create_labels(self):
        for label in self._labels.values():
            label.destroy()
        self._labels.clear()
        self._labels = {
            "KATA-KATA": tk.Label(
                self._word_list, text="KATA-KATA", pady=4, font=tkFont.Font(weight="bold")
            )
        }
        self._labels["KATA-KATA"].grid(row=2, column=0, columnspan=2)
        for i, word in enumerate(sorted(self._words)):
            self._labels[word] = tk.Label(
                self._word_list, text=word, anchor="w")
            self._labels[word].grid(
                row=(i // 2) + (i % 1) + 3, column=i % 2, sticky="W"
            )

    def _choose_random_words(self):
        self._words = set()
        for _ in range(choice(range(self._size // 3, self._size))):
            self._words.add(choice(self._kumpulan_katatxt).upper())
        self._words = list(self._words)

    def _pressed(self, row, col):
        if self._buttons[row][col].cget("bg") == self._color:
            self._buttons[row][col].configure(bg="SystemButtonFace")
            self._pushed.remove(
                (self._buttons[row][col].cget("text"), col, row))
        else:
            self._buttons[row][col].configure(bg=self._color)
            self._pushed.add((self._buttons[row][col].cget("text"), col, row))
            for word, coords in self._Cari_kata.solutions.items():
                if coords & self._pushed == coords:
                    for _, col, row in coords:
                        self._buttons[row][col].configure(state=tk.DISABLED)
                    self._labels[word].configure(bg=self._color)

    def _solution(self):
        if self._solution_shown:
            bg = "orange"
            state = tk.NORMAL
            self._pushed.clear()
        else:
            bg = self._color
            state = tk.DISABLED

        self._solution_shown = not self._solution_shown
        for word, coords in self._Cari_kata.solutions.items():
            self._labels[word].configure(bg=bg)
            for _, col, row in coords:
                self._buttons[row][col].configure(state=state, bg=bg)

    def _reshuffle(self):

        if self._solution_shown:
            self._solution_shown = not self._solution_shown
        self._Cari_kata = Search(self._size, self._words)
        self._pushed.clear()

        for i in range(self._size):
            for j in range(self._size):
                self._buttons[i][j].configure(
                    text=self._Cari_kata.board[i][j],
                    bg="SystemButtonFace",
                    state=tk.NORMAL,
                )

        for label in self._labels.values():
            label.configure(bg="SystemButtonFace")

    def _select_new(self):
        self._choose_random_words()
        self._reshuffle()
        self._create_labels()

        number = 0
        file_name = "Permainan.html"
        while file_name in listdir(getcwd()):
            number += 1
            file_name = f"Permainan{number}.html"

        with open(file_name, mode="w") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("\t<title>Word Search</title>\n")
            # Scripts required to display LaTeX
            f.write(
                """\t<script type="text/x-mathjax-config">
                    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}});
                    </script>
                    <script type="text/javascript"
                    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
                    </script>\n"""
            )
            f.write("</head>\n")
            f.write('<h2 align="center">HTML Table WordSearch Grid:</h2>\n<br><br>')

            f.write('<table align="center">\n')
            for i in range(self._size):
                f.write("\t<tr>\n\t\t")
                for j in range(self._size):
                    f.write(
                        f"<td padding=1em>{self._Cari_kata.board[i][j]}</td>")
                f.write("\t</tr>\n")
            f.write("</table>\n<br><br>")

            f.write('<h2 align="center">Latex PencarianKata Grid:</h2>\n<br><br>')
            f.write("\\begin{matrix}")
            f.write(" \\\\ ".join([" & ".join(row)
                    for row in self._Cari_kata.board]))
            f.write("\\end{matrix}\n<br><br>")
            f.write('<h2 align="center">PencarianKata Grid as String:</h2>\n<br><br>')

            f.write('<div align="center">\n')
            f.write(
                " ::: ".join(
                    ["".join(self._Cari_kata.board[i])
                     for i in range(self._size)]
                )
            )
            f.write("\n<br><br>\n")
            f.write(
                "\n".join(
                    ["".join(self._Cari_kata.board[i])
                     for i in range(self._size)]
                )
            )
            f.write("</div>\n")

            f.write('\n<br><br><h2 align="center">Solution</h2><br><br>\n')
            f.write("\\begin{matrix}")

            coordinates = set()
            for coords in self._Cari_kata.solutions.values():
                for coord in coords:
                    coordinates.add(coord)

            board = []
            for i in range(self._size):
                row = []
                for j in range(self._size):
                    if (self._Cari_kata.board[i][j], j, i) in coordinates:
                        row.append(self._Cari_kata.board[i][j])
                    else:
                        row.append("")
                board.append(row)

            f.write(" \\\\ ".join([" & ".join(row) for row in board]))
            f.write("\\end{matrix}")

            f.write('\n<br><br><h2 align="center">Words</h2><br><br>\n')
            f.write(
                f"""<ul align="center"><li>{'</li><li>'.join(self._words)}</li></ul>\n"""
            )
            f.write(
                f'\n<br><br><h2 align="center">SIZE: {self._size}x{self._size}</h2><br><br>\n'
            )
            f.write("</html>")


