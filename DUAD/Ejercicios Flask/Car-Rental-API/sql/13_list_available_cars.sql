-- Lists all currently available cars.

SELECT id, brand, model, year, status
FROM lyfter_car_rental.cars
WHERE status = 'available'
ORDER BY id;
