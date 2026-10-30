# source me: helpers to drive a bu1ld0r started by run.sh on :99 (never the real display)
#   win; clk X Y [BUTTON]; mv X Y; key KEYS; typ TEXT; shot NAME; drag X0 Y0 X1 Y1 X2 Y2
BT=${BT:-/tmp/claude-1000/bu1ld0r-test}
export DISPLAY=:99; unset WAYLAND_DISPLAY
win() { PID=$(pgrep -x bu1ld0r.run | head -1); W=$(xdotool search --pid $PID 2>/dev/null | tail -1); }
clk() { xdotool mousemove --window $W $1 $2; sleep .25; xdotool click --window $W ${3:-1}; sleep .35; }
mv() { xdotool mousemove --window $W $1 $2; sleep .3; }
key() { xdotool key --window $W "$@"; sleep .3; }
typ() { xdotool type --window $W "$1"; sleep .3; }
shot() { ffmpeg -loglevel error -y -f x11grab -video_size 1280x800 -i :99.0 -frames:v 1 $BT/$1.png; }
drag() { xdotool mousemove --window $W $1 $2; sleep .2; xdotool mousedown --window $W 1; sleep .3; xdotool mousemove --window $W $3 $4; sleep .4; xdotool mousemove --window $W $5 $6; sleep .5; xdotool mouseup --window $W 1; sleep .4; }
