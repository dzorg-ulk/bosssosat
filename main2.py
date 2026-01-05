def check_status(func):
    def wrapper():
        print("Checking status")
        func()
        print("Done")
    return wrapper

@check_status
def summmm():
    print(2 + 2)

summmm()
