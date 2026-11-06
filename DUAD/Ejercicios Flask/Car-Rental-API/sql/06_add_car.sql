-- Adds a new car. Edit the values below to test different inputs.

INSERT INTO lyfter_car_rental.cars (brand, model, year, status)
VALUES ('Toyota', 'RAV4', 2023, 'available')
RETURNING id, brand, model, year, status;
