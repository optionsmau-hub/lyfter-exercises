-- Changes the account status of a user.
-- Edit v_user_id and v_new_status to test different scenarios.

DO $$
DECLARE
    v_user_id    INTEGER := 1;
    v_new_status TEXT := 'suspended';
BEGIN
    IF v_new_status NOT IN ('active', 'inactive', 'suspended', 'delinquent') THEN
        RAISE EXCEPTION 'Invalid status: %', v_new_status;
    END IF;

    UPDATE lyfter_car_rental.users
    SET status = v_new_status
    WHERE id = v_user_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'User % does not exist', v_user_id;
    END IF;

    RAISE NOTICE 'User % status updated to %', v_user_id, v_new_status;
END $$;
