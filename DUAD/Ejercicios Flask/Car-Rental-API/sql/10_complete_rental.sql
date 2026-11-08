-- ============================================================
-- Confirms the return of a car, completing its rental.
--
-- Flow:
--   1. Confirm the rental exists and is active.
--   2. Mark the rental as completed and stamp the return date.
--   3. Mark the related car as available again.
--
-- Edit v_rental_id to test different scenarios
-- (non-existent rental, already completed rental, successful return).
-- ============================================================

DO $$
DECLARE
    v_rental_id     INTEGER := 1;
    v_car_id        INTEGER;
    v_rental_status TEXT;
BEGIN
    SELECT car_id, status INTO v_car_id, v_rental_status
    FROM lyfter_car_rental.rentals
    WHERE id = v_rental_id;

    IF v_car_id IS NULL THEN
        RAISE EXCEPTION 'Rental % does not exist', v_rental_id;
    ELSIF v_rental_status <> 'active' THEN
        RAISE EXCEPTION 'Rental % is not active (current status: %)', v_rental_id, v_rental_status;
    END IF;

    UPDATE lyfter_car_rental.rentals
    SET status = 'completed', return_date = NOW()
    WHERE id = v_rental_id;

    UPDATE lyfter_car_rental.cars
    SET status = 'available'
    WHERE id = v_car_id;

    RAISE NOTICE 'Rental % completed. Car % is now available', v_rental_id, v_car_id;
END $$;
