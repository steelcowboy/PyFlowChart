import json
from .course import Course 
from .coursetime import courseTime 
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
            course_id = int(course_id)
            if isinstance(course['prereqs'], str):
                course['prereqs'] = [x.strip() for x in 
                    course['prereqs'].split(',')]

            if 'ge_type' not in course:
                course['ge_type'] = None

            course['time'] = courseTime(int(course['time'][0]), course['time'][1])

            self.courses[course_id] = course

            if self.store:
                self.store.append([
                    course['catalog'], 
                    str(
                        str(course['time'][0]) + 
                        ', ' + 
                        course['time'][1]
                        ), 
                    course['credits'], 
                    course['course_type'],
                    course_id
                ])
            course_ids.append(course_id)

        self.last_course_id = max(course_ids)
        return 1


    def edit_entry(self, chosen_course):
        """Edit existing entry.
        
        Arguments:
            chosen_course (Course): The course to edit.
            selection (Gtk.TreeSelection): An optional Gtk TreeSelection representing
                the current selection in the treeview that is to be edited.
                                           
        """
        c_id = chosen_course.course_id 

        for row in self.store:
            if row[4] == c_id:
                course_iter = row.iter 

        self.store[course_iter] = [
                chosen_course.catalog, 
                str(
                    str(chosen_course.time[0]) + 
                    ', ' + 
                    chosen_course.time[1]
                    ), 
                chosen_course.credits, 
                chosen_course.course_type,
                c_id
                ]
        
        # Convert the tuple to a courseTime
        time = courseTime(chosen_course.time[0], chosen_course.time[1])
        
        # Course ID from the arguments
        self.courses[c_id]['title']       = chosen_course.title
        self.courses[c_id]['catalog']     = chosen_course.catalog
        self.courses[c_id]['credits']     = chosen_course.credits
        self.courses[c_id]['prereqs']     = chosen_course.prereqs
        self.courses[c_id]['time']        = time
        self.courses[c_id]['course_type'] = chosen_course.course_type
        self.courses[c_id]['ge_type']     = chosen_course.ge_type 
        
        self.saved = False
        return chosen_course.course_id   

    def delete_entry(self, selected_id): 
        """Delete existing entry.
        
        Arguments:
            selected_id (int): The id of the course to delete.
        """
        for row in self.store:
            if row[4] == selected_id:
                self.store.remove(row.iter)

        entry = self.courses.pop(selected_id)
        
        self.saved = False
        return entry

    def add_entry(self, course):
        """Add a course to the CourseManager's list."""
        self.saved = False
        course = course.export() 
        c_id = course.pop('course_id') 
        
        if not c_id:
            c_id = self.last_course_id
        elif c_id in self.courses:
            c_id = self.last_course_id + 1
            self.last_course_id = self.last_course_id + 1

        self.courses[c_id] = course 
        if self.store:
            self.store.append([
                course['catalog'], 
                str(
                    str(course['time'][0]) + 
                    ', ' + 
                    course['time'][1]
                ), 
                course['credits'],
                course['course_type'], 
                c_id 
            ])

        self.last_course_id = self.last_course_id + 1
    
    def check_prereq_conflicts(self, entry):
        time = courseTime(int(entry.time[0]), entry.time[1])

        for c_id, course in self.courses.items():
            if course['time'] >= time:
                if course['catalog'] in entry.prereqs:
                    return True
                    break

        return False

    def get_course(self, c_id):
        course = self.courses[c_id] 
        return Course(
                course['title'],
                course['catalog'],
                course['credits'],
                course['prereqs'],
                course['time'],
                course['course_type'],
                course['ge_type'],
                c_id)

    def save(self, filename):
        """Save all courses to the given filename."""
        with open(filename, 'w') as flowfile:
            courses = {
                    'courses' : self.courses
                    }
            flowfile.write(json.dumps(courses, indent=4))
        self.saved = True
