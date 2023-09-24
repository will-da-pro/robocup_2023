import math

# Define the coordinates of the two circles
circle1_x, circle1_y = 0, 0  # Replace with the coordinates of your first circle
circle2_x, circle2_y = -5, 5  # Replace with the coordinates of your second circle

# Calculate the angle relative to the vertical line
angle_rad = math.atan2(circle2_x - circle1_x, circle2_y - circle1_y)

# Convert the angle from radians to degrees and reverse its sign
angle_deg = -math.degrees(angle_rad)

print(f"The angle relative to the vertical line is {angle_deg} degrees.")