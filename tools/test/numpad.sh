#!/bin/bash
# The numpad's view keys, with Num Lock on and off, on Xvfb :99 (tools/test/run.sh's).
#   tools/test/numpad.sh          -> PASS / FAIL lines, exit 1 if any failed
# Each numpad key is held (as a person presses it) and tapped (xdotool's instant
# press); --keylog says which numpad key the program took each key as. The top
# row's 7 and the arrow keys must stay themselves.
R=$(cd "$(dirname "$0")/../.." && pwd)
BT=${BT:-/tmp/claude-1000/bu1ld0r-test}; LOG=$BT/numpad-keys.log
export DISPLAY=:99
xdpyinfo -display :99 >/dev/null 2>&1 || { echo ":99 is down"; exit 9; }
source "$R/tools/test/drv.sh"
testkill; sleep .5; rm -f $LOG
( T=120 "$R/tools/test/run.sh" --open kbox --keylog $LOG >/dev/null 2>&1 & )
for i in $(seq 1 40); do sleep .25; win; [ -n "$W" ] && break; done
[ -z "$W" ] && { echo "FAIL: no window"; exit 1; }
sleep 2; xdotool windowfocus --sync $W; xdotool mousemove --window $W 700 500; sleep .3
numlock() { xset q | grep -q "Num Lock: *on"; }
setnum() { if [ "$1" = on ]; then numlock || xdotool key Num_Lock; else numlock && xdotool key Num_Lock; fi; sleep .3; }
fails=0
expect() { # KEYSYM HOW WANT(numpad key, 0 = a plain key) - press it, check the log's last line
    local before=$(wc -l < $LOG 2>/dev/null || echo 0)
    if [ "$2" = hold ]; then xdotool keydown $1; sleep .12; xdotool keyup $1; else xdotool key $1; fi
    sleep .35
    local got=$(tail -n +$((before + 1)) $LOG 2>/dev/null | awk '{print $4}' | head -1)
    if [ "$got" = "$3" ]; then echo "PASS  numlock $NL  $1 ($2) -> numpad ${3}"
    else echo "FAIL  numlock $NL  $1 ($2) -> took it as numpad '${got:-nothing}', wanted $3"; fails=$((fails + 1)); fi
}
NL=on; setnum on
for k in 1 2 3 4 6 7 8 9 0; do b=$k; [ $k = 0 ] && b=10; expect KP_$k hold $b; done
expect KP_5 hold 5; expect KP_5 hold 5                       # (flat, and back)
expect KP_Decimal hold 11; expect KP_Add hold 12; expect KP_Subtract hold 13
expect KP_Multiply hold 14; expect KP_Divide hold 15; expect KP_Enter hold 16
expect KP_7 tap 7; expect KP_2 tap 2
expect 7 hold 0                                               # (the top row's 7: a shape)
expect Escape tap 0
NL=off; setnum off
expect KP_End hold 1; expect KP_Down hold 2; expect KP_Next hold 3; expect KP_Left hold 4
expect KP_Right hold 6; expect KP_Home hold 7; expect KP_Up hold 8; expect KP_Prior hold 9
expect KP_Insert hold 10; expect KP_Delete hold 11; expect KP_Add hold 12; expect KP_Enter hold 16
expect KP_Home tap 7
expect Home hold 0                                            # (the real Home key)
setnum on
testkill
echo "--- log:"; cat $LOG
[ $fails = 0 ] && echo "ALL PASS" || { echo "$fails FAILED"; exit 1; }
