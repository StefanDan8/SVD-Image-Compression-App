import tkinter as tk
import tkinterdnd2 as tk2


class DropImageWidget(tk.Frame):
    def __init__(self, parent, display_widget):
        super().__init__(master = parent)
        tk.Label(self, text = 'Drop an image here or pick a sample image', bg = '#9e9db3',
                        font = ('Helvetica', 11)).pack(anchor = tk.NW)
        self.display_widget = display_widget
        self.text_var = tk.StringVar()
        self.entrybox = tk.Entry(self, textvariable = self.text_var, width = 80)
        self.entrybox.pack(fill = tk.X)
        self.entrybox.drop_target_register(tk2.DND_FILES)
        self.entrybox.dnd_bind('<<Drop>>', self._drop)
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3)

    def _drop(self, event):
        self.text_var.set(event.data)
        self.display_widget.display(self.text_var.get())

    def drop_path(self, path):
        # there is no support for passing data through virtual events in tkinter
        # the easiest way around is to do a custom function and avoid virtual events
        self.text_var.set(path)
        self.display_widget.display(self.text_var.get())
