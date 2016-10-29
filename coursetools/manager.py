import json
from .course import Course 
from datetime import datetime 

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
        
        self.courses = {}
        self.ge_map = {}        
        self.user = {
                'year': 1
                }
        
        today = datetime.today()
        
        fall = datetime(today.year, 9, 15)
        winter = datetime(today.year, 1, 1)
        spring = datetime(today.year, 3, 31)
        summer = datetime(today.year, 6, 15)

        if fall <= today <= datetime(today.year, 12, 31):
            self.quarter = 0
        elif winter <= today < spring:
            self.quarter = 1
        elif spring <= today < summer:
            self.quarter = 2
        else:
            self.quarter = 3

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
            except ValueError: 
                return 0

            file_courses = courses
            course_id = 0
            course_ids = []

            ## old behavior
            # for file_course in file_courses['courses']: 
                # if 'course_id' not in file_course:
                    # file_course['course_id'] = course_id
                    # course_id = course_id + 1
                    # course_ids.append(course_id)

                # else:
                    # course_ids.append(file_course['course_id'])
                
                # if isinstance(file_course['prereqs'], str):
                    # file_course['prereqs'] = [x.strip() for x in 
                        # file_course['prereqs'].split(',')]

                # if 'ge_type' not in file_course:
                    # file_course['ge_type'] = None

                # self.courses.append(file_course)
                # if self.store:
                    # self.store.append([
                        # file_course['catalog'], 
                        # str(
                            # str(file_course['time'][0]) + 
                            # ', ' + 
                            # file_course['time'][1]
                            # ), 
                        # file_course['credits'], 
                        # file_course['course_type']
                    # ])
            
            tmp_cs = file_courses['courses'] 
            
            if isinstance(tmp_cs, list):
                cs = {}
                for course_object in tmp_cs:
                    object_id = course_object.pop('course_id')
                    cs[object_id] = course_object
            elif isinstance(tmp_cs, dict): 
                cs = tmp_cs 
            else:
                raise Exception("Invalid course object!")
                return 0

            for course_id, course in cs.items(): 
                if isinstance(course['prereqs'], str):
                    course['prereqs'] = [x.strip() for x in 
                        course['prereqs'].split(',')]

                if 'ge_type' not in course:
                    course['ge_type'] = None

                self.courses[course_id] = course

                if self.store:
                    self.store.append([
                        cs[course_id]['catalog'], 
                        str(
                            str(cs[course_id]['time'][0]) + 
                            ', ' + 
                            cs[course_id]['time'][1]
                            ), 
                        cs[course_id]['credits'], 
                        cs[course_id]['course_type'],
                        course_id
                    ])
                course_ids.append(course_id)

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

        # Course ID from the arguments
        c_id = chosen_course.course_id 
        self.courses[c_id]['title']       = chosen_course.title
        self.courses[c_id]['catalog']     = chosen_course.catalog
        self.courses[c_id]['credits']     = chosen_course.credits
        self.courses[c_id]['prereqs']     = chosen_course.prereqs
        self.courses[c_id]['time']        = chosen_course.time
        self.courses[c_id]['course_type'] = chosen_course.course_type
        self.courses[c_id]['ge_type']     = chosen_course.ge_type 
        
        self.saved = False
        return chosen_course.course_id   


    def delete_entry(self, chosen_course=None, selection=None): 
        """Delete existing entry.
        
        Arguments (optional):
            chosen_course (Course): The course to delete.
            selection (Gtk.TreeSelection): The selection to delete. 
        """
### THIS MAY BE BUGGY ###
        if selection:
            # I think the documentation for get_seleceded_rows is 
            # incorrect because index 0 is a ListStore...
            path = selection.get_selected_rows()[1][0]
            index = path.get_indices()[0]
            model, treeiter = selection.get_selected()
            print(self.store[treeiter])
            
            course = self.courses[index]

            self.store.remove(treeiter)
            del self.courses[index]
        
        if chosen_course:
            self.courses.pop(chosen_course.course_id)

    def add_entry(self, course):
        """Add a course to the CourseManager's list."""
        self.saved = False
        if not course.course_id:
            course.course_id = self.last_course_id

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
                course.course_type, 
                self.last_course_id 
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
        





