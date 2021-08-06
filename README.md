# GravityEngine

Gravity Simulation with Python and Pygame.

# What it does

When the program starts there is the sun and the four closest planets to it rotating around it with very precise distance and velocities to scale. The velocities are shown on the right.

<br/>

It is then possible to add your own objects : by clicking on the screen, a planet appears with a textfield allowing to choose the mass. 

You can then choose it's velocity by clicking again on the window. The velocity vector will be in the direction of your cursor and the value proportional to the distance. A red arrow will appear on screen indicating that you are about to select the velocity.

The last step will be to choose the color : an image will appear in the corner and the color you click on will be selected.

# How it works

Every frame, for each object, the gravitational acceleration due to all other objects is calculated with Newton's gravitational law and the object's velocity is updated. The object then moves according to its velocity in the x and y direction.
