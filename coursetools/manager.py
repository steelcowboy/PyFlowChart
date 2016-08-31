import json
from .course import Course 

class CourseManager():
    def __init__(self, store=None):
        self.store = store 
        
        self.courses = []
        
        self.saved = True

    def load_file(self, filename):
        with open(filename, 'r') as jsonfile:
            try:
                courses = json.loads(jsonfile.read())
            except json.decoder.JSONDecodeError:
                return 1

            file_courses = courses
            for file_course in file_courses['courses']: 
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
            return 0


    def edit_entry(self, chosen_course=None, index=None, treeiter=None):
        """Edit existing entry"""
        """Stub until I figure out a better way to implement"""
        raise NotImplementedError

    def delete_entry(self, chosen_course=None, tree=None): 
        """Delete existing entry"""
        # Need to modify to get from chart view
        if tree:
            course_selection = tree.get_selection()
            # I think the documentation for get_seleceded_rows is 
            # incorrect because index 0 is a ListStore...
            path = course_selection.get_selected_rows()[1][0]
            index = path.get_indices()[0]
            model, treeiter = course_selection.get_selected()

            course = self.courses[index]

            self.store.remove(treeiter)
            del self.courses[index]
        
        if chosen_course:
            for index, course in enumerate(self.courses):
                if chosen_course.catalog == course['catalog']:
                    del self.courses[index]

    def add_entry(self, course):
        self.saved = False
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

    def save(self, filename):
        with open(filename, 'w') as flowfile:
            courses = {
                    'courses' : self.courses
                    }
            flowfile.write(json.dumps(courses, indent=4))
        self.saved = True
        





