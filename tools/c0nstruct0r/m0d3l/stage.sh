#!/bin/bash
# Stage a m0d3l model in the game's layout, under the game's name, without touching neon-caster:
#   tools/c0nstruct0r/m0d3l/stage.sh NAME [MODEL]      (MODEL default c0-NAME)
# -> export/neon-stage/models/NAME.obj .mtl _tex.png (64) _mat.png _0.._7.png, hd/models/NAME_tex.png (256)
# Runs a test copy of bu1ld0r on a hidden Xvfb :98 (started if down; never Rick's display).
# Installing later: cp export/neon-stage/models/NAME* ~/git/neon-caster/neon-caster/models/ (and hd/models).
set -e
N=$1; M=${2:-c0-$1}
[ -n "$N" ] || { echo "usage: stage.sh NAME [MODEL]"; exit 2; }
R=$(cd "$(dirname "$0")/../../.." && pwd)
BT=/tmp/claude-1000/bu1ld0r-stage; S=$R/export/neon-stage
mkdir -p $S/models $S/hd/models $BT/app/models $BT/app/pictures
cp $R/bu1ld0r.run $BT/app/
cp $R/models/$M.bld $BT/app/models/$N.bld
rm -rf $BT/app/pictures/c0nstruct0r; cp -r $R/pictures/c0nstruct0r $BT/app/pictures/
[ -d $R/pictures/neon ] && { rm -rf $BT/app/pictures/neon; cp -r $R/pictures/neon $BT/app/pictures/; }
if ! xdpyinfo -display :98 >/dev/null 2>&1; then setsid Xvfb :98 -screen 0 1280x800x24 >/dev/null 2>&1 & sleep 2; fi
unset WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS; export XDG_SESSION_TYPE=x11 QT_QPA_PLATFORM=xcb DISPLAY=:98
pactl list short sinks | grep -q claude_mute || pactl load-module module-null-sink sink_name=claude_mute >/dev/null
cd $BT/app
PULSE_SINK=claude_mute LP_NUM_THREADS=2 nice -n 19 timeout -k 5 90 ./bu1ld0r.run --open models/$N.bld --export --neon $S/ --quit
# (the export names the copy it was made from, models/NAME.bld: point it at the real one)
[ "$M" != "$N" ] && sed -i "1s#edit models/$N.bld there#edit models/$M.bld there#" $S/models/$N.obj
ls -la $S/models/$N.obj $S/hd/models/${N}_tex.png
