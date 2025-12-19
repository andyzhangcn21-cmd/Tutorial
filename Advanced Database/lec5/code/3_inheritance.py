from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship

# Define the base class for our models
Base = declarative_base()

# Define the Person class that maps to a PostgreSQL table
class Person(Base):
    __tablename__ = 'people'  # Table name in PostgreSQL

    # Define columns for the table
    ID = Column(String(20), primary_key=True)
    name = Column(String(20))
    address = Column(String(20))
    type = Column(String(20))  # Discriminator column

    # Define the discriminator for the polymorphic inheritance
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f"<Person(ID='{self.ID}', name='{self.name}', address='{self.address}')>"

# Define the Student class that inherits from Person
class Student(Person):
    __tablename__ = 'students'

    # Define the primary key and foreign key
    ID = Column(String(20), ForeignKey('people.ID'), primary_key=True)
    degree = Column(String(20))

    # Define the discriminator for the polymorphic inheritance
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __repr__(self):
        return f"<Student(ID='{self.ID}', name='{self.name}', address='{self.address}', degree='{self.degree}')>"

# Define the Teacher class that inherits from Person
class Teacher(Person):
    __tablename__ = 'teachers'

    # Define the primary key and foreign key
    ID = Column(String(20), ForeignKey('people.ID'), primary_key=True)
    salary = Column(Integer)

    # Define the discriminator for the polymorphic inheritance
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }

    def __repr__(self):
        return f"<Teacher(ID='{self.ID}', name='{self.name}', address='{self.address}', salary={self.salary})>"

# Create an engine that stores data in a PostgreSQL database
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual PostgreSQL credentials
engine = create_engine('postgresql://postgres:1@localhost:5432/lec5b')
# Drop all tables
Base.metadata.drop_all(engine)

# Create all tables
# Base.metadata.create_all(engine)

# Create all tables in the engine (this will create the 'people', 'students', and 'teachers' tables if they don't exist)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new Student object
new_student = Student(ID='S001', name='Alice', address='123 Main St', degree='Bachelor')

# Create a new Teacher object
new_teacher = Teacher(ID='T001', name='Bob', address='456 Elm St', salary=50000)

# Add the new Student and Teacher to the session and commit them to the database
session.add(new_student)
session.add(new_teacher)
session.commit()

# Query the database and print the results
student = session.query(Student).filter_by(ID='S001').first()
print(student)  # Output: <Student(ID='S001', name='Alice', address='123 Main St', degree='Bachelor')>

teacher = session.query(Teacher).filter_by(ID='T001').first()
print(teacher)  # Output: <Teacher(ID='T001', name='Bob', address='456 Elm St', salary=50000)>

# Update the student's degree
student.degree = 'Master'
session.commit()

# Update the teacher's salary
teacher.salary = 55000
session.commit()

# Query again to see the updated results
student = session.query(Student).filter_by(ID='S001').first()
print(student)  # Output: <Student(ID='S001', name='Alice', address='123 Main St', degree='Master')>

teacher = session.query(Teacher).filter_by(ID='T001').first()
print(teacher)  # Output: <Teacher(ID='T001', name='Bob', address='456 Elm St', salary=55000)>

# Delete the student and teacher
session.delete(student)
session.delete(teacher)
session.commit()

# Close the session
session.close()
