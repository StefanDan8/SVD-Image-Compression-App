import tkinter as tk
from tkinter import ttk


class HalfSplitFrame(tk.Frame):
    def __init__(self, parent, title = None, weight1 = 1, weight2 = 1):
        super().__init__(master = parent)
        # TODO implement a way to modify parameters after initialization
        # title
        self.title_label = tk.Label(self, text = title)
        self.title_label.pack(fill = tk.X, side = tk.TOP)
        # paned window
        self.paned_window = ttk.PanedWindow(self, orient = tk.HORIZONTAL)
        self.paned_window.pack(expand = True, fill = tk.BOTH)
        # Styles TODO cover later
        s1 = ttk.Style()
        s1.configure('f1.TFrame', background = 'red')
        s2 = ttk.Style()
        s2.configure('f2.TFrame', background = 'green')
        # Frame 1
        self.frame1 = ttk.Frame(self.paned_window, style = 'f1.TFrame')
        self.paned_window.add(self.frame1, weight = weight1)
        # Frame 2
        self.frame2 = ttk.Frame(self.paned_window, style = 'f2.TFrame')
        self.paned_window.add(self.frame2, weight = weight2)

    def force_aspect_ratio(self, pad_frame, content_frame, aspect_ratio):
        def enforce_aspect_ratio(event):
            desired_width = event.width
            desired_height = int(event.width / aspect_ratio)

            if desired_height > event.height:
                desired_height = event.height
                desired_width = int(event.height * aspect_ratio)
            content_frame.place(in_ = pad_frame, x = 0, y = 0,
                                width = desired_width, height = desired_height)
            print(content_frame.winfo_height())

        pad_frame.bind("<Configure>", enforce_aspect_ratio)


if __name__ == '__main__':
    root = tk.Tk()
    window = HalfSplitFrame(root)
    root.geometry('500x500')
    window.pack(fill = tk.BOTH, expand = True)
    root.mainloop()
