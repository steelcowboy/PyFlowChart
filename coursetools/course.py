class Course():
    """An object to store information about a course. 
    
    Attributes:
        title (str): The course's full title.
        catalog (str): The course's catalog title (e.g. AERO 121).
        credits (int): How many units the course is worth.
        prereqs (list): A list of the catalog titles of the prereqs of the course.
        time (list): A list representing the year and quarter the course will be taken.
        course_type (str): One of:
             Major, Support, Concentration, General Ed, or Free Elective.
        course_id (int): An id used internally to reference the course. 

    """ 
    
    def __init__(self, title, catalog, credits, prereqs, time, course_type, ge_type=None, course_id=None):
        
        self.title = title
        self.catalog = catalog
        self.credits = credits
        self.prereqs = prereqs
        self.time = time
        self.course_type = course_type
        self.ge_type = ge_type 
        self.course_id = course_id 

    def __str__(self):
        """Return a string with the course's information, usually for debugging."""
        return "{}\n{}\n{} Credits\n{}".format(
                self.title,
                self.catalog,
                self.credits,
                self.time
                )

    def export(self):
        """Return the course's attributes."""
        export_dict = {
                'course_id'   : self.course_id,
                'title'       : self.title,
                'catalog'     : self.catalog,
                'credits'     : self.credits,
                'prereqs'     : self.prereqs, 
                'time'        : self.time,
                'course_type' : self.course_type,
                'ge_type'     : self.ge_type
                }
        return export_dict
    

