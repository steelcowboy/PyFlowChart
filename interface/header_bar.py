import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ControlBar(Gtk.HeaderBar):
    def __init__(self):
        Gtk.HeaderBar.__init__(self)

        self.set_show_close_button(True)
        self.props.title = "PyFlowChart"
        # Don't forget this in appwin
        #self.set_titlebar(hb)
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.file_button = Gtk.Button.new_with_label("File")
        self.edit_button = Gtk.Button.new_with_label("Edit")
        self.view_button = Gtk.Button.new_with_label("View")
        self.help_button = Gtk.Button.new_with_label("Help")
        
        self.init_file_menu()
        #self.init_edit_menu()

        self.file_button.connect('clicked', self.file_clicked)

        self.box.add(self.file_button)
        self.box.add(self.edit_button)
        self.box.add(self.view_button)
        self.box.add(self.help_button)

        self.pack_start(self.box)

    def init_file_menu(self):
        self.file_menu = Gtk.Menu()
        self.new_button = Gtk.MenuItem.new_with_label('New')
        self.open_button = Gtk.MenuItem.new_with_label('Open')
        self.save_button = Gtk.MenuItem.new_with_label('Save')
        self.save_as_button = Gtk.MenuItem.new_with_label('Save As...')
        self.quit_button = Gtk.MenuItem.new_with_label('Quit')

        self.file_menu.append(self.new_button)
        self.file_menu.append(self.open_button)
        self.file_menu.append(Gtk.SeparatorMenuItem())
        self.file_menu.append(self.save_button)
        self.file_menu.append(self.save_as_button)
        self.file_menu.append(Gtk.SeparatorMenuItem())
        self.file_menu.append(self.quit_button)

    def file_clicked(self, widget, event):
        self.file_menu.popup(None, None, None, None, event.button, event.time)
