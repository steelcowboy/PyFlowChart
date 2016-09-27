import gi, signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from appwin import AppWindow
from coursetools.course import Course
from coursetools.changer import CourseChanger

class BuilderWindow(AppWindow):
    """A class to create an interface for building a flowchart."""
    def __init__(self):
        """Constructor.

        No arguments accepted. Initializes as an AppWindow and sets up interface."""
        AppWindow.__init__(self, title="Flowchart Builder")

        self.setup_window()

    def setup_window(self):
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

    def treeview_clicked(self, widget, event):
        """Responds to right click events on the TreeView."""
        if event.button == 3:
            self.editmenu.popup(None, None, None, None, event.button, event.time)

    def edit_entry(self, button):
        """Edit existing entry."""
        course_selection = self.added_tree.get_selection()
        path = course_selection.get_selected_rows()[1][0]
        index = path.get_indices()[0]
        course = self.course_manager.courses[index]

        entry = self.create_add_edit_dialog(course)
        if entry:
            self.course_manager.edit_entry(entry, course_selection)

    def delete_entry(self, button): 
        """Delete existing entry."""
        self.course_manager.delete_entry(selection=self.added_tree.get_selection())

    def add_entry(self, button):
        """Add info to treeview, and update the course manager and changer."""        
        new_id = self.course_manager.last_course_id + 1
        self.add_changer.course_id = new_id

        #course_changer.init_objects(self.addbuilder)
        input_course = self.add_changer.get_course()
        input_course.course_id = new_id

        self.course_manager.add_entry(input_course)
        self.add_changer.clean_form()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = BuilderWindow()
    window.show_all()

    Gtk.main()
