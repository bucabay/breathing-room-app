#!/bin/sh
set -eu
# Every packaged desktop rebuild updates the Applications copy.
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
pnpm --dir "$root" desktop:build
