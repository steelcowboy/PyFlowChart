import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .editable_label import editable_label 

class preferences_dialog(Gtk.Dialog):
    def __init__(self, parent, courses, user):
        Gtk.Dialog.__init__(self, "Preferences", parent,
            0, (Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        self.set_size_request(400, -1)
        self.planned_ges = courses  

        self.ge_list = [
                'A1', 'A2', 'A3', 
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 
                'C1', 'C2', 'C3', 'C4', 'C5', 
                'D1', 'D2', 'D3', 'D4/E', 'D5', 
                'F'
                ]
        
        self.ge_length = len(self.ge_list)

        self.notebook = Gtk.Notebook()
        self.box = self.get_content_area()
        self.box.add(self.notebook)

        self.user = Gtk.Grid()
        self.user.set_column_homogeneous(True)
        self.user.attach(Gtk.Label("Year:"), 0, 0, 1, 1)
        
        self.year_selector = Gtk.ComboBoxText()
        self.user.attach(self.year_selector, 1, 0, 1, 1)
        for x in range(1,7):
            self.year_selector.append_text(str(x))
        self.year_selector.set_active(user['year']-1)

        self.user.attach(Gtk.Label("Years to display:"), 0, 1, 1, 1)
        self.display_years_selector = Gtk.ComboBoxText()
        self.user.attach(self.display_years_selector, 1, 1, 1, 1)
        for x in range(1,7):
            self.display_years_selector.append_text(str(x))
        self.display_years_selector.set_active(user['display_years']-1)
        
        self.notebook.append_page(self.user, Gtk.Label("User Info"))

        self.ges = Gtk.Grid()
        self.ges.set_column_homogeneous(True)
        
        for pos, ge in enumerate(self.ge_list):
            self.ges.attach(Gtk.Label(ge), 0, pos, 1, 1)
            if ge in self.planned_ges:
                self.ges.attach(editable_label(self.planned_ges[ge]), 1, pos, 1, 1)
            else:
                self.ges.attach(editable_label(), 1, pos, 1, 1)

        self.notebook.append_page(self.ges, Gtk.Label("GEs"))
        
        self.show_all()
