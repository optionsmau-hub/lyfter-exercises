# Exercise 3: read_lines function (given in the activity statement)
 
 
def read_lines(path):
    with open(path, "r") as f:
        return f.readlines()
 
