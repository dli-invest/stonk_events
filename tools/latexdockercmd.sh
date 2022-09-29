#!/bin/sh
# to run ../latexdockercmd.sh /bin/sh -c "pdflatex main.tex && pdflatex main.tex"
IMAGE=ghcr.io/friendlyuser/dimages/lwarp_docker:latest
exec docker run --rm -i --user="$(id -u):$(id -g)" --net=none -v "$PWD":/data "$IMAGE" "$@"
# move files to output
