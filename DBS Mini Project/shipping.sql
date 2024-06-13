CREATE OR REPLACE TRIGGER execute_shipping_info_update
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    EXECUTE IMMEDIATE '
        DECLARE 
            v_shipping_id shipping_info.shipping_id%TYPE;
            v_order_id orders.order_id%TYPE;
            v_products shipping_info.products%TYPE;
            v_address customer.address%TYPE;
            v_shipping_date DATE := SYSDATE; -- Set v_shipping_date to the current system date
            v_delivery_date DATE;

        BEGIN
            SELECT COUNT(*) + 1 INTO v_shipping_id FROM shipping_info;
            SELECT MAX(order_id) INTO v_order_id FROM orders;
            SELECT products INTO v_products FROM orders WHERE order_id = v_order_id;
            SELECT address INTO v_address FROM customer WHERE customer_id = (SELECT customer_id FROM orders WHERE order_id = v_order_id);

            -- Insert into shipping_info table
            INSERT INTO shipping_info (shipping_id, products, shipping_address, shipping_date, delivery_date)
            VALUES (v_shipping_id, v_products, v_address, v_shipping_date, v_shipping_date + 7);

            COMMIT;
            DBMS_OUTPUT.PUT_LINE(''Shipping information inserted successfully.'');
        EXCEPTION
            WHEN OTHERS THEN
                ROLLBACK;
                DBMS_OUTPUT.PUT_LINE(''Error inserting shipping information: '' || SQLERRM);
        END;';
END;
/
