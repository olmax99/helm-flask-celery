#!/bin/bash
while true
do
sleep 20
# Echo current date to stdout
echo "[workerservice: keep-alive] INFO $(date)"
# Echo 'error!' to stderr
echo '[workerservice: keep-alive] INFO .. confirm \"dev\/stderr\": error!' >&2
done