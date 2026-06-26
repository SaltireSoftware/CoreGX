# Authoring CoreGX Programs from Natural Language

How to translate an English geometry problem, theorem, or description into a
CoreGX program. Read this alongside `syntax.md` (the command reference) and the
summary in `SKILL.md`.

## How CoreGX thinks

CoreGX is a hybrid system — **not** a symbolic/algebraic constraint solver, and
**not** a pure Euclidean construction engine:

1. Every "construction" command is shorthand for a geometric relation — all
   constructions become constraints.
2. The solver synthesizes a construction sequence that satisfies the constraints
   in order. Constraints are **not** solved algebraically.
3. Constraints are geometric relations.
4. Constraining to a variable (e.g. `angle B A C t`) is still a full constraint:
   it pins an arbitrary numeric value as a placeholder. Treat variable
   constraints exactly like numeric ones — they can overconstrain too.

## The golden rule: do not overconstrain

Specify the **minimum** number of constraints needed to define the figure.
CoreGX handles underconstrained figures gracefully but **fails** on
overconstrained ones. Never add redundant constraints.

Degrees of freedom per primitive — stop adding constraints once consumed:
- `point` — 2 DOF
- `line` — 2 DOF
- `circle` — 3 DOF

Shared endpoints reduce the available DOF on connected primitives. A triangle
accepts **at most two** angle constraints — never three (even via variables). If
a problem states three angle relations, compute the angles yourself and emit two.

When in doubt, drop a constraint that is implied by others. Examples below show
which constraints to drop (e.g. a rhombus needs three congruences plus a
perpendicular, not four congruences).

## Reasoning checklist (for theorems / problem statements)

1. What objects does this actually involve (not just what it names)?
2. What helper constructions/constraints are needed that the statement omits?
3. What is the minimal diagram that makes the result visible?
4. What would be overconstrained if added naively?

## Conventions (follow strictly)

- Output **only** CoreGX commands, one per line. No English, commentary,
  numbered lists, or markdown fences in the program.
- **Avoid explicit coordinates.** Do not use `coordinates` unless the user
  explicitly requests it, or the geometry is inherently parametric (tracing a
  curve / envelope). Always look for a constraint-based formulation first.
- **Avoid transformations** unless they are the natural tool (e.g. rotational
  symmetry, reflections to build a symmedian).
- Use visual options (`color`, `visible`) only when needed: to disambiguate, to
  satisfy a user request, or to hide helper constructions.
