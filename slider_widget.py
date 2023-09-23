import tkinter as tk


class SliderWidget(tk.Frame):
    def __init__(self, parent, display_widget, to):
        super().__init__(master = parent)
        self.display_widget = display_widget
        self.to = to
        self.slider = tk.Scale(self, from_ = 1, to = self.to, tickinterval = to//20, orient = tk.HORIZONTAL, width = 10)
        self.slider.bind("<ButtonRelease-1>", self._update)
        self.slider.pack(expand = True, fill = tk.X)
        display_widget.set_slider(self.slider)

    def _update(self, event):
        print(self.slider.get())
        self.display_widget.do_update(self.slider.get())
