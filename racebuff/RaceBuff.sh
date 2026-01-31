#!/bin/sh
set -eu

CONFIG_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/RaceBuff/launcher.conf"
if [ -f "${CONFIG_FILE}" ] && [ -z "${RACEBUFF_RUN_ARGS:-}" ];
then
    . "${CONFIG_FILE}"
fi

./run.py ${RACEBUFF_RUN_ARGS:-} "$@"
