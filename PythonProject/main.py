import matplotlib.pyplot as plt
from src.points import generate_points

points = generate_points(50)

X = [p[0] for p in points]
Y = [p[1] for p in points]

plt.title("Random Points Plotting")
plt.scatter(X, Y)
plt.xlabel("X")
plt.ylabel("Y")
plt.savefig("random_points.png")
