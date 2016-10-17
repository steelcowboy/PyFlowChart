import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class editable_label(Gtk.EventBox):
    def __init__(self, text=None):
        Gtk.EventBox.__init__(self)
        self.text = text 
        self.has_entry = False 
        
        if text is not None:
            self.label = Gtk.Label(text)
            self.add(self.label)
        else:
            self.entry = Gtk.Entry()
            self.entry.connect('activate', self.enter_key)
            self.add(self.entry)
            self.has_entry = True 
        
        self.connect('button-press-event', self.double_click)


        self.show_all()

    def double_click(self, widget, event):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            if not self.has_entry:
                self.label.destroy()
                self.entry = Gtk.Entry()
                self.entry.connect('activate', self.enter_key)
                self.entry.set_text(self.text)
                self.add(self.entry)
                self.text = None
                
                self.show_all() 
                self.has_entry = True
        return True 
    
    def enter_key(self, widget=None):
        if self.entry.get_text() == '' or self.entry.get_text().isspace():
            self.text = None 
        else:
            self.text = self.entry.get_text()
        self.entry.destroy()
        self.has_entry = False

        self.label = Gtk.Label(self.text) if self.text is not None else Gtk.Label('')
        self.add(self.label)
        self.show_all()
        return True 


