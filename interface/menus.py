import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 

class dataMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.edit_button = Gtk.MenuItem.new_with_label('Edit')
        self.copy_button = Gtk.MenuItem.new_with_label('Copy')
        self.delete_button = Gtk.MenuItem.new_with_label('Delete')

        self.append(self.edit_button)
        self.append(self.copy_button)
        self.append(Gtk.SeparatorMenuItem())
        self.append(self.delete_button)
        
        self.show_all() 

class addMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.add_button = Gtk.MenuItem.new_with_label('Add')
        self.paste_button = Gtk.MenuItem.new_with_label('Paste')

        self.append(self.add_button)
        self.append(Gtk.SeparatorMenuItem())
        self.append(self.paste_button)

        self.show_all()
