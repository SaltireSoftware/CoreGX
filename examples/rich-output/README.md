# CoreGX Rich Output Examples

This folder contains pipeline examples showing how to extract different types of output from CoreGX programs. Each example demonstrates a different way that developers can use the CoreGX output and transform it into another format.

The pipelines can be modified by adding functionality directly to the Python scripts. Developers can extend these examples to extract multiple output types at once, combine outputs, or send the generated content into another application such as a webpage or visualization system.

Example output types include:

- JSON equations extracted from CoreGX measurements.
- TeX equations for mathematical rendering.
- DXF files for CAD workflows.
- Full JSON output from the CoreGX API.
- SVG output for diagrams and drawings.
- Animated SVG output when the CoreGX program contains an animation.
- XML output, which can be imported into GXWeb.
- Web app output for an automatic CoreGX-generated web application. 

The examples are intended as starting points for developers building custom workflows around CoreGX. The Python scripts can be adapted to extract additional information from the CoreGX response or to connect CoreGX output to other tools and applications.

More information about the CoreGX API can be found at:

https://coregx.dev/dev/index.html