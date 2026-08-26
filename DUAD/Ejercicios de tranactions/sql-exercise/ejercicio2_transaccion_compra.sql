-- ============================================================
-- Exercise 2: Purchase Transaction
--
-- Flow:
--   1. Check that there is enough stock of each product.
--   2. Confirm that the user placing the purchase exists.
--   3. Insert the bill related to the user.
--   4. Reduce each product's stock by the purchased quantity.
--
-- The cart is defined as an array of [ProductID, Quantity] pairs.
-- Edit v_user_id and v_cart to test different scenarios
-- (non-existent user, insufficient stock, successful purchase, etc).
-- ============================================================

DO $$
DECLARE
    v_user_id    INTEGER := 1;
    v_cart       INTEGER[][] := ARRAY[[1, 2], [3, 5], [4, 1]];  -- [ProductID, Quantity]
    v_bill_id    INTEGER;
    v_product_id INTEGER;
    v_quantity   INTEGER;
    v_stock      INTEGER;
    v_price      NUMERIC(10, 2);
    i            INTEGER;
BEGIN
    -- 1. Confirm the user exists
    IF NOT EXISTS (SELECT 1 FROM Users WHERE ID = v_user_id) THEN
        RAISE EXCEPTION 'User % does not exist', v_user_id;
    END IF;

    -- 2. Check there is enough stock for every product in the cart
    FOR i IN 1 .. array_upper(v_cart, 1) LOOP
        v_product_id := v_cart[i][1];
        v_quantity   := v_cart[i][2];

        SELECT Stock INTO v_stock FROM Products WHERE ID = v_product_id;

        IF v_stock IS NULL THEN
            RAISE EXCEPTION 'Product % does not exist', v_product_id;
        END IF;

        IF v_stock < v_quantity THEN
            RAISE EXCEPTION 'Not enough stock for product % (requested %, available %)',
                v_product_id, v_quantity, v_stock;
        END IF;
    END LOOP;

    -- 3. Insert the bill related to the user
    INSERT INTO Bills (UserID, State)
    VALUES (v_user_id, 'Completed')
    RETURNING ID INTO v_bill_id;

    -- 4. Insert each line item and reduce the matching stock
    FOR i IN 1 .. array_upper(v_cart, 1) LOOP
        v_product_id := v_cart[i][1];
        v_quantity   := v_cart[i][2];

        UPDATE Products
        SET Stock = Stock - v_quantity
        WHERE ID = v_product_id
        RETURNING Price INTO v_price;

        INSERT INTO BillDetails (BillID, ProductID, Quantity, UnitPrice)
        VALUES (v_bill_id, v_product_id, v_quantity, v_price);
    END LOOP;

    RAISE NOTICE 'Purchase completed. Bill generated with ID: %', v_bill_id;
END $$;
