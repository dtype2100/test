class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    def say_hello(self):
        print(f"Hello. my name is {self.name}")
    def check_name(self, name):
        return self.name == name
    
user1 = User("John", "naver.com", "5678")


print(user1.name)
print(user1.email)
print(user1.password)
