-- ============================================================
-- Creates a new rental for a user and a car.
--
-- Flow:
--   1. Confirm the user exists.
--   2. Confirm the car exists and is available.
--   3. Insert the rental (rental_date is auto-generated).
--   4. Mark the car as rented.
--
-- Edit v_user_id and v_car_id to test different scenarios
-- (non-existent user/car, car not available, successful rental).
-- ============================================================

DO $$
DECLARE
    v_user_id    INTEGER := 1;
    v_car_id     INTEGER := 1;
    v_car_status TEXT;
    v_rental_id  INTEGER;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM lyfter_car_rental.users WHERE id = v_user_id) THEN
        RAISE EXCEPTION 'User % does not exist', v_user_id;
    END IF;

    SELECT status INTO v_car_status FROM lyfter_car_rental.cars WHERE id = v_car_id;

    IF v_car_status IS NULL THEN
        RAISE EXCEPTION 'Car % does not exist', v_car_id;
    ELSIF v_car_status <> 'available' THEN
        RAISE EXCEPTION 'Car % is not available (current status: %)', v_car_id, v_car_status;
    END IF;

    INSERT INTO lyfter_car_rental.rentals (user_id, car_id, status)
    VALUES (v_user_id, v_car_id, 'active')
    RETURNING id INTO v_rental_id;

    UPDATE lyfter_car_rental.cars
    SET status = 'rented'
    WHERE id = v_car_id;

    RAISE NOTICE 'Rental created with ID: %', v_rental_id;
END $$;
