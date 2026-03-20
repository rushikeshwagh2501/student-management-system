from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Student:
    id: int
    name: str
    age: int
    major: str

@dataclass
class Course:
    id: int
    name: str
    instructor: str
    credits: int

@dataclass
class Enrollment:
    student_id: int
    course_id: int
    grade: Optional[str] = None

class StudentManagementSystem:
    def __init__(self):
        self.students: Dict[int, Student] = {}
        self.courses: Dict[int, Course] = {}
        self.enrollments: List[Enrollment] = []

    # Student operations
    def add_student(self, student: Student):
        if student.id in self.students:
            raise ValueError(f"Student with ID {student.id} already exists")
        self.students[student.id] = student

    def get_student(self, student_id: int) -> Student:
        return self.students[student_id]

    def update_student(self, student_id: int, **kwargs):
        if student_id not in self.students:
            raise KeyError(f"Student {student_id} not found")
        for key, value in kwargs.items():
            if hasattr(self.students[student_id], key):
                setattr(self.students[student_id], key, value)

    def delete_student(self, student_id: int):
        self.students.pop(student_id, None)
        self.enrollments = [e for e in self.enrollments if e.student_id != student_id]

    # Course operations
    def add_course(self, course: Course):
        if course.id in self.courses:
            raise ValueError(f"Course with ID {course.id} already exists")
        self.courses[course.id] = course

    def get_course(self, course_id: int) -> Course:
        return self.courses[course_id]

    def update_course(self, course_id: int, **kwargs):
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found")
        for key, value in kwargs.items():
            if hasattr(self.courses[course_id], key):
                setattr(self.courses[course_id], key, value)

    def delete_course(self, course_id: int):
        self.courses.pop(course_id, None)
        self.enrollments = [e for e in self.enrollments if e.course_id != course_id]

    # Enrollment operations
    def enroll(self, student_id: int, course_id: int):
        if student_id not in self.students:
            raise KeyError(f"Student {student_id} not found")
        if course_id not in self.courses:
            raise KeyError(f"Course {course_id} not found")
        if any(e.student_id == student_id and e.course_id == course_id for e in self.enrollments):
            raise ValueError("Already enrolled")

        self.enrollments.append(Enrollment(student_id=student_id, course_id=course_id))

    def assign_grade(self, student_id: int, course_id: int, grade: str):
        for e in self.enrollments:
            if e.student_id == student_id and e.course_id == course_id:
                e.grade = grade
                return
        raise KeyError("Enrollment not found")

    def get_student_enrollments(self, student_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.student_id == student_id]

    def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        return [e for e in self.enrollments if e.course_id == course_id]


def print_menu():
    print("\nStudent Management System")
    print("1. Add Student")
    print("2. Add Course")
    print("3. Enroll Student")
    print("4. Assign Grade")
    print("5. List Students")
    print("6. List Courses")
    print("7. List Enrollments")
    print("8. Exit")


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    sms = StudentManagementSystem()
    while True:
        print_menu()
        choice = input_int("Choose an option (1-8): ")

        if choice == 1:
            student_id = input_int("Student ID: ")
            name = input("Name: ")
            age = input_int("Age: ")
            major = input("Major: ")
            try:
                sms.add_student(Student(id=student_id, name=name, age=age, major=major))
                print("Student added successfully.")
            except ValueError as err:
                print(err)

        elif choice == 2:
            course_id = input_int("Course ID: ")
            name = input("Name: ")
            instructor = input("Instructor: ")
            credits = input_int("Credits: ")
            try:
                sms.add_course(Course(id=course_id, name=name, instructor=instructor, credits=credits))
                print("Course added successfully.")
            except ValueError as err:
                print(err)

        elif choice == 3:
            student_id = input_int("Student ID: ")
            course_id = input_int("Course ID: ")
            try:
                sms.enroll(student_id, course_id)
                print("Enrollment successful.")
            except KeyError as err:
                print(err)
            except ValueError as err:
                print(err)

        elif choice == 4:
            student_id = input_int("Student ID: ")
            course_id = input_int("Course ID: ")
            grade = input("Grade: ")
            try:
                sms.assign_grade(student_id, course_id, grade)
                print("Grade assigned.")
            except KeyError as err:
                print(err)

        elif choice == 5:
            if not sms.students:
                print("No students.")
            else:
                for s in sms.students.values():
                    print(s)

        elif choice == 6:
            if not sms.courses:
                print("No courses.")
            else:
                for c in sms.courses.values():
                    print(c)

        elif choice == 7:
            if not sms.enrollments:
                print("No enrollments.")
            else:
                for e in sms.enrollments:
                    student = sms.students.get(e.student_id)
                    course = sms.courses.get(e.course_id)
                    print(f"Student {student.name if student else e.student_id} -> Course {course.name if course else e.course_id}, grade={e.grade}")

        elif choice == 8:
            print("Exiting.")
            break

        else:
            print("Invalid choice.")
