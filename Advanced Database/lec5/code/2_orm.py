from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# Create an engine that stores data in a PostgreSQL database
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual PostgreSQL credentials
engine = create_engine('postgresql://postgres:1@localhost:5432/lec5')

# Create all tables in the engine (this will create the 'people' table if it doesn't exist)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new Person object
new_person = Person(ID='P001', name='Alice', address='123 Main St')

# Add the new Person to the session and commit it to the database
session.add(new_person)
session.commit()

# Query the database and print the result
person = session.query(Person).filter_by(ID='P001').first()
print(person)  # Output: <Person(ID='P001', name='Alice', address='123 Main St')>

# Update the person's address
person.address = '456 Elm St'
session.commit()

# Query again to see the updated result
person = session.query(Person).filter_by(ID='P001').first()
print(person)  # Output: <Person(ID='P001', name='Alice', address='456 Elm St')>

# Delete the person
session.delete(person)
session.commit()

# Close the session
session.close()
