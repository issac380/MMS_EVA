def zoom_selection(self):
    print("zoom in pressed")
    xlim = self.axes[0].get_xlim()
    if xlim is not None and self.start_time is not None and self.end_time is not None:
        self.zooms += [xlim]
        self.change_view(self.start_time[1], self.end_time[1])

def zoom_in(self):
    print("zoom in pressed")
    xlim = self.axes[0].get_xlim()
    if xlim is not None:
        self.zooms += [xlim]
        x_range = abs(xlim[0] - xlim[1])
        self.change_view(xlim[0] + x_range/10, xlim[1] - x_range/10)

def zoom_out(self):
    print("zoom out pressed")
    xlim = self.axes[0].get_xlim()
    if xlim is not None:
        self.zooms += [xlim]
        x_range = abs(xlim[0] - xlim[1])
        self.change_view(xlim[0] - x_range/10, xlim[1] + x_range/10)

def move_left(self):
    print("move left pressed")
    xlim = self.axes[0].get_xlim()
    if xlim is not None:
        self.zooms += [xlim]
        x_range = abs(xlim[0] - xlim[1])
        self.change_view(xlim[0] - x_range/10, xlim[1] - x_range/10)

def move_right(self):
    print("move right pressed")
    xlim = self.axes[0].get_xlim()
    if xlim is not None:
        self.zooms += [xlim]
        x_range = abs(xlim[0] - xlim[1])
        self.change_view(xlim[0] + x_range/10, xlim[1] + x_range/10)

def undo(self):
    print("undo pressed")
    if self.zooms != []:
        new_xlim = self.zooms.pop()
        self.axes[1].set_xlim(new_xlim)
        self.canvas.draw()

def clear_selection(self):
    for line in self.axes[1].get_lines():
        if line.get_color() == 'r' and line.get_linestyle() == '--':
            line.remove()
    self.start_time = self.end_time = None

def change_view(self, left, right):
    self.axes[1].set_xlim((left, right))
    self.canvas.draw()