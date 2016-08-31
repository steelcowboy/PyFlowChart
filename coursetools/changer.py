import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .course import Course

class CourseChanger():
    def __init__(self):

        self.quarter_map = {
                'Fall'   : 0,
                'Winter' : 1,
                'Spring' : 2,
                'Summer' : 3
                }

        self.type_map = {
                'Major'         : 0,
                'Support'       : 1,
                'Concentration' : 2, 
                'General Ed'    : 3,
                'Free Elective' : 4
                }

        self.add_year = None
        self.add_quarter = None
        self.tile = None 

        self.builder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        self.grid = self.builder.get_object('modifygrid')
        self.builder_objects = self.builder.get_objects()
        self.get_fields()

    def run_dialog(self, parent, course=None):
        if course:
            function = "Edit"
        else:
            function = "Add"

        new_course = None
        modify_dialog = Gtk.Dialog(function, parent, 0)
        box = modify_dialog.get_content_area()
        dialog_builder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        grid = dialog_builder.get_object('modifygrid')
        box.add(grid)
        
        if self.add_year:
            dialog_builder.get_object('year').set_active(
                    int(self.add_year)-1)
            dialog_builder.get_object('quarter').set_active(
                    self.quarter_map[self.add_quarter])

        if course:
            modify_dialog.add_button('_Edit', Gtk.ResponseType.OK)
            self.get_fields(dialog_builder)
            self.load_entry(course)

        else:
            modify_dialog.add_button('_Add', Gtk.ResponseType.OK)
            self.get_fields(dialog_builder)

        response = modify_dialog.run()

        if response == Gtk.ResponseType.OK:
            new_course = self.get_course()

        modify_dialog.destroy()
        if new_course:
            return new_course
        

    def get_fields(self, location=None):
        """Get fields from builder object"""
        if location is None:
            location = self.builder 

        self.title = location.get_object("title")
        self.catalog = location.get_object("catalog")
        self.credits = location.get_object("credits")
        self.prereqs = location.get_object("prereqs")
        self.year = location.get_object("year")
        self.quarter = location.get_object("quarter")
        self.course_type = location.get_object("type")

    def clean_form(self):
        for field in self.builder_objects:
            if isinstance(field, gi.repository.Gtk.Entry):
                field.set_text('')
            elif isinstance(field, gi.repository.Gtk.SpinButton):
                field.set_value(field.get_range()[0])
            elif isinstance(field, gi.repository.Gtk.ComboBoxText):
                field.set_active(0)

    def load_entry(self, course):
        self.title.set_text(course['title'])
        self.catalog.set_text(course['catalog'])
        self.credits.set_value(course['credits'])
        self.prereqs.set_text(course['prereqs'])
        self.year.set_active(int(course['time'][0])-1)
        self.quarter.set_active(self.quarter_map[course['time'][1]])
        self.course_type.set_active(self.type_map[course['course_type']])

    def get_course(self):
        new_course = Course(
                self.title.get_text(),
                self.catalog.get_text(),
                self.credits.get_value(),
                self.prereqs.get_text(),
                [
                    self.year.get_active_text(), 
                    self.quarter.get_active_text()
                ],
                self.course_type.get_active_text()
                )
        return new_course 
