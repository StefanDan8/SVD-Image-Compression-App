import tkinter as tk


class InfoWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.k = 1
        self.n, self.m = 0, 0
        self.size_label = tk.Label(master = self, text = f'IMAGE SIZE  {self.n} x {self.m}', anchor = tk.W)
        self.num_pixels = tk.Label(master = self, text = f'#PIXELS = {self.n * self.m}', anchor = tk.W)
        self.rank_label = tk.Label(master = self, text = f'current_rank = {self.k}', anchor = tk.W)
        self.compressed_size = tk.Label(master = self, text = self._compressed_size_text(), anchor = tk.W)
        self.compression_ratio = tk.Label(master = self, text = self._compressed_ratio_text(), anchor = tk.W)
        self.size_label.pack(fill = tk.BOTH)
        self.num_pixels.pack(fill = tk.BOTH)
        self.rank_label.pack(fill = tk.BOTH)
        self.compressed_size.pack(fill = tk.BOTH)
        self.compression_ratio.pack(fill = tk.BOTH)

    def set_RGBSVD(self, ncols, nrows):
        self.n = ncols
        self.m = nrows
        self.size_label.config(text = f'IMAGE SIZE  {self.n} x {self.m}')
        self.num_pixels.config(text = f'#PIXELS = {self.n * self.m}')

    def do_update(self, new_k):
        self.k = new_k
        self.rank_label.config(text = f'current_rank = {self.k}')
        self.compressed_size.config(text = self._compressed_size_text())
        self.compression_ratio.config(text = self._compressed_ratio_text())

    def _compressed_size_text(self):
        return f'COMPRESSED SIZE \n approximately proportional to \n ' \
               f'{self.m} x {self.k} + {self.k} + {self.k} x {self.n} \n' \
               f'={(self.m + self.n + 1) * self.k}'

    def _compressed_ratio_text(self):
        return f'COMPRESSION RATIO \n {self.n * self.m} / ' \
               f'{(self.m + self.n + 1) * self.k} = '  \
               f'{self.n * self.m / (self.m + self.n + 1) / self.k}'
