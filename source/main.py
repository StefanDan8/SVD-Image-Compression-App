import tkinter as tk
import tkinterdnd2 as tk2
from matplotlib_SVD_widget import SVDWidget
from drop_image_widget import DropImageWidget
from slider_widget import SliderWidget
from half_split_gui import HalfSplitFrame
from matplotlib_widget import MatplotlibWidget
from info_widget import InfoWidget


class App(tk2.Tk):
    def __init__(self):
        super().__init__()
        self.title('SVD-Based Image Compression')
        self.geometry('1400x750')


def main():
    app = App()
    half_gui = HalfSplitFrame(app, weight1 = 3, weight2 = 1)
    # Left Frame
    svd_frame = SVDWidget(half_gui.frame1)
    drop_frame = DropImageWidget(half_gui.frame1, svd_frame)
    drop_frame.pack(fill = tk.X)
    svd_frame.pack(fill = tk.BOTH, expand = True)

    slider_frame = SliderWidget(half_gui.frame1, svd_frame, to = 100)
    slider_frame.pack(fill = tk.X)

    # Right Frame
    singular_values_frame = MatplotlibWidget(half_gui.frame2)
    singular_values_frame.pack(fill = tk.X)

    # half_gui.force_aspect_ratio(half_gui.frame2,singular_values_frame, 1.0/1.0)  # Not worth the trouble
    svd_frame.set_plotter(singular_values_frame)
    info_frame = InfoWidget(half_gui.frame2)

    svd_frame.set_info_widget(info_frame)
    slider_frame.set_info_widget(info_frame)
    info_frame.pack(fill = tk.X)
    half_gui.pack(fill = tk.BOTH, expand = True)
    app.mainloop()


if __name__ == '__main__':
    # TODO solve clipping
    main()
