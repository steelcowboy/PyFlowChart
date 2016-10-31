import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .course import Course

class CourseChanger():
    """A class for dealing with an add/edit interface."""
    def __init__(self):
        """Initialize a CourseChanger object with a mapping of 
        both quarters, types, and setting default values to none
        """
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
                'Free Elective' : 4,
                'Minor'         : 5
                }

        self.ge_type_map = {
                None: -1,
                'B6': 9, 
                'D2': 16, 
                'B3': 6, 
                'D5': 19, 
                'C1': 10, 
                'B5': 8, 
                'D1': 15, 
                'B1': 4, 
                'C2': 11, 
                'D3': 17, 
                'B2': 5, 
                'A1': 1, 
                'A2': 2, 
                'C5': 14, 
                'C4': 13, 
                'A3': 3, 
                'C3': 12, 
                'B4': 7, 
                'D4/E': 18, 
                'F': 20
                }

        self.add_year = None
        self.add_quarter = None
        self.tile = None 

    def init_objects(self, builder):
        """Retreive relevant objects from a Gtk.Builder()."""
        self.grid = builder.get_object('modifygrid')
        self.builder_objects = builder.get_objects()

        self.title = builder.get_object("title")
        self.catalog = builder.get_object("catalog")
        self.credits = builder.get_object("credits")
        
        self.add_button_box = builder.get_object('add_button_box')
        self.prereq_button = builder.get_object('prereq_button')
        self.prereq_button.connect('clicked', self.add_prereq)

        self.prereq_box = builder.get_object('prereq_box')
        self.prereq_entry = builder.get_object('prereq_entry')

        self.year = builder.get_object("year")
        self.quarter = builder.get_object("quarter")
        self.course_type = builder.get_object("type")

        self.ge_type = builder.get_object("ge_type")
    
    def add_prereq(self, button=None, prereq=None):
        """Create a new prereq entry field."""
        new_entry = Gtk.Entry() 
        new_button = Gtk.Button.new_from_icon_name('list-add', Gtk.IconSize.MENU)
        new_button.connect('clicked', self.add_prereq)

        if prereq is not None:
            new_entry.set_text(prereq)

        self.prereq_box.pack_start(new_entry, True, True, 0)
        self.add_button_box.pack_end(new_button, True, True, 0)
        self.grid.show_all()

    def clean_form(self):
        """Clean the form, preserving the year and quarter."""
        for field in self.builder_objects:
            if isinstance(field, gi.repository.Gtk.Entry):
                field.set_text('')
            elif isinstance(field, gi.repository.Gtk.SpinButton):
                field.set_value(field.get_range()[0])
        self.course_type.set_active(-1)
        self.ge_type.set_active(-1)

        for entry in self.prereq_box.get_children()[1:]:
            entry.destroy()
        for button in self.add_button_box.get_children()[1:]:
            button.destroy()

    def reset_form(self):
        """Reset the form."""
        for field in self.builder_objects:
            if isinstance(field, gi.repository.Gtk.Entry):
                field.set_text('')
            elif isinstance(field, gi.repository.Gtk.SpinButton):
                field.set_value(field.get_range()[0])
            elif isinstance(field, gi.repository.Gtk.ComboBoxText):
                field.set_active(-1)
        
        for entry in self.prereq_box.get_children()[1:]:
            entry.destroy()
        for button in self.add_button_box.get_children()[1:]:
            button.destroy()

    def load_entry(self, course):
        """Load course information into the interface."""
        self.title.set_text(course['title'])
        self.catalog.set_text(course['catalog'])
        self.credits.set_value(course['credits'])
        
        prereqs = course['prereqs']
        if isinstance(prereqs, str):
            prereqs = list(filter(None, prereqs.split(',')))
        else:
            prereqs = list(filter(None, prereqs))

        
        if len(prereqs):
            self.prereq_entry.set_text(prereqs[0])
            prereqs = prereqs[1:]

        for prereq in prereqs:
            self.add_prereq(prereq=prereq)

        self.year.set_active(int(course['time'][0])-1)
        self.quarter.set_active(self.quarter_map[course['time'][1]])
        self.course_type.set_active(self.type_map[course['course_type']])
        
        if course['ge_type'] is not None:
            self.ge_type.set_active(self.ge_type_map[course['ge_type']])

    def get_course(self):
        """Retreive course information from the interface."""
        prereqs = [] 
        for entry in self.prereq_box.get_children():
            prereqs.append(entry.get_text())

        prereqs = list(filter(None, prereqs))
        
        ge_text = self.ge_type.get_active_text()
        ge_text = None if ge_text == 'None' else ge_text 

        new_course = Course(
                self.title.get_text(),
                self.catalog.get_text(),
                self.credits.get_value(),
                prereqs,
                [
                    self.year.get_active_text(), 
                    self.quarter.get_active_text()
                ],
                self.course_type.get_active_text(),
                ge_text 
                )
        self.course_id = None
        return new_course 
