scores = [12, 17, 9, 15, 14]

best = -1
best_pos = 0

for pos, s in enumerate(scores, start=1):
    if s > best:
        best = s
        best_pos = pos

print(f"Best: {best} (student #{best_pos})")