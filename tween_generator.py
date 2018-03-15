#
#    Author: Ezra Reynolds
#            thingiverse@shadowwynd.com
#
#   Function:
#       Create 2D profiles that can be "tweened" into other shapes
#       To tween one shape into another, both must have the same number of
#       points. This program creates the file "tween_shapes.scad" for use in
#       OpenSCAD
#
#   Theory:
#
#       A line is defined by two points, and has infintely many points between
#       them.
#       A circle is defined by center and the radius, and is made of infinitely
#       many points.
#       A circle is approximated by a regular polygon with a large number of
#       sides.
#
#       For example, if you made a shape with 360 sides (each side being one
#       degree), it would be very circular, but it is actually a 360-gon.
#       A better approximation would be to have three line segments for every
#       degree, Thus resulting in an 1080-gon, and an even smoother
#       approximation of a circle. At some point, the approximation of the
#       circle is "good enough" for practical uses. At some point, the
#       (really big approximation) 3600000-gon has surpassed our ability to
#       manufacture or measure.
#
#       To interpolate between two data sets, each data set should have the
#       same number of elements.
#
#       A triangle is defined by three points.
#       A hexagon is defined by six points.
#
#       To smoothly shift from triangle to hexagon, you must have the same
#       number of points in each array. The easist way to do this is to add
#       a hidden node in the middle of each side, cutting each triangle side
#       in half.
#
#       This transforms the triangle from:
#           A --> B --> C --> A   <AB = 60, <BC = 60, <CA = 60  (3 points) to:
#           A --> B --> C --> D --> E --> F --> A    <AB = 180 (a straight line)
#                , <BC = 60, <CD = 180, <DE = 60, <EF = 180, <FA = 60 (6 points)
#
#       We can now smoothly transform the 6-point triangle to a hexagon,
#       as both have 6 points. We could adjust both shapes to have 60 points,
#       or 1000 points using the same technique - as long as we have at least
#       6 (for the hexagon)
#
#       Note that we have to have at least 6 points to define the hexagon -
#       but we could define a hexagon with 7 points (1 colinear),
#       8 points(2 colinear), 12 points (6 colinear),
#
#       Or even higher - an 360 point set for a hexagon would have 6 real
#       points and 354 filler points... but we could now smoothly shift a
#       hexagon to a very close circle.
#
#       This program starts with a calculating values for a "unit circle",
#       or in actuality, a "unit n-gon" with large n (128, 180, etc.)
#       Other shapes (square, rectangle, heart, hexagon....) are defined,
#       then the number of points is enlarged to match the "unit circle"
#
#       When finished, each shape will have the same number of points as the
#       "unit circle", and is thus "tweenable" and can be smoothly shifted
#       into any other defined shape.
#
#       It is easy to add new user-defined shapes.
#
#       These definitions are written as variables into an OpenSCAD file
#       "tween_shapes.scad"
#
#   The superellipse technique used in http://www.thingiverse.com/thing:50363
#   is worth examining. Unfortunately, it only works for squares and circles.
import argparse
import random
from math import sin, cos, radians
from datetime import date

import sys


def interpolate_pairs(input_array):
    """ For an array of [x, y, True] pairs
        [ [x0, y0, True], [x1, y1, True], [x2, y2, True]... ],
        return an array with an interpolated point between each point:
        [ [x0, y0, True], [xi1, yi1, False], [x1, y1, True],
          [xi2, yi2, False], [x2, y2, True] ...] """
    new_array = []
    for i in range(len(input_array) - 1):
        new_array.append(input_array[i])
        # Average each point n and n+1, create a new node between N and N+1
        new_array.append(
            [(input_array[i][0] + input_array[i + 1][0]) / 2,
             (input_array[i][1] + input_array[i + 1][1]) / 2,
             False
             ])
    # We don't handle interpolate the last element (N+1 does not exist),
    # so we add it to the array as the last element.
    new_array.append(input_array[-1])
    return new_array


