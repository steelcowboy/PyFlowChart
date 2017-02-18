# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class about_dialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self, parent=parent)

        self.set_program_name('PyFlowChart')
        self.set_version('0.9.2')
        self.set_comments('A program to create interactive cirriculum flowcharts')

        self.set_logo_icon_name('applications-accessories')

        self.set_copyright('© 2016 Jim Heald')
        self.set_license_type(Gtk.License.BSD)

        self.set_authors('Jim Heald https://github.com/steelcowboy')

        self.connect('response', self.hide_dialog)
        self.connect('delete-event', self.hide_dialog)

    def hide_dialog(self, widget=None, event=None):
        self.hide()
        return True

