-- ============================================================
-- Exercise 1.3: Cars table
--
-- Creates lyfter_car_rental.cars and populates it with 30 cars
-- in the same script execution.
-- ============================================================

DROP TABLE IF EXISTS lyfter_car_rental.cars CASCADE;

CREATE TABLE lyfter_car_rental.cars (
    id     SERIAL PRIMARY KEY,
    brand  TEXT NOT NULL,
    model  TEXT NOT NULL,
    year   INTEGER NOT NULL CHECK (year BETWEEN 1990 AND 2026),
    status TEXT NOT NULL DEFAULT 'available'
           CHECK (status IN ('available', 'rented', 'disabled', 'maintenance'))
);

-- ------------------------------------------------------------
-- Seed data: 30 cars built from matched brand/model pairs
-- ------------------------------------------------------------
WITH pools AS (
    SELECT
        ARRAY['Toyota','Honda','Ford','Chevrolet','Nissan','Hyundai','Kia','Mazda',
              'Volkswagen','Subaru','BMW','Mercedes-Benz','Audi','Jeep','Tesla']::TEXT[] AS brands,
        ARRAY['Corolla','Civic','Focus','Malibu','Sentra','Elantra','Sportage','CX-5',
              'Jetta','Outback','3 Series','C-Class','A4','Wrangler','Model 3']::TEXT[] AS models,
        ARRAY['available','available','available','available','rented','maintenance']::TEXT[] AS statuses
)
INSERT INTO lyfter_car_rental.cars (brand, model, year, status)
SELECT
    pools.brands[((n - 1) % array_length(pools.brands, 1)) + 1] AS brand,
    pools.models[((n - 1) % array_length(pools.models, 1)) + 1] AS model,
    (2015 + floor(random() * 10))::INT AS year,
    pools.statuses[(floor(random() * array_length(pools.statuses, 1)) + 1)::INT] AS status
FROM generate_series(1, 30) AS n
CROSS JOIN pools;