def match_array_sizes(source_array, target_array):
    """ Given a source array of size X, and a target array of size Y,
        add or remove points from X until len(X)==len(Y), return X """
    # Since the shapes are closed figures (and OpenSCAD automatically seals the
    # shape), OpenSCAD does not need the end point (same as the start point).
    # However, for a nice interpolation we do need the ending point, otherwise
    # the last segment will be out of alignment.
    # Copy the start point to the end
    source_array.append(source_array[0])
    target_array.append(target_array[0])

    # These are [x,y] pairs.  Add a third parameter n so that each tuple is
    # [x, y, n].  The n is set for 1 to indicate an original (vs 0 for
    # interpolated) point. If we have too many points, we may only delete
    # an interpolated point.
    [a.append(True) for a in source_array]

    random.seed()  # Initialize random generator with time

    # For this usage, X should be less than Y
    #   Start by interpolating all of X until len(X interpolated) > len(Y)
    #   Once we overshoot so that len(X) > len(Y), randomly delete interpolated
    #   points (not original points) until len(X)==len(Y).
    while len(source_array) != len(target_array):
        if len(source_array) < len(target_array):
            # Roughly Double the array, interpolating between points
            source_array = interpolate_pairs(source_array)
        elif len(source_array) > len(target_array):
            # Remove a random interpolated element (not the first or last)
            r = random.randint(1, len(source_array) - 2)
            if source_array[r][2] is False:
                del source_array[r]
    # Return the final array, which should be same size as target array
    del source_array[-1]  # Remove the last element for OpenSCAD
    return source_array


def export_array(filename, array_name, target_array):
    """ Write the 2D array of points to disk.
        Python's string representation of an array
        is already in the format used by openSCAD.
    """
    # Generate a variable, containing the contents of the array
    # (x,y pairs only) in OpenSCAD format. Note: If the precision is too high,
    #  OpenSCAD screws up the floating point math.
    with open(filename, 'w') as f:
        f.write(f'\n\n {array_name} = [')
        for a in target_array:
            f.write(f'[{a[0]:.7f}, {a[1]:.7f} ],')
        f.write('];\n\n')
    return


def ngon(sides):
    """ Return an array of [x,y] pairs of polygon vertices inscribed about the
        unit circle for a polygon of n sides. """
    points = []
    # Calculate the points around the circle
    for i in range(0, sides):
        points.append([cos(radians((360.0 / sides) * i)),
                       sin(radians((360.0 / sides) * i))])
    return points


# The circle is the base unit of reference (doesn't have to be, but it is
# a good convention). The question must be answered: how much precision do
# I need? A higher value for the unit circle yields a more precise curve,
# but greatly increases triangle count in OpenSCAD. Values that are
# "good enough" yield dramatically better render times.

# For example, ngon(360) is a 360-sided polygon; this is fairly close for most
# things; one line segment per degree
#   ngon(1080) has 3 line segments per degree - more precise curves, but
#   much slower and more memory usage.
#   ngon(64) would have some discernable segments on bigger curves, but
#   might still be OK for small holes, Values of the reference unit circle
#   that are too high often crash OpenSCAD

size = 180
unit_circle = ngon(size)

# Need a regular polygon with 29 sides?
# poly29 = ngon(29)
# square = ngon(4);
# hexagon = ngon(6);
# etc.

# Add your own shapes or edit the existing ones.
# Open your favorite drawing program.  Draw a Circle of radius 1 at (0,0).
# Draw your shape inscribed in the circle (for a scale of 1)
# Record the points that define the shape into this program.
# How you input the shape determines how easily it will tween.
# By convention, 0 degrees is the starting point.
# Try to align your shape so that a point is defined for x=1, y=0 and
# work your way around.
# A-->B-->C-->A is not the same (for a tween) as B-->C--A-->B is not the
#  same as C-->A-->B-->C

# If your shape is defined by:  A-->B-->C-->D-->E-->A,
# leave off the last "A" - OpenSCAD closes the shape automatically.
#
# PolyName = [ [x0,y0], [x1, y1] .....]


star = [[1.0, 0.0], [0.32, 0.23], [0.31, 0.93], [-0.12, 0.37], [-0.79, 0.57],
        [-0.39, 0.0], [-0.79, -0.57], [-0.12, -0.38], [0.31, -0.93],
        [0.32, -0.24]]

