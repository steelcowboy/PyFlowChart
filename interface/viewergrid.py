import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class quarterColumn(Gtk.EventBox):
    """An EventBox that contains courseTiles and is associated with a year and quarter."""
    def __init__(self, year, quarter):
        Gtk.EventBox.__init__(self)

        self.year = year
        self.quarter = quarter.capitalize()

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_valign(Gtk.Align.FILL)

        self.box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,spacing=10
                )
        self.box.set_hexpand(True)
        self.box.set_vexpand(True)
        self.box.set_valign(Gtk.Align.START)
        self.add(self.box)


class yearGrid(Gtk.Grid):
    def __init__(self, year):
        Gtk.Grid.__init__(self)
        self.year = year

        self.quarters = {
                0: "Fall",
                1: "Winter",
                2: "Spring",
                3: "Summer"
        }
        self.quarter_map = {}

        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_valign(Gtk.Align.FILL)
        self.set_halign(Gtk.Align.FILL)

class courseGrid(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        # Tells which position the rightmost column is
        self.width = 0
        
        self.nth = {
            1: "First",
            2: "Second",
            3: "Third",
            4: "Fourth",
            5: "Fifth",
            6: "Sixth"
        }
        self.year_map = {}
        
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_margin_start(10)
        self.set_margin_end(10)
    
        horizontal_separator = Gtk.Separator(Gtk.Orientation.HORIZONTAL)
        self.attach(0, 1, 1, 1)

    def new_column(self):
        self.width = self.width + 1
        self.insert_column(self.width)
        return self.width 

    def add_year(self, year_number):
        # Create a new grid for the year 
        year_grid = yearGrid(year_number)
        # Update map of years
        self.year_map[year_number] = year_grid
        label = Gtk.Label.new_with_text(self.nth[year_number])

        left_separator = Gtk.Separator(Gtk.Orientation.VERTICAL)
        left_separator.set_margin_start(10)
        left_separator.set_margin_end(1)
        self.attach(left_separator, self.new_column(), 0, 1, 3)

        self.attach(year_grid, self.new_column(), 2, 1, 1)
        self.attach(label, self.width, 0, 1, 1)
        
        right_separator = Gtk.Separator(Gtk.Orientation.VERTICAL)
        right_separator.set_margin_start(1)
        right_separator.set_margin_end(10)
        self.attach(right_separator, self.new_column(), 0, 1, 3)



