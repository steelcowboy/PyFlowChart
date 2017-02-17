# PyFlowChart v0.9.2

PyFlowChart is a project to help students plan out courses 
for their college career. It is currently beta quality 
and under heavy development.

## Features
- A ChartBuilder with a minimalistic interface for building flowcharts
- A ChartViewer that can open flowcharts and includes the same 
  functionality as ChartBuilder
- ChartViewer color codes the courses based on type
- Ability to keep track of what GE requirements each course fulfills

## Version 1.0 Milestones
- ~~Add IDs to each course~~ 9/2/2016
- ~~About dialog~~ 9/6/2016
- ~~Better widget sizing~~ 9/8/2016
- ~~Check validity of JSON files (currently freezes program)~~ 9/25/2016
- ~~Show remaining GEs~~ 10/6/2016
- ~~Preferences~~ 10/6/2016 
- ~~Show interface with completed GEs and allow user to write-in~~ 10/6/2016
- ~~Drag and drop in the viewer~~ 10/21/2016 
- ~~More dynamic interface~~ *Can now show and hide quarters* 10/21/2016
  - Allow adding special quarters (AP, Q+)
- ~~Combine chartbuilder and chartviewer~~ 10/31/2016
- ~~Allow copy/pasting of courses~~ 9/11/2016
- ~~Deal with case where user adds a course before its prereqs have been fulfilled~~ 1/2/2017
- ~~Add support for multiple GE categories~~ 2/12/2017
- ~~Add Notes section for courses~~ 2/15/2017
- Develop a mechanism to show how many units are in each quarter
- Add some help pages 
- Package PyFlowChart for all three major operating systems, including multiple Linux distributions

## Version 2.0 Milestones
- Make this a Kivy Application
  - ~~Drag and Drop in viewer~~ *Successfully implemented in Gtk*
- Client-server architecture for CourseManager
- Allow for transferring data between instances
- Be able to compare two flowcharts
- Import flowcharts from repository
- Undo functionality
