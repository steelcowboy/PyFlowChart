class Course():
    """An object to store information about a course""" 
    
    def __init__(self, title, catalog, credits, prereqs, time, course_type, course_id=None):
        
        self.title = title
        """A string with the course's title"""

        self.catalog = catalog
        """
        A string with the department and course number
        e.g. AERO 121
        """

        self.credits = credits
        """
        An interger that tells how many units 
        the course is worth
        """
        
        self.prereqs = prereqs
        """
        A list of prereqs for the course,
        or 'None' if no prereqs
        """

        self.time = time
        """
        A tuple representing the time and quarter
        """

        self.course_type = course_type
        """
        One of: Major, Support, Concentration, General Ed, or Free Elective
        """

        self.course_id = course_id 
        """An id used internally for referencing"""

    def __str__(self):
        return "{}\n{}\n{} Credits\n{}".format(
                self.title,
                self.catalog,
                self.credits,
                self.time)

    def export(self):
        export_dict = {
                'course_id'   : self.course_id,
                'title'       : self.title,
                'catalog'     : self.catalog,
                'credits'     : self.credits,
                'prereqs'     : self.prereqs, 
                'time'        : self.time,
                'course_type' : self.course_type 
                }
        return export_dict
    