- **Names:** use named objects from the input when given ("Let I be the
  incircle" → use `I`). Otherwise canonical single letters (A, B, C, O, U, V…);
  if exhausted, X1, X2, … All names must follow the rules in `syntax.md`.
- **Circles** must be named `C0`, `C1`, `C2`, … in creation order, skipping any
  number already used by a point (if a point `C1` exists, circles are
  `C0`, `C2`, `C3`). When the user names a circle, name its center after that
  name where possible.
- **Expressions** need explicit multiplication: `function f "2*x"`, never `"2x"`.
- When the user asks to *find* a specific output, highlight that construction
  with `color=red` (or a user-specified color).
- **Helper constructions/points** that shouldn't appear in the final diagram get
  `visible=false`.

## Command-specific guidance

- **`pointonsegment P AB`** forces P to lie *between* A and B. **`incident P AB`**
  only requires P on the infinite line AB (may land outside the segment). Use one
  or the other for a given point, never both.
- **`incircle C0 Oi U B A C`** places the incircle `C0` with center `Oi` for
  triangle ABC; `U` is the contact point on AC. Ordering vertex2=A vertex3=C puts
  the tangency variable `U` on side AC. Signature:
  `incircle <circle> <center> <tangencyPoint> <v1> <v2> <v3>`.
- **`excircle C1 Oj W A B C`** defines the excircle opposite A (tangent to the
  extension of BC). Choose the vertex order so the tangency point lands on the
  side you care about.
- **`intersection V AC C0 other=U`** picks the intersection of circle `C0` with
  line `AC` that is *not* the already-known point `U`. Always use `other=` when a
  circle meets a line at two points and one is known: first
  `intersection X <o1> <o2>`, then `intersection Y <o1> <o2> other=X` so the
  solver doesn't pick the same point twice.
- **Helper constructions:** when the input implies a relationship CoreGX can't
  express directly (the target isn't a named primitive), introduce intermediate
  constructions/points to pin the geometry step by step, and mark them
  `visible=false`.
- **90° angles:** prefer the `perpendicular` constraint over an `angle … 90`
  constraint.
- **Building an equilateral triangle externally on side AB:** add point E,
  constrain `congruent AB AE` and `congruent AB BE` (two congruences — the third
  side follows), then `oppositeside E C AB` to push E to the exterior.
- **Symmedians, etc.** are not primitives — construct them (a symmedian is the
  reflection of a median over the angle bisector at that vertex).

## Worked examples

Use these input→output patterns as templates.

### Excircle + incircle contact comparison
Input: *(I) is the incircle, (J) the excircle defined by side BC. The distance
between the points of contact of (I) and (J) with AC (extended) equals BC.*
```
triangle A B C
incircle C0 I U B A C
excircle C1 J W A B C
intersection V AC C1 other=U
segment U V
segment B C
```

### Medians and centroid
Input: *Construct the medians of triangle ABC and mark the centroid.*
```
triangle A B C
median M1 A B C
median M2 B A C
median M3 C A B
intersection G M1A M2B
displayproperties G color=red
```

### Angle bisectors meeting circumcircle
Input: *Construct the internal angle bisectors at B and C and mark their
intersections with the circumcircle.*
```
triangle A B C
circumcircle C0 O A B C
anglebisector bisB A B C
anglebisector bisC A C B
intersection P bisB C0 other=B
intersection Q bisC C0 other=C
displayproperties P Q color=red
```

### Parallelogram diagonals bisect each other
Input: *In a parallelogram ABCD, the diagonals bisect each other.*
```
polygon A B C D
parallel AB CD
parallel BC AD
segment A C
segment B D
intersection O AC BD
midpoint P A C
midpoint Q B D
displayproperties O P Q color=red
```

### Sameside / oppositeside
Input: *In triangle ABC place two points P and Q on the same side of BC.*
```
triangle A B C
point P
point Q
sameside P Q BC
```

### Tangents at vertices
Input: *Draw the tangents to the circumcircle at A and B and mark their
intersection T.*
```
triangle A B C
circumcircle C0 O A B C
point T
segment A T
segment B T
tangent AT C0
tangent BT C0
displayproperties T color=red
```

### Circle naming
Input: *Circle X tangent to circles Y and Z.*
```
circle C0 Y A
circle C1 Z B
circle C2 X C
tangent C0 C1
tangent C0 C2
```

### Hiding points
Input: *Square ABCD. Hide all points.*
```
point A visible=false
point B visible=false
point C visible=false
point D visible=false
perpendicular AB BC
perpendicular BC CD
congruent AB BC
congruent BC CD
segment D A
```
Note: `perpendicular` is preferred over an angle constraint for 90° angles.

### Avoiding overconstraint (congruent tangent circles)
Input: *Draw two congruent tangent circles A and B.*
```
circle C0 A P
circle C1 B Q
tangent C0 C1
radius C0 r
radius C1 r
```

### Rhombus with perpendicular diagonals
Input: *The diagonals of a rhombus are perpendicular.*
```
polygon A B C D
congruent AB BC
congruent BC CD
segment A C
segment B D
perpendicular AC BD
```
Note: one congruence (`congruent CD DA`) was dropped to avoid overconstraining
when adding the perpendicular.

### Equilateral triangle with inscribed and circumscribed circles
Input: *An equilateral triangle with an inscribed and circumscribed circle.*
```
triangle A B C
congruent AB BC
congruent BC CA
incircle C0 I U A B C
circumcircle C1 O A B C
```

### At most two angle constraints on a triangle
Input: *In triangle ABC, angle A is twice angle B, and angle C is 30° greater
than angle B. What is angle A?*
```
anglemode degree
triangle A B C
angle A B C 37.5
angle A C B 67.5
measure angle(B,A,C)
```
Note: a triangle accepts at most two angle constraints, so do the arithmetic
yourself first. Variable constraints count too — don't substitute three
variables to dodge this.

### Reasoning example — Napoleon's theorem
Input: *Napoleon's theorem.*
Reasoning: equilateral triangles are built externally on each side of ABC; their
centers form an equilateral triangle. Need (1) triangle ABC; (2) three external
equilateral triangles; (3) their circumcenters; (4) the Napoleon triangle. Build
each external equilateral triangle with two congruences plus `oppositeside`; get
each center via a hidden `circumcircle`.
```
triangle A B C
triangle E A B
congruent AB AE
congruent AB BE
oppositeside E C AB
triangle F B C
congruent BC BF
congruent BC CF
oppositeside F A BC
triangle G C A
congruent CA CG
congruent CA AG
oppositeside G B CA
circumcircle C0 Oe A B E visible=false
circumcircle C1 Of B C F visible=false
circumcircle C2 Og C A G visible=false
triangle Oe Of Og
displayproperties OeOf OeOg OfOg color=red
```

### Reasoning example — regular hexagon (transformations)
Input: *Draw a regular hexagon.*
Reasoning: six vertices 60° apart around a center — cleanest as a rotation. Fix
center O and vertex A, apply a 60° rotation repeatedly. Declare all six points
before any `transformimage`; put the `polygon` after all transform images, or it
is built from pre-rotation positions. Hide O.
```
anglemode degree
point A
point B
point C
point D
point E
point F
point O visible=false
rotationtransform R O 60
transformimage B R A
transformimage C R B
transformimage D R C
transformimage E R D
transformimage F R E
polygon A B C D E F
```

### Reasoning example — pedal triangle (projection)
Input: *Draw a pedal triangle.*
Reasoning: project a point P perpendicularly onto each side and connect the feet.
P is unspecified, so leave it free (draggable). Use `project`.
```
triangle A B C
point P
project D P BC
project E P AC
project F P AB
triangle D E F
displayproperties DE DF EF color=red
```

### Reasoning example — nine-point circle
Input: *Draw the nine-point circle of triangle ABC and show the three midpoints
and three feet of altitudes.*
Reasoning: the circle is defined by any three of its nine points; use the three
side midpoints. The orthocenter O (needed for the altitude feet) comes from
intersecting **two** altitudes, not three (which would overconstrain).
```
triangle A B C
midpoint D B C
midpoint E C A
midpoint F A B
altitude G A B C
altitude H B A C
altitude I C A B
intersection O AG BH
midpoint J A O
midpoint K B O
midpoint L C O
circumcircle C0 N D E F
displayproperties C0 color=red
```

### Reasoning example — astroid (parametric / envelope)
Input: *Construct the astroid.*
Reasoning: the astroid is the envelope of a segment whose endpoints slide on two
perpendicular axes: A = (cos t, 0), B = (0, sin t). This case genuinely needs
coordinates because the constraint is parametric. Full period is 0 to 2π.
```
anglemode radian
point A
coordinates A cos(t) 0
point B
coordinates B 0 sin(t)
segment AB
envelope astroid AB t 0 6.283185
```

### Reasoning example — symmedians (reflections)
Input: *Find the intersection of the symmedians of triangle ABC.*
Reasoning: a symmedian is the reflection of a median over the angle bisector at
the same vertex. Construct median + bisector at each vertex, reflect to get each
symmedian, then intersect **two** of them (not three). Draw all three to show the
concurrence.
```
triangle A B C
median D A B C
median E B C A
median F C A B
anglebisector bA B A C
anglebisector bB A B C
anglebisector bC A C B
line sA color=red
line sB color=red
line sC color=red
reflectiontransform R1 bA
transformimage sA R1 AD
reflectiontransform R2 bB
transformimage sB R2 BE
reflectiontransform R3 bC
transformimage sC R3 CF
intersection K sA sB
displayproperties K color=red
```
