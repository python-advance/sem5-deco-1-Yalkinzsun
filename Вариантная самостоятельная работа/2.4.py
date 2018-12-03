def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def my_function(foo, bar):
    return foo+bar

print(my_function(5, 10))
print(my_function(5, 10))