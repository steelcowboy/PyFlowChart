import gi, signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from coursetools.tile import courseTile, tileColumn
from appwin import AppWindow
from interface.viewergrid import courseGrid
from interface.header_bar import ControlBar 
from coursetools.changer import CourseChanger

TARGET_ENTRY_TEXT = 0
COLUMN_TEXT = 0

DRAG_ACTION = Gdk.DragAction.COPY

class FlowChartWindow(AppWindow):
    """A class to create an interface for viewing and modifying a flowchart.."""
    def __init__(self):
        """Constructor.

        No arguments accepted. Initializes as an AppWindow and sets up interface."""
        AppWindow.__init__(self, title="Flowchart Viewer")

        self.column_template = "year_{}_{}"
        self.quarter_map = dict(enumerate(["fall", "winter", "spring", "summer"]))
        self.mode = 'viewer'
        
        self.setup_window()
        self.connect('delete-event', self.quit)
    
    def setup_window(self):
        self.action_builder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        self.action_builder.connect_signals(self.events)
        self.menubar = self.action_builder.get_object('menubar')
        # self.menubar = ControlBar() 
        # self.set_titlebar(self.menubar)

        self.editmenu = self.action_builder.get_object('edit_menu')
        self.addmenu = self.action_builder.get_object('add_menu')

        main_grid = Gtk.Grid()
        self.add(main_grid)

        main_grid.attach(self.menubar, 0, 0, 1, 1)

        self.interface_switcher = Gtk.Notebook()
        self.interface_switcher.set_show_tabs(False)
        main_grid.attach(self.interface_switcher, 0, 1, 1, 1)
        self.setup_viewer()
        self.setup_builder()

    def setup_viewer(self):
        viewer_grid = Gtk.Grid()
        
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_vexpand(True)
        scroll_window.set_hexpand(True)
        viewer_grid.attach(scroll_window, 0, 0, 1, 1)

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

        self.interface_switcher.append_page(viewer_grid)

    def setup_builder(self):
        """
        Setup the layout for the window and containers.
        """
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)

        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_vexpand(True)
        grid.attach(scroll_window, 0, 0, 1, 1)
        
        self.add_changer = CourseChanger()
        self.add_changer.init_objects(self.action_builder)
        modifygrid = self.add_changer.grid

        add_button = Gtk.Button.new_with_label("Add")
        add_button.connect('clicked', self.add_entry)
        add_button.set_margin_top(5)
        modifygrid.attach(add_button, 1, 8, 2, 1)

        grid.attach(modifygrid, 1, 0, 1, 1)
        
        self.course_manager.store = Gtk.ListStore(str, str, int, str, int)

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

        self.interface_switcher.append_page(grid)

    def change_to_viewer(self, button):
        self.interface_switcher.set_current_page(0)
        self.mode = 'viewer'

    def change_to_builder(self, button):
        self.interface_switcher.set_current_page(1)
        self.mode = 'builder'

    def treeview_clicked(self, widget, event):
        """Responds to right click events on the TreeView."""
        if event.button == 3:
            store, course_iter = widget.get_selection().get_selected()
            course_id = store.get(course_iter, 4)[0] 
            self.selected_id = course_id  
            self.selected_course = self.course_manager.courses[course_id]

            self.editmenu.popup(None, None, None, None, event.button, event.time)

    def tile_clicked(self, widget, event):
        if event.button == 3:
            self.editmenu.popup(None, None, None, None, event.button, event.time)
            self.selected_id = widget.course_id
            self.selected_tile = widget
            self.course_changer.edit_year = widget.time[0]
            self.course_changer.edit_quarter = widget.time[1]
        return True 
    
    def box_clicked(self, widget, event):
        if event.button == 3:
            self.addmenu.popup(None, None, None, None, event.button, event.time)
            self.course_changer.add_year = widget.year
            self.course_changer.add_quarter = widget.quarter
        return True

    def new_file(self, widget):
        if not super(FlowChartWindow, self).new_file(widget):
            return

        for time, box in self.columns.items():
            for tile in box.get_children():
                tile.destroy()

    def open_file(self, widget):
        if not super(FlowChartWindow, self).open_file(widget):
            return
    
        self.load_courses()

    def load_courses(self):
        for time, box in self.columns.items():
            for tile in box.get_children():
                tile.destroy()

        for c_id, course in self.course_manager.courses.items():
            tile = courseTile(
                    course['title'], 
                    course['catalog'], 
                    course['credits'],
                    course['prereqs'], 
                    course['time'], 
                    course['course_type'],
                    course['ge_type'],
                    c_id  
                    )
            tile.connect('button-press-event', self.tile_clicked)
            tile.connect("drag-data-get", self.on_drag_data_get)
            
            # Drag and drop
            tile.drag_source_set_target_list(None)
            tile.drag_source_add_text_targets()

            time = self.column_template.format(
                    course['time'][0], 
                    course['time'][1].lower()
                    )

            self.columns[time].pack_start(tile, True, True, 0)

        for year in range(1, self.course_manager.user['year']+1):
            if year == self.course_manager.user['year']:
                for x in range(0, self.course_manager.quarter):
                    time = self.column_template.format(year, dict(self.quarter_map)[x])
                    self.columns[time].get_style_context().add_class('completed')
            else:
                for x in range(0,4):
                    time = self.column_template.format(year, dict(self.quarter_map)[x])
                    self.columns[time].get_style_context().add_class('completed')
    
    def make_tile(self, course):
        tile = courseTile(
                course.title,       
                course.catalog,    
                course.credits,    
                course.prereqs,
                course.time,    
                course.course_type,  
                course.ge_type,
                course.course_id 
                )
        
        tile.connect('button-press-event', self.tile_clicked)
        tile.connect("drag-data-get", self.on_drag_data_get)
        
        # Drag and drop
        tile.drag_source_set_target_list(None)
        tile.drag_source_add_text_targets()
        
        return tile

    def add_entry(self, button):
        new_id = self.course_manager.last_course_id + 1

        if self.mode == 'builder':
            self.add_changer.course_id = new_id
            entry = self.add_changer.get_course()
            entry.course_id = new_id

            self.add_changer.clean_form()
        elif self.mode == 'viewer':
            self.course_changer.course_id = new_id
            entry = self.create_add_edit_dialog()
            entry.course_id = new_id
            if not entry:
                return False
        else:
            raise Exception('Unknown course mode: {}'.format(self.mode))

        self.course_manager.add_entry(entry)
        tile = self.make_tile(entry)

        time = self.column_template.format(
                entry.time[0], 
                entry.time[1].lower()
                )

        self.columns[time].pack_start(tile, True, True, 0)

    def edit_entry(self, button):
        """Does not connect builder and viewer well"""
        entry = self.create_add_edit_dialog(self.course_manager.courses[self.selected_id])
        if not entry:
            return False 
        entry.course_id = self.selected_id 

        self.course_manager.edit_entry(entry)

        if self.mode == 'builder':
            for key, column in self.columns.items():
                for tile in column:
                    if tile.course_id == self.selected_id:
                        tile.destroy()
                        break
        elif self.mode == 'viewer':
            self.selected_tile.destroy()

        tile = self.make_tile(entry)

        time = self.column_template.format(
                entry.time[0], 
                entry.time[1].lower()
                )

        self.columns[time].pack_start(tile, True, True, 0)


    def delete_entry(self, button):
        self.course_manager.delete_entry(self.selected_id)

        if self.mode == 'builder':
            for key, column in self.columns.items():
                for tile in column:
                    if tile.course_id == self.selected_id:
                        tile.destroy()
                        break
        elif self.mode == 'viewer':
            self.selected_tile.destroy()
        else:
            raise Exception('Unknown course mode: {}'.format(self.mode))

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        text = str(widget.course_id)  
        widget.destroy()
        data.set_text(text, -1)

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
        tile_id = int(data.get_text())
        course = self.course_manager.courses[tile_id]

        time = [widget.year, widget.quarter]
        tile = courseTile(
                course['title'],       
                course['catalog'],    
                course['credits'],    
                course['prereqs'],
                time,    
                course['course_type'],  
                course['ge_type'],
                tile_id
                )
        
        tile.connect('button-press-event', self.tile_clicked)
        tile.connect("drag-data-get", self.on_drag_data_get)
        
        # Drag and drop
        tile.drag_source_set_target_list(None)
        tile.drag_source_add_text_targets()

        time = self.column_template.format(
                time[0], 
                time[1].lower()
                )

        self.columns[time].pack_start(tile, True, True, 0)

        self.course_manager.edit_entry(chosen_course=tile)

if __name__ == "__main__":
    css = b"""
.major {
    background-color: #FFFF99;
}
.completed .major {
    background-color: #ffffe5;
}


.support {
    background-color: #FFCC99;
}
.completed .support {
    background-color: #fff2e5;
}


.concentration {
    background-color: #FF99CC;
}
.completed .concentration {
    background-color: #ffe5f2;
}


.general-ed {
    background-color: #CCFFCC;
}
.completed .general-ed {
    background-color: #e5ffe5;
}


.free-elective {
    background-color: #CCFFFF;
}
.completed .free-elective {
    background-color: #f2ffff;
}


.minor {
    background-color: #CC99FF;
}
.completed .minor {
    background-color: #f2e5ff;
}


.ge-text {
    color: #00366C;
}

.prereq-text {
    color: #047440;
}
"""

    provider = Gtk.CssProvider()
    provider.load_from_path('./interface/chart_tile.css')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
            provider,  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = FlowChartWindow()
    window.show_all()
    window.maximize()
    Gtk.main()
