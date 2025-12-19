# Encapsulation (封装)
class Animal:
    def __init__(self, name, age):
        # Private attributes
        self.__name = name
        self.__age = age

    # Getter method for name
    def get_name(self):
        return self.__name

    # Setter method for name
    def set_name(self, name):
        self.__name = name

    # Getter method for age
    def get_age(self):
        return self.__age

    # Setter method for age
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Age must be greater than 0")

    def make_sound(self):
        # Abstract method, meant to be overridden by subclasses
        pass


# Inheritance (继承)
class Dog(Animal):
    def __init__(self, name, age, breed):
        # Call the constructor of the parent class
        super().__init__(name, age)
        self.breed = breed

    def make_sound(self):
        # Polymorphism (多态): Override the method from the parent class
        return "AAAA!"

    def fetch(self):
        return f"{self.get_name()} is fetching the ball."


# Inheritance (继承)
class Cat(Animal):
    def __init__(self, name, age, color):
        # Call the constructor of the parent class
        super().__init__(name, age)
        self.color = color

    def make_sound(self):
        # Polymorphism (多态): Override the method from the parent class
        return "Meow!"

    def climb(self):
        return f"{self.get_name()} is climbing the tree."
class Cat2(Animal):
    def __init__(self, name, age, color):
        # Call the constructor of the parent class
        super().__init__(name, age)
        self.color = color

    def make_sound(self):
        # Polymorphism (多态): Override the method from the parent class
        return "Meow!"

    def climb(self):
        return f"{self.get_name()} is climbing the tree."

# Create instances of Dog and Cat
dog = Dog("Buddy", 3, "Golden Retriever")
cat = Cat2("Whiskers", 2, "Black")

# Demonstrate encapsulation
print(dog.get_name())  # Accessing private attribute via getter
dog.set_name("Max")  # Modifying private attribute via setter
print(dog.get_name())

# Demonstrate polymorphism
print(dog.make_sound())  # Output: Woof!
print(cat.make_sound())  # Output: Meow!

# Demonstrate additional methods in subclasses
print(dog.fetch())  # Output: Max is fetching the ball.
print(cat.climb())  # Output: Whiskers is climbing the tree.
