# Geometry Command Reference

This document describes the syntax of the GenerativeGX Intermediate Representation (hereafter the IR). The IR is the declarative command language produced by the LLM. It is not the solver's internal representation. Some IR commands (segments, congruence, intersection) expand into primitive objects and constraints before solving.

Primitive objects:
 * point (2 DOF)
 * line  (2 DOF)
 * circle (3 DOF)

## General line grammar

- One command per line.
- **Comments:** a line is ignored only if its **first character** is `#` (column 1). Inline comments are **not** supported.
- **Object names are case-sensitive** (e.g., `A` and `a` are different).
- Tokens are whitespace-separated. Quoted tokens use C++ `std::quoted` syntax, e.g. `"like this"`.

## Positional arguments vs. options (`key=value`)

- After the command keyword, each remaining token is either:
  - a **positional argument**, or
  - an **option** of the form `key=value`.
- If a positional argument needs to contain `=` (common for equation strings), it **must be quoted**.
  - Example: `equation L "y=x"` (unquoted `y=x` would be parsed as an option).
- Option keys are **case-sensitive**; use lowercase (`visible`, `color`).
- All construction commands accept these common options:
  - `visible=true|false` (default: `true`)
  - `color=<string>` (default: empty)
  
- **Example:**
```
point A color=red
point B visible=false
```

---

## Naming rules

These rules are enforced by CoreGX and will produce errors if violated.

### Point names
- Must begin with an **uppercase Latin letter** (A–Z) or an **uppercase Greek letter** (Α–Ω, Unicode 0x0391–0x03A9).
- May be followed by any combination of: digits, lowercase letters, or underscores (`_`).
- Valid examples: `A`, `B3`, `P_1`, `Α` (Greek alpha).
- Invalid examples: `a` (lowercase first letter), `1A` (digit first), `AB` (two uppercase letters — that is a segment name).

### Segment names
- A segment name is any string that can be split at some position into two valid point names. The two parts must be different from each other.
- Segment names using undeclared points will create those points.
- Valid examples: `AB`, `AC`, `DZ0`, `A4A5`, `B9B11`.
- A string that matches the segment-name pattern **cannot** be used as the name for a non-segment object.

### Circle names
- Must be of the form **`C`** followed by a non-negative integer with no leading zeros (`C0`, `C1`, `C2`, …).
- Must be the **next available index**: `Cn` is only valid if `C0` through `C(n-1)` already exist. For example, `C2` is invalid if `C1` has not yet been created. If a point named `C1` exists, circle indices skip that number.
- Zero-padded names (e.g. `C01`) are rejected.

### All other object names (Vector, locus, envelope, function, conic, transform names)
- Must **not** match the segment-name pattern (i.e. cannot be split into two valid point names) to avoid collisions.
- Must not already be used by another object.

---

## 1. Basic shapes

### point

- **Syntax:**
  `point <pointName> [key=value options...]`

- **Description:**
  Creates a point with the given name.

### line

- **Syntax:**
  `line <lineName> [key=value options...]`

- **Description:**
  A line is declared by name only. This creates an abstract line with no points attached. Points may later be constrained to lie on the line using incidence or other constraints. The solver positions the line to satisfy all constraints in the figure.

- **Example:**
```
line L1 color=gray
line D
reflectiontransform R D
transformimage L2 R L1
```

### segment

- **Syntax:**
  `segment <point1> <point2> [key=value options...]`

- **Description:**
  `segment` creates a line object together with the two point objects and two incidence constraints that place the points on that line. Segments do not introduce a new primitive geometry type; they are shorthand for a line plus two incidences. The solver may move either endpoint or both to satisfy other constraints.
  If `<point1>` or `<point2>` do not exist, they are created automatically.
  The segment automatically acquires the name `<point1><point2>` or `<point2><point1>`, whichever puts the end points in canonical order.
  Because segment naming conditions are unambiguous, segments may be implicitly declared by referencing a segment name without prior declaration. This will cause the segment and its component points to be created, if they do not exist. 

  Examples in canonical order are `AC`, `DZ0`, `A4A5`, `B9B11`.

- **Example:**
```
segment A B
```


### triangle

