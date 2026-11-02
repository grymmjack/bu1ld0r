---
name: m0d3l
description: Build a NEW low-poly model in bu1ld0r from an idea (not a rebuild of a game prop) - shape from primitives and mesh edits, textures painted by pixelmon and laid out as one picture by code, mapped face by face, materials, checked - live on Rick's screen with the steps explained so he can learn. Use when Rick says "/m0d3l THING", "make a model of a THING", "build a THING like the game's", or wants a prop that doesn't exist yet.
---

# m0d3l: a new model, fast

c0nstruct0r's other half. `/c0nstruct0r NAME` rebuilds a game prop from its painting;
`/m0d3l THING` makes something new: no painting to copy, so the shape is designed and the
textures come from pixelmon. First ones: `c0-barrel` (2026-11-01) - 10 parts, 608 triangles,
score 17 against the game's barrel's 41; `c0-crate` (Raiders-style shipping crate) - 10
boxes, 120 triangles, score 0 in bu1ld0r, 5 exported, against the game's crate's 54
(`tools/c0nstruct0r/m0d3l/crate/`: `shape.txt`, `atlas.py`, `texture.txt`). Its sources are `tools/c0nstruct0r/m0d3l/barrel/`
(the renders, `atlas.py`, `shape.txt`, `texture.txt`): copy that folder's way of working.

## How Rick wants it run

- **On his screen, live.** He's new to 3D and watches to learn. No hidden rehearsal unless
  he asks (the c0nstruct0r skill's "rehearse hidden first" doesn't apply here). If he hasn't
  started one: `cd ~/git/bu1ld0r && setsid nohup ./bu1ld0r.run --port &`. Check
  `inspect status` first: `new force` would throw away unsaved work - ask if `dirty` is 1.
- **Teach in the strip.** A `say` before each step: what it does and *why* (the 3D idea:
  extrude, inset, faces, low poly, texture columns, materials). The strip is one line and
  cuts long text: keep each `say` short. `pace 1400` for shape steps; for long runs of
  mapping lines `pace 80`, with `pace 3500` round each `say` so it can be read.
- **Through the MCP tools.** The MCP server holds his bu1ld0r's port, so `rc.py` gets
  "busy": send with `bu1ld0r` (lines), read with `inspect` / `look`, score with `fix` /
  `check`. Control ends with each connection: every `bu1ld0r` call starts with `take`.
  Several commands as `rc.py A B` are joined into ONE line - use `-f FILE` (or `/dev/stdin`).
- Tell him in chat what's coming before it appears; when something fails, say so in the strip.

## The method

1. **Size and style from the game.** Look at the game's own props of that kind
   (`~/git/neon-caster/neon-caster/hd/NAME.png`, `painting NAME`): the height is models.py's
   PROPS figure (barrel 0.45), proportions from the painting (barrel 0.76 as wide as tall).
   Budget 1000 triangles.
2. **Shape** (`shape.txt`): primitives, then mesh edits.
   - `add KIND X Y Z SX SY SZ [RX RY RZ] seg= col= name=` - X Y Z is the foot's middle; a
     turn goes round the foot. Kinds: box cylinder sphere cone (amt = top radius share: a
     frustum) wedge tube (amt = hole share) and the bin's others. seg 16 for a big round
     thing, 8 for small ones.
   - Seen from the front (yaw 0), **+x is on the screen's left** (the view's right is -x).
   - A bulge or taper: `edit P`, `pick facing 0 1 0`, `extrude D`, `scale K 1 K` - each
     extrude makes a band, each scale leans its wall; the same on `facing 0 -1 0`.
   - A sunk lid / panel / screen: `pick` it, `inset 0.12`, `extrude -0.012`.
   - Things that stand proud (hoops, trims, bands): their own thin parts a little bigger
     than the body where they sit - put them at the band joints, where the body's radius is
     exactly known (hoop radius = joint radius + 0.006).
   - Parts touch or sink in a little: no floating, no gaps.
