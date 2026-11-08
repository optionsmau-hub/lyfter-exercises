-- ============================================================
-- Exercise 1.4: Rentals table (cross table between users and cars)
--
-- rental_date is auto-generated on insert via DEFAULT NOW().
-- return_date stays NULL until the rental is completed.
-- ============================================================

DROP TABLE IF EXISTS lyfter_car_rental.rentals CASCADE;

CREATE TABLE lyfter_car_rental.rentals (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES lyfter_car_rental.users(id),
    car_id      INTEGER NOT NULL REFERENCES lyfter_car_rental.cars(id),
    rental_date TIMESTAMP NOT NULL DEFAULT NOW(),
    return_date TIMESTAMP,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'cancelled'))
);
