import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk

DRAG_ACTION = Gdk.DragAction.COPY

class quarterColumn(Gtk.EventBox):
    """An EventBox that contains courseTiles and is associated with a year and quarter."""
    def __init__(self, year, quarter):
        Gtk.EventBox.__init__(self)

        self.year = year
        self.quarter = quarter

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

        self.drag_dest_set(Gtk.DestDefaults.ALL, [], DRAG_ACTION)

        self.show_all() 

class yearGrid(Gtk.Grid):
    def __init__(self, year):
        Gtk.Grid.__init__(self)
        self.year = year
        self.selected_quarter = None 

        self.quarters = {
                0: "Fall",
                1: "Winter",
                2: "Spring",
                3: "Summer"
        }
        self.hidden = {x: False for x in [0,2,4,6]} 

        self.quarter_map = {}

        self.set_vexpand(True)
        self.set_hexpand(True)
        self.set_valign(Gtk.Align.FILL)
        self.set_halign(Gtk.Align.FILL)

        horizontal_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        horizontal_separator.set_margin_top(2)
        horizontal_separator.set_margin_bottom(5)
        self.attach(horizontal_separator, 0, 1, 2, 1)

        for x in [0,2,4,6]:
            if x < 6:
                # Don't insert a column if it's at position 0 
                if x: self.insert_column(x)
                # Insert column to expand horizontal separator
                self.insert_column(x+1)

                vertical_separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                vertical_separator.set_margin_start(5)
                vertical_separator.set_margin_end(5)
                self.attach(vertical_separator, x+1, 0, 1, 3)
                
            quarter = quarterColumn(self.year, self.quarters[x/2])
            
            label_box = Gtk.EventBox()
            label = Gtk.Label(self.quarters[x/2])
            label_box.add(label)
            label_box.connect('button-press-event', self.quarter_clicked) 
            self.attach(label_box, x, 0, 1, 1)

            self.quarter_map[x/2] = quarter 
            self.attach(quarter, x, 2, 1, 1)

        self.hide_menu = Gtk.Menu()
        hide_button = Gtk.MenuItem.new_with_label('Hide')
        self.hide_menu.append(hide_button)
        hide_button.show()
        hide_button.connect('activate', self.toggle_quarter)
        

        self.show_all()

    def create_quarter_menu(self):
        quarter_menu = Gtk.Menu()

        for key in self.quarters:
            quarter_item = Gtk.MenuItem()
            button = Gtk.CheckButton.new_with_label(self.quarters[key])
            if not self.hidden[key*2]:
                button.set_active(True)
            
            quarter_key = key*2
            quarter_item.connect('activate', self.toggle_quarter, quarter_key)
            quarter_item.add(button)
            quarter_menu.append(quarter_item)

        quarter_menu.show_all()
        return quarter_menu 

    def quarter_clicked(self, widget, event):
        if event.button == 3:
            self.selected_quarter = self.child_get_property(widget, 'left-attach')
            self.hide_menu.popup(None, None, None, None, event.button, event.time)
        return True

    def toggle_quarter(self, button=None, quarter=None):
        if quarter is None:
            quarter = self.selected_quarter 
        self.selected_quarter = None

        if self.hidden[quarter]:
            for x in [0,2]:
                self.get_child_at(quarter,x).show()
            self.hidden[quarter] = False 
        else:
            for x in [0,2]:
                self.get_child_at(quarter,x).hide()
            self.hidden[quarter] = True
        return True

class courseGrid(Gtk.Grid):
    def __init__(self, years=4):
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
    
        horizontal_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        horizontal_separator.set_margin_top(5)
        horizontal_separator.set_margin_bottom(10)
        self.attach(horizontal_separator, 0, 1, 2, 1)
        
        for x in range(1,years+1):
            self.add_year(x)

        self.show_all()

    def new_column(self):
        self.width = self.width + 1
        self.insert_column(self.width)
        return self.width 

    def add_year(self, year_number):
        # Create a new grid for the year 
        year_grid = yearGrid(year_number)
        # Update map of years
        self.year_map[year_number] = year_grid
        label_box = Gtk.EventBox()
        label_box.connect('button-press-event', self.year_clicked)
        label = Gtk.Label(self.nth[year_number] + " Year")
        label_box.add(label)

        left_separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        left_separator.set_margin_start(1)
        left_separator.set_margin_end(10)
        self.attach(left_separator, self.new_column(), 0, 1, 3)

        self.attach(year_grid, self.new_column(), 2, 1, 1)
        self.attach(label_box, self.width, 0, 1, 1)
        
        right_separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        right_separator.set_margin_start(10)
        right_separator.set_margin_end(1)
        self.attach(right_separator, self.new_column(), 0, 1, 3)

    def year_clicked(self, widget, event):
        if event.button == 3:
            selected_year = int((self.child_get_property(widget, 'left-attach')-2)/3+1)
            quarter_menu = self.year_map[selected_year].create_quarter_menu()
            quarter_menu.popup(None, None, None, None, event.button, event.time)
        return True


