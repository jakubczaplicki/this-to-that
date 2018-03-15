// Example. Star to Pentagon Spiral. Cool Desk toy.

use <tween_loft.scad>
include <tween_shapes.scad>

shape1= tween_star;
shape1Size = 100;
shape1Rotation = 144;
shape1Extension = 10;
shape1Centroid  = [0,0];

shape2= tween_pentagon;
shape2Size = 100;
shape2Rotation = 0;
shape2Extension = 30;
shape2Centroid= [0,0];
shape2ExtensionAdjustment= 0;

wallThickness= 50;

isHollow = 0;

extrusionHeight= 100;
extrusionSlices = 50;
sliceAdjustment= 0;

sliceHeight = extrusionHeight * 1.0 / extrusionSlices;

tweenLoft(shape1, shape1Size, shape1Rotation, shape1Centroid, shape1Extension,
          shape2, shape2Size, shape2Rotation, shape2Centroid, shape2Extension, shape2ExtensionAdjustment,
          extrusionSlices, sliceHeight, sliceAdjustment, wallThickness/2, isHollow);
