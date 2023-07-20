from funcs import read_table, interp_xyz, generate


tl = read_table("data/task.txt")
# tl = generate()
# print(tl)
# print(tl)
# x = float(input("Input x - "))
# y = float(input("Input y - "))
# z = float(input("Input z - "))
x = 1.5
y = 1.5
z = 1.5
print("Newton - ", interp_xyz(tl, "newton", x, y, z))
print("Spline - ", interp_xyz(tl, "spline", x, y, z))
print("Mix - ", interp_xyz(tl, "mix", x, y, z))
