// Example. Hanging hopper of some sort - demonstrates use in part of larger assembly

use <tween_loft.scad>
include <tween_shapes.scad>

shape1= tween_circle;
shape1Size = 40;
shape1Rotation = 0;
shape1Extension = 100;
shape1Centroid  = [0,0];

shape2= tween_cross;
shape2Size = 200;
shape2Rotation = 0;
shape2Extension = 100;
shape2Centroid= [0,0];
shape2ExtensionAdjustment= 0;

wallThickness= 20;

isHollow = 1;

extrusionHeight= 100;
extrusionSlices = 30;
sliceAdjustment= 0;

sliceHeight = extrusionHeight * 1.0 / extrusionSlices;

difference()
{
  tweenLoft(shape1, shape1Size, shape1Rotation, shape1Centroid, shape1Extension,
            shape2, shape2Size, shape2Rotation, shape2Centroid, shape2Extension,
            shape2ExtensionAdjustment,
            extrusionSlices, sliceHeight, sliceAdjustment, wallThickness/2, isHollow);

  translate ([0,0,150]) rotate ([0,90,0]) cylinder (500, 10, 10, center=true);
  translate ([0,0,150]) rotate ([90,90,0]) cylinder (500, 10, 10, center=true);
}

