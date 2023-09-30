import time
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from svd import rsvd_image_approximation, RGBSVD
from threading import Thread
from tkinter.messagebox import showwarning, showinfo


class SVDWidget(tk.Frame):
    def __init__(self, parent, initial_rank = 50, plotter = None, info_widget = None):
        super().__init__(master = parent)
        self.initial_rank = initial_rank
        self.max_rank = 0
        self.is_png = False
        self.empty = True
        # Figure and axes
        self.figure = Figure()
        self.ax = self.figure.add_subplot()
        self.figure.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        # Canvas
        self.canvas = FigureCanvasTkAgg(figure = self.figure, master = self)
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.SVD = None
        self.slider = None
        self.plotter = plotter
        self.info_widget = info_widget
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3, bg = 'white')

    def _plot_image(self, tensor_img):
        """
        Plots a 3-channeled np.array as an image on the canvas.
        :param tensor_img: (M,N,3) np.array representing an RGB image
        """
        self.ax.imshow(tensor_img)
        self.canvas.draw()

    def display(self, path: str):
        self.SVD = None  # reset the stored SVD decomposition
        self.is_png = path.endswith('.png')
        self.empty = False
        img = plt.imread(path)  # read the image from the path
        self.plotter.clear()  # reset the matplotlib plot
        self.max_rank = min(img.shape[0], img.shape[1])  # store the maximum possible rank of the matrix for convenience
        # update slider
        self.slider.configure(to = self.max_rank, tickinterval = self.max_rank // 25)
        self.slider.set(self.initial_rank)
        # update info widget
        self.info_widget.set_RGBSVD(img.shape[1], img.shape[0])
        self.info_widget.do_update(self.initial_rank)
        # compute a randomized SVD decomposition for
        # a preview. Way faster, but not as precise
        new_image_r = rsvd_image_approximation(img, k = self.initial_rank, png = self.is_png)

        self._plot_image(new_image_r) # plot the obtained self.initial_rank - approximation

        # compute exact SVD in parallel
        t1 = Thread(target = self._compute_SVD, args = (img,), daemon = True)  # important to be daemon
        t1.start()

        # add a loading status for the thread above.
        t2 = Thread(target = load, args = (t1, self.info_widget), daemon = True)
        t2.start()

    def _compute_SVD(self, tensor_img):
        """
        Computes the exact SVD of every channel of `tensor_img` and saves it internally in self.SVD.
        Plots the corresponding singular values and raises a note before computing if the size of image is big.

        :param tensor_img: (M,N,3) np.array representing an RGB image
        """
        check_size(tensor_img)  # raise an Info if the size is big -- computation might be long
        self.SVD = RGBSVD(tensor_img)  # save new RGBSVD object
        self.plot_singular_values()
        self.info_widget.title.config(text = "Information")  # reset info title -- while computing the title is changed
        # to signal this

    def do_update(self, rank):
        if self.SVD is None:
            if not self.empty:
                showwarning(title = 'Warning', message = 'Please be patient. The computation takes a little longer!')
        else:
            self._plot_image(self.SVD.get_rank_k_approximation(rank, png = self.is_png))

    def set_slider(self, slider):
        self.slider = slider

    def set_plotter(self, plotter):
        self.plotter = plotter

    def set_info_widget(self, info_widget):
        self.info_widget = info_widget

    def plot_singular_values(self):
        ax, _, canvas = self.plotter.get_info()
        self.plotter.clear()

        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.R_SVD.S, c = 'red', s = .7)  # RED
        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.G_SVD.S, c = 'green', s = .7)  # GREEN
        ax.scatter(x = range(1, self.max_rank + 1), y = self.SVD.B_SVD.S, c = 'blue', s = .7)  # BLUE
        canvas.draw()


def load(t1, info):
    i = 0
    while t1.is_alive():
        # TODO instead of a loading animation
        i += 1
        i = i % 3
        info.title.config(
            text = 'Information    status: calculating SVD' + '.' * (i + 1) + ' ' * (3 - i))
        print('calculating...')
        time.sleep(1)

    info.title.config(text = 'Information')


def check_size(image_tensor):
    shape = image_tensor.shape
    if shape[0] * shape[1] > 1920 * 1080:
        showinfo(title = 'Info', message = 'It looks like your image is quite big. The exact computation might take a '
                                           'few seconds.')
