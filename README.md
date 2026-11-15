 I am starting with the lower part of the path in Figure 7(a), from A to I. For now, I have worked on drawing the path and rounding its corners. The speed of the tool has not been calculated yet.

First, I read the coordinates from the figure and entered them into two Python lists, one for X and one for Y. These values were taken from the graph, so they are a reconstruction rather than the authors’ original dataset. I joined the points with straight lines and added their names to compare the drawing with the figure.

After this, I calculated the length of each straight section. I also calculated the direction in which the tool approaches each corner and the direction in which it leaves. This allowed me to find the turning angle. I used a loop to repeat these calculations for every corner instead of writing separate code for each one.

The paper explains in Section 3.2 that the sharp corners are rounded using a cubic B-spline with five control points. It also gives an allowed deviation of 0.02 mm from the original path. The purpose is to let the tool change direction smoothly while staying close to the intended route.

The paper does not give all the details needed to place the five control points. I therefore used a symmetric arrangement, where the bend starts and finishes at equal distances from the corner. This is a choice made for the reconstruction, rather than an exact construction provided by the authors.

I kept this distance small, at no more than 0.02 mm. For shorter sections, the code reduces it further so that neighbouring bends do not overlap. This distance is not the same as the actual deviation of the curve, which still needs to be checked. The arrangement of the control points and the knot values used to create the spline are explained in the code.

I used SciPy to calculate the curves and Matplotlib to draw them. The straight sections are shown in blue and the bends in red. These colours only help show the different parts of the path; they do not show the tool’s speed. The original points are also shown as black dots.

The code calculates the geometry from the coordinate lists, so it is not limited to manually drawing this particular shape. If the coordinates are changed, it recalculates the lengths, directions and bends. However, I still need to test it on another path to demonstrate this properly.

Initial checks showed that each bend starts and ends at the intended positions. The direction of the curve was also checked where it meets the straight sections. Further checks are needed to confirm that the complete path joins smoothly and stays within the allowed tolerance.

The work completed so far is the first geometry stage. It is not yet a complete reproduction of Figure 7. The next step is to finish checking the rounded path and then implement the paper’s VPOp method to calculate the feedrate and the jerk of the X and Y axes.# feedrate-reproducibilty
