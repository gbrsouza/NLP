def min_max(numbers):
    return min(numbers), max(numbers)

class Person:
    def __init__(self,name):
        self.name = name
    pass

class Student(Person):
    def __init__(self, name, id):
        super().__init__(name)
        self.id = id
    pass

import numpy as np
import pandas as pd

def nonpositives(x):
    return x<=0

message = "Ping!"

def pong(count):
    for i in range(count):
        print("Pong!", end=" ")
        yield message


def my_decorator(function):
    def wrapper():
        print("<-", end="")
        function()
        print("->", end="")
    return wrapper


@my_decorator
def some_function():
    print("|", end="")



if __name__ == '__main__':
    df = pd.DataFrame(np.arange(20).reshape(5,4), index=[1,3,4,2,5])
    X, y = df.iloc[:,:-1], df.iloc[:,-1]

    print(X)
    print(y)

    # data = np.arange(20).reshape(4,5)
    # df = pd.DataFrame(data)
    #
    # print(df)
    # print(df.sum())

    # for message in pong(2):
    #     print(message, end=" ")
    # 'raining'.find('z')

    # data = np.arange(1,17).reshape(4,4)
    # for i in range(4):
    #     data[i][3-i] *= -1
    # print(data)

    # x = [4, -1, 0, 3, 5]
    # sorted(x)
    # for i in range(3):
    #     print("Hello", end=" ")
    #     if i < max(x[:i+1]):
    #         break
    #     else:
    #         print("world!")

    # list_of_numbers = [1,2,3]
    # str_to_numbers = str(n) for n in list_of_numbers
    # print(type(str_to_numbers))

    # df = pd.DataFrame(np.arange(20).reshape(5,4), index=[1,3,4,2,5])
    # print(df.loc[1:2])

    # B = {1, 2, 3}
    # A = {1, 2, 3, 4, 5, 6}
    # print(len(A), len(B))
    # print(A<B)


    # value1, value2, value3, value4 = True, False, False, True
    # print(value1 or value2 and value3 or not value4)

    # init_tuple = ()
    # print(init_tuple.__len__())

    # a = [-10, 27, 1000, -1, 0, -30]
    # result = [x for x in filter(nonpositives, a)]
    # print(result)

    # data = np.arange(20).reshape(4,5)
    # print(data.shape)

    # test = Student("Tom", 123)
    # print(test.name)

    # numbers = [1,3,5.0]
    # min_number, max_number = min_max(numbers)
    # min_max_numbers = min_max(numbers)
    #
    # print(type(min_number))
    # print(type(max_number))
    # print(type(min_max_numbers))
    # names = ["Snowball", "Chewy", "Bubbles", "Gruff"]
    # animals = ["cat", 'dog', "fish", "goat"]
    # ages=[1,2,2,6]
    # t = zip(names, animals, ages)
    # for name, animal, age in t:
    #     print(f"The {animal} {name} is {age}")

    # languages = ["Python", "C++", "Javascript"]
    # typing = ["dynamic", "static", "dynamic"]
    #
    # lang_dict = {
    #     lang: type_system
    #     for lang, type_system in zip(languages, typing)
    #     if type_system == "dynamic"
    # }
    #
    # print(lang_dict)

    # text = "paranaue"
    # print(text[-5:-2])

    # round1 = ["Chuck Norris", "Bruce Lee", "Jackie Chan"]
    # round2 = round1.copy()
    # round2.remove("Jackie Chan")
    # print(round1)
    # print(round2)