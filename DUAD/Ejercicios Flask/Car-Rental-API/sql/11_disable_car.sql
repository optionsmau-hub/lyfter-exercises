-- Disables a car so it can no longer be rented.
-- Edit v_car_id to test different scenarios.

DO $$
DECLARE
    v_car_id INTEGER := 1;
BEGIN
    UPDATE lyfter_car_rental.cars
    SET status = 'disabled'
    WHERE id = v_car_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Car % does not exist', v_car_id;
    END IF;

    RAISE NOTICE 'Car % disabled', v_car_id;
END $$;
