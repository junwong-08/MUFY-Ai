import random
name=input("What is your name?")
adjective=('smart','wise','shady','brave','sly','mystic')
animal_names=("phoenix","dragon","owl","fox","wolf","tiger")
integers = list(range(1, 100))
print(name+", your codename is "+random.choice(adjective)+" "+random.choice(animal_names)+"!"+ " \n Your lucky number is "+str(random.choice(integers)))