import tkinter as tk
import tkinterdnd2 as tk2


class DropImageWidget(tk.Frame):
    def __init__(self, parent, display_widget):
        super().__init__(master = parent)
        text = tk.Label(self, text = 'drop image here or write path', bg = '#fcba03')
        text.pack(anchor = tk.NW)
        self.display_widget = display_widget
        self.text_var = tk.StringVar()
        self.entrybox = tk.Entry(self, textvariable = self.text_var, width = 80)
        self.entrybox.pack(fill = tk.X)
        self.entrybox.drop_target_register(tk2.DND_FILES)
        self.entrybox.dnd_bind('<<Drop>>', self._drop)

    def _drop(self, event):
        self.text_var.set(event.data)
        self.display_widget.display(self.text_var.get())
