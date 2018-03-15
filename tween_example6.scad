// Example. Simple loft triangle to circle

use <tween_loft.scad>
include <tween_shapes.scad>

shape1= tween_circle;
shape1Size = 100;
shape1Rotation = 0;
shape1Extension = 40;
shape1Centroid  = [0,0];

shape2= tween_triangle;
shape2Size = 100;
shape2Rotation = 0;
shape2Extension = 40;
shape2Centroid= [0,0];
shape2ExtensionAdjustment= 0;

wallThickness= 20;

isHollow = 1;

extrusionHeight= 100;
extrusionSlices = 30;
sliceAdjustment= 0;

sliceHeight = extrusionHeight * 1.0 / extrusionSlices;

tweenLoft(shape1, shape1Size, shape1Rotation, shape1Centroid, shape1Extension,
          shape2, shape2Size, shape2Rotation, shape2Centroid, shape2Extension,
          shape2ExtensionAdjustment, extrusionSlices, sliceHeight,
          sliceAdjustment, wallThickness/2, isHollow);
