import tkinter as tk
import tkinterdnd2 as tk2
from PIL import ImageTk, Image
from matplotlib_SVD_widget import SVDWidget
from drop_image_widget import DropImageWidget
from slider_widget import SliderWidget


class App(tk2.Tk):
    def __init__(self):
        super().__init__()
        self.title('SVD-Based Image Compression')
        self.geometry('1000x700')


def main():
    app = App()
    svd_frame = SVDWidget(app)
    drop_frame = DropImageWidget(app, svd_frame)
    drop_frame.pack()
    svd_frame.pack()
    slider_frame = SliderWidget(app, svd_frame, 100)
    slider_frame.pack(expand = True, fill = tk.X)
    app.mainloop()


if __name__ == '__main__':
    main()
