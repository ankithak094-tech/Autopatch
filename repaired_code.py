def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print('Error: Division by zero')
        return None

print(divide(10, 0))