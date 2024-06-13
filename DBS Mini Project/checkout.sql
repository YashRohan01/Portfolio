CREATE OR REPLACE PROCEDURE process_checkout(
    p_customer_id IN orders.customer_id%TYPE,
    p_total_cost IN NUMBER,
    p_product_ids_str IN VARCHAR2,
    p_products IN VARCHAR2
)
IS
    l_next_order_id NUMBER;
    l_product_count NUMBER;
BEGIN
    -- Calculate the next order ID
    SELECT COUNT(*) + 1 INTO l_next_order_id FROM orders;
    
    -- Insert the order into the orders table
    INSERT INTO orders (order_id, cost, products, customer_id)
    VALUES (l_next_order_id, p_total_cost, p_products, p_customer_id);
    
    -- Count the number of products
    SELECT COUNT(*) INTO l_product_count FROM dual WHERE p_product_ids_str IS NOT NULL;
    
    -- Decrease the stock of products in the cart by 1
    FOR product_id IN (
        SELECT TRIM(REGEXP_SUBSTR(p_product_ids_str, '[^,]+', 1, LEVEL)) AS product_id 
        FROM DUAL 
        CONNECT BY LEVEL <= l_product_count
    )
    LOOP
        UPDATE product
        SET stock = stock - 1
        WHERE product_id = product_id;
    END LOOP;
    
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END process_checkout;
/
