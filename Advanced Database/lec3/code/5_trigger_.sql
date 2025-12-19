-- 创建模式和表
DROP SCHEMA IF EXISTS trigger_ CASCADE;
CREATE SCHEMA trigger_;
SET search_path = trigger_;
-- Create tables for demonstration
CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    tot_cred INT DEFAULT 0
);

CREATE TABLE course (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT
);

CREATE TABLE takes (
    student_id INT,
    course_id INT,
    grade CHAR(1),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

-- Insert some sample data
INSERT INTO student (id, name) VALUES (1, 'Alice'), (2, 'Bob');
INSERT INTO course (course_id, course_name, credits) VALUES (101, 'Math', 3), (102, 'Science', 4);
INSERT INTO takes (student_id, course_id, grade) VALUES (1, 101, 'A'), (2, 102, 'F');

-- Create a BEFORE trigger to convert blank grades to null
CREATE OR REPLACE FUNCTION set_null_grade()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.grade = ' ' THEN
        NEW.grade := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER setnull_trigger
BEFORE UPDATE OF grade ON takes
FOR EACH ROW
EXECUTE FUNCTION set_null_grade();

-- Create an AFTER trigger to update student credits earned
CREATE OR REPLACE FUNCTION update_credits_earned()
RETURNS TRIGGER AS $$
DECLARE
    credits INT;
BEGIN
    IF NEW.grade <> 'F' AND NEW.grade IS NOT NULL
       AND (OLD.grade = 'F' OR OLD.grade IS NULL) THEN
        SELECT course.credits INTO credits
        FROM course
        WHERE course.course_id = NEW.course_id;

        UPDATE student
        SET tot_cred = tot_cred + credits
        WHERE student.id = NEW.student_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER credits_earned
AFTER UPDATE OF grade ON takes
FOR EACH ROW
EXECUTE FUNCTION update_credits_earned();

-- Example of a statement-level trigger to handle multiple rows
CREATE OR REPLACE FUNCTION update_credits_for_multiple_rows()
RETURNS TRIGGER AS $$
DECLARE
    r RECORD;
    credits INT;
BEGIN
    FOR r IN SELECT student_id, course_id FROM new_table LOOP
        SELECT course.credits INTO credits
        FROM course
        WHERE course.course_id = r.course_id;

        UPDATE student
        SET tot_cred = tot_cred + credits
        WHERE student.id = r.student_id;
    END LOOP;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER credits_earned_multiple
AFTER UPDATE ON takes
REFERENCING NEW TABLE AS new_table
FOR EACH STATEMENT
EXECUTE FUNCTION update_credits_for_multiple_rows();

-- Test the triggers
-- Update a grade to trigger the setnull_trigger
UPDATE takes SET grade = ' ' WHERE student_id = 1 AND course_id = 101;

-- Update a grade to trigger the credits_earned trigger
UPDATE takes SET grade = 'B' WHERE student_id = 2 AND course_id = 102;

-- Update multiple grades to trigger the credits_earned_multiple trigger
UPDATE takes SET grade = 'C' WHERE student_id IN (1, 2) AND course_id IN (101, 102);

-- Check the results
SELECT * FROM student;
SELECT * FROM takes;
