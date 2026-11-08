-- Changes the status of a car.
-- Edit v_car_id and v_new_status to test different scenarios.

DO $$
DECLARE
    v_car_id     INTEGER := 1;
    v_new_status TEXT := 'maintenance';
BEGIN
    IF v_new_status NOT IN ('available', 'rented', 'disabled', 'maintenance') THEN
        RAISE EXCEPTION 'Invalid status: %', v_new_status;
    END IF;

    UPDATE lyfter_car_rental.cars
    SET status = v_new_status
    WHERE id = v_car_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Car % does not exist', v_car_id;
    END IF;

    RAISE NOTICE 'Car % status updated to %', v_car_id, v_new_status;
END $$;
