# def print_hello():
#     print("Hello World")

def add_print_to(original): # 데코레이터 함수
    def wrapper():
        print('함수 시작') # print_hello를 데코레이팅
        original()
        print('End') # print_hello를 데코레이팅
    return wrapper

# add_print_to(print_hello)()

@add_print_to
def print_hello():
    print("Hello World")

# print_hello = add_print_to(print_hello) # print_hello -> original

print_hello()