- **Syntax:**
  `triangle <vertex1> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Defines a triangle with vertices `<vertex1>`, `<vertex2>`, and `<vertex3>`. This translates directly into creating three line segments.
  - Each vertex must be a distinct point. Vertices may be existing points or unused point names.

- **Example:**
```
triangle A B C color=green
```

### polygon

- **Syntax:**
  `polygon <vertex1> <vertex2> <vertex3> ... <vertexN> [key=value options...]`

- **Description:**
  Constructs a polygon whose vertices are listed in order. The command implicitly creates the segments between consecutive vertices and the closing segment from `<vertexN>` to `<vertex1>`.
  - Each vertex must be a distinct point. Vertices may be existing points or unused point names.

- **Example:**
```
polygon A B C D
```

### cyclicpolygon

- **Syntax:**
  `cyclicpolygon <circleName> <centerName> <vertex1> <vertex2> ... <vertexN> [key=value options...]`

- **Description:**
  Constructs a polygon whose vertices all lie on a common circle (a cyclic polygon). Creates the circle as well as the polygon.
  `<circleName>` is the name of the circle, and `<centerName>` the name of its center.
  - `<centerName>` must be a valid, **unused** point name.
  - Each vertex must be a distinct point. 

- **Example:**
```
cyclicpolygon C0 O A B C D
```

### vector

- **Syntax:**
  `vector <vectorName> <point1> <point2> [key=value options...]`

- **Description:**
  Creates a named vector from `<point1>` to `<point2>`.
  - `<vectorName>` must not match the segment-name pattern and must be an unused name.

- **Example:**
```
vector v A B
```

---

## 2. Circle Constructions

### circumcircle

- **Syntax:**
  `circumcircle <circleName> <centerName> <vertex1> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Constructs the circumcircle of triangle `<vertex1>`, `<vertex2>`, `<vertex3>`.
  - `<circleName>` must be an unused circle name.
  - `<centerName>` must be a valid, **unused** point name.
  
- **Example:**
```
triangle A B C
circumcircle C0 O A B C
```

### incircle

- **Syntax:**
  `incircle <circle_name> <center_name> <tangency_point> <vertex1> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Constructs the incircle (tritangent circle) of triangle `<vertex1>`, `<vertex2>`, `<vertex3>`.
  - `circle_name` must be an unused circle name.
  - `center_name` must be a valid, **unused** point name, for the circle's center point
  - `tangency_point`: must be a valid, **unused** point name, for the contact point on side `vertex2`–`vertex3`

- **Example:**
```
triangle A B C
incircle C0 O U A B C
```

### excircle

- **Syntax:**
  `excircle <circle_name> <center_name> <tangency_point> <vertex1> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Constructs the excircle (tritangent circle) of triangle `<vertex1>`, `<vertex2>`, `<vertex3>`, external to the side `vertex2`–`vertex3`.
  - `circle_name` must be an unused circle name.
  - `center_name` must be a valid, **unused** point name, for the circle's center point
  - `tangency_point`: must be a valid, **unused** point name, for the contact point on side `vertex2`–`vertex3`
  
- **Example:**
```
triangle A B C
excircle C0 O V A B C
```


### circle

- **Syntax:**
  `circle <circleName> <center> <pointOnCircle> [key=value options...]`

- **Description:**
  Constructs a circle with the given center and, optionally, a point on the circle.
  - `<circleName>` must satisfy circle-naming rules and be unused. `<circleName>` must be of the form `Cn`, where `n` is the first available number. If there are three circles they must have the names `C0`, `C1`, and `C2`, in order of creation. If a point with the name `C1` exists, the circles must be `C0`, `C2`, and `C3`.
  - `<center>` must be a valid point name; may be new or existing.
  - `<pointOnCircle>` (optional third argument) must be a valid point name; may be new or existing.
 

- **Example:**
```
# Circle with a center and circumference point
circle C0 O A
# Circle with just a center point
circle C1 J
```

---

## 3. Derived points and lines


### midpoint

- **Syntax:**
  `midpoint <midpointName> <point1> <point2> [key=value options...]`

- **Description:**
  Creates the midpoint of segment `<point1>`–`<point2>` and labels it `<midpointName>`, with optional properties.
  - `<midpointName>` must be a valid, **unused** point name.

- **Example:**
```
segment A B
midpoint N A B
```

### pointonsegment

- **Syntax:**
  `pointonsegment <pointName> <segmentName> [key=value options...]`

- **Description:**
  Creates a point on the given segment.
  `pointonsegment` is a construction and should only be used when introducing a new point.
  To constrain an existing point to lie on a segment (or other curve), use the `incident` constraint.
  - `<pointName>` must be a valid, **unused** point name.

