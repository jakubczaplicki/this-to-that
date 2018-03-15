# this-to-that
This-To-That - Loft from one shape to another in OpenSCAD

This is cleaned version of the This-To-That project by Ezra Reynolds
The original files can be found here:  https://www.thingiverse.com/thing:161646

This project demonstrates a way to "loft" from one shape to another in OpenSCAD
using the concept of tweening. Using this project, one can easily shift from
a circle to a circle(of different size), a triangle, square, pentagon, hexagon,
heptagon, octagon, nonagon, decagon, hendecagon, dodecagon, rectangle,
trapezoid, heart, star, or cross. You can even add your own shapes or customize
the default shapes for your own applications.

Sample cases: you need an adapter to go from one hose size to another, you need
to go from a rectangular duct to a trapezoidal duct, you need to drive
a pentagonal bolt but only have a square driver, you need a hopper or a stand...

Due to limitations in OpenSCAD (variables, array concatenation, etc.) this
project uses a python script to generate the tweens. This file
"tween_generator.py" is where the shapes, and their resolution, are defined
(and where one can customize/add new shapes). When run, it creates the file
"tween_shapes.scad" (a default version of this file is included in the project).
"Tweening" allows shifting from one shape to another by using a weighted
average. For example, if tweening between a circle and a triangle - at 0%,
the shape is a circle, at 100%, a triangle, and for all other values some
amalgum of the two.

The main project file is "tween_loft.scad". In this file, I document the
program, the logic, and the parameters. There are several examples that use
these two files to create a solid or a tube.

You can either create solid shapes (stamps, press tools, etc.), or hollow tubes.
All the parameters are controllabled - the size, rotation, and centroid position
of your base shapes, the granularity of the loft, the thickness of the walls,
etc. You can also create an extension of each base shape, which you could use
as a mounting point for tube clamps or other hardware.

The complexity of the design is controlled in two places. The resolution of
the tween shapes is determined in the "tween_generator.py" file. The number
of slices in the loft ("tween_loft.scad") also affects the complexity.
If either value is too high, the computation time increases sharply.
Values that are too high will also crash OpenSCAD. The program may work fine
with a smaller number of horizontal slices, but may crash with higher numbers.
Save your work often.

Notes from the Author:
	
I have seen examples on Thingiverse (http://www.thingiverse.com/thing:50363)
where people use a superellipse to convert 	from a circle to a square.  
Unfortunately, this is only an elegant solution for circles to squares.  
What happens if I need to convert from other shapes?  
What if I have need to go from rectangle to circle?

This program generates a number of tweens (in-between slices) that are a
weighted average of the two shapes. For example, consider a triangle and a
circle. If the weight is 0, the tween is a triangle. If 1,the tween is a circle.
If 0.5, it is some average of a triangle and a circle. These are unioned in
OpenSCAD to create a solid or hollow shape.

Wall thickness, number of slices, and tween translation/rotation all combine to 
make (or break) holes in the manifold of the design (important if making a
fluid connector)

Due to limitations in OpenSCAD (actual variables, list concatenation, etc.) this
program uses a Python program, `tween_generator.py`, to create a file containing
OpenSCAD named polygons (list of x,y pairs). This allows one shape to
be interpolated to another, as the "tween" shapes all have the same number of
points-pairs. The resolution of the tweens is controlled by the generator.

Depending on what is "good enough", you may want to decrease the complexity of
the base shape (normally the unit circle in the tween_generator.py file and
increase the number of slices in OpenSCAD.

For example, defining the unit_circle in the generator as a 128-sided polygon
(instead of 180-sided) allows a smoother transition on the loft (more slices)
for the same polygon count.  The more detailed the base shape, the higher
computational load of the whole model.

The default shapes are:
	tween_circle, tween_triangle, tween_square, tween_pentagon, tween_hexagon, 
	tween_septagon, tween_octagon, tween_nonagon, tween_decagon, tween_hendecagon,
	tween_dodecagon, tween_star, tween_rectangle, tween_trapezoid, tween_heart,
	tween_cross


Other Notes:

* OpenSCAD does not support true variables, array concatenation, etc.
* This program helps fill in gaps that can not be solved using OpenSCAD alone.
* This program does some of the heavy lifting for these types of shapes.
