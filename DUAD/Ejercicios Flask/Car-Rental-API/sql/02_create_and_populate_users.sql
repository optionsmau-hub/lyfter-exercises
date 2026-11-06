-- ============================================================
-- Exercise 1.2: Users table
--
-- Creates lyfter_car_rental.users and populates it with 50 users
-- in the same script execution (passwords are stored hashed with
-- md5 just for seeding purposes; the API hashes real passwords
-- with werkzeug's generate_password_hash).
-- ============================================================

DROP TABLE IF EXISTS lyfter_car_rental.users CASCADE;

CREATE TABLE lyfter_car_rental.users (
    id         SERIAL PRIMARY KEY,
    full_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    username   TEXT NOT NULL UNIQUE,
    password   TEXT NOT NULL,
    birth_date DATE NOT NULL,
    status     TEXT NOT NULL DEFAULT 'active'
               CHECK (status IN ('active', 'inactive', 'suspended', 'delinquent'))
);

-- ------------------------------------------------------------
-- Seed data: 50 fake users built from name pools + generate_series
-- ------------------------------------------------------------
WITH pools AS (
    SELECT
        ARRAY['James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda','William','Elizabeth',
              'David','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Charles','Karen',
              'Carlos','Maria','Jose','Ana','Luis','Laura','Miguel','Sofia','Diego','Valentina']::TEXT[] AS first_names,
        ARRAY['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
              'Hernandez','Lopez','Gonzalez','Perez','Sanchez','Ramirez','Torres','Flores','Rivera','Gomez']::TEXT[] AS last_names,
        ARRAY['active','active','active','active','inactive','suspended','delinquent']::TEXT[] AS statuses
)
INSERT INTO lyfter_car_rental.users (full_name, email, username, password, birth_date, status)
SELECT
    pools.first_names[((n - 1) % array_length(pools.first_names, 1)) + 1] || ' ' ||
        pools.last_names[((n * 3 - 1) % array_length(pools.last_names, 1)) + 1] AS full_name,
    lower(
        pools.first_names[((n - 1) % array_length(pools.first_names, 1)) + 1] || '.' ||
        pools.last_names[((n * 3 - 1) % array_length(pools.last_names, 1)) + 1] || n || '@example.com'
    ) AS email,
    lower(
        pools.first_names[((n - 1) % array_length(pools.first_names, 1)) + 1] ||
        pools.last_names[((n * 3 - 1) % array_length(pools.last_names, 1)) + 1] || n
    ) AS username,
    md5('Passw0rd!' || n) AS password,
    (DATE '1960-01-01' + floor(random() * (DATE '2005-12-31' - DATE '1960-01-01' + 1))::INT) AS birth_date,
    pools.statuses[(floor(random() * array_length(pools.statuses, 1)) + 1)::INT] AS status
FROM generate_series(1, 50) AS n
CROSS JOIN pools;