- **Example:**
```
segment A B
pointonsegment G AB
```

### intersection

- **Syntax:**
  `intersection <pointName> <object1> <object2> [other=<knownPoint>] [key=value options...]`

- **Description:**
  Creates point `<pointName>` at the intersection of `<object1>` and `<object2>`. Internally: it creates a point plus two incidence constraints.
  Intersection may place the intersection point on the line defined by a segment, but not the segment itself. If a point must be on the segment itself, use `pointonsegment`.
  If the option `other=<knownPoint>` is present and there are two intersections (typically when a circle is involved), GenerativeGX selects the intersection point **other than** `<knownPoint>`.
  - `<pointName>` must be a valid, **unused** point name. Intersection is a construction and cannot be applied to existing points.
  - `<object1>` and `<object2>` must each be one of: a valid segment name (implicitly created if absent but both constituent points must exist), or an existing **line, vector, circle, conic, locus, polar function, parametric curve, function, or envelope**. Points are not accepted. Non-existent names that do not match the segment pattern are not accep

- **Example:**
```
segment A B
segment C D
intersection I AB CD
```

### altitude

- **Syntax:**
  `altitude <footPointName> <vertex> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Draws the altitude from `<vertex>` to segment `<vertex2>`–`<vertex3>`.
  - `<footPointName>`: must be a valid, **unused** point name, for the foot of the perpendicular

- **Example:**
```
triangle A B C
altitude E A B C color=blue
```

### project

- **Syntax:**
  `project <footPointName> <point> <line> [key=value options...]`

- **Description:**
  Draws the projection of point `<point>` onto line `<line>`, extending the line if necessary.
  - `<footPointName>` must be a valid, **unused** point name.
  - `<line>` must be a valid segment name (implicitly created if absent) or an existing line or vector.
  
- **Example:**
```
point P
segment A B
project D P AB
```

### median

- **Syntax:**
  `median <footPointName> <vertex> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Draws the median from `<vertex>` to side `<vertex2>`–`<vertex3>`. `<footPointName>` is the label for the foot of the median. The resulting line segment will have the name `<footPointName><vertex>`, or vice-versa; referring to the line segment by just `<footPointName>` will fail.
   - `<footPointName>` must be a valid, **unused** point name (checked after the other points are created).

- **Example:**
```
triangle A B C
median E A B C
```

### anglebisector

- **Syntax:**
  `anglebisector <lineName> <vertex1> <vertex2> <vertex3> [key=value options...]`

- **Description:**
  Constructs the angle bisector at `<vertex2>` of triangle `<vertex1><vertex2><vertex3>`, i.e., the bisector of the angle at `<vertex2>` between segments `<vertex2><vertex1>` and `<vertex2><vertex3>`, with optional properties.
  - `<lineName>` must **not** match the segment-name pattern and must be unused.

- **Example:**
```
triangle A B C
# bisector at B of triangle ABC
anglebisector L1 A B C
# external bisector at B of triangle ABC
anglebisector L2 A B C external=true
```

### perpendicularbisector

- **Syntax:**
  `perpendicularbisector <lineName> <point1> <point2> [key=value options...]`

- **Description:**
  Constructs the perpendicular bisector of segment `<point1>`–`<point2>`, with optional properties.
  - `<lineName>` must **not** match the segment-name pattern and must be unused.

- **Example:**
```
segment A B
perpendicularbisector L1 A B
```

### parallel

- **Syntax:**
  `parallel <line1> <line2>`

- **Description:**
  `parallel <line1> <line2>` asserts that `<line1>` and `<line2>` are parallel. It does not construct new lines, extend lines, or create intersection points. The solver positions the lines to satisfy the constraint.
  - Each argument must be a valid segment name or an existing line or vector. 

- **Example:**
```
polygon A B C D
parallel AB CD
parallel AD BC
```

### congruent

- **Syntax:**
  `congruent <segment1> <segment2>`

- **Description:**
  Declares segments `<segment1>` and `<segment2>` as congruent. Internally becomes a constraint between four points (or three if segments share an endpoint). No midpoints or bisectors are created.

- **Example:**
```
triangle A B C
congruent AB BC
```

### incident

- **Syntax:**
  `incident <object1> <object2>`

