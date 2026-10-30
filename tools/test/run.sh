#!/bin/bash
# A bu1ld0r test run on Xvfb :99, muted, from a copy (never the repo's binary):
#   T=40 tools/test/run.sh ARGS...      (T = seconds before it's killed)
# Start Xvfb first: Xvfb :99 -screen 0 1280x800x24 &   (check: xdpyinfo -display :99)
# Copy dir: $BT (default /tmp/claude-1000/bu1ld0r-test)
R=$(cd "$(dirname "$0")/../.." && pwd)
BT=${BT:-/tmp/claude-1000/bu1ld0r-test}; mkdir -p $BT/app
unset WAYLAND_DISPLAY DBUS_SESSION_BUS_ADDRESS; export XDG_SESSION_TYPE=x11 QT_QPA_PLATFORM=xcb DISPLAY=:99
xdpyinfo -display :99 >/dev/null 2>&1 || { echo ":99 is down"; exit 9; }
pactl list short sinks | grep -q claude_mute || pactl load-module module-null-sink sink_name=claude_mute >/dev/null
cp "$R/bu1ld0r.run" $BT/app/
[ -d $BT/app/models ] || cp -r "$R/models" $BT/app/
[ -d $BT/app/prefabs ] || [ ! -d "$R/prefabs" ] || cp -r "$R/prefabs" $BT/app/
PULSE_SINK=claude_mute LP_NUM_THREADS=2 nice -n 19 timeout -k 5 ${T:-40} $BT/app/bu1ld0r.run "$@"
echo "exit $?"
