import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from svd import rsvd_image_approximation, RGBSVD
import numpy as np


class SVDWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        # Title
        label = tk.Label(master = self, text = 'matplotlib')
        label.config(font = ('Courier', 32))
        label.pack(expand = True)
        # Figure and axes
        self.figure = Figure()
        self.ax = self.figure.add_subplot()

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        # Canvas
        self.canvas = FigureCanvasTkAgg(figure = self.figure, master = self)
        self.canvas.get_tk_widget().pack()

        self.SVD = None
        self.slider = None

    def plot_image(self, tensor):
        self.ax.imshow(np.around(tensor).astype(int))
        self.canvas.draw()

    def display(self, path):
        img = plt.imread(path)
        new_image_r = rsvd_image_approximation(img, k = 150)
        self.plot_image(new_image_r)
        self.SVD = RGBSVD(img)
        max_rank = min(self.SVD.nrows, self.SVD.ncols)
        self.slider.configure(to = max_rank, tickinterval = max_rank//20)

    def do_update(self, rank):
        self.plot_image(self.SVD.get_rank_k_approximation(rank))

    def set_slider(self, slider):
        self.slider = slider
