age={"Hans": 25, "Prag": 23, "Bunyod": 18}
print(age)
print(age["Hans"])
age.update({"Prag": 24})
print(age["Prag"])
age.pop('Bunyod')
print(age)