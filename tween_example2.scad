
use <tween_loft.scad>
include <tween_shapes.scad> 

shape1= tween_circle;
shape1Size = 200;
shape1Rotation= 0;
shape1Extension= 140;
shape1Centroid = [0,0]; 

shape2= tween_circle;
shape2Size = 50;
shape2Rotation= 0;
shape2Extension= 150;
shape2Centroid = [0,0]; 
shape2ExtensionAdjustment = 0; 

wallThickness= 20;

isHollow= 1;

extrusionHeight = 200;
extrusionSlices= 20;
sliceAdjustment = 0;

sliceHeight = extrusionHeight * 1.0 / extrusionSlices;

tweenLoft(shape1, shape1Size, shape1Rotation, shape1Centroid, shape1Extension,
          shape2, shape2Size, shape2Rotation, shape2Centroid, shape2Extension,
          shape2ExtensionAdjustment,
          extrusionSlices, sliceHeight, sliceAdjustment, wallThickness/2, isHollow);


