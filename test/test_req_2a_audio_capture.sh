#!/bin/bash

#echo "Please make sure that headphone is at 25% in Alsamixer!"
#echo "Press CTRL+C to quit!"
#arecord -f cd | aplay

echo "Please talk for 3 seconds!"
arecord -f cd -r 16000 -d 3 > "test.wav"

echo "Now playing the recording..."
aplay "test.wav"

rm "test.wav"
echo "Done."
