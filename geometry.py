# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:26:20 2026

@author: lenovo
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline
# 1. INPUT PATH

# I reconstructed these coordinates from Figure 7(a). Each matching pair of x and y values defines one point.
# The points are ordered from A to I.
x = [0, 3, 3, -3, -3, 6, 6, -6, -6]
y = [0, 0, -3, -3, 3, 3, -6, -6, 6]

# Section 3.2 gives a contour tolerance of 0.02 mm.
tolerance = 0.02

# Each point must have both an X and a Y coordinate.
if len(x) != len(y) or len(x) < 3:
    raise ValueError("Provide matching X and Y lists with at least 3 points.")
# Consecutive identical points would create a zero-length segment.
for i in range(len(x) - 1):
    if x[i] == x[i + 1] and y[i] == y[i + 1]:
        raise ValueError("Two consecutive points are identical.")
# 2. PREPARE THE DRAWING
plt.figure(figsize=(7, 7))
# I show the original points as black dots for reference.
plt.plot(x, y, "ko", markersize=3)

# Label the points A, B, C, etc.
# The 0.2 offset moves only the labels, not the actual points.
for i in range(len(x)):
    name = chr(65 + i) if i < 26 else str(i + 1)
    plt.text(x[i] + 0.2, y[i] + 0.2, name)
# The first straight section begins at the first point.
last_x = x[0]
last_y = y[0]
# 3. PROCESS EACH INTERIOR CORNER

# The first and last points are endpoints, so I skip them.
for i in range(1, len(x) - 1):

    # Find the displacement from the previous point to this corner.
    dx_in = x[i] - x[i - 1]
    dy_in = y[i] - y[i - 1]

    # Find the displacement from this corner to the next point.
    dx_out = x[i + 1] - x[i]
    dy_out = y[i + 1] - y[i]

    # Calculate segment lengths using Pythagoras.
    length_in = (dx_in**2 + dy_in**2)**0.5
    length_out = (dx_out**2 + dy_out**2)**0.5

    # Dividing by length gives unit vectors.
    # These describe direction independently of segment length.
    incoming = (dx_in / length_in, dy_in / length_in)
    outgoing = (dx_out / length_out, dy_out / length_out)

    # Calculate the turning angle using the dot product.
    cos_angle = (
        incoming[0] * outgoing[0]
        + incoming[1] * outgoing[1]
    )

    # Keep the cosine within its valid range despite rounding errors.
    cos_angle = max(-1, min(1, cos_angle))
    angle_degrees = math.degrees(math.acos(cos_angle))

    # This construction does not support a complete reversal.
    if angle_degrees > 179.999:
        raise ValueError("A 180-degree reversal needs separate treatment.")

    print("Corner index:", i, "| Turning angle:", angle_degrees)

    # I choose a conservative rounding distance. This rule is my reconstruction choice, not a paper equation.
    # Limiting it to a quarter of each segment leaves room for the rounding at neighbouring corners.
    d = min(tolerance, length_in / 4, length_out / 4)

    # Move backward from the corner to locate the bend's start.
    start_x = x[i] - d * incoming[0]
    start_y = y[i] - d * incoming[1]
    # Move forward from the corner to locate the bend's end.
    end_x = x[i] + d * outgoing[0]
    end_y = y[i] + d * outgoing[1]
    # 4. CONSTRUCT THE FIVE CONTROL POINTS
    # Section 3.2 specifies a cubic B-spline with five control points. The exact placement below is my
    # symmetric reconstruction of that description.
    P0 = [start_x, start_y]
    # Place P1 one-third of the way from the start to the corner.
    P1 = [
        start_x + (x[i] - start_x) / 3,
        start_y + (y[i] - start_y) / 3
    ]

    # Use the original corner as the middle control point.
    # The spline does not necessarily pass through this point.
    P2 = [x[i], y[i]]

    # Place P3 one-third of the way from the end to the corner.
    P3 = [
        end_x + (x[i] - end_x) / 3,
        end_y + (y[i] - end_y) / 3
    ]

    P4 = [end_x, end_y]

    control_points = [P0, P1, P2, P3, P4]

    # This symmetric knot vector is an implementation choice.
    # These values are spline parameters, not physical distances.
    knots = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]

    # Degree 3 means a cubic B-spline.
    curve = BSpline(knots, control_points, 3)
    # Evaluate 100 parameter values to display the bend.
    # These are not time steps or equally spaced path distances.
    u = np.linspace(0, 1, 100)
    bend = curve(u)
    # 5. DRAW THE STRAIGHT SECTION AND THE BEND.Connect the previous bend's end to this bend's start.
    plt.plot(
        [last_x, start_x],
        [last_y, start_y],
        color="blue"
    )

    # Column 0 contains X; column 1 contains Y.
    plt.plot(bend[:, 0], bend[:, 1], color="red")

    # Store the endpoint for the next straight section.
    last_x = end_x
    last_y = end_y
# 6. FINISH AND DISPLAY THE PATH
# Connect the final bend to the last point.
plt.plot(
    [last_x, x[-1]],
    [last_y, y[-1]],
    color="blue"
)

plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("Reconstructed A–I path with proposed corner smoothing")

# Equal scaling prevents the geometry from appearing stretched.
plt.axis("equal")
plt.grid()
plt.show()