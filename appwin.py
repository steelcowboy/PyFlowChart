import gi, json, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from interface.about import about_dialog
from interface.preferences import preferences_dialog 
from coursetools.manager import CourseManager
from coursetools.changer import CourseChanger

class AppWindow(Gtk.Window):
    """A class to set up a FlowChart app window.

    Note:
        All derived classes must implement the following functions:
            add_entry()
            edit_entry()
            delete_entry()
            
    Attributes:
        filename (str): a filename associated with the session.
        course_manager (CourseManager): the CourseManager instance associated with the session.
        course_changer (CourseChanger): the CourseChanger instance associated with the session.
    """
    def __init__(self, title): 
        Gtk.Window.__init__(self, title=title)
        
        self.filename = None

        self.config_dir = os.path.expanduser("~/.config/PyFlowChart")
        self.config_file = os.path.expanduser("~/.config/PyFlowChart/config")
        self.chart_dir = os.path.expanduser("~/.config/PyFlowChart/charts")
        self.check_config()

        self.events = {
                'onNewPress'     : self.new_file,
                'onOpenPress'    : self.open_file,
                'onAddPress'     : self.add_entry,
                'onEditPress'    : self.edit_entry,
                'onDeletePress'  : self.delete_entry,
                'onSavePress'    : self.save_entry,
                'onSaveAsPress'  : self.save_as,
                'onQuitPress'    : self.quit, 
                'onAboutPress'   : self.about,
                'onPrefPress'    : self.preferences
                }

        self.course_manager = CourseManager()
        self.course_changer = CourseChanger()
        self.about_dialog = about_dialog(self)
        # Preferences dialog should work like this, to be implemented
        #self.preferences_dialog = preferences_dialog(self)
        
        self.parse_config()

    def check_config(self):
        """Make sure all files and folders exist, and make sure 
        the config file is properly formatted."""
        if not os.path.exists(self.chart_dir):
            os.makedirs(self.chart_dir)
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as conf:
                config = {
                        'userInfo' : {'year': 1},
                        'GEs'      : {}
                        }
                conf.write(json.dumps(config, indent=4))

    def create_confirm_dialog(self):
        """Returns a dialog object to prompt the user if the flowchart is unsaved."""
        return Gtk.MessageDialog(self, 0, 
                Gtk.MessageType.WARNING, 
                Gtk.ButtonsType.OK_CANCEL, 
                "You have unsaved changes! Are you sure you wish to proceed?")

    def create_save_as_dialog(self):
        """Returns a Save As dialog object."""
        return Gtk.FileChooserDialog("Save as...", self,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))


    def create_add_edit_dialog(self, course=None):
        """Creates a dialog to either add or edit a course.
        
        Arguments:
            course (Course or subclass): course to edit.

        Returns:
            New course if successful. Nothing otherwise. 
        """
        builder = Gtk.Builder.new_from_file('./interface/glade/modify_interface.glade')
        self.course_changer.init_objects(builder)
    
        if course:
            function = "Edit"
        else:
            function = "Add"

        new_course = None
        modify_dialog = Gtk.Dialog(function, self, 0)
        box = modify_dialog.get_content_area()
        grid = self.course_changer.grid 
        box.add(grid)
        
        prereq_box = self.course_changer.prereq_box  
        add_button_box = self.course_changer.add_button_box 

        if self.course_changer.add_year:
            builder.get_object('year').set_active(
                    int(self.course_changer.add_year)-1)
            builder.get_object('quarter').set_active(
                    self.course_changer.quarter_map[self.course_changer.add_quarter])

        if course:
            modify_dialog.add_button('_Edit', Gtk.ResponseType.OK)
            self.course_changer.load_entry(course)

        else:
            modify_dialog.add_button('_Add', Gtk.ResponseType.OK)

        response = modify_dialog.run()

        if response == Gtk.ResponseType.OK:
            new_course = self.course_changer.get_course()

        modify_dialog.destroy()
        if new_course:
            return new_course

    def parse_config(self):
        """Open the config file and read the data."""
        with open(self.config_file, 'r') as jsonfile:
            try:
                config = json.loads(jsonfile.read())
            except ValueError:
                return 0

            self.course_manager.ge_map = config["GEs"]
            self.course_manager.user   = config["userInfo"]

    def new_file(self, widget=None):
        """Clears everything from CourseManager to create a new file.
        
        Returns:
            1 if successful, 0 otherwise. 
        """
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog()
            confirm_response = dialog.run()
            dialog.destroy()

            if confirm_response == Gtk.ResponseType.CANCEL: 
                return 0 
        
        self.filename = None 
        self.course_manager.courses = []
        if self.course_manager.store:
            self.course_manager.store.clear()
        self.course_manager.saved = True
        return 1


    def open_file(self, widget):
        """Runs an open file dialog, then instructs the CourseManager 
        to load the chosen file.

        Returns:
            1 if successful, 0 otherwise.
        """
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog()
            confirm_response = dialog.run()
            dialog.destroy()

            if confirm_response == Gtk.ResponseType.CANCEL: 
                return 0 

        while True:
            open_dialog = Gtk.FileChooserDialog("Please choose a file", self,
                Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            open_dialog.set_current_folder(self.chart_dir)

            response = open_dialog.run()

            if response == Gtk.ResponseType.OK:
                self.filename = open_dialog.get_filename()
                self.course_manager.saved = True 
                
                self.course_manager.courses = []
                if self.course_manager.store:
                    self.course_manager.store.clear()

                if not self.course_manager.load_file(self.filename):
                    fail_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                    Gtk.ButtonsType.OK, "Not a valid JSON file, please try again")
                    fail_dialog.run()
                    pass
                    fail_dialog.destroy()
                    open_dialog.destroy()
                else:
                    open_dialog.destroy()
                    return 1
            else:
                open_dialog.destroy()
                return 0


    def save_entry(self, window):
        """Creates a save dialog (or save as if no filename)."""
        if not self.filename:
            self.save_as()
        else:
            self.course_manager.save(self.filename)

    def save_as(self, window=None):
        """Save file under another name."""
        dialog = self.create_save_as_dialog()
        dialog.set_current_folder(self.chart_dir)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            fn = dialog.get_filename()
            self.filename = fn if ".json" in fn else fn + ".json"
            #self.filename = dialog.get_filename() + ".json"
            dialog.destroy()
            self.course_manager.save(self.filename)
        
        dialog.destroy()

    def about(self, button=None):
        self.about_dialog.present()

    def preferences(self, button=None):
        for course in self.course_manager.courses:
            if (course['ge_type'] != None and
                    course['catalog'] not in self.course_manager.ge_map and
                    course['ge_type'] not in self.course_manager.ge_map): 
                self.course_manager.ge_map[course['ge_type']] = course['catalog']

        dialog = preferences_dialog(self, self.course_manager.ge_map, self.course_manager.user)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            year = int(dialog.year_selector.get_active_text())
            self.course_manager.user['year'] = year
            self.course_manager.ge_map = {}

            for x in range(dialog.ge_length):
                ge_label = dialog.ges.get_child_at(1, x)
                if ge_label.text is not None :
                    text = ge_label.text
                elif ge_label.has_entry and ge_label.entry.get_text() != '':
                    text = ge_label.entry.get_text()
                else:
                    continue

                label = dialog.ges.get_child_at(0, x).get_label()
                self.course_manager.ge_map[label] = text


            self.save_preferences()

        dialog.destroy()

    def save_preferences(self):
        """Save preferences."""
        with open(self.config_file, 'w') as conf:
            config = {
                    'userInfo' : self.course_manager.user,
                    'GEs'      : self.course_manager.ge_map
                    }
            conf.write(json.dumps(config, indent=4))

    def quit(self, widget, thing=None):
        """Checks if the file is saved before closing."""
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog() 
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.CANCEL:
                return True

        Gtk.main_quit()
