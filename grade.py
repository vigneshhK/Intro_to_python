grade = float(input("GRADE /20"))
if grade < 0 or grade > 20:
  print ("Invalid grade")
elif grade >= 16:
  print ("very good")
elif grade >= 14:
  print ("Good")
elif grade >= 12:
  print ("fairly good")
elif grade >= 10:
  print ("pass")
else:
  print ("fail")
