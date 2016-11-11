import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class controlBar(Gtk.HeaderBar):
    def __init__(self):
        Gtk.HeaderBar.__init__(self)

        self.set_show_close_button(True)
        self.props.title = "PyFlowChart"
        
        self.info_box = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)

        self.file_button = Gtk.Button.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.LARGE_TOOLBAR)
        
        
        self.settings_button = Gtk.Button.new_from_icon_name("preferences-system", Gtk.IconSize.LARGE_TOOLBAR)
        self.help_button = Gtk.Button.new_from_icon_name("help-about", Gtk.IconSize.LARGE_TOOLBAR)
        
        self.main_menu = self.init_main_menu()
        self.settings_menu = self.init_settings_menu()
        self.help_menu = self.init_help_menu() 
        #self.init_edit_menu()

        self.file_button.connect('clicked', self.file_clicked)
        self.settings_button.connect('clicked', self.settings_clicked)
        self.help_button.connect('clicked', self.help_clicked)

        self.info_box.add(self.settings_button)
        self.info_box.add(self.help_button)

        self.pack_start(self.file_button) 
        self.pack_end(self.info_box)

        self.buttons = []
        # self.populate_buttons() 
        
        self.show_all()

    def init_main_menu(self):
        main_menu = Gtk.Menu()

        self.new_button = Gtk.MenuItem.new_with_label('New')
        self.open_button = Gtk.MenuItem.new_with_label('Open')
        
        view_button = Gtk.MenuItem.new_with_label('View')
        
        self.view_menu = Gtk.Menu()
        self.viewer_button = Gtk.MenuItem.new_with_label('Viewer')
        self.builder_button = Gtk.MenuItem.new_with_label('Builder')
        self.view_menu.append(self.viewer_button)
        self.view_menu.append(self.builder_button)
        self.view_menu.show_all() 

        view_button.set_submenu(self.view_menu)

        self.save_button = Gtk.MenuItem.new_with_label('Save')
        self.save_as_button = Gtk.MenuItem.new_with_label('Save As...')
        self.quit_button = Gtk.MenuItem.new_with_label('Quit')

        main_menu.append(self.new_button)
        main_menu.append(self.open_button)
        main_menu.append(Gtk.SeparatorMenuItem())
        main_menu.append(view_button)
        main_menu.append(Gtk.SeparatorMenuItem())
        main_menu.append(self.save_button)
        main_menu.append(self.save_as_button)
        main_menu.append(Gtk.SeparatorMenuItem())
        main_menu.append(self.quit_button)
        main_menu.show_all()
        
        return main_menu 

    def init_settings_menu(self):
        settings_menu = Gtk.Menu()

        self.preferences_button = Gtk.MenuItem.new_with_label('Preferences')
        settings_menu.append(self.preferences_button)

        settings_menu.show_all()
        return settings_menu 

    def init_help_menu(self):
        help_menu = Gtk.Menu()

        self.app_help_button = Gtk.MenuItem.new_with_label('Help')
        self.about_button = Gtk.MenuItem.new_with_label('About')

        help_menu.append(self.about_button)
        help_menu.append(self.app_help_button)

        help_menu.show_all()
        return help_menu 

    def file_clicked(self, widget):
        self.main_menu.popup( None, None, None, None, 0, Gtk.get_current_event_time())

    def settings_clicked(self, widget):
        self.settings_menu.popup( None, None, None, None, 0, Gtk.get_current_event_time())

    def help_clicked(self, widget):
        self.help_menu.popup( None, None, None, None, 0, Gtk.get_current_event_time())
