# 0.9 (11-20-2016)
- Unified ChartBuilder and ChartViewer
- Made new, custom header bar
- Prompts for confirmation when trying to delete a course
- Copy/Paste functionality for courses
- Eliminated UI Builder dependence

# 0.8 (10-22-2016)
- Made editing a course more efficient
- Columns now bear a completed CSS class, and all courses determine their color based on it
- Implemented Drag and Drop
- More dynamic interface
  - Quarters can now be hidden by right clicking them
  - Right clicking the year will allow you to toggle quarter visibility

# 0.7.1 (10-16-2016)
- Fixed bug where attempting to delete GE entry failed

# 0.7 (10-15-2016)
- Set up mechanism to determine which courses have been completed
- Set up better handling of the config file
- Colored GE indicators, prereqs, and completed courses
- Made GEs editable in preferences
- Added a "New" button

# 0.6 (10-6-2016)
- PyFlowChart now makes a config directory, which stores
  configs and charts
- Fixed bug where pressing cancel when saving for the
  first time still attempts to save
- GE list, writing in credit, and saving user year now implemented

# 0.5 (9-25-2016)
- Fixed bug when trying to open files other than JSON files

# 0.4 (9-8-2016) 
- Set better sizing for tile widgets
- Added a new GE type field
- Added course type minor

# 0.3 (9-6-2016)
- Fixed bug where prereq add button does not work after making edits in ChartBuilder
- `clean_form` function in CourseChanger now properly resets forms
- Added About dialog 

# 0.2 (9-2-2016)
- Added editing support
- IDs added for each course
- Can now dynamically create prereq fields
- JSON info format checking 
 
