import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from coursetools.tile import courseTile, tileColumn
from coursetools.manager import CourseManager
from appwin import AppWindow

DRAG_ACTION = Gdk.DragAction.MOVE
provider = Gtk.CssProvider()
provider.load_from_path('./interface/chart_tile.css')
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
        provider,  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


class ViewerWindow(AppWindow):
    def __init__(self):
        AppWindow.__init__(self, title="Flowchart Viewer")

        self.column_template = "year_{}_{}"

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

        chart_builder = Gtk.Builder.new_from_file('./interface/glade/chartview_grid.glade')
        courses_grid = chart_builder.get_object('courses_grid')
        scroll_window.add(courses_grid)
    
        self.columns = {}
        for year in range(1,6):
            grid = chart_builder.get_object("year_{}".format(year))
            for pos, quarter in enumerate(["fall", "winter", "spring", "summer"]):
                column_id = self.column_template.format(year, quarter)
                column = tileColumn(year, quarter)
                grid.attach(column, pos*2, 2, 1, 1)
                column.connect('button-press-event', self.box_clicked)
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
                    course['course_id'] 
                    )
            tile.connect('button-press-event', self.tile_clicked)

            time = self.column_template.format(
                    course['time'][0], 
                    course['time'][1].lower()
                    )

            self.columns[time].pack_start(tile, True, True, 0)

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
                new_id
                )
        tile.connect('button-press-event', self.tile_clicked)

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
        self.load_courses()

    def delete_entry(self, button):
        self.course_manager.delete_entry(self.selected_tile)
        self.selected_tile.destroy()

window = ViewerWindow()
window.show_all()
window.maximize()
Gtk.main()
