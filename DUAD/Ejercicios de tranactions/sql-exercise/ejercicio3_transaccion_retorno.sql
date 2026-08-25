-- ============================================================
-- Exercise 3: Product Return Transaction
--
-- Flow:
--   1. Verify that the bill exists in the database.
--   2. Increase each product's stock by the quantity that was
--      recorded on the original purchase.
--   3. Update the original bill, marking it with state 'Returned'.
--
-- Edit v_bill_id to test different scenarios
-- (non-existent bill, already-returned bill, successful return, etc).
-- ============================================================

DO $$
DECLARE
    v_bill_id INTEGER := 1;   -- Bill to return
    rec       RECORD;
BEGIN
    -- 1. Verify the bill exists
    IF NOT EXISTS (SELECT 1 FROM Bills WHERE ID = v_bill_id) THEN
        RAISE EXCEPTION 'Bill % does not exist', v_bill_id;
    END IF;

    -- Prevent returning the same bill twice
    IF EXISTS (SELECT 1 FROM Bills WHERE ID = v_bill_id AND State = 'Returned') THEN
        RAISE EXCEPTION 'Bill % has already been returned', v_bill_id;
    END IF;

    -- 2. Restore the stock of every product on the bill
    FOR rec IN
        SELECT ProductID, Quantity FROM BillDetails WHERE BillID = v_bill_id
    LOOP
        UPDATE Products SET Stock = Stock + rec.Quantity WHERE ID = rec.ProductID;
    END LOOP;

    -- 3. Mark the original bill as 'Returned'
    UPDATE Bills SET State = 'Returned' WHERE ID = v_bill_id;

    RAISE NOTICE 'Bill % marked as returned and stock restored', v_bill_id;
END $$;
