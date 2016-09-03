# Need to figure out sizing tiles

from .course import Course
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

class courseTile(Gtk.EventBox, Course):
    def __init__(self, title, catalog, units, prereqs, time, course_type, course_id):
        Gtk.EventBox.__init__(self)
        Course.__init__(
                self, title, catalog, units, prereqs, time, course_type, course_id)

        self.name = catalog

        self.get_style_context().add_class(self.course_type.lower().replace(" ", "-"))
        
        self.frame = Gtk.Frame()
        self.add(self.frame) 

        self.self = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.self.set_margin_top(10)
        self.self.set_margin_bottom(10)
        self.self.set_margin_start(5)
        self.self.set_margin_end(5)
        self.frame.add(self.self)

        self.title_text = Gtk.Label(self.title)
        self.catalog_text = Gtk.Label(self.catalog)
        self.credits_text = Gtk.Label("(" + str(self.credits) + ")")
        self.prereqs_text = Gtk.Label("(" + ', '.join(self.prereqs) + ")")

        self.title_text.set_justify(Gtk.Justification.CENTER)
        self.catalog_text.set_justify(Gtk.Justification.CENTER)
        self.credits_text.set_justify(Gtk.Justification.CENTER)
        self.prereqs_text.set_justify(Gtk.Justification.CENTER)

        self.self.pack_start(self.title_text, True, True, 0)
        self.self.pack_start(self.catalog_text, True, True, 0)
        self.self.pack_start(self.credits_text, True, True, 0)
        self.self.pack_start(self.prereqs_text, True, True, 0)

        self.connect("drag-data-get", self.on_drag_data_get)

        self.show_all()
   
    def on_drag_data_get(self, widget, drag_context, data, info, time):
        text = self.title 
        data.set_text(text, -1)

class tileColumn(Gtk.EventBox):
    def __init__(self, year, quarter):
        Gtk.EventBox.__init__(self)

        self.year = year
        self.quarter = quarter.capitalize()

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_valign(Gtk.Align.FILL)

        self.box = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,spacing=10
                )
        self.box.set_hexpand(True)
        self.box.set_vexpand(True)
        self.box.set_valign(Gtk.Align.START)
        self.add(self.box)

