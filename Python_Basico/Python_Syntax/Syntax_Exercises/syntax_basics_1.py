#1. string + string  → FUNCIONA
print("Hi, " + "World!")
print("123" + "456")
print("Python " + "3.10")   
#2. string + int  → ERROR 
#print("Hello, " + 5)  # This creates an error
#print("123" + 456)  # This creates an error  
#3.int + string  → ERROR
#print(5 + "Hello")  # This creates an error
#print(456 + "123")  # This creates an error
# 4. list + list → WORKS
print([1, 2, 3] + [4, 5, 6])
print(["a", "b"] + ["c", "d"])  
# 5. string + list → ERROR 
#print("Hello" + [1, 2, 3])  # This creates an error
#print("abc" + ["d", "e"])  # This creates an error
# 6. float + int → WORKS
print(5.5 + 2)
print(3.14 + 10)    
# 7. bool + bool → WORKS
print(True + False)
print(False + False)    
print(True + True)
