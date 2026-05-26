import random
name=input("What is your name?")
adjective=('smart','wise','agile','brave','sly','honorable')
animal_names=("phoenix","dragon","owl","fox","wolf","tiger")
integers = list(range(1, 100))
print(random.choice(integers))
print(name+", your codename is "+random.choice(adjective)+" "+random.choice(animal_names)+"!"+ " Your lucky number is "+str(random.choice(integers)))