import gi, signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from coursetools.tile import courseTile, tileColumn
from coursetools.manager import CourseManager
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

    def setup_window(self):
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

        #chart_builder = Gtk.Builder.new_from_file('./interface/glade/chartview_grid.glade')
        #courses_grid = chart_builder.get_object('courses_grid')
        self.courses_grid = courseGrid()
        scroll_window.add(self.courses_grid)
    
        self.columns = {}
        for year in range(1,5):
            for pos, quarter in enumerate(["fall", "winter", "spring", "summer"]):
                column_id = self.column_template.format(year, quarter)
                #column = tileColumn(year, quarter)
                column = self.courses_grid.year_map[year].quarter_map[pos]

                # For drag and drop
                column.drag_dest_set_target_list(None)
                column.drag_dest_add_text_targets()

                #grid.attach(column, pos*2, 2, 1, 1)
                column.connect('button-press-event', self.box_clicked)
                column.connect("drag-data-received", self.on_drag_data_received)
                self.columns[column_id] = column.box
        
    
    def tile_clicked(self, widget, event):
        if event.button == 3:
            self.editmenu.popup(None, None, None, None, event.button, event.time)
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
        if not super(ViewerWindow, self).new_file(widget):
            return

        for time, box in self.columns.items():
            for tile in box.get_children():
                tile.destroy()

    def open_file(self, widget):
        if not super(ViewerWindow, self).open_file(widget):
            return
    
        self.load_courses()

    def load_courses(self):
        for time, box in self.columns.items():
            for tile in box.get_children():
                tile.destroy()

        for course in self.course_manager.courses:
            tile = courseTile(
                    course['title'], 
                    course['catalog'], 
                    course['credits'],
                    course['prereqs'], 
                    course['time'], 
                    course['course_type'],
                    course['ge_type'],
                    course['course_id'] 
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
                    #for tile in self.columns[time].get_children():
                    #    tile.get_style_context().remove_class(tile.course_class)
                    #    tile.get_style_context().add_class(tile.course_class + '-completed')
            else:
                for x in range(0,4):
                    time = self.column_template.format(year, dict(self.quarter_map)[x])
                    self.columns[time].get_style_context().add_class('completed')

                    #for tile in self.columns[time].get_children():
                    #    tile.get_style_context().remove_class(tile.course_class)
                    #    tile.get_style_context().add_class(tile.course_class + '-completed')
    
    def add_entry(self, button):
        new_id = self.course_manager.last_course_id + 1
        self.course_changer.course_id = new_id

        entry = self.create_add_edit_dialog()
        if not entry:
            return False

        self.course_manager.add_entry(entry)

        tile = courseTile(
                entry.title, 
                entry.catalog, 
                entry.credits,
                entry.prereqs, 
                entry.time, 
                entry.course_type,
                entry.ge_type, 
                new_id
                )
        tile.connect('button-press-event', self.tile_clicked)
        tile.connect("drag-data-get", self.on_drag_data_get)
        
        # Drag and drop
        tile.drag_source_set_target_list(None)
        tile.drag_source_add_text_targets()

        time = self.column_template.format(
                entry.time[0], 
                entry.time[1].lower()
                )

        self.columns[time].pack_start(tile, True, True, 0)

    def edit_entry(self, button):
        entry = self.create_add_edit_dialog(self.selected_tile.export())
        if not entry:            
            return False

        self.course_manager.edit_entry(chosen_course=entry)
            
        tile = courseTile(
                entry.title,       
                entry.catalog,    
                entry.credits,    
                entry.prereqs,
                entry.time,    
                entry.course_type,  
                entry.ge_type,
                entry.course_id
                )
        
        tile.connect('button-press-event', self.tile_clicked)
        tile.connect("drag-data-get", self.on_drag_data_get)
        
        # Drag and drop
        tile.drag_source_set_target_list(None)
        tile.drag_source_add_text_targets()

        time = self.column_template.format(
                entry.time[0], 
                entry.time[1].lower()
                )

        self.columns[time].pack_start(tile, True, True, 0)

        self.selected_tile.destroy()

    def delete_entry(self, button):
        self.course_manager.delete_entry(self.selected_tile)
        self.selected_tile.destroy()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        """Not yet implemented."""
        text = str(widget.course_id)  
        widget.destroy()
        data.set_text(text, -1)

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
        tile_id = int(data.get_text())
        for course in self.course_manager.courses:
            if course['course_id'] == tile_id:
                time = [widget.year, widget.quarter]
                tile = courseTile(
                        course['title'],       
                        course['catalog'],    
                        course['credits'],    
                        course['prereqs'],
                        time,    
                        course['course_type'],  
                        course['ge_type'],
                        course['course_id']
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

                # print("Know what you're talking about!")
                # print(course['catalog'])
                # print("I will now put it in year {} {} quarter for you cause I love you!".format(widget.year, widget.quarter))
if __name__ == "__main__":
    provider = Gtk.CssProvider()
    provider.load_from_path('./interface/chart_tile.css')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
            provider,  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = ViewerWindow()
    window.show_all()
    window.maximize()
    Gtk.main()
