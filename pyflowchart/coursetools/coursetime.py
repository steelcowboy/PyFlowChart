class courseTime(tuple):
    """A way to represent when a course should be taken, 
        adding some extensions to a tuple for comparison purposes"""
    def __new__ (cls, y, q):
        return super(courseTime, cls).__new__(cls, (y,q))

    def __init__(self, year, quarter):
        tuple.__init__(self)
        self.quarter_map =  {
                "Fall":   0,
                "Winter": 1,
                "Spring": 2,
                "Summer": 3  
                }
        self.year = year
        self.quarter = self.quarter_map[quarter]

    def __gt__(self, other):
        if self.year > other.year:
            return True
        elif self.year == other.year: 
            if self.quarter > other.quarter:
                return True
        return False
    
    def __lt__(self, other):
        if self.year < other.year:
            return True
        elif self.year == other.year: 
            if self.quarter < other.quarter:
                return True
        return False
