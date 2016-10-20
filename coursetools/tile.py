# Need to figure out sizing tiles

from .course import Course
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

DRAG_ACTION = Gdk.DragAction.COPY

class courseTile(Gtk.EventBox, Course):
    """An EventBox that contains all data and menthods of a Course."""
    def __init__(self, title, catalog, units, prereqs, time, course_type, ge_type, course_id):
        Gtk.EventBox.__init__(self)
        Course.__init__(
                self, title, catalog, units, prereqs, time, course_type, ge_type, course_id)

        self.course_class = self.course_type.lower().replace(" ", "-")
        self.get_style_context().add_class(self.course_class)

        self.set_size_request(200, -1)
        
        self.frame = Gtk.Frame()
        self.add(self.frame) 

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box.set_margin_top(10)
        self.box.set_margin_bottom(10)
        self.box.set_margin_start(5)
        self.box.set_margin_end(5)
        self.frame.add(self.box)

        self.title_text = Gtk.Label(self.title)
        self.catalog_text = Gtk.Label(self.catalog)
        self.credits_text = Gtk.Label("(" + str(self.credits) + ")")

        if self.prereqs and self.prereqs != ['']:
            self.prereqs_text = Gtk.Label("(" + ', '.join(self.prereqs) + ")")
            self.prereqs_text.get_style_context().add_class('prereq-text')
            self.prereqs_text.set_justify(Gtk.Justification.CENTER)
            self.prereqs_text.set_line_wrap(True)
            self.box.pack_end(self.prereqs_text, True, True, 0)

        if self.ge_type is not None:
            self.ge_text = Gtk.Label("[" + self.ge_type + "]")
            self.ge_text.get_style_context().add_class('ge-text')
            self.box.pack_end(self.ge_text, True, True, 0)

        self.title_text.set_line_wrap(True)

        self.title_text.set_justify(Gtk.Justification.CENTER)
        self.catalog_text.set_justify(Gtk.Justification.CENTER)
        self.credits_text.set_justify(Gtk.Justification.CENTER)

        self.box.pack_start(self.title_text, True, True, 0)
        self.box.pack_start(self.catalog_text, True, True, 0)
        self.box.pack_start(self.credits_text, True, True, 0)

        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [],
            DRAG_ACTION)

        self.show_all()
   

class tileColumn(Gtk.EventBox):
    """An EventBox that contains courseTiles and is associated with a year and quarter."""
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
    
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], DRAG_ACTION)
