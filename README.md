# Subdivision Curves

### Content

This package provides modules to compute a few different types of subdivision curves as listed below.
* Lagrange Interpolation
* Hermite Interpolation
* B-Splines
* Hermite Splines
* Catmull-Rom Splines
* NURBS

Each module is carefully documented. If there are any errors, feel free to submit a PR. 

### Demo

There is also an included demo webapp built using Bokeh. If you have Bokeh installed, it can be run with the following command.

```bokeh serve --show interface.py```

The webapp allows users to select an algorithm, set points, and view the resulting curve. In the case of Hermite curves, the user also needs to provide a tangent vector to use with the curve. This can be done by using click-and-drag to draw a line. The starting point of the line is used as the control point. Although Hermite curves support taking higher order derivatives, this webapp only supports the first derivative due to limitations on input. 

### Surfaces

Subdivision curve algorithms can also be extended to support surfaces. Demos for these applications are coming soon. Additionally, there are algorithms that function solely on surfaces. Some such algorithms are Catmull-Clark and Loop subdivision. Code for these methods is also coming soon.

### Credits

The code for showing the convex hull on control points in the webapp is taken from Tomas Bouda.
