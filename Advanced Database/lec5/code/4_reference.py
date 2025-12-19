from sqlalchemy import create_engine, Column, String, Integer, ForeignKey,text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

# Define the base class for our models
Base = declarative_base()

# Define the Person class that maps to a PostgreSQL table
class Person(Base):
    __tablename__ = 'people'  # Table name in PostgreSQL

    # Define columns for the table
    ID = Column(String(20), primary_key=True)
    name = Column(String(20))
    address = Column(String(20))

    def __repr__(self):
        return f"<Person(ID='{self.ID}', name='{self.name}', address='{self.address}')>"

# Define the Department class that maps to a PostgreSQL table
class Department(Base):
    __tablename__ = 'departments'  # Table name in PostgreSQL

    # Define columns for the table
    dept_name = Column(String(20), primary_key=True)
    head_id = Column(String(20), ForeignKey('people.ID'))
    head = relationship('Person', backref='departments')

    def __repr__(self):
        return f"<Department(dept_name='{self.dept_name}', head='{self.head}')>"

# Create an engine that stores data in a PostgreSQL database
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual PostgreSQL credentials
engine = create_engine('postgresql://postgres:1@localhost:5432/lec5c')

# # 获取一个连接
# with engine.connect() as conn:
#     # 执行 DROP TABLE 命令，使用 CASCADE 选项
#     conn.execute(text("DROP TABLE IF EXISTS people CASCADE"))
#     conn.execute(text("DROP TABLE IF EXISTS students CASCADE"))
#     conn.execute(text("DROP TABLE IF EXISTS teachers CASCADE"))

# Create all tables in the engine (this will create the 'people' and 'departments' tables if they don't exist)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new Person object
new_person = Person(ID='P001', name='Alice', address='123 Main St')

# Add the new Person to the session and commit it to the database
session.add(new_person)
session.commit()

# Create a new Department object with a valid head
new_department = Department(dept_name='Engineering', head=new_person)

# Add the new Department to the session and commit it to the database
session.add(new_department)
session.commit()

# Attempt to create a Department with an invalid head_id (foreign key violation)
try:
    invalid_department = Department(dept_name='Marketing', head_id='P999')
    session.add(invalid_department)
    session.commit()
except IntegrityError as e:
    print("IntegrityError:", e)
    session.rollback()  # Rollback the transaction

# Attempt to update a Department with an invalid head_id (foreign key violation)
try:
    # new_department.head_id = 'P999'
    new_department.head_id = 'P001'
    session.commit()
except IntegrityError as e:
    print("IntegrityError:", e)
    session.rollback()  # Rollback the transaction

# Clean up: delete the Department and Person
session.delete(new_department)
session.delete(new_person)
session.commit()

# Close the session
session.close()