3. **Textures from pixelmon** - the AI paints *materials*, code draws *structure*.
   - SDXL won't draw exact structure: asked for vertical staves it drew planks lying down,
     then mixed in grey wood. Ask for the surface ("worn red painted wood, grain running up
     and down"), then draw seams, rivets, panel lines in code exactly on the model's edges.
   - Untiled art renders came out clean; `--tile` art renders came out fried. A texture
     that wraps round needn't tile: put the wrap on a seam line the code draws.
   - Objects seen from one side come out well as a picture of their own (the lid: "top-down
     view of a round red painted barrel lid ... plain black background").
   - The AI lays long things along the picture's long side: render portrait for things that
     run up and down.
   - **Use juggernautXL with heun + karras** (Rick's tip, and it showed: the crate's pine came
     out clean and real with `--base juggernautXL_v9.safetensors --sampler heun --scheduler
     karras`, where the default checkpoint's wood was muddled or fried); look through pixelmon-gui's presets
     (`~/pixelmon-gallery/gui-presets/`, `~/pixelmon/presets/`) for a baseline; depth lock
     (`--depth IMG`, the Lab) holds a render to a shape - e.g. a depth picture of the part,
     or a drawn pattern - when structure has to come from the AI.
   - Template (renders go to the scratchpad; keep the ones used in the model's folder):
     `python3 ~/pixelmon/pixelmon.py "PROMPT" --negative "..." --art --out 512x1024 -n 3
     --seed S --server rtx --no-open --output-to DIR --create-dirs --name NAME`
     (~10 s a picture on rtx). Look at a contact sheet (`/usr/bin/python3` has PIL + numpy;
     brew's python3 doesn't) and pick.
4. **One square picture, laid out at 256, drawn at 512** (`atlas.py K`, written to
   `pictures/c0nstruct0r/c0-NAME.png`). The game's model textures are 256 x 256 in `hd/models`
   and 64 x 64 in `models/` (retro); the export writes both from bu1ld0r's picture
   (`WriteTex ... 256` / `64`). (The 512s in the game are HD *wall* pictures, not models.) So lay
   the regions out on a 256 x 256 square (~200 pixels a cell for a prop this size) and draw it
   at K = 2 - every coordinate x K, from the full-size renders: bu1ld0r shows the 512 sharp,
   the export halves it exactly. Spots are 0..1 of the picture, so the same mapping fits K = 1
   and K = 2. A non-square picture is squeezed (the barrel's 512 x 256). One picture also
   because several get packed 2x2 and shrunk. Every region at the same pixels a cell: a round
   part's region is (its perimeter in cells x px a cell) wide - 16 columns, one per face - by
   (height x px a cell). Draw seams / rivets at the column edges; give each column its own
   slice of the material and a slight brightness change, so neighbouring faces read as
   separate pieces.
   - **Grain follows the piece.** A thin strip takes boards running along its own length: the
     crate's lips round the body (band tops / undersides) got a "frame" region - boards along
     each side, the end ones turned to run along z. The lid's boards there (all along x) ran
     across the end lips and read as chopped chunks (Rick spotted it).
   - **Don't AI-upscale a picture you can redraw.** pixelmon's `--upscale --upscale-to 2x`
     (Real-ESRGAN, 2 s) sharpened the wood but scrambled the small stencils into squiggles.
     Redraw from the sources at K = 2; upscale only what has no bigger source.
   - bu1ld0r reloads a picture whose file changed by itself (every 2 s, and the port's
     `picture` checks first), so re-running atlas.py shows on screen with no re-open. (Before
     2026-11-01 it didn't: a picture rewritten at a new size kept its old size in memory and
     the mapping came out halved - `open NAME force` reloaded it.)
5. **Map face by face** - `tools/c0nstruct0r/m0d3l.py wrap`:
   `inspect faces` (part P; save the reply to a file) -> `m0d3l.py wrap faces.json REF X0 Y0
   W H N --box X0 X1 Z0 Z1 Y0 Y1` -> `pick F` / `picture REF view YAW RECT own` lines: each
   outward side face seen head on takes exactly its column, neighbours meet, every pixel the
   same size (four `view 0/90/180/270` quarters squash the pixels near each quarter's edge
   and don't meet). `--box` is the part's own box. Tops: `pick facing 0 1 0` ->
   `top RECT own`, RECT = the round picture's middle +- its radius in px x (box half-width /
   the top's radius).
   **Nothing untextured** (Rick's rule): every face gets a picture - bottoms, undersides,
   thin lips and cleat sides, recess walls, caps, even faces hidden against another part. A
   plain colour face shows as a flat patch the moment a camera finds it. Done means `fix`
   says `plain 0 colour 0`, and a look from below (`look pitch=-25`) and up close shows wood
   (or metal...) everywhere.
6. **Materials** - bu1ld0r has them (Q / MATERIAL; the port has no command yet): `save`,
   add `m=SEE:GLOW:SHINE:ROUGH:METAL:BUMP:COAT:SHEEN` (percent) to each `part` line of
   `models/c0-NAME.bld`, `open c0-NAME force`. Barrel: wood `m=0:0:20:73:0:47:20:0`
   (BUMP takes the grain from the picture), iron `m=0:0:40:60:87:27:0:0`, bare metal
   `m=0:0:60:40:100:13:0:0`. Presets in MODEL/MAT.BM `MatSetup`.
   **Export catch (to fix in bu1ld0r):** each picture + material pair counts as its own
   picture, so three materials on one picture pack 2x2 and the export's pixels a cell drop
   ~3x (302 -> 107). Until ExAtlas / WriteMat keep one picture whose pairs use separate
   areas, one material per picture keeps it sharp.
7. **Check**: `fix` (in bu1ld0r), `look eight=true`, `save c0-NAME`, `export` (as built -
   never tidied: Rick doesn't want the tidy export for these; the reply says "as built"),
   `check c0-NAME against=SIMILAR`. Into the game only when Rick says.
8. **Keep**: the folder `tools/c0nstruct0r/m0d3l/NAME/` (renders used, atlas.py,
   shape.txt, texture.txt, the faces JSON the mapping came from) - the model can be made
   again from it.

## Boxes (the crate)

A box's sides need no wrap: `edit P`, `pick facing 0 0 -1` -> `picture REF view 0 RECT own`,
`0 0 1` -> `view 180`, `1 0 0` -> `view 90`, `-1 0 0` -> `view 270`, `0 1 0` -> `top RECT own` -
RECT a region exactly the face's size in pixels, so each face takes its whole patch with no
stretch (the crate: score 0). Words and arrows (stencils, labels) are drawn by code into the
face's region - PIL at 4x then shrunk, ink a little uneven; the DIN Bold Condensed font is
`~/.local/share/fonts/d/DINNeuzeitGroteskStd_BdCond.otf`. A part that would cover them
(the crate's middle cleat over TOP SECRET) goes: `del P`, and the parts after it renumber.
A whole box as a band (a top band the full footprint) gives the top face itself - a body top
under it would sit in the same place and flicker. One material for the whole model keeps the
export to one picture.

## Worked numbers: the barrel

Drum: cylinder seg 16, 0.344 across, 0.11 tall at y 0.17; up: extrude 0.10 scale 0.930,
extrude 0.07 scale 0.906; the same down (radii 0.145 / 0.160 / 0.172 / 0.172 / 0.160 /
0.145 at y 0 / 0.07 / 0.17 / 0.28 / 0.38 / 0.45); lid inset 0.12, extrude -0.012. Hoops:
cylinders 0.022 tall at the joints, radius + 0.006. Atlas 512 x 256: staves 320 x 134 at 0,0
(16 x 20 px); lid 102 x 102 at 330,0 (its circle 86 px); iron 336 x 7 at 0,140 (16 x 21,
a rivet each); canister 48 x 39 at 340,140 (8 x 6).
