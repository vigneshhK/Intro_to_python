scores = [12, 17, 9, 15,14]
best = -1
best_position = 0
for position , s  in enumerate(scores , start =1):
    if s > best :
        best = s
        best_position = position
        print (f"Best:{best} (student {best_position})")