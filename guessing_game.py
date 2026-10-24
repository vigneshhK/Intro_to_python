import random 

secret = random.randint(1 , 100)
attempts = 0

while attempts < 7 :
    guess = int (input("guess:"))
    attempts += 1
    if guess == secret:
        print (f"great! found in {attempts} attempts")
        break
    elif guess <secret :
        print("too low")
    else:
        print ("too high ")
if guess != secret:
    print ("lost! It was", secret)
