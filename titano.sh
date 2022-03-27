#!/bin/bash

# Terminate already running bar instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# if you run multiple bars you need to launch each bar like below.

polybar -rq titano -c ~/.config/polybar/titano-bar/titano.ini &
polybar -rq clock -c ~/.config/polybar/titano-bar/titano.ini &

echo "Polybars launched..."