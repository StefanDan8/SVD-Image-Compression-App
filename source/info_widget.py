import tkinter as tk


class InfoWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.k = 1
        self.n, self.m = 0, 0
        self.title = tk.Label(self, text = 'Information', font = ('Helvetica', 16), bg = 'white')
        self.title.pack(anchor = tk.NW)
        self.size_label = tk.Label(self, text = f'Image Size  {self.n} x {self.m}',
                                   anchor = tk.W, font = ('Helvetica', 11), bg = 'white')
        self.num_pixels = tk.Label(self, text = f'Number of Pixels = {self.n * self.m}',
                                   anchor = tk.W, font = ('Helvetica', 11), bg = 'white')
        self.rank_label = tk.Label(self, text = f'Current rank = {self.k}',
                                   anchor = tk.W, font = ('Helvetica', 11), bg = 'white')
        self.compressed_size = tk.Label(self, text = self._compressed_size_text(),
                                        anchor = tk.W, font = ('Helvetica', 11), justify = tk.LEFT, bg = 'white')
        self.compression_ratio = tk.Label(self, text = self._compressed_ratio_text(),
                                          anchor = tk.W, font = ('Helvetica', 11), justify = tk.LEFT, bg = 'white')
        self.size_label.pack(fill = tk.BOTH)
        self.num_pixels.pack(fill = tk.BOTH)
        self.rank_label.pack(fill = tk.BOTH)
        self.compressed_size.pack(fill = tk.BOTH)
        self.compression_ratio.pack(fill = tk.BOTH)
        self.configure(padx = 10, pady = 10, relief = 'sunken', borderwidth = 3, bg = 'white')

    def set_RGBSVD(self, ncols, nrows):
        self.n = ncols
        self.m = nrows
        self.size_label.config(text = f'Image Size  {self.n} x {self.m}')
        self.num_pixels.config(text = f'Number of Pixels = {self.n * self.m}')

    def do_update(self, new_k):
        self.k = new_k
        self.rank_label.config(text = f'Current rank = {self.k}')
        self.compressed_size.config(text = self._compressed_size_text())
        self.compression_ratio.config(text = self._compressed_ratio_text())

    def _compressed_size_text(self):
        return f'Compressed Size: approximately proportional to \n ' \
               f'{self.m} x {self.k} + {self.k} + {self.k} x {self.n} ' \
               f'={(self.m + self.n + 1) * self.k}'

    def _compressed_ratio_text(self):
        return f'Compression Ratio \n ' \
               f'{self.n * self.m} / ' \
               f'{(self.m + self.n + 1) * self.k} = ' \
               f'{round(self.n * self.m / (self.m + self.n + 1) / self.k, 4)}'
