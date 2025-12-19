DROP SCHEMA IF EXISTS plsql CASCADE;
CREATE SCHEMA plsql;
SET search_path = plsql;

-- Drop existing tables
DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS classroom;
DROP TABLE IF EXISTS section;

-- Create the takes table to store student course enrollment information
CREATE TABLE takes (
    id VARCHAR(5) NOT NULL,          -- Student ID
    course_id VARCHAR(8) NOT NULL,   -- Course ID
    sec_id VARCHAR(8) NOT NULL,      -- Section ID
    semester VARCHAR(6) NOT NULL,    -- Semester
    year NUMERIC(4,0) NOT NULL,      -- Year
    grade VARCHAR(2)                 -- Grade
);

-- Create the classroom table to store classroom information
CREATE TABLE classroom (
    building VARCHAR(50),            -- Building
    room_number VARCHAR(7) NOT NULL, -- Room number
    capacity NUMERIC(4,0) NOT NULL   -- Capacity
);

-- Create the section table to store course section information
CREATE TABLE section (
    course_id VARCHAR(8) NOT NULL,   -- Course ID
    sec_id VARCHAR(8) NOT NULL,      -- Section ID
    semester VARCHAR(6) NOT NULL,    -- Semester
    year NUMERIC(4,0) NOT NULL,      -- Year
    building VARCHAR(50),            -- Building
    room_number VARCHAR(7),          -- Room number
    time_slot_id VARCHAR(4)          -- Time slot ID
);

--------------------------------------------------------

-- Insert data into the classroom table
INSERT INTO classroom (building, room_number, capacity) VALUES
('Main Hall', '101', 8),
('Main Hall', '102', 25),
('Science Building', '201', 35);

-- Insert data into the section table
INSERT INTO section (course_id, sec_id, semester, year, building, room_number, time_slot_id) VALUES
('CS101', '1', 'Spring', 2023, 'Main Hall', '101', 'A'),
('CS102', '1', 'Spring', 2023, 'Main Hall', '102', 'B'),
('CS103', '1', 'Spring', 2023, 'Science Building', '201', 'C');

-- Insert data into the takes table
INSERT INTO takes (id, course_id, sec_id, semester, year, grade) VALUES
('S0001', 'CS101', '1', 'Spring', 2023, 'A'),
('S0002', 'CS101', '1', 'Spring', 2023, 'B'),
('S0003', 'CS101', '1', 'Spring', 2023, 'C');

--------------------------------------------------------

-- Create the registerMultipleStudents function
CREATE OR REPLACE FUNCTION registerMultipleStudents(
    IN student_list VARCHAR(5)[],  -- List of student IDs
    IN s_courseid VARCHAR(8),
    IN s_secid VARCHAR(8),
    IN s_semester VARCHAR(6),
    IN s_year NUMERIC(4,0),
    OUT result INT,                -- Registration result
    OUT errorMsg VARCHAR(100)      -- Error message
) AS $$
DECLARE
    currEnrol INT;
    limit_ INT;
    student_id VARCHAR(5);
BEGIN
    -- Initialize result and error message
    result := 0;
    errorMsg := '';

    -- Get the current number of enrolled students
    SELECT COUNT(*)
    INTO currEnrol
    FROM takes
    WHERE course_id = s_courseid
      AND sec_id = s_secid
      AND semester = s_semester
      AND year = s_year;

    -- Get the maximum capacity of the course section
    SELECT capacity
    INTO limit_
    FROM classroom
    NATURAL JOIN section
    WHERE course_id = s_courseid
      AND sec_id = s_secid
      AND semester = s_semester
      AND year = s_year;

    -- Loop through the list of students and attempt to enroll each one
    FOREACH student_id IN ARRAY student_list LOOP
        IF currEnrol < limit_ THEN
            -- Insert the student into the takes table
            INSERT INTO takes (id, course_id, sec_id, semester, year, grade)
            VALUES (student_id, s_courseid, s_secid, s_semester, s_year, NULL);
            -- Update the current number of enrolled students
            currEnrol := currEnrol + 1;
        ELSE
            -- Set the error message if the capacity limit is reached
            errorMsg := 'Enrollment limit reached for course ' || s_courseid || ' section ' || s_secid;
            -- Set the result to failure
            result := -1;
            -- Exit the loop
            EXIT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------

-- Call the registerMultipleStudents function to attempt to enroll multiple students in a course
DO $$
DECLARE
    result INT;
    msg VARCHAR(100);
BEGIN
    SELECT * INTO result, msg FROM registerMultipleStudents(ARRAY['S0004', 'S0005', 'S0006'], 'CS101', '1', 'Spring', 2023);
    IF result = 0 THEN
        RAISE NOTICE 'Registration successful for all students';
    ELSE
        RAISE NOTICE 'Registration failed: %', msg;
    END IF;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------------------------

-- View the data in the takes table
SELECT * FROM takes;

-------------------------------------------------------------------

-- Call the registerMultipleStudents function to attempt to enroll more students in the course
DO $$
DECLARE
    result INT;
    msg VARCHAR(100);
BEGIN
    SELECT * INTO result, msg FROM registerMultipleStudents(ARRAY['S0007', 'S0008', 'S0009', 'S0010'], 'CS101', '1', 'Spring', 2023);
    IF result = 0 THEN
        RAISE NOTICE 'Registration successful for all students';
    ELSE
        RAISE NOTICE 'Registration failed: %', msg;
    END IF;
END;
$$ LANGUAGE plpgsql;
