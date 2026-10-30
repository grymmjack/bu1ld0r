''
' bu1ld0r - a 3D model builder
' =============================================================================
' Put simple shapes together (boxes, cylinders, spheres, cones, wedges,
' tubes), colour them, and save the model - as its own .bld file to edit
' again, as an OBJ for any 3D program, and as a NEON-CASTER prop.
'
' The 3D view is drawn here, in BASIC (VIEW/VIEW.BM): a depth buffer says
' what's nearest at each pixel, and a second buffer which triangle it is,
' so a click knows exactly which part - and where on it - it landed.
'
' Layout: CORE (the window, input, helpers), MODEL (the parts, the shapes'
' triangles), VIEW (the camera, drawing, picking), UI (the bin, the panel,
' keys and clicks), OUT (OBJ and NEON-CASTER export). PLAN.md has what's
' next.
'
'$INCLUDE:'./_ALL.BI'

AppStart
DO
    InputFrame
    UiFrame
    IF meshDirty THEN MeshBuild
    IF viewDirty THEN ViewRender
    UiDraw
    _DISPLAY
    WindowFrame
    UiAfterFrame
    _LIMIT 60
LOOP UNTIL quitWant
SYSTEM

'$INCLUDE:'./_ALL.BM'
