DROP SCHEMA IF EXISTS loop_ CASCADE;
CREATE SCHEMA loop_;
SET search_path = loop_;

-- Create prerequisite table 
CREATE TABLE prereq (
    course_id varchar(8),
    prereq_id varchar(8),
    PRIMARY KEY (course_id, prereq_id)
);
 
-- Insert sample data 
INSERT INTO prereq VALUES 
('C101', 'C102'), ('C102', 'C103'), ('C104', 'C103');
 
-- Function to find all prerequisites (directly or indirectly) for a given course
CREATE OR REPLACE FUNCTION findAllPrereqs(p_cid VARCHAR(8))
RETURNS TABLE (prereq_course_id VARCHAR(8)) AS $$
DECLARE
  -- Variable to store the count of rows inserted in the last iteration
  rows_inserted INTEGER;
BEGIN
  -- Create a temporary table to store the set of courses to be returned
  CREATE TEMPORARY TABLE c_prereq (prereq_course_id VARCHAR(8));

  -- Create a temporary table to store courses found in the previous iteration
  CREATE TEMPORARY TABLE new_c_prereq (prereq_course_id VARCHAR(8));

  -- Create a temporary table to store intermediate results
  CREATE TEMPORARY TABLE temp (prereq_course_id VARCHAR(8));

  -- Insert the direct prerequisites of the given course into new_c_prereq
  INSERT INTO new_c_prereq (prereq_course_id)
  SELECT p.prereq_id
  FROM prereq p
  WHERE p.course_id = p_cid;

  -- Loop to find indirect prerequisites
  LOOP
    -- Insert the courses found in the previous iteration into c_prereq
    INSERT INTO c_prereq (prereq_course_id)
    SELECT ncp.prereq_course_id
    FROM new_c_prereq ncp;

    -- Find the next level of prerequisites and store them in temp
    INSERT INTO temp (prereq_course_id)
    SELECT p.prereq_id
    FROM new_c_prereq ncp, prereq p
    WHERE ncp.prereq_course_id = p.course_id
    EXCEPT
    SELECT cp.prereq_course_id
    FROM c_prereq cp;

    -- Check if any new prerequisites were found
    GET DIAGNOSTICS rows_inserted = ROW_COUNT;

    -- If no new prerequisites were found, exit the loop
    IF rows_inserted = 0 THEN
      EXIT;
    END IF;

    -- Move the contents of temp to new_c_prereq for the next iteration
    DELETE FROM new_c_prereq;
    INSERT INTO new_c_prereq (prereq_course_id)
    SELECT t.prereq_course_id
    FROM temp t;

    -- Clear the temp table for the next iteration
    DELETE FROM temp;
  END LOOP;

  -- Return the set of all prerequisites found
  RETURN QUERY
  SELECT cp.prereq_course_id
  FROM c_prereq cp;

  -- Clean up temporary tables
  DROP TABLE c_prereq;
  DROP TABLE new_c_prereq;
  DROP TABLE temp;
END;
$$ LANGUAGE plpgsql;

-- Example usage
-- Assuming the 'prereq' table is already defined with columns 'course_id' and 'prereq_id'
-- Example data for 'prereq' table
-- INSERT INTO prereq VALUES ('C101', 'C102'), ('C102', 'C103'), ('C104', 'C103');

-- Call the function to find all prerequisites for course 'C101'
SELECT * FROM findAllPrereqs('C101');
