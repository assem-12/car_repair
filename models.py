class person:
    def __init__(self, name, age,hobby):
        self.name = name
        self.age = age
        self.hobby=hobby


    def printall(self):
        print(self.age,self.name ,self.hobby)


d1 = person("hamza", 30)
d2 = person("mohamed", 60)
d3 = person("hamed", 50)
d1.printall()
d2.printall()
d3.printall()