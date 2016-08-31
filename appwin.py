import gi, json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from coursetools.manager import CourseManager

class AppWindow(Gtk.Window):
    def __init__(self, title): 
        Gtk.Window.__init__(self, title=title)
        
        self.filename = None

        self.events = {
                'onOpenPress'    : self.open_file,
                'onAddPress'     : self.add_entry,
                'onEditPress'    : self.edit_entry,
                'onDeletePress'  : self.delete_entry,
                'onAddPress'     : self.add_entry,
                'onSavePress'    : self.save_entry,
                'onSaveAsPress'  : self.save_as,
                'onQuitPress'    : self.quit 
                }

        self.course_manager = CourseManager()
        
    def create_confirm_dialog(self):
        return Gtk.MessageDialog(self, 0, 
                Gtk.MessageType.WARNING, 
                Gtk.ButtonsType.OK_CANCEL, 
                "You have unsaved changes! Are you sure you wish to proceed?")


    def open_file(self, widget):
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog()
            confirm_response = dialog.run()
            dialog.destroy()

            if confirm_response == Gtk.ResponseType.CANCEL: 
                return 0 

        dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
            self.course_manager.saved = True 
            
            self.course_manager.courses = []
            if self.course_manager.store:
                self.course_manager.store.clear()

            while self.course_manager.load_file(self.filename):
                fail_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Not a valid JSON file, please try again")
                fail_dialog.run()
                pass
                fail_dialog.destroy()

        dialog.destroy()
        return 1

    def save_entry(self, window):
        """Save file"""
        if not self.filename:
            dialog = Gtk.FileChooserDialog("Save as...", self,
                Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                self.filename = dialog.get_filename() + ".json"
                dialog.destroy()
 
        self.course_manager.save(self.filename)

    def save_as(self, window):
        """Save file under another name"""
        dialog = Gtk.FileChooserDialog("Save as...", self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename() + ".json"
            dialog.destroy()
 
        self.course_manager.save(self.filename)

    def quit(self, widget, thing=None): 
        if not self.course_manager.saved:
            dialog = self.create_confirm_dialog() 
            response = dialog.run()
            dialog.destroy()

            if response == Gtk.ResponseType.CANCEL:
                return True

        Gtk.main_quit()
