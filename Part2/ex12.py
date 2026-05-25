def check_string(string):
    if "the" in string.lower():
        print("Found it!")
    else:
        print("Nope!")


str_1 = "the"
str_2 = "Thumbs up!"
str_3 = "Theatre can be boring."

check_string(str_1)
check_string(str_2)
check_string(str_3)