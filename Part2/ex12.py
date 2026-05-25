def calculator(x, y, operation):
    if operation == "+":
        return x + y

    elif operation == "-":
        return x - y

    elif operation == "*":
        return x * y

    elif operation == "/":
        return x / y

    else:
        return "Invalid operation"


print(calculator(10, 5, "+"))