#!/bin/bash

echo "Please talk for 3 seconds!"
arecord -f cd -r 16000 -d 3 > "test.wav"

echo "Now playing the recording..."
aplay "test.wav" &

echo "You said:"
cp "test.wav" ../../whisper.cpp/
cd ../../whisper.cpp/
./main -m models/ggml-tiny.en.bin -f test.wav -t 4

rm "test.wav"
cd -
echo "Done."
