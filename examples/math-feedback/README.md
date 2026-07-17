# CoreGX Math Feedback Examples

This folder contains examples showing how CoreGX equations can be extracted from the output JSON and used for additional mathematical processing.

The `equations` field within the CoreGX output JSON contains equations corresponding to measurements made in the input CoreGX program. These equations may contain symbolic expressions, but they can also simplify to real number values when the constraints of the input program determine a fixed result.

The equations are provided in multiple formats, including:

- `valueTex` for TeX formatted output.
- `derive` for symbolic derivation-style expressions.
- `string` for a general symbolic representation.
- `python`, `javascript`, `cpp`, `c`, and other language-specific formats.
- MathML representations such as `displaymathml` and `contentmathml`.

Developers can extract the format that best matches the tool they want to use and perform additional computation as needed.

## Open-loop math

The examples in the `open-loop` folder demonstrate mathematical processing where a math result is calculated from CoreGX equations. 

Examples include:

- Differentiation to find critical points. 
- Computing symbolic limits.

These examples show how CoreGX measurements can be passed into symbolic math tools such as SymPy for additional analysis.

## Closed-loop math

The examples in the `closed-loop` folder demonstrate workflows where mathematical results are fed back into CoreGX.

Examples include:

- Optimizing the maximum area of a rectangle, substituting the optimal values back into the original CoreGX program, and rndering the resulting optimized geometry.
- Optimizing the maximum area of a triangle, substituting the optimal values back into the original CoreGX program, and rndering the resulting optimized geometry.

Developers can adapt these pipelines by editing the math scripts. These scripts' names begin with `equations` because their input is an equations JSON object. They can be modified to perform different operations in SymPy or another mathematical tool depending on the equation format being used.

The final output stage can also be changed. For example, instead of producing an SVG, a developer could output XML, JSON, or another format for use in a different application.

These examples demonstrate how CoreGX can provide mathematically constrained geometry that can then be analyzed, optimized, and used as input for further automated workflows.