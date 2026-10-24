a= float(input("Enter the first number: "))
op= input("operator (+ - * / % ** //)")
b= float(input("Enter the second number: "))
if op == '+':
    print (a+b)
elif op == '-':
    print (a-b)
elif op == '*':
    print (a*b)
elif op == '/':
    if b == 0:
        print ("error :divison by zero")
    else:
        print (a/b)
elif op == '%':
    print (a%b)
elif op == '**':
    print (a**b)

elif op == '//' :
    print (a//b)

else:
    print ("no operator" , op)

