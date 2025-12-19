/* ------------------------------------------------------------------
   0.  Set-up
-------------------------------------------------------------------*/
DROP SCHEMA IF EXISTS func CASCADE;
CREATE SCHEMA func;
SET search_path = func;

/* two base tables used in the examples */
CREATE TABLE department (
    dept_name VARCHAR(20) PRIMARY KEY,
    budget    NUMERIC(12,2) NOT NULL
);

CREATE TABLE instructor (
    id        VARCHAR(5)  PRIMARY KEY,
    name      VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20) REFERENCES department,
    salary    NUMERIC(8,2) NOT NULL
);

/* tiny sample so that “> 12” can still return something */
INSERT INTO department VALUES
  ('Physics', 1000000),
  ('Music',   500000),
  ('CS',      2000000);

INSERT INTO instructor(id, name, dept_name, salary)
SELECT
  'I'||lpad(seq::text,3,'0'),
  'Prof-'||seq,
  CASE WHEN seq%14=0 THEN 'Physics'
       WHEN seq%5=0  THEN 'Music'
       ELSE 'CS' END,
  70000+random()*50000
FROM generate_series(1,40) seq;   -- 40 rows: CS=24, Physics=3, Music=13

/* ------------------------------------------------------------------
   1.  Scalar function  dept_count  (original example)
-------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION dept_count(p_dept_name VARCHAR(20))
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    d_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO d_count
    FROM instructor
    WHERE instructor.dept_name = p_dept_name;
    RETURN d_count;
END;
$$;

/* usage */
SELECT dept_name, budget
FROM department
WHERE dept_count(dept_name) > 2;   -- returns CS and Music

/* ------------------------------------------------------------------
   2.  Table function  instructor_of  (returns a setof rows)
-------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION instructor_of(p_dept_name VARCHAR(20))
RETURNS TABLE (
    id        VARCHAR(5),
    name      VARCHAR(20),
    dept_name VARCHAR(20),
    salary    NUMERIC(8,2)
)
LANGUAGE sql
AS $$
    SELECT id, name, dept_name, salary
    FROM instructor
    WHERE instructor.dept_name = p_dept_name;
$$;

/* usage */
SELECT *
FROM instructor_of('Music');        -- 13 rows

/* ------------------------------------------------------------------
   3.  Stored procedure  dept_count_proc  (IN / OUT parameters)
-------------------------------------------------------------------*/
CREATE OR REPLACE PROCEDURE dept_count_proc(
    IN  p_dept_name VARCHAR(20),
    OUT p_d_count   INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT COUNT(*) INTO p_d_count
    FROM instructor
    WHERE instructor.dept_name = p_dept_name;
END;
$$;

/* invocation from PL/pgSQL block (anonymous code) */
DO $$
DECLARE
    v_count INTEGER;
BEGIN
    CALL dept_count_proc('Physics', v_count);
    RAISE NOTICE 'Physics has % instructors', v_count;
END;
$$;

/* ------------------------------------------------------------------
   4.  Dynamic-SQL demo  (build & run any statement at run time)
-------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION dynamic_instructor_cnt(
    p_dept_name VARCHAR(20)
)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_sql  TEXT;
    v_cnt  INTEGER;
BEGIN
    v_sql := format(
        'SELECT COUNT(*) FROM instructor WHERE dept_name = %L',
        p_dept_name);
    EXECUTE v_sql INTO v_cnt;
    RETURN v_cnt;
END;
$$;

/* quick test */
SELECT dynamic_instructor_cnt('CS');   -- 24

/* ------------------------------------------------------------------
   5.  Overloading demo  (same name, different arity)
-------------------------------------------------------------------*/
CREATE OR REPLACE FUNCTION add_instructor(
    p_id   VARCHAR(5),
    p_name VARCHAR(20),
    p_dept VARCHAR(20)
)
RETURNS VOID
LANGUAGE sql
AS $$
    INSERT INTO instructor(id, name, dept_name, salary)
    VALUES (p_id, p_name, p_dept, 0);
$$;

CREATE OR REPLACE FUNCTION add_instructor(
    p_id   VARCHAR(5),
    p_name VARCHAR(20),
    p_dept VARCHAR(20),
    p_sal  NUMERIC(8,2)
)
RETURNS VOID
LANGUAGE sql
AS $$
    INSERT INTO instructor(id, name, dept_name, salary)
    VALUES (p_id, p_name, p_dept, p_sal);
$$;

/* both variants coexist */
SELECT add_instructor('I999', 'New-1', 'Music');
SELECT add_instructor('I998', 'New-2', 'CS', 95000);

/* ------------------------------------------------------------------
   6.  Clean-up  (optional)
-------------------------------------------------------------------*/
-- DROP SCHEMA demo_5 CASCADE;

