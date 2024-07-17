class Car:

    total_car=0 #class variable

    def __init__(self,userbrand,usermodel):  #constructor
        self.__brand=userbrand   #self.brand is an instance variable . self is a reference to the current instance of the class. It is used to access variables or methods of the class.
        self.__model=usermodel
        Car.total_car+=1

    def get_brand(self):
        return f"{self.__brand}"
    
    def set_brand(self, new_brand):
        self.__brand = new_brand

    def fuel_type(self):
        return "Petrol or Diesel"

    def fullname(self):
        return f"{self.__brand} {self.__model}" #formatted string literals (f-strings) are string literals that have an f at the beginning and curly braces containing expressions that will be replaced with their values.

    @staticmethod #decorators are a form of metaprogramming and provide a way to extend the behavior of functions or methods without modifying them.
    def declaration():
        return "This is a Car class"

    @property #The @property decorator is used to customize getters and setters for class attributes.
    def model(self):
        return f"{self.__model}"

class ElectriCar(Car):  #Inheritance is a way of creating a new class for using details of an existing class without modifying it. The newly formed class is a derived class (or child class). Similarly, the existing class is a base class (or parent class).
    
    def __init__(self,userband,usermodel,battery):
        super().__init__(userband,usermodel) #super() function that will make the child class inherit all the methods and properties from its parent
        self.battery=battery

    
    def fuel_type(self):
        return "Electric Charge"



class Battery:
   def battery_info(self):
       return "Battery: 100kWh"
    
class Engine:
    def engine_info(self):
        return "Engine: 2.0L"


class ElectricCar1(Battery,Engine,Car):
    pass
    


#sol1.py
my_car = Car("Toyota", "Corolla")
#print(my_car.brand) #brand is a private variable so it will give an error


#sol2.py
my_car1 = Car("Toyota1", "Corolla1")
print(my_car.fullname())



#sol3.py
my_car2 = ElectriCar("Toyota2", "Corolla2", "100")
print(my_car2.battery)


#sol4.py
#__brand means made that variable as private and the brand can be acceseed through get_brand that is the getter method
my_car3 = Car("Toyota3", "Corolla3")
print(my_car3.get_brand())
my_car3.set_brand("Honda")

#sol5.py
my_car4 = ElectriCar("Toyota4", "Corolla4", "100")
print(my_car4.fuel_type())

#sol6.py
print(Car.total_car) #class variable can be accessed by class name

#sol7.py
#static methods are methods that are bound to a class rather than its object. They do not require a class instance creation. So, they are not dependent on the state of the object.
print(Car.declaration())

#sol8.py
#property decorator to allow only-read access to the model attribute
my_car5 = Car("Toyota5", "Corolla5")
print(my_car5.model) #model is a property so it can be accessed by class object

#sol9.py
#Multiple Inheritance
my_car6 = ElectricCar1("Toyota6", "Corolla6")
print(my_car6.battery_info())





####DECORATORS

#Decorators are a way to dynamically alter the functionality of your functions. They are perfect for wrapping other functions or methods.
#Decorators are functions that takes function as an argument and return a function.

#A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure. Decorators are usually called before the definition of a function you want to decorate.

def decorator_function(original_function):
    def wrapper_function():
        print(f"Wrapper executed this before ")
        original_function()
        return original_function()
    return wrapper_function

def hello():
    print("Hello")

hello1=decorator_function(hello)

#SHORTCUT

@decorator_function
def hello():
    print("Hello")

hello()
#when we call hello () this function will execute the wrapper function and the wrapper function will execute the original function and return the original function.So basically
#hello() will pass through the decorator_function




