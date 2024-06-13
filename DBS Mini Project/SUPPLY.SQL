SET SERVEROUTPUT ON

DECLARE
    pid varchar (20);
    sid varchar (20);
    p number;
    unit number;
    total_cost number;


BEGIN
    pid:='&productid';
    sid:='&supplierid';
    unit:='&units';
    SELECT price into p from product where product_id=pid;
    total_cost:=p*unit*0.3;
    DBMS_OUTPUT.PUT_LINE('TOTAL COST: '||total_cost);
    UPDATE product set stock=stock+unit where product_id=pid;
END;
/