import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print((3+0)%3)
#using set 0


#PART A
scan_A = pd.read_csv("scan_posA.csv")
scan_B = pd.read_csv("scan_posB.csv")

# print(scan_A)

x_coords_A = scan_A['x'].values
y_coords_A = scan_A['y'].values

# print(x_coords_A)

x_coords_B = scan_B['x'].values
y_coords_B = scan_B['y'].values

plt.figure(figsize=(8, 7))

plt.scatter(x_coords_A, y_coords_A, s=10, label="Scan A")
plt.scatter(x_coords_B, y_coords_B, s=10, label="Scan B")

plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("LiDAR Scans Before Transformation")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Q1A_1.png", dpi=300)
plt.show()

#PART B

# transformation matrix of B onto A
# T= [[cos    -sin    tx]
#     [sin    cos    ty]
#     [0      0       1]]

# theta is +90 as to go from B to A u need to rotate 90 degrees counterclockwise
# we know B is 1.3m away from A in the y_a direction meaning ty is 1.3 tx is 0
# therefore
# T= [[0    -1    0]
#     [1    0    1.3]
#     [0    0     1]]

T_B_to_A = np.array([
    [0, -1, 0],
    [1,  0, 1.3],
    [0,  0, 1]
])

#we need to add a 3rd row of ones so we can matrix multiply
B_3by3 = np.vstack([x_coords_B, y_coords_B, np.ones(len(x_coords_B))])

B_transformed = np.matmul(T_B_to_A, B_3by3)

# print(B_transformed)

#now we need to remove the last row of ones
x_transformed = B_transformed[0,:]
y_transformed = B_transformed[1,:]



plt.figure(figsize=(8, 7))

plt.scatter(x_coords_A, y_coords_A, s=10, label="Scan A")
plt.scatter(x_transformed, y_transformed, s=10, label="Scan B")

plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.title("LiDAR Scans After Transformation")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Q1A_2.png", dpi=300)
plt.show()


#PART C
#A way to visually see if the transformation was incorrect would be if the scans dont allign