DROP SCHEMA IF EXISTS recursion_ CASCADE;
CREATE SCHEMA recursion_;
SET search_path = recursion_;

-- Create the 'prereq' table to store course prerequisites
CREATE TABLE prereq (
    course_id VARCHAR(8),
    prereq_id VARCHAR(8)
);

-- Insert some example data into the 'prereq' table
INSERT INTO prereq VALUES ('C101', 'C102'), ('C102', 'C103'), ('C104', 'C103');

-- Recursive CTE to find all prerequisites (directly or indirectly) for a given course
WITH RECURSIVE rec_prereq(course_id, prereq_id) AS (
    -- Anchor member: direct prerequisites
    SELECT course_id, prereq_id
    FROM prereq
    UNION
    -- Recursive member: indirect prerequisites
    SELECT rec_prereq.course_id, p.prereq_id
    FROM rec_prereq
    JOIN prereq p ON rec_prereq.prereq_id = p.course_id
)
-- Select all courses and their prerequisites
SELECT *
FROM rec_prereq;

-- Clean up example data
--DELETE FROM prereq;
