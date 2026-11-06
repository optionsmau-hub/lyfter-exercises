-- Adds a new user. Edit the values below to test different inputs.

INSERT INTO lyfter_car_rental.users (full_name, email, username, password, birth_date, status)
VALUES ('Test User', 'test.user@example.com', 'testuser51', md5('Passw0rd!'), '1995-05-20', 'active')
RETURNING id, full_name, email, username, birth_date, status;
