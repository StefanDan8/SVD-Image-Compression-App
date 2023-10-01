import os
import sys
import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient = tk.VERTICAL, command = self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.canvas.configure(scrollregion = self.canvas.bbox('all')))
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)
        self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = tk.NW)
        self.canvas.configure(yscrollcommand = scrollbar.set, bg = 'white')
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y, expand = 0)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class ImageSampleWidget(ScrollableFrame):
    def __init__(self, parent, drop_image_widget, images):
        super().__init__(parent)
        tk.Label(self.scrollable_frame,
                 text = "Sample Images" + " " * 300,  # TODO canvas filling problems require weird solutions
                 anchor = tk.N, font = ('Helvetica', 16), bg = 'white').pack(expand = True, fill = tk.X)
        self.drop_image_widget = drop_image_widget
        self.buttons = []
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3, bg = 'white')
        for image_title in images:
            self.buttons.append(tk.Button(self.scrollable_frame, text = image_title,
                                          command = lambda p = image_title:
                                          (drop_image_widget.drop_path(resource_path(f'resources/{p}.jpg'))),
                                          bg = 'white',
                                          anchor = tk.W))

        for button in self.buttons:
            button.pack(anchor = tk.W, fill = tk.BOTH, expand = True)


def resource_path(relative_path):
    """
        For PyInstaller. Thanks to Rainer Niemann for the solution regarding accessing images.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
