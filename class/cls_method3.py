class User:
    count = 0
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        User.count += 1

    def say_hello(self):
        print(f"Hello, {self.name}")
    
    def __str__(self):
        return f"User(name={self.name}, email={self.email}, password={self.password})"
    
    @classmethod
    def number_of_users(cls):
        '''
        인스턴스가 하나도 없는 경우라도 사용할 가능성이 있다면, class method 사용.
        '''
        print(f"Number of users:{cls.count}")

User.number_of_users()
