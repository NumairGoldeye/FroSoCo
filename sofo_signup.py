"""Places students in SoFos based on their input into a form.
The data should be in a csv file.  The first line will be column names,
and all other lines will be formatted as follows:
timestamp,name,max_seminars,first_choice,...sixth_choice,email."""

import csv
import random

"""File columns as follows:
Timestamp, Name, NumberSeminars, FirstChoice,...SixthChoice.
"""
data_filename = 'data.csv'
seminar_names = [
  'The FroSoCo Mural [Sat 10:00am - 11:00am]',
  'Web Development [Mon 7:00pm - 8:00pm]',
  'Calligraphy [Sun 4:00pm - 5:00pm]',
  'Rocket Science [Thurs 6:30pm - 8:30pm]',
  'Yaoi to Yuri [Thurs 7:30pm - 9:30pm]',
  'J.R.R. Tolkien [Tues 7:00pm - 9:00pm]',
  ]

def main():
  unfinished_students = getStudentData(data_filename)
  finished_students = []
  num_rounds = 0
  while unfinished_students:
  	num_rounds += 1
  	print "Round ", num_rounds
  	performEnrollmentRound(unfinished_students, finished_students)
  	print
  printResults(finished_students, seminars) 

def printResults(students, seminars):
  print 'Students:'
  for student in students:
    printStudent(student)
    print
  print '____________'
  print 'Classes:'
  for seminar in seminars:
  	print seminar.name, '[%d enrolled]' % len(seminar.currently_enrolled)
  	for student in seminar.currently_enrolled:
  		print student.name, ' (%s)' % student.email
  	print
 
def printStudent(student):
  print student.name, ' (%s)' % student.email
  for s in student.enrolled:
  	print s.name

def performEnrollmentRound(unfinished_students, finished_students):
  random.shuffle(unfinished_students)  # Random ordering for the round
  for student in unfinished_students: # Make deep copy so the body doesn't affect the loop
    performEnrollment(student)
    if student.isFinished():
      unfinished_students.remove(student)
      finished_students.append(student)

def performEnrollment(student):
  for choice in list(student.choices):
    student.choices = student.choices[1:]  # Remove the first from the list 
    if choice.hasSpacesLeft():
      student.enroll(choice)
      choice.enroll(student)
      return  # Stop when we get to one a valid choice

# Gets the information from the file a list of students.
def getStudentData(filename):
  result = []
  with open(filename, 'rb') as signup_file:
    reader = csv.reader(signup_file)
    reader.next() # Skip title row
    for row in reader:
    	result.append(parseRow(row))
  return result

def parseRow(row):
  student_name = row[1]
  numSeminars = int(row[2])
  choice_names = removeEmpty(row[3:-1])
  choices = [seminar_names_to_objects[choice_name] for choice_name in choice_names]
  email = row[-1]
  # print 'New student:', student_name, 'Max Courses', numSeminars, 'Choices', choice_names
  return Student(student_name, choices, max_seminars=numSeminars, email=email)

def removeEmpty(choices):
  result = []
  for item in choices:
    if item:
    	result.append(item)
  return result


class Seminar:
  def __init__(self, name=None, course_id=None, max_students=12):
    self.name = name
    self.course_id = course_id
    self.max_students = max_students
    self.currently_enrolled = set([])

  def enroll(self, student_name):
    if not self.hasSpacesLeft():
      raise TooManyStudentsError
    self.currently_enrolled.add(student_name)
  
  def numSpacesLeft(self):
    return self.max_students - len(self.currently_enrolled)
    
  def hasSpacesLeft(self):
    return self.numSpacesLeft() > 0

  def __str__(self):
    return 'name:%s, course_id:%s, max_students%s, currently_enrolled:%s' % (
      self.name, self.course_id, self.max_students, self.currently_enrolled)

class Student:
  def __init__(self, name, choices, max_seminars=1, email=None):
    self.name = name
    self.max_seminars = max_seminars
    self.enrolled = set([])
    self.choices = choices
    self.email = email

  def enroll(self, course):
    print 'enrolling', self.name, 'in', course.name
    if not self.hasSlotsLeft():
    	raise TooManyClassesError('Student %s is already in %d classes; max is %d' % 
    	  (self.name, len(self.enrolled), self.max_seminars))
    self.enrolled.add(course)

  def hasSlotsLeft(self):
    return self.max_seminars > len(self.enrolled)

  def isFinished(self):
    """Returns true if the student is finished enrolling.

    This can be accomplished if either (1) The student is in his or her maximum
    number of classes or (2) all of the students remaining choices are full or
    (3) there are no more choices left.
    """
    if not self.hasSlotsLeft():
    	return True
    if not self.choices:
    	return True
    for choice in self.choices:
    	if choice.hasSpacesLeft:
    		return False
    return True

  def __str__(self):
    return self.name

class TooManyStudentsError(Exception):
  pass

class TooManyClassesError(Exception):
  pass

# Need to do this instead of just a loop because not all seminars
# are guaranteed to have the same max_students
seminars = [
  Seminar(name=seminar_names[0], course_id=0),
  Seminar(name=seminar_names[1], course_id=1),
  Seminar(name=seminar_names[2], course_id=2),
  Seminar(name=seminar_names[3], course_id=3),
  Seminar(name=seminar_names[4], course_id=4),
  Seminar(name=seminar_names[5], course_id=5),
]

seminar_names_to_objects = {
  seminar_names[0]: seminars[0],
  seminar_names[1]: seminars[1],
  seminar_names[2]: seminars[2],
  seminar_names[3]: seminars[3],
  seminar_names[4]: seminars[4],
  seminar_names[5]: seminars[5],
}

if __name__ == '__main__':
	main()
