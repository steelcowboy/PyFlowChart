import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from collections import OrderedDict

GRID_MARGIN = 5
ICON_SIZE = Gtk.IconSize.MENU 

class ModifyGrid(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.generate_labels()
        self.generate_entries()
        self.attach_items() 
        
        self.set_margin_top(GRID_MARGIN)
        self.set_margin_bottom(GRID_MARGIN)
        self.set_margin_start(GRID_MARGIN)
        self.set_margin_end(GRID_MARGIN)
        
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
        self.show_all()
        
    def generate_labels(self):
        self.instructions_label = Gtk.Label('Fill in the following information:')
        self.title_label = Gtk.Label('Course Title:')
        self.catalog_label = Gtk.Label('Catalog Title:')
        self.credits_label = Gtk.Label('Units:')
        self.prereqs_label = Gtk.Label('Prereqs:')
        self.time_label = Gtk.Label('Year and Quarter:')
        self.course_type_label = Gtk.Label('Course Type:')
        self.ge_type_label = Gtk.Label('GE Type: (optional)')
        self.notes_label = Gtk.Label('Notes: (optional)')

        self.labels = [self.title_label, self.catalog_label, self.credits_label,
                self.prereqs_label, self.time_label, 
                self.course_type_label, self.ge_type_label, self.notes_label]

    def generate_entries(self):
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text('Full title of the course')

        self.catalog_entry = Gtk.Entry()
        self.catalog_entry.set_placeholder_text('E.g. COMS 101')

        self.credits_spinner = Gtk.SpinButton.new_with_range(1,6,1)
        self.credits_spinner.set_digits(0)
        self.credits_spinner.set_numeric(True) 
        self.credits_spinner.set_snap_to_ticks(True)
        self.credits_spinner.set_value(1)
        
        # Box to hold prereq entries and buttons
        self.prereqs_box = Gtk.Box()
        self.prereqs_box.set_margin_top(5)
        self.prereqs_box.set_margin_bottom(5)
        
        # Box to hold prereq entry
        self.prereq_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.change_buttons_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.prereq_box.pack_start(Gtk.Entry(), True, True, 0)
        self.change_buttons_box.pack_start(self.create_change_box(), True, True, 0)
        
        self.prereqs_box.pack_start(self.prereq_box, True, True, 0)
        self.prereqs_box.pack_end(self.change_buttons_box, True, True, 0)
        
        self.time_box = Gtk.Box()
        self.time_box.set_homogeneous(True)

        self.year_selector = Gtk.ComboBoxText()
        self.quarter_selector = Gtk.ComboBoxText() 
        for year in range(1,6):
            self.year_selector.append_text(str(year))
        for quarter in ['Fall','Winter','Spring','Summer']:
            self.quarter_selector.append_text(quarter)
        self.time_box.pack_start(self.year_selector, True, True, 0)
        self.time_box.pack_start(self.quarter_selector, True, True, 0)
        
        self.course_type_selector = Gtk.ComboBoxText()
        for c_type in ['Major','Support','Concentration','General Ed','Free Elective','Minor']:
            self.course_type_selector.append_text(c_type)

        # Box to hold GE selectors and buttons 
        self.ge_box = Gtk.Box()
        self.ge_box.set_margin_top(5)
        self.ge_box.set_margin_bottom(5)

        # Box to hold GE selector 
        self.ge_type_selector_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.ge_type_selector_box.pack_start(self.generate_ge_selector(), True, True, 0)
        self.ge_box.pack_start(self.ge_type_selector_box, True, True, 0)
        
        self.ge_buttons_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.ge_buttons_box.pack_start(self.create_change_box("ge"), True, True, 0)
        self.ge_box.pack_end(self.ge_buttons_box, True, True, 0)

        self.notes_entry = Gtk.Entry() 

    def generate_ge_selector(self):
        ge_type_selector = Gtk.ComboBoxText()
        ge_type_selector.append_text('None')
        ge_numbers = {'A':3, 'B':6, 'C':5, 'D':3} 
        ge_numbers = OrderedDict(sorted(ge_numbers.items(), key=lambda t: t[0]))
        for ge_type, how_many in ge_numbers.items():
            for x in range(how_many):
                ge_type_selector.append_text('{}{}'.format(ge_type,x+1))
        ge_type_selector.append_text('D4/E')
        ge_type_selector.append_text('D5')
        ge_type_selector.append_text('F')
        return ge_type_selector 

    def attach_items(self):
        self.attach(self.instructions_label, 0, 0, 2, 1)
        
        for pos, label in enumerate(self.labels):
            self.attach(label, 0, pos+1, 1, 1)

        self.attach(self.title_entry,           1, 1, 1, 1)
        self.attach(self.catalog_entry,         1, 2, 1, 1)
        self.attach(self.credits_spinner,       1, 3, 1, 1)
        self.attach(self.prereqs_box,           1, 4, 1, 1)
        self.attach(self.time_box,              1, 5, 1, 1)
        self.attach(self.course_type_selector,  1, 6, 1, 1)
        self.attach(self.ge_box,                1, 7, 1, 1)
        self.attach(self.notes_entry,           1, 8, 1, 1)
        
        self.bottom_row = 8
    
    def create_change_box(self, button_type="prereq"):
        change_box = Gtk.Box() 
        add_button = Gtk.Button.new_from_icon_name('list-add', ICON_SIZE)
        if button_type == "prereq":
            add_button.connect('clicked', self.add_prereq)
        elif button_type == "ge":
            add_button.connect('clicked', self.add_ge)

        remove_button = Gtk.Button.new_from_icon_name('list-remove', ICON_SIZE)

        if button_type == "prereq":
            remove_button.connect('clicked', self.remove_prereq)
        elif button_type == "ge":
            remove_button.connect('clicked', self.remove_ge)

        change_box.pack_start(add_button, True, True, 0)
        change_box.pack_end(remove_button, True, True, 0)
        return change_box 
    
    def get_entry_values(self):
        """Retreive course information from the interface."""
        notes = self.notes_entry.get_text()
        if notes == '':
            notes = None

        prereqs = [] 
        for entry in self.prereq_box.get_children():
            prereqs.append(entry.get_text())

        prereqs = list(filter(None, prereqs))
        
        ges = []
        for ge in self.ge_type_selector_box.get_children():
            ge_text = ge.get_active_text()
            ge_text = None if ge_text == 'None' else ge_text
            ges.append(ge_text)

        new_course = {
                'title'  : self.title_entry.get_text(),
                'catalog': self.catalog_entry.get_text(),
                'credits': self.credits_spinner.get_value(),
                'prereqs': prereqs,
                'time'   : (
                    int(self.year_selector.get_active_text()), 
                    self.quarter_selector.get_active_text()
                    ),
                'course_type': self.course_type_selector.get_active_text(),
                'ge_type' : ges,
                'notes'  : notes 
                }
        self.course_id = None
        return new_course

    def add_prereq(self, button=None, prereq=None):
        """Create a new prereq entry field."""
        new_entry = Gtk.Entry() 
        change_box = self.create_change_box()

        if prereq is not None:
            new_entry.set_text(prereq)

        self.prereq_box.pack_start(new_entry, True, True, 0)
        self.change_buttons_box.pack_end(change_box, True, True, 0)
        self.show_all()

    def add_ge(self, button=None, ge=None):
        """Create a new prereq entry field."""
        new_selector = self.generate_ge_selector() 
        change_box = self.create_change_box("ge")

        if ge is not None:
            new_selector.set_active(self.ge_type_map[ge])

        self.ge_type_selector_box.pack_start(new_selector, True, True, 0)
        self.ge_buttons_box.pack_end(change_box, True, True, 0)
        self.show_all()

    def remove_prereq(self,button):
        print("I'll remove one eventually!")

    def remove_ge(self,button):
        print("I'll remove one eventually!")

    def clean_form(self):
        """Clean the form, preserving the year and quarter."""
        for entry in [self.title_entry,self.catalog_entry]:
            entry.set_text('')
        
        self.credits_spinner.set_value(self.credits_spinner.get_range()[0])
        self.course_type_selector.set_active(-1)

        for selector in self.ge_type_selector_box.get_children()[1:]:
            selector.destroy()
        self.ge_type_selector_box.get_children()[0].set_active(-1)

        for entry in self.prereq_box.get_children()[1:]:
            entry.destroy()
        self.prereq_box.get_children()[0].set_text('')

        for button in self.change_buttons_box.get_children()[1:]:
            button.destroy()

        for button in self.ge_buttons_box.get_children()[1:]:
            button.destroy()

    def load_entry(self, course):
        """Load course information into the interface."""
        self.title_entry.set_text(course['title'])
        self.catalog_entry.set_text(course['catalog'])
        self.credits_spinner.set_value(course['credits'])
        
        prereqs = course['prereqs']
        if isinstance(prereqs, str):
            prereqs = list(filter(None, prereqs.split(',')))
        else:
            prereqs = list(filter(None, prereqs))

        
        if len(prereqs):
            self.prereq_box.get_children()[0].set_text(prereqs[0])
            prereqs = prereqs[1:]

        for prereq in prereqs:
            self.add_prereq(prereq=prereq)

        self.year_selector.set_active(course['time'][0]-1)
        self.quarter_selector.set_active(self.quarter_map[course['time'][1]])
        self.course_type_selector.set_active(self.type_map[course['course_type']])

        ge_types = list(filter(None, course['ge_type']))

        if len(prereqs):
            self.prereq_box.get_children()[0].set_text(prereqs[0])
            prereqs = prereqs[1:]

        for ge in course['ge_type']:
            self.add_ge(ge=ge)

        if course['notes'] is not None:
            self.notes_entry.set_text(course['notes'])
