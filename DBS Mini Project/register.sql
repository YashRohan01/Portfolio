CREATE OR REPLACE PROCEDURE register_customer (
    p_username IN VARCHAR2,
    p_password IN VARCHAR2,
    p_contact IN VARCHAR2,
    p_address IN VARCHAR2
)
IS
    v_cid customer.customer_id%TYPE;
BEGIN
    -- Get the next customer ID
    SELECT NVL(MAX(customer_id), 0) + 1 INTO v_cid FROM customer;

    -- Insert the new customer into the database
    INSERT INTO customer (customer_id, name, password, contact, address)
    VALUES (v_cid, p_username, p_password, p_contact, p_address);

    COMMIT;
    DBMS_OUTPUT.PUT_LINE('Customer registered successfully!');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END;
/
