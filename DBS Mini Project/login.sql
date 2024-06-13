CREATE OR REPLACE PROCEDURE check_login(
    p_username IN VARCHAR2,
    p_contact IN VARCHAR2,
    p_password IN VARCHAR2
) AS
    v_count NUMBER;
BEGIN
    -- Check if the username, contact, and password match
    SELECT COUNT(*) INTO v_count
    FROM customer
    WHERE username = p_username
    AND contact = p_contact
    AND password = p_password;

    -- If the count is greater than 0, login is successful
    IF v_count > 0 THEN
        dbms_output.put_line('Login successful.');
    ELSE
        dbms_output.put_line('Login failed. Invalid username, contact, or password.');
    END IF;
END ;
/
