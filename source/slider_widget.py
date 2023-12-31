import tkinter as tk


class SliderWidget(tk.Frame):
    def __init__(self, parent, display_widget, to, info_widget = None):
        super().__init__(master = parent)
        self.display_widget = display_widget
        self.info_widget = info_widget
        self.to = to
        self.slider = tk.Scale(self, from_ = 1, to = self.to, tickinterval = to//25, orient = tk.HORIZONTAL,
                               width = 10)
        self.slider.bind("<ButtonRelease-1>", self._update)
        self.slider.pack(expand = True, fill = tk.X)
        display_widget.set_slider(self.slider)
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3)

    def _update(self, event):
        self.info_widget.do_update(self.slider.get())
        self.display_widget.do_update(self.slider.get())

    def set_info_widget(self, info_widget):
        self.info_widget = info_widget
