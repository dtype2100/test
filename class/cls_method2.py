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
    
    # @classmethod
    # def number_of_users(cls):
    #     print(f"Number of users:{cls.count}")
    def number_of_users(self):
        '''
        if you need to use class method, instance method, Use instance method
        '''
        print(f"Number of users:{User.count}")

user1 = User("Young", "young@codeit.kr", "123456")
user2 = User("Yoonsoo", "yoonsoo@codeit.kr", "abcdef")
user3 = User("Taeho", "taeho@codeit.kr", "123abc")

User.number_of_users(user1)
user1.number_of_users()