heart = [[1.0, 0.0], [0.92, 0.04], [0.75, 0.22], [0.57, 0.45], [0.40, 0.66],
         [0.27, 0.79], [0.14, 0.87], [0.00, 0.93], [-0.10, 0.95], [-0.24, 0.95],
         [-0.40, 0.92], [-0.54, 0.85], [-0.63, 0.74], [-0.71, 0.60],
         [-0.72, 0.43], [-0.70, 0.29], [-0.65, 0.19], [-0.60, 0.13],
         [-0.53, 0.06], [-0.39, 0.0], [-0.53, -0.06], [-0.60, -0.13],
         [-0.65, -0.19], [-0.70, -0.29], [-0.72, -0.43], [-0.71, -0.60],
         [-0.63, -0.74], [-0.54, -0.85], [-0.40, -0.92], [-0.24, -0.95],
         [-0.10, -0.95], [0.00, -0.93], [0.14, -0.87], [0.27, -0.79],
         [0.40, -0.66], [0.57, -0.45], [0.75, -0.22], [0.92, -0.04]]

rectangle = [[1, 0], [1, 0.5],
             [0, 0.5], [-1, 0.5],
             [-1, 0], [-1, -0.5],
             [0, -0.5], [1, -0.5]]

trapezoid = [[0.5, 0.5], [-0.5, 0.5], [-1, -0.5], [1, -0.5]]

cross = [[1.00, 0.5], [0.5, 0.5], [0.5, 1.0], [-0.5, 1.0], [-0.5, 0.5],
         [-1.0, 0.5], [-1.0, -0.5], [-0.5, -0.5], [-0.5, -1.0], [0.5, -1.0],
         [0.5, -0.5], [1.0, -0.5]]


# Build the extrapolations; each array must have same number of units.
# For convention, we will use the unit circle as a base reference,
# but you could use any shape
def parse_args(args):
    p = argparse.ArgumentParser()
    p.add_argument('--output', help='Output scad file.',
                   default='tween_shapes.scad')
    args = p.parse_args(args)
    return args


def main(args=sys.argv[1:]):
    args = parse_args(args)
    with open(args.output, 'w') as f:
        f.write("// Tween_shapes for use with tween_loft.scad\n\n")
        f.write("// Based on unit circle of size " + str(size) + ".\n")
        f.write("// Created: " + date.isoformat(date.today()) + "\n")

    export_array(args.output, "tween_circle",     unit_circle)
    export_array(args.output, "tween_triangle",   match_array_sizes(ngon(3),  unit_circle) )
    export_array(args.output, "tween_square",     match_array_sizes(ngon(4),  unit_circle) )
    export_array(args.output, "tween_pentagon",   match_array_sizes(ngon(5),  unit_circle) )
    export_array(args.output, "tween_hexagon",    match_array_sizes(ngon(6),  unit_circle) )
    export_array(args.output, "tween_septagon",   match_array_sizes(ngon(7),  unit_circle) )
    export_array(args.output, "tween_octagon",    match_array_sizes(ngon(8),  unit_circle) )
    export_array(args.output, "tween_nonagon",    match_array_sizes(ngon(9),  unit_circle) )
    export_array(args.output, "tween_decagon",    match_array_sizes(ngon(10), unit_circle) )
    export_array(args.output, "tween_hendecagon", match_array_sizes(ngon(11), unit_circle) )
    export_array(args.output, "tween_dodecagon",  match_array_sizes(ngon(12), unit_circle) )

    export_array(args.output, "tween_star",      match_array_sizes(star,      unit_circle) )
    export_array(args.output, "tween_heart",     match_array_sizes(heart,     unit_circle) )
    export_array(args.output, "tween_rectangle", match_array_sizes(rectangle, unit_circle) )
    export_array(args.output, "tween_trapezoid", match_array_sizes(trapezoid, unit_circle) )
    export_array(args.output, "tween_cross",     match_array_sizes(cross,     unit_circle) )

    print(f'FILE: {args.output} generated OK.')


if __name__ == '__main__':
    main()
