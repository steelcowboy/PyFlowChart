import gi, json, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from copy import deepcopy

from interface.about import about_dialog
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
        self.chart_dir = os.path.expanduser("~/.config/PyFlowChart/charts")
        if not os.path.exists(self.chart_dir):
            os.makedirs(self.chart_dir)
    
        Gtk.Window.__init__(self, title=title)
        
        self.filename = None

        self.events = {
                'onOpenPress'    : self.open_file,
                'onAddPress'     : self.add_entry,
                'onEditPress'    : self.edit_entry,
                'onDeletePress'  : self.delete_entry,
                'onSavePress'    : self.save_entry,
                'onSaveAsPress'  : self.save_as,
                'onQuitPress'    : self.quit, 
                'onAboutPress'   : self.about 
                }

        self.course_manager = CourseManager()
        self.course_changer = CourseChanger()
        self.about_dialog = about_dialog(self)
        
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


    def open_file(self, widget):
        """Runs an open file dialog, then instructs the CourseManager 
        to load the chosen file.

        Note: 
            Ensuring the file is a proper JSON file has not been properly
            implemented yet.

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
            self.filename = dialog.get_filename() + ".json"
            dialog.destroy()
            self.course_manager.save(self.filename)
        
        dialog.destroy()

    def about(self, button=None):
        self.about_dialog.present()

    def quit(self, widget, thing=None):
        """Checks if the file is saved before closing."""
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog() 
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.CANCEL:
                return True

        Gtk.main_quit()
