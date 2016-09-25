import json
from .course import Course 

class CourseManager():
    """A class for managing courses.
    
    Attributes:
        courses (list): A list of all course objects being handled by the session.
        saved (bool): Whether or not the course information is consistent with
                      the file on the disk.
        last_course_id (int): The greatest course id in use by a Course object.
    """
    def __init__(self, store=None):
        """Initialize a CourseManager.

        Arguments:
            store (Gtk.ListStore): a store to append data into.
        """
        self.store = store 
        
        self.courses = []
        self.saved = True
        self.last_course_id = 0

    def load_file(self, filename):
        """Load a file into the course manager.

        Arguments:
            filename (str): The path to the JSON file 
                            containing the course information.

        Returns:
            1 if successful, 0 otherwise.
        """
        with open(filename, 'r') as jsonfile:
            try:
                courses = json.loads(jsonfile.read())
            except json.decoder.JSONDecodeError:
                return 0

            file_courses = courses
            course_id = 0
            course_ids = []

            for file_course in file_courses['courses']: 
                if 'course_id' not in file_course:
                    file_course['course_id'] = course_id
                    course_id = course_id + 1
                    course_ids.append(course_id)

                else:
                    course_ids.append(file_course['course_id'])
                
                if isinstance(file_course['prereqs'], str):
                    file_course['prereqs'] = [x.strip() for x in 
                        file_course['prereqs'].split(',')]

                if 'ge_type' not in file_course:
                    file_course['ge_type'] = None

                self.courses.append(file_course)
                if self.store:
                    self.store.append([
                        file_course['catalog'], 
                        str(
                            file_course['time'][0] + 
                            ', ' + 
                            file_course['time'][1]
                            ), 
                        file_course['credits'], 
                        file_course['course_type']
                    ])
            
            self.last_course_id = max(course_ids)
            return 1


    def edit_entry(self, chosen_course, selection=None):
        """Edit existing entry.
        
        Arguments:
            chosen_course (Course): The course to edit.
            selection (Gtk.TreeSelection): An optional Gtk TreeSelection representing
                the current selection in the treeview that is to be edited.
                                           
        """
        if selection:
            model, treeiter = selection.get_selected()
            self.store[treeiter] = [
                    chosen_course.catalog, 
                    str(
                        chosen_course.time[0] + 
                        ', ' + 
                        chosen_course.time[1]
                        ), 
                    chosen_course.credits, 
                    chosen_course.course_type
                    ]

        for course in self.courses:
            if course['course_id'] == chosen_course.course_id:
                course['title']       = chosen_course.title
                course['catalog']     = chosen_course.catalog
                course['credits']     = chosen_course.credits
                course['prereqs']     = chosen_course.prereqs
                course['time']        = chosen_course.time
                course['course_type'] = chosen_course.course_type
                course['ge_type']     = chosen_course.ge_type 
                
                self.saved = False
                return chosen_course.course_id   


    def delete_entry(self, chosen_course=None, selection=None): 
        """Delete existing entry.
        
        Arguments (optional):
            chosen_course (Course): The course to delete.
            selection (Gtk.TreeSelection): The selection to delete. 
        """
        if selection:
            # I think the documentation for get_seleceded_rows is 
            # incorrect because index 0 is a ListStore...
            path = selection.get_selected_rows()[1][0]
            index = path.get_indices()[0]
            model, treeiter = selection.get_selected()

            course = self.courses[index]

            self.store.remove(treeiter)
            del self.courses[index]
        
        if chosen_course:
            for index, course in enumerate(self.courses):
                if chosen_course.course_id == course['course_id']:
                    del self.courses[index]

    def add_entry(self, course):
        """Add a course to the CourseManager's list."""
        self.saved = False
        if not course.course_id:
            course.course_id = self.last_course_id
            self.last_course_id = self.last_course_id + 1

        self.courses.append(course.export())
        if self.store:
            self.store.append([
                course.catalog, 
                str(
                    course.time[0] + 
                    ', ' + 
                    course.time[1]
                ), 
                course.credits,
                course.course_type 
            ])

        self.last_course_id = self.last_course_id + 1

    def save(self, filename):
        """Save all courses to the given filename."""
        with open(filename, 'w') as flowfile:
            courses = {
                    'courses' : self.courses
                    }
            flowfile.write(json.dumps(courses, indent=4))
        self.saved = True
        





