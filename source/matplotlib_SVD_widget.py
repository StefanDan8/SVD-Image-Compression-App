import time
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from svd import rsvd_image_approximation, RGBSVD
import numpy as np
from threading import Thread
from tkinter.messagebox import showwarning, showinfo


class SVDWidget(tk.Frame):
    def __init__(self, parent, initial_rank = 50, plotter = None, info_widget = None):
        super().__init__(master = parent)
        self.initial_rank = initial_rank
        self.max_rank = 0
        # Title
        label = tk.Label(master = self, text = 'matplotlib')
        label.config(font = ('Courier', 32))
        label.pack()
        # Figure and axes
        self.figure = Figure()
        self.ax = self.figure.add_subplot()
        # TODO tight layout
        self.figure.tight_layout()

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        # Canvas
        self.canvas = FigureCanvasTkAgg(figure = self.figure, master = self)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.SVD = None
        self.slider = None
        self.plotter = plotter
        self.info_widget = info_widget

    def plot_image(self, tensor):
        self.ax.imshow(np.around(tensor).astype(int))
        self.canvas.draw()

    def display(self, path):
        self.SVD = None
        img = plt.imread(path)
        self.max_rank = min(img.shape[0], img.shape[1])
        self.slider.configure(to = self.max_rank, tickinterval = self.max_rank // 20)
        self.slider.set(self.initial_rank)
        self.info_widget.set_RGBSVD(img.shape[1], img.shape[0])
        new_image_r = rsvd_image_approximation(img, k = self.initial_rank)
        self.plot_image(new_image_r)

        # compute exact SVD in parallel
        t1 = Thread(target = self.compute_SVD, args = (img,), daemon = True)
        t1.start()

        # loading screen for the computation above
        t2 = Thread(target = load, args = (t1,), daemon = True)
        t2.start()

    def compute_SVD(self, img):
        check_size(img)
        self.SVD = RGBSVD(img)
        self.plot_singular_values()
        print('finished')

    def do_update(self, rank):
        if self.SVD is None:
            # TODO check too when no path was given. Then no warning is necessary
            showwarning(title = 'Warning', message = 'Please be patient. The computation takes a little longer!')
        else:
            self.plot_image(self.SVD.get_rank_k_approximation(rank))

    def set_slider(self, slider):
        self.slider = slider

    def set_plotter(self, plotter):
        self.plotter = plotter

    def set_info_widget(self, info_widget):
        self.info_widget = info_widget

    def plot_singular_values(self):
        ax, canvas = self.plotter.get_ax_and_canvas()
        ax.clear()
        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.R_SVD.S, c = 'red', s = .7) # RED
        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.G_SVD.S, c = 'green', s = .7) # GREEN
        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.B_SVD.S, c = 'blue', s = .7)  # BLUE
        canvas.draw()


def load(t1):
    while t1.is_alive():
        print('calculating...')
        time.sleep(2)


def check_size(image_tensor):
    shape = image_tensor.shape
    if shape[0] * shape[1] > 1920 * 1080:
        showinfo(title = 'Info', message = 'It looks like your image is quite big. The exact computation might take a '
                                           'few seconds.')