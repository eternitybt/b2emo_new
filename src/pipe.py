import re
import sys
import subprocess
import openai

N_STEP_MAX = 12

WALLEE_NAMES = [
    "robot", "runbot", "wall-e", "wall e", "wally", "wallee", "walee", "well-e",
    "wolly", "wolee", "wole-e", "wal-hee", "roll e", "vol-e", "volee", "volky",
    "wargill", "woggy", "vul-e", "mulkey", "well, e", "walghee", "vaul t",
    "volity", "valee", "while e", "ball-he", "wall key", "wal-i", "mulhee",
    "wole", "wallie", "woly", "all e", "wali", "well-eat", "wollief", "molly"
    ]

GPT3_MODEL = "ada:ft-personal-2023-01-31-19-25-58"
GPT3_BOS = "AHEM"
GPT3_EOS = "miau"

PYTHON_CMD = "python3 /home/mause/Github/b2emo/Tests/{cmd}.py &"

# GPT-3 Test:
#prompt_raw = "Stop right here, wall E, robot. Now turn the bit to the root. right, while he robot turn right. a bit more to the right, then stop while E."
#prompt = prompt_raw + " " + GPT3_BOS
#response_json = openai.Completion.create(model=GPT3_MODEL, prompt=prompt, temperature=0.5, max_tokens=100)
#response_str = re.sub(r"{gpt3_eos}.+".format(gpt3_eos=GPT3_EOS), "", response_json["choices"][0]["text"].lower()).lstrip().rstrip()
##print(response_json)
#print(prompt_raw + " -> " + response_str)
#exit()

n = 0
lines = []
for line in sys.stdin:
    #sys.stderr.write(str(n) + ">>>>>>>>>>>>>>>>>>>>>>> \n")
    lines.append(line.rstrip()[:40])
        
    # Join last four lines.
    l = len(lines)
    joined = ""
    for i in range(max(0, l - 4), l):
        joined = joined + " " + lines[i]
    joined = joined.lstrip()

    found = False
    for name in WALLEE_NAMES:
        if joined.lower().find(name) > -1:
            found = True
            break
    if found:
        # Call GPT-3.
        prompt = joined + " " + GPT3_BOS
        response_json = openai.Completion.create(
                model=GPT3_MODEL,
                prompt=prompt,
                temperature=0.5,
                max_tokens=100)
        response_str = re.sub(
                r"{gpt3_eos}.+".format(gpt3_eos=GPT3_EOS),
                "",
                response_json["choices"][0]["text"].lower()
                ).lstrip().rstrip()
        joined = joined + " -> " + response_str
        #print(response_json)
        print(joined)
        #sys.stderr.write(joined + '\n')
        sys.stderr.write(response_str + '\n')

        # Follow command.
        if response_str.lstrip().rstrip().lower() == "drive forward.":
            #sys.stderr.write("F\n")
            subprocess.call(PYTHON_CMD.format(cmd="drive_forward"), shell=True)
        elif response_str.lstrip().rstrip().lower() == "drive backward.":
            #sys.stderr.write("B\n")
            subprocess.call(PYTHON_CMD.format(cmd="drive_backward"), shell=True)
        elif response_str.lstrip().rstrip().lower() == "turn left.":
            #sys.stderr.write("L\n")
            subprocess.call(PYTHON_CMD.format(cmd="turn_left"), shell=True)
        elif response_str.lstrip().rstrip().lower() == "turn right.":
            #sys.stderr.write("R\n")
            subprocess.call(PYTHON_CMD.format(cmd="turn_right"), shell=True)
        else:
            #sys.stderr.write("S\n")
            subprocess.call(PYTHON_CMD.format(cmd="stop"), shell=True)

    n += 1
    if n >= N_STEP_MAX:
        exit(0)
