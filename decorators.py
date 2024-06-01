def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'Calling {func.__name__} with args:{args} => kwargs : {kwargs}')
        result = func(*args, **kwargs)
        print(f'Result of {result}')
        return result

    return wrapper


@my_decorator
def add_number(*args, **kwargs):
    res = kwargs['a'] + kwargs['b']
    return res


response = add_number(3, 4, 5, a=3, b=4)
print(response)
