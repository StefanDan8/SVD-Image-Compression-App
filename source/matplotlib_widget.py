from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk


class MatplotlibWidget(tk.Frame):
    def __init__(self, parent, width_inch = 3, height_inch = 3):
        super().__init__(master = parent)

        self.figure = Figure(figsize = (width_inch, height_inch), dpi = 100)
        self.ax = self.figure.add_subplot()
        self.ax.semilogy()
        self.figure.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.figure, master = self)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar = False)
        self.toolbar.update()

        self.toolbar.pack(side = tk.BOTTOM, fill = tk.X)
        self.canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3, bg = 'white')

    def get_info(self):
        return self.ax, self.figure, self.canvas

    def clear(self):
        self.ax.clear()
        self.ax.semilogy()
        self.canvas.draw()
