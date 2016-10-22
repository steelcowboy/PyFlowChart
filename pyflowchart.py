import gi, signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from coursetools.tile import courseTile, tileColumn
from appwin import AppWindow
from interface.viewergrid import courseGrid

TARGET_ENTRY_TEXT = 0
COLUMN_TEXT = 0

DRAG_ACTION = Gdk.DragAction.COPY

class ViewerWindow(AppWindow):
    """A class to create an interface for viewing and modifying a flowchart.."""
    def __init__(self):
        """Constructor.

        No arguments accepted. Initializes as an AppWindow and sets up interface."""
        AppWindow.__init__(self, title="Flowchart Viewer")

        self.column_template = "year_{}_{}"
        self.quarter_map = dict(enumerate(["fall", "winter", "spring", "summer"]))
        
        self.setup_window()
        self.connect('delete-event', self.quit)

    def setup_viewer(self):
        main_grid = Gtk.Grid()
        self.add(main_grid)

        self.action_builder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        self.action_builder.connect_signals(self.events)
        menubar = self.action_builder.get_object('menubar')
        main_grid.attach(menubar, 0, 0, 1, 1)
        
        self.editmenu = self.action_builder.get_object('edit_menu')
        self.addmenu = self.action_builder.get_object('add_menu')

        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_vexpand(True)
        scroll_window.set_hexpand(True)
        main_grid.attach(scroll_window, 0, 1, 1, 1)

        self.courses_grid = courseGrid()
        scroll_window.add(self.courses_grid)
    
        self.columns = {}
        for year in range(1,5):
            for pos, quarter in enumerate(["fall", "winter", "spring", "summer"]):
                column_id = self.column_template.format(year, quarter)
                column = self.courses_grid.year_map[year].quarter_map[pos]

                # For drag and drop
                column.drag_dest_set_target_list(None)
                column.drag_dest_add_text_targets()

                column.connect('button-press-event', self.box_clicked)
                column.connect("drag-data-received", self.on_drag_data_received)
                self.columns[column_id] = column.box

    def setup_builder(self):
        """
        Setup the layout for the window and containers.
        """

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        self.add(grid)

        self.addbuilder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        self.addbuilder.connect_signals(self.events)

        menubar = self.addbuilder.get_object('menubar')
        grid.attach(menubar, 0, 0, 2, 1)
        self.editmenu = self.addbuilder.get_object('edit_menu')
        
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_vexpand(True)
        grid.attach(scroll_window, 0, 1, 1, 1)
        

        self.add_changer = CourseChanger()
        self.add_changer.init_objects(self.addbuilder)
        modifygrid = self.add_changer.grid

        add_button = Gtk.Button.new_with_label("Add")
        add_button.connect('clicked', self.add_entry)
        add_button.set_margin_top(5)
        modifygrid.attach(add_button, 1, 8, 2, 1)

        grid.attach(modifygrid, 1, 1, 1, 1)
        
        self.course_manager.store = Gtk.ListStore(str, str, int, str)

        self.added_tree = Gtk.TreeView(self.course_manager.store)
        
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Course", renderer, text=0)
        self.added_tree.append_column(column)

        column = Gtk.TreeViewColumn("Year/Quarter", renderer, text=1)
        self.added_tree.append_column(column)

        column = Gtk.TreeViewColumn("Units", renderer, text=2)
        self.added_tree.append_column(column)

        column = Gtk.TreeViewColumn("Type", renderer, text=3)
        self.added_tree.append_column(column)
        
        self.added_tree.connect('button-press-event', self.treeview_clicked)

        scroll_window.add(self.added_tree)

        self.connect('delete-event', self.quit)
