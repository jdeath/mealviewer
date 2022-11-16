# mealviewer for Homeassistant

Place mealviewer/ directory inside /config/custom_components/

In your /config/configuration.yaml add a block under sensors:

```
- platform: mealviewer
  accounts:
    - 'SchoolName'
    - 'SchoolName2'
```      
      
SchoolName is the name in the Mealviewer URL: https://schools.mealviewer.com/school/HookstadtHighSchool , school name is HookstadtHighSchool

This will create a sensor called sensor.mealviewever_hookstadthighschool with attributes of lunch0, lunch1, lunch2, lunch3, lunch4 which are the lunches of today - five days from now.
Multiple schools should work, but not tested.

This code works for me, but may need to be changed if your school offers breakfast.

I am using a markdown card to display the first 3 entries.

```
type: markdown
content: |-
  {{ states.sensor.mealviewer_hookstadthighschool.attributes.lunch0 }}
  {{ states.sensor.mealviewer_hookstadthighschool.attributes.lunch1 }}
  {{ states.sensor.mealviewer_hookstadthighschool.attributes.lunch2 }}
title: School Lunch

```
Let me know if have any suggestions. Right now I leave the entry blank if no information. Each school gets upated once every 12 hours. 
