from datetime import datetime
from collections import defaultdict

class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []
        self._grades = {}  # Dictionary to store grades {enrollment: grade}

    def enroll(self, course):
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
            return enrollment
        else:
            raise TypeError("course must be an instance of Course")

    def get_enrollments(self):
        return self._enrollments.copy()
    
    def add_grade(self, enrollment, grade):
        if enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Enrollment doesn't belong to this student")

    # Aggregate methods
    def course_count(self):
        """Count of all courses the student is enrolled in"""
        return len(self._enrollments)
    
    def aggregate_average_grade(self):
        """Calculate average grade across all courses"""
        if not self._grades:
            return None
        return sum(self._grades.values()) / len(self._grades)
    
    def highest_grade(self):
        """Get the highest grade received"""
        return max(self._grades.values()) if self._grades else None
    
    def courses_by_grade(self):
        """Return dictionary of {course: grade}"""
        return {enrollment.course: grade for enrollment, grade in self._grades.items()}


class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        return self._enrollments.copy()
    
    # Aggregate methods
    def student_count(self):
        """Count of students enrolled in this course"""
        return len(self._enrollments)
    
    def average_grade(self):
        """Calculate average grade for this course"""
        grades = []
        for enrollment in self._enrollments:
            if enrollment in enrollment.student._grades:
                grades.append(enrollment.student._grades[enrollment])
        return sum(grades) / len(grades) if grades else None
    
    def top_student(self):
        """Return student with highest grade in this course"""
        top_enrollment = None
        top_grade = -1
        for enrollment in self._enrollments:
            if enrollment in enrollment.student._grades:
                current_grade = enrollment.student._grades[enrollment]
                if current_grade > top_grade:
                    top_grade = current_grade
                    top_enrollment = enrollment
        return top_enrollment.student if top_enrollment else None


class Enrollment:
    all = []
    
    def __init__(self, student, course):
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        return self._enrollment_date
    
    # Class-level aggregate methods
    @classmethod
    def aggregate_enrollments_per_day(cls):
        """Count enrollments grouped by date"""
        enrollment_count = defaultdict(int)
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] += 1
        return dict(enrollment_count)
    
    @classmethod
    def most_popular_course(cls):
        """Find course with most enrollments"""
        if not cls.all:
            return None
        course_counts = defaultdict(int)
        for enrollment in cls.all:
            course_counts[enrollment.course] += 1
        return max(course_counts.items(), key=lambda x: x[1])[0]