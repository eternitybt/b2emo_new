#!/bin/bash
# $ ./models/download-ggml-model.sh tiny.en
# $ make tiny.en

STREAM="stdbuf -i0 -o0 -e0 ./stream -m models/ggml-tiny.en.bin --step 4000 --length 8000 -c 0 -t 4 -ac 512"
FILTER="stdbuf -i0 -o0 -e0 sed 's/\x1b\[2K\r *//g'"
PIPE="stdbuf -i0 -o0 -e0 python3 ../b2emo/src/pipe_req_2c_audio_stream.py"
OUTFILE="../b2emo/test/result_req_2c_audio_stream.txt"

# Start stream.
cd ../../whisper.cpp/
$STREAM | $FILTER | $PIPE > $OUTFILE

cd -
echo "Results written to result_req_2c_audio_stream.txt."

## Prompt user for success.
#echo
#echo "Did the robot understand what you were saying?"
#select yn in "Yes" "No"
#do
#    case $yn in
#        "Yes" ) RESULT=0;;
#        "No" ) RESULT=1;;
#    esac
#    break
#done
#
## Return result (0==success, 1==fail).
#exit $RESULT
