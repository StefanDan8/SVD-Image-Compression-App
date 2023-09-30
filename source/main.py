import sys
import tkinter as tk
import tkinterdnd2 as tk2
from image_sample_widget import ImageSampleWidget
from matplotlib_SVD_widget import SVDWidget
from drop_image_widget import DropImageWidget
from slider_widget import SliderWidget
from half_split_gui import HalfSplitFrame
from matplotlib_widget import MatplotlibWidget
from info_widget import InfoWidget
import os

# Commands for PyInstaller
# pyinstaller --noconfirm --onefile --windowed --add-data "C:\Users\40767\Desktop\Holiday Python\Programming\for GitHub\imageCompression\venv\Lib\site-packages\tkinterdnd2;tkinterdnd2/" main.py
# pyinstaller --noconfirm --onefile --windowed --add-data "C:\Users\40767\Desktop\Holiday Python\Programming\for GitHub\imageCompression\venv\Lib\site-packages\tkinterdnd2;tkinterdnd2/" --add-data "Capybara (225x225).jpg;." --add-data "Bran Castle (1920x1080).jpg;." --add-data "Giraffes (275x183).jpg;." --add-data "Jupiter (2260x3207).jpg;." --add-data "Mandelbrot Set (2560x1920).jpg;." --add-data "Palatul Culturii, Iași (1260x580).jpg;." --add-data "Skyrim Landscape (1920x1080).jpg;." --add-data "Squirrel (2706x1804).jpg;." --add-data "Stefan Dan (2448x3264).jpg;." --add-data "Wanderer above the Sea of Fog (2140x2699).jpg;." main.py
class App(tk2.Tk):
    def __init__(self):
        super().__init__()
        self.title('SVD-Based Image Compression')
        self.geometry('1400x750')


def resource_path(relative_path):
    """
    For PyInstaller. Thanks to Rainer Niemann for the solution regarding accessing images.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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

    svd_frame.set_plotter(singular_values_frame)
    info_frame = InfoWidget(half_gui.frame2)

    svd_frame.set_info_widget(info_frame)
    slider_frame.set_info_widget(info_frame)
    info_frame.pack(fill = tk.X)
    half_gui.pack(fill = tk.BOTH, expand = True)
    sample_images = ['Giraffes (275x183)',
                     'Capybara (225x225)',
                     'Palatul Culturii, Iași (1260x580)',
                     'Bran Castle (1920x1080)',
                     'Skyrim Landscape (1920x1080)',
                     'Mandelbrot Set (2560x1920)',
                     'Squirrel (2706x1804)',
                     'Wanderer above the Sea of Fog (2140x2699)',
                     'Jupiter (2260x3207)',
                     'Stefan Dan (2448x3264)']
    image_sample_frame = ImageSampleWidget(half_gui.frame2, drop_image_widget = drop_frame,
                                           images = sample_images)
    image_sample_frame.pack(fill = tk.BOTH, expand = True)
    app.mainloop()


if __name__ == '__main__':
    main()
