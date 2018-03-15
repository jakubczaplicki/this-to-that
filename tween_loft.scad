// Create either a hollow tube or a solid shape that lofts from one profile to another

include <tween_shapes.scad>

// The lower shape
shape1          = tween_star;
shape1Size      = 100;    // Size of the lower shape
shape1Rotation  = 0;      // Rotation of the lower shape
shape1Extension = 20;     // Extend the profile (space for tube clamp, etc.)
shape1Centroid  = [0,0];  // Location of center point


// The upper shape
shape2          = tween_heart;
shape2Size      = 100;    // Size of the upper shape
shape2Rotation  = 0;      // RotationSize of the upper shape
shape2Extension = 20;     // Extend the profile (space for tube clamp, etc.)
shape2Centroid  = [0,0];  // Location of center point

// Sometimes the top extension is disjoint from the top of the loft.
// This moves it downwards by n slices.
shape2ExtensionAdjustment = 0;

// Wall Thickness - higher values add material but will seal gaps
// If making a tube, the thickness is added to the exterior diameter
// This parameter has no effect if making a solid (non-hollow) object
wallThickness  = 20;
    
isHollow        = 1;   // If 1, create a tube.  If 0, create a solid.
extrusionHeight = 100; // Height of the loft
extrusionSlices = 10;
sliceAdjustment = 0;   // Ensure the slices intersect by this amount,
                       // needed if OpenSCAD is generating more than 2 volumes
                       // for an STL file
/* 
 The extrusionSlices determines the granularity. If this is too low, you may
 get gaps in the tube. These could be corrected by increasing the wall
 thickness. A thicker wall will compensate for gaps in the loft with no
 computation hit.

 Higher extrusionSlices are smoother, but are much more computationally
 intensive. OpenSCAD crashes if the slices are too high (and the tween_shapes
 are too complex).

 There is a balance between tween complexity and number of slices.
 The higher these numbers, the smoother the result (and the longer the
 computation time), but if too high, OpenSCAD crashes.

 You may want to reduce the complexity of the tween_shapes in the
 tween_generator.py python file. You may want to prototype with a small number
 and use a larger number for final production.

 For example, for a heart-->triangle tween
  unit_circle reference at 360, slices = 10  ---> Works OK, but chunky
  unit_circle reference at 360, slices = 15  ---> OpenSCAD crashes

  unit_circle reference at 128, slices = 15  ---> Works OK
  unit_circle reference at 128, slices = 60  ---> Works OK, smooth extrusion

 It will be much faster render to model with fewer extrusionSlices and
 a thicker wall. It will be a smoother model with more extrusionSlices and
 a thinner wall.
*/

// Calculate the height of each slice
sliceHeight = extrusionHeight * 1.0 / extrusionSlices;

// -------------------------------------------------------------------------------

// Weighted average works on both scalars (like a size) or vectors (like a grid of points)
function weightedAverage(item1, item2, weight) = item1 * (1.0 - weight) + (item2 * weight * 1.0);

// -----------------------------------------------------------------------------

// Percent takes two numbers and returns the percentage as a floating point number.
function percent (partial, whole) = partial * 1.0 / whole;

// -----------------------------------------------------------------------------

module tweenExtension (tween, tweenSize, tweenRot, extensionSize, thicknessRadius, hollow)
{
  // Create a straight extrusion of a tween profile (good for attaching to objects/clamps)
  linear_extrude(extensionSize)
  {
    if (hollow == 1)
    {
      difference()
      {
        // Create a shape with an extra thickness, then subtract the original
        minkowski()
        {
          scale([tweenSize, tweenSize, 0])
          rotate([0, 0, tweenRot])
          polygon(points = tween);
          circle(thicknessRadius); // Trace outside with circle, generating wall
        }
        // Original Shape
        scale([tweenSize, tweenSize, 0]) rotate ([0, 0, tweenRot])
        polygon (points = tween);
      }
    }
    else
    {
      // Original Shape
      scale ( [ tweenSize, tweenSize, 0]) rotate ([0, 0, tweenRot])
      polygon (points = tween);
    }
  }
}

// -----------------------------------------------------------------------------

module tweenLoft(tween1, tween1Size, tween1Rot, tween1Center, tween1Ext,
                 tween2, tween2Size, tween2Rot, tween2Center, tween2Ext,
                 tween2SliceAdjustment,
                 slices, sliceHeight, sliceAdjustment, thicknessRadius, hollow)
{
  // Create a Loft between two tweens - basically, a weighted average of two
  // shapes, as the weight increases it blends from one shape to the other.
 
  // Create the Loft
  for (i = [0 : slices])
  {
    // Move each slice upwards to build the shape
    translate([weightedAverage(tween1Center, tween2Center, percent (i, slices))[0],
               weightedAverage(tween1Center, tween2Center, percent (i, slices))[1], sliceHeight * i])
    {
      // Extrude each slice (slightly thicker, overlaps help ensure a manifold
      linear_extrude(sliceHeight + sliceAdjustment, center=true)
      {
        if (hollow == 1)
        {
          // Create a shaped tube
          difference()
          {
            // Create a shape with an extra thickness, then subtract the original
            minkowski()
            {
              // We increase the scale uniformly on both X and Y
              scale([weightedAverage( tween1Size, tween2Size, percent (i, slices)),
                     weightedAverage( tween1Size, tween2Size, percent (i, slices)), 0])
              rotate([0, 0, weightedAverage( tween1Rot, tween2Rot, percent (i, slices))])
              polygon(points = weightedAverage(tween1, tween2, percent (i, slices)));
              circle(thicknessRadius); // Trace outside with circle, generating wall
            }
            // Original Shape
            scale([weightedAverage( tween1Size, tween2Size, percent (i, slices)),
                   weightedAverage( tween1Size, tween2Size, percent (i, slices)), 0])
            rotate([0, 0, weightedAverage( tween1Rot, tween2Rot, percent (i, slices))])
            polygon(points = weightedAverage(tween1, tween2, (percent (i, slices))) );
          }
        }
        else
        {
          // Create a solid shape
          // Original Shape
          scale([weightedAverage( tween1Size, tween2Size, percent (i, slices)),
                 weightedAverage( tween1Size, tween2Size, percent (i, slices)), 0])
          rotate( [0, 0, weightedAverage( tween1Rot, tween2Rot, percent (i, slices))])
          polygon (points = weightedAverage (tween1, tween2, (percent (i, slices))));
        }
      }
    }
  }
  // --- End Loft, Create extensions (good for clamping, containing....) ---
  if (tween1Ext > 0)  // Create the extension of shape1, if needed
  {
    translate([tween1Center[0], tween1Center[1], sliceAdjustment - tween1Ext])
    tweenExtension(tween1, tween1Size, tween1Rot, tween1Ext, thicknessRadius, hollow);
  }
  if (tween2Ext > 0)  // Create the extension of shape2, if needed
  {
    translate([tween2Center[0], tween2Center[1], (sliceHeight * (slices - tween2SliceAdjustment))] )
    tweenExtension(tween2, tween2Size, tween2Rot, tween2Ext, thicknessRadius, hollow);
  }
}

// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------
// -----------------------------------------------------------------------------

// Generate the top level part
tweenLoft(shape1, shape1Size, shape1Rotation, shape1Centroid, shape1Extension,
          shape2, shape2Size, shape2Rotation, shape2Centroid, shape2Extension,
          shape2ExtensionAdjustment,
          extrusionSlices, sliceHeight, sliceAdjustment, wallThickness/2, isHollow);
