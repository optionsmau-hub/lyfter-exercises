-- Lists all currently rented cars.

SELECT id, brand, model, year, status
FROM lyfter_car_rental.cars
WHERE status = 'rented'
ORDER BY id;
