CREATE OR REPLACE FUNCTION factorial(n INT)
RETURNS INT AS $$
BEGIN
    -- Base case: if n is 0 or 1, return 1
    IF n <= 1 THEN
        RETURN 1;
    ELSE
        -- Recursive case: n * factorial(n - 1)
        RETURN n * factorial(n - 1);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Example usage
SELECT factorial(5);  -- Output: 120
