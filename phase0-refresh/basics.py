def is_leap_year(year):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False

for x in range(2000, 2027):
    if is_leap_year(x):
        print(x)

def fizzbuzz(n):
    if (n % 3 == 0) and (n % 5 == 0):
        return "FizzBuzz"
    if (n % 3 == 0):
        return "Fizz"
    if (n % 5 == 0):
        return "Buzz"
    return n

for x in range(1, 31):
    print(fizzbuzz(x))
    