- **Description:**
  Asserts that point `<object1>` lies on object `<object2>` (line, circle, segment's underlying line, curve, conic). Does not create intersection points automatically.
  - Each resolved object must be one of: **point, line, vector, segment, circle, conic, locus, polar function, parametric curve, function, or envelope**. Variables and transforms are not accepted.

- **Example:**
```
point A
segment B C
incident A BC
```

### tangent

- **Syntax:**
  `tangent <object1> <object2>`

- **Description:**
  Tangent is a geometric constraint, not a construction. It does not create points, does not draw tangent lines, and does not compute common tangents.
  `tangent <object1> <object2>` asserts that the two objects touch at exactly one point. It does not specify or construct the point of tangency. The solver determines how to position the objects to satisfy the tangency relation.
  Tangency may be applied between a circle and a line, or a circle and a circle. Tangency does not imply sidedness. Branch selection for common tangents is handled separately.
  Note that when a segment is a tangency object, it is applied to the underlying line, not the portion of the line defined by the segment, and the intersection point may be outside the segment.
  - Each resolved object must be one of: **line, vector, segment, circle, conic, locus, polar function, parametric curve, function, or envelope**. Points are not accepted.

- **Example:**
```
circle C0 O
segment A B
tangent AB C0
```

---

## 4. Relationship constraints

These commands add constraints between already-named objects (segments, lines, circles, points). They do not usually create new points by themselves.

### perpendicular

- **Syntax:**
  `perpendicular <object1> <object2>`

- **Description:**
  `perpendicular <object1> <object2>` asserts a right-angle relation between lines. It does not create points or auxiliary constructions.
  - Both arguments must either be valid segment names or existing lines or vectors.

### sameside / oppositeside

- **Syntax:**
  `sameside <point1> <point2> <lineOrSegment>`
  `oppositeside <point1> <point2> <lineOrSegment>`

- **Description:**
  Asserts that `<point1>` and `<point2>` are on the same or opposite sides of the line described by `<lineOrSegment>`.
  - `<lineOrSegment>` either be a valid segment names or an existing line or vector.

### inside / outside

- **Syntax:**
  `inside <point> <circle>`
  `outside <point> <circle>`

- **Description:**
  - `<circle>` must be an existing **circle or conic** (circle, eclipse, parabola, or central conic).

### circleinside / circleoutside / circleoverlaps

- **Syntax:**
  `circleinside <circle0> <circle1>`
  `circleoutside <circle0> <circle1>`
  `circleoverlaps <circle0> <circle1>`

- **Description:**
  `circleinside` constrains `circle0` to be inside of `circle1`. `circleoutside` constrains the circles to be wholly outside of each other. `circleoverlaps` constrains the circles to overlap, being partially inside and partially outside of each other.
  - Both `<circle0>` and `<circle1>` must be **existing circles**. 

### convex

- **Syntax:**
  `convex <point1> <point2> <point3> ... <pointN>`

- **Description:**
  `convex A B C D` will try to put points A B C D in a position such that the resulting polygon is convex. This specifies only the cyclic order of the listed points. It does not create polygons or edges. It asserts ordering, not geometry.
  
### concave

- **Syntax:**
  `concave <point1> <point2> <point3> ... <pointN>`

- **Description:**
  `concave A B C D` will try to put points A B C D in a position such that the resulting polygon is non-convex. This specifies only the cyclic order of the listed points. It does not create polygons or edges. It asserts ordering, not geometry.
  
- **Example:**

A concave kite:
```
polygon A B C D
congruent AB BC
congruent CD DA
concave A B C D
```
  
### acute

- **Syntax:**
  `acute <point0> <point1> <point2>`

- **Description:** 
  Constrains the angle defined by `<point0>`, `<point1>` and `<point2>` to be less than 90 degrees.
  Angle names use the 3-point form only: `acute A B C`.
  
### obtuse

- **Syntax:**
  `obtuse <point0> <point1> <point2>`

- **Description:** 
  Constrains the angle defined by `<point0>`, `<point1>` and `<point2>` to be greater than 90 degrees.
  Angle names use the 3-point form only: `obtuse A B C`.

---

## 5. Numeric and equation constraints

These commands take expression strings. If an argument contains spaces or `=`, quote it.

### coordinates

- **Syntax:**
  `coordinates <point> <x> <y> [key=value options...]`

- **Description:**
  Declares that a point has fixed Cartesian coordinates. The expressions may be numeric literals, indeterminates, or algebraic expressions. Indeterminates are symbolic placeholders; the solver may assign them numeric values for clarity, but must preserve all symbolic relationships.
  Creates point `<point>` if it does not exist.

- **Example:**
```
coordinates P 4 6
coordinates R t t^2
```

### coefficients

- **Syntax:**
  `coefficients <line> <A-expression> <B-expression> <C-expression> [key=value options...]`

- **Description:**
  Declares that the line satisfies `Ax + By + C = 0`. Expressions may include numbers, indeterminates, or algebraic combinations. May be rewritten into `slope` or `direction` constraints when this produces a simpler or more canonical representation.
  - `<line>` must be a valid segment name or an existing line or vector.

### distance

- **Syntax:**
  `distance <object0> <object1> <d>`

- **Typechecking:**
  - Requires exactly 3 positional arguments.

- **Description:**    
  A constraint between two objects. Does not create a segment or any other construction.
  - Both `<object0>` and `<object1>` must each be a valid segment name or an existing **point, line, vector, or circle**.
   
### angle

- **Syntax:**
  `angle <point0> <point1> <point2> <theta>`

- **Description:** 
  Constrains the angle ABC. Internally it becomes a constraint between the lines BA and BC. No bisectors or auxiliary lines are created.
  Before an angle in degrees can be specified, the `anglemode degree` command must be run.
  - The segments `<point1><point0>` and `<point1><point2>` are created if absent.

- **Example:**
Two line segments with an 89 degree angle between them.
```
anglemode degree
segment A B
segment A C
angle B A C 89
```

### radius

- **Syntax:**
  `radius <circle> <r>`

- **Description:**
  Creates a radius constraint for `<circle>`. The solver may move the center, the radius point, or both to satisfy it.
  - `<circle>` must be an **existing circle**.

### slope

- **Syntax:**
  `slope <lineOrSegment> <m>`

- **Description:**
  Fixes the gradient of the line. This is a direction-fixing constraint: it fixes the direction of a line but not its location.
  - `<lineOrSegment>` is must be a valid segment name, or an existing line or vector.

- **Example:**
```
line l0
slope l0 1
```

### direction

- **Syntax:**
  `direction <lineOrSegment> <dir>`

- **Description:**
  Fixes the angle of the line measured counterclockwise from the positive x-axis. This is a direction-fixing constraint: it fixes the direction of a line but not its location.
  - `<lineOrSegment>` is must be a valid segment name, or an existing line or vector.

- **Example:**
```
anglemode degree
line l2
direction l2 120
```

### parametric

- **Syntax:**
  `parametric <point> <object> <t> [key=value options...]`

- **Description:**
   Creates or places `<point>` at parameter position `<t>` along `<object>`, where `<t>` is a value between 0 and 1 representing proportional distance from the start to the end of the object. If `<object>` is a circle or conic, `<t>` will instead be an angle in radians (regardless of degreemode) around the circle or conic, between `0` and `6.2831853`.
   Use `parametric` when the position of a point along an object needs to be symbolically or numerically fixed. For a free point that simply lies somewhere on an object, `pointonsegment` or `incident` are simpler choices.
	- `<object>` must either be a valid segment name, or an existing **line, vector, circle, conic, locus, polar function, parametric curve, function, or envelope**. Points are not accepted.
	- `<t>` must be an expression or literal, not a range

- **Example:**
```
segment A B
parametric P AB 0.25
```

### equation

- **Syntax:**
  `equation <object> <eqn>`

- **Description:**
  Attaches an explicit algebraic equation to a line or circle. The equation is parsed symbolically and may involve numbers, indeterminates, and algebraic expressions. May be rewritten into simpler primitive constraints (such as `slope`, `coefficients`, or center/radius) when this yields a clearer representation.
  - `<object>` must either be a valid segment name, or an existing **line, vector, circle, conic, locus, polar function, parametric curve, function, or envelope**. Points are not accepted.

- **Example:**
```
line L
equation L "y=x"
circle C0 O E
equation C0 "(x-1)^2+(y+2)^2=9"
```

---

## 6. Transforms

Transformations are constraints, not constructions. They do not inherently move geometry; instead they express geometric relationships. If a transformation depends on a parameter, then applying it to an object produces parameter-dependent geometry, which may be used in locus or envelope constructions, or animations. Motion arises only when a parameter varies; transformations themselves do not define motion.

### reflectiontransform

- **Syntax:**
  `reflectiontransform <transformName> <line>`

- **Description:**
  Creates a transformation object representing reflection across the given line. If the mirror line depends on parameters, the transformation depends on those parameters. Applying the transformation to an object produces its reflection across the line.
  - `<transformName>` must be an unused name.
  - `<line>` must be a valid segment name or an existing line or vector.

### rotationtransform

- **Syntax:**
  `rotationtransform <transformName> <centerPoint> <theta>`

- **Typechecking:**
  - Requires exactly 3 positional arguments.

- **Description:**
  Creates a transformation object representing rotation about the given center point by the given angle expression. The angle expression follows the global `anglemode` rules. `rotationtransform` contributes evidence to the global anglemode decision but is not determinative by itself.
  - `<transformName>` must be an unused name.

### dilationtransform

- **Syntax:**
  `dilationtransform <transformName> <centerPoint> <scale>`

- **Description:**
  Creates a transformation object representing dilation about the given center point with the given scale factor. The scale expression may be numeric, symbolic, or parameter-dependent. A dilation with scale factor −1 about a point is exactly reflection in that point.
  - `<transformName>` must be an unused name.

### translationtransform

- **Syntax:**
  `translationtransform <transformName> <vectorName>`
  
- **Description:**
  Creates a transformation object representing translation by the given vector. If the vector depends on parameters, the transformation depends on those parameters. A vector is a directed segment created with the `vector` command.
  - `<transformName>` must be an unused name.
  - `<vectorName>` must be an **existing vector**.

- **Example:**
```
vector v A B
point C
translationtransform T v
transformimage C T B
```

### transformimage

- **Syntax:**
  `transformimage <imageName> <transformName> <objectName> [key=value options...]`

- **Description:**
  Asserts that `<imageName>` is the image of `<objectName>` under transformation `<transformName>`. In functional notation: `image = transform(original)`. Does not move the original object; creates a new object defined by the transformation.
  - `<transformName>` must be an **existing transformation** (reflection, rotation, dilation, or translation).
  - `<objectName>` must be an **existing construction**.
  - `<imageName>` must be consistent with the type of `<objectName>`:
    - **Point object** → `<imageName>` must be a valid point name; may be new or existing.
    - **Line object** → `<imageName>` must be a valid line or segment name; may be new or an existing line, segment, or vector (line-like objects are mutually interchangeable as transform targets).
    - **Segment object** → `<imageName>` must be a valid segment name, or an existing line/vector.
    - **Circle object** → `<imageName>` must satisfy circle-naming rules or already be an existing circle; a new circle center is created automatically if needed (with a point name derived by appending `'` to `<objectName>`'s center point name.
    - **Vector object** → `<imageName>` may be an existing vector, existing line, or unused symbol. If it is an unused symbol, a new vector/segment will be created, with point names derived from `<objectName>`'s point names (appending `'`).
    - **Locus/envelope/function objects** → `<imageName>` must not match the segment-name pattern and must be unused.
    - Mixing incompatible types (e.g. reflecting a point into a name that already exists as a circle) is an error.

---

## 7. Curves: locus, envelope, function

### locus

- **Syntax:**
  `locus <name> <point> <t> [t0] [t1] [key=value options...]`

- **Description:**
  Creates the locus curve traced by `<point>` as the parameter `<t>` varies. The point must depend on the parameter directly or indirectly — the parameter may appear in distance constraints, angle constraints, or any other geometric constraint, and need not appear directly in the coordinates of the point. 

  When a problem states that certain points are fixed but at indeterminate coordinates, encode them with symbolic coordinates:
```
point A
coordinates A xA yA
```
  Fixed objects must not be given numeric coordinates unless the user explicitly specifies them.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - `<t0>` and `<t1>` (optional), if supplied, must be parseable as real numeric literals (not expressions). If omitted, the system chooses default bounds `t0=0.0`, `t1=6.2831853`.


### envelope

- **Syntax:**
  `envelope <name> <lineOrCurve> <t> [t0] [t1] [key=value options...]`

- **Description:**
  Creates the envelope curve of a one-parameter family of lines or curves. The line or curve must depend on the parameter directly or indirectly.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - `<lineOrCurve>` must be a valid segment name or an **existing line, vector, or circle**.
  - `<t0>` and `<t1>` (optional), if supplied, must be parseable as real numeric literals (not expressions). If omitted, the system chooses default bounds `t0=0.0`, `t1=6.2831853`.

### function

- **Syntax:**
  `function <name> <expression> [t0] [t1] [key=value options...]`

- **Description:**
  Defines a curve as the graph of a function `y = f(x)`. The expression may be numeric, symbolic, parameter-dependent, or may involve generic functions. If `t0` and `t1` are supplied, they define the finite domain of the function; if omitted, the system chooses a default domain.

  The system supports two kinds of genericity:

  - **Parameterized functions.** If the expression includes symbolic parameters, the system treats the curve as a family of analytic objects (e.g., `x^3 + a*x` defines a family of cubic curves parameterized by `a`). Symbolic parameters are not assigned numeric values unless required by a constraint.
  - **True generic functions.** The expression may be a generic function `f(x)`, where `f` is an unspecified analytic function. The system treats `f` as an unknown differentiable function and finds a sensible visual representation consistent with any constraints imposed on `f`. Generic functions may appear anywhere in expressions, including coordinate definitions, distances, directions, and other constraints.

  If the equation contains spaces or `=`, quote it.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - `<t0>` and `<t1>` (optional), if supplied, must be parseable as real numeric literals (not expressions). If omitted, the system chooses default bounds `t0=0.0`, `t1=6.2831853`.

- **Example:**
```
function g f(x)
```

### polarfunction

- **Syntax:**
  `polarfunction <name> <equation> [t0] [t1] [key=value options...]`

- **Description:**
  Defines a curve in polar coordinates `r = f(theta)`. The expression may be numeric, symbolic, parameter-dependent, or may involve generic functions. The global `anglemode` rules apply to the interpretation of theta. If `theta0` and `theta1` are supplied, they define the finite domain; if omitted, the system chooses a default domain. If the equation contains spaces or `=`, quote it.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - `<t0>` and `<t1>` (optional), if supplied, must be parseable as real numeric literals (not expressions). If omitted, the system chooses default bounds `t0=0.0`, `t1=6.2831853`.

### parametriccurve

- **Syntax:**
  `parametriccurve <name> <xEquation> <yEquation> [t0] [t1] [key=value options...]`

- **Typechecking:**
  - Requires at least 1 positional argument; 3 or more are needed to produce meaningful output.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - The combined expression `(<xEquation>,<yEquation>)` must parse as a vector expression.
  - `<t0>` and `<t1>` (optional) must be parseable as `double` literals.

- **Description:**
  Defines a curve parametrically as `(x(t), y(t))`. The expressions may be numeric, symbolic, parameter-dependent, or may involve generic functions. If either equation contains spaces or `=`, quote it.
  - `<name>` must **not** match the segment-name pattern and must be unused.
  - `<t0>` and `<t1>` (optional), if supplied, must be parseable as real numeric literals (not expressions). If omitted, the system chooses default bounds `t0=0.0`, `t1=6.2831853`.

  A `function`, `polarfunction`, or `parametriccurve` may be used as input to `transformimage`. The result is a new curve defined by applying the transformation to every point of the original curve. If the transformation depends on a parameter, the transformed curve becomes parameter-dependent.

---

## 8. Variables and animation

### animate

- **Syntax:**
  `animate <t> [t0] [t1] [duration] [repeats] [style=cycling|toandfro|singleshot]`

- **Description:**
  Creates an animation by varying parameter `<t>`.
  - `<t0>`, `<t1>`, `<duration>`, `<repeats>` (optional) must each be parseable as `double` literals. `<t0>` defaults to `0.0`, `<t1>` defaults to `6.2831853`, `<duration>` defaults to `5.0` (seconds), and `repeats` defaults to `0` (loop continuously), and `style` defaults to `cycling`.
  - Only **one** animation may be declared per program; a second `animate` command results in an error.

### value

- **Syntax:**
  `value <name> <t> [t0] [t1] [key=value options...]`

- **Description:**
  Sets variable `<name>` to a value of `<t>`, varying within a range between `t0` and `t1`.
  - `<name>` must be an unused name (duplicate names are rejected).
  - `<t>`, `<t0>`, `<t1>` must each be parseable as `double` literals.
  
---

## 9. Conics

### ellipse

- **Syntax:**
  `ellipse <name> <foci0> <foci1> <perimeterpoint> [key=value options...]`

- **Description:**
  - `<name>` must **not** match the segment-name pattern and must be unused.


### hyperbola

- **Syntax:**
  `hyperbola <name> <f0> <f1> <pp> [key=value options...]`

- **Description:**
  - `<name>` must **not** match the segment-name pattern and must be unused.


### parabola

- **Syntax:**
  `parabola <name> <focus> <vertex> [key=value options...]`

- **Typechecking:**
  - `<name>` must **not** match the segment-name pattern and must be unused.

---

## 10. Meta Commands

### anglemode

- **Syntax:**
  `anglemode <degree/radian>`

- **Description:**
  Allows selection of degrees or radians for displayed angle measurements. Angle mode is a global setting for the entire problem. Set `anglemode` exactly once per problem; never mix degrees and radians or switch modes mid-problem.

### arbitrarypoints

- **Syntax:**
  `arbitrarypoints <polar|cartesian>`

- **Description:**
  Sets whether arbitrary points use polar or cartesian form.

### displayproperties

- **Syntax:**
  `displayproperties <object1> ... <objectN> [key=value options...]`

- **Description:**
  Allows display properties to be declared for multiple already-existing objects in one line. Overwrites previously-set display properties.

- **Example:**
```
vector v A B
point C
displayproperties v C color=blue
```

### measure

- **Syntax:**
  `measure <expression>`

- **Description:**
  Evaluates a geometric or algebraic expression and displays the result in addition to the diagram. The expression may reference named geometric objects (points, segments, lines, circles, curves), parameters, or any combination of supported measurement functions. Results update dynamically when the referenced objects move or parameters change. If the expression contains spaces, quote it.
  Measure statements cannot be used as values in other constraints or constructions. For instance, `radius C0 distance(A,B)` is invalid. The proper way of doing this is to create a distance constraint and a radius constraint to the same variable or value.
  
- **Example:**
```
triangle A B C
distance A B c
distance A C b
distance B C a
measure area(A,B,C)
measure distance(A,BC)
measure "distance(A,BC)*distance(B,AC)*distance(C,AB)"
```

**Supported geometry functions:**

| Function | Description |
|---|---|
| `angle(A,B,C)` | Angle ABC |
| `angle(AB,CD)` | Angle between segments AB and CD |
| `angle(L0,AB)` | Angle between line L0 and segment AB |
| `angle(L0,L1)` | Angle between lines L0 and L1 |
| `area(A,B,C,D)` | Area of polygon ABCD |
| `area(C0)` | Area of circle C0 |
| `coefficients(AB)` | Coefficients of vector AB |
| `coordinates(A)` | Coordinates of point A |
| `direction(A,B)` | Slope of a line from A to B |
| `direction(AB)` | Slope of segment AB |
| `direction(L0)` | Slope of line L0 |
| `distance(A,B)` | Distance from point A to point B |
| `distance(A,BC)` | Perpendicular distance from point A to segment BC |
| `distance(A,L0)` | Perpendicular distance from point A to line L0 |
| `equation(AB)` | Equation of the line AB |
| `equation(L0)` | Equation of line L0 |
| `equation(C0)` | Equation of circle C0 |
| `equation(K0)` | Equation of curve K0 |
| `length(AB)` | Length of segment AB |
| `parametricequations(AB)` | Parametric equations of line AB |
| `parametricequations(L0)` | Parametric equations of line L0 |
| `parametricequations(C0)` | Parametric equations of circle C0 |
| `parametricequations(K0)` | Parametric equations of curve K0 |
| `perimeter(A,B,C,D)` | Perimeter of polygon ABCD |
| `perimeter(C0)` | Perimeter of circle C0 |
| `radius(C0)` | Radius of circle C0 |
| `slope(A,B)` | Slope of a line from A to B |
| `slope(AB)` | Slope of segment AB |
| `slope(L0)` | Slope of line L0 |

**Supported engineering functions:**

| Function | Description |
|---|---|
| `centroid(A,B,C,D)` | Centroid of polygon ABCD |
| `Ix(A,B,C,D)` | Area moment of inertia about axis through centroid, parallel to x-axis |
| `Ixy(A,B,C,D)` | Area product of inertia about the centroid |
| `Iy(A,B,C,D)` | Area moment of inertia about axis through centroid, parallel to y-axis |

Measurement expressions may also use standard math functions (`sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`, `sinh`, `cosh`, `tanh`, `sqrt`, `abs`, `signum`, `exp`, `log`, `ln`, `ceil`, `floor`) and arithmetic operators to form compound expressions such as `distance(A,BC)*distance(B,AC)*distance(C,AB)`.