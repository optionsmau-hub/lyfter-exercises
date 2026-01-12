#Ejercicio 7 Funcionrd programa lista de numeros
def is_prime(n):
    if n < 2:
        return False  

    # check divisibility from 2 up to n-1
    for i in range(2, n):
        if n % i == 0:  # if n es divisible por i is not prime
            return False

    return True  # if we reach here, n is prime
def filter_primes(numbers):
    """Return a list of prime numbers from the given list."""
    primes = []
    for num in numbers:
        if is_prime(num):
            primes.append(num)
    return primes
# quick test
data = [10, 15, 3, 7, 19, 20, 23, 24, 29]
print(filter_primes(data))   # → [3, 7, 19, 23, 29]
#Ejercicio 7 Funcionrd programa lista de numeros