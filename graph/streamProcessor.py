import json
import pprint
import sys

def JsonLinesProcessor(fname):
    file = open(fname, "r")

    try:
        while True:
            bracket_count = 0
            curr_str = ""

            while True:
                c = file.read(1)
                if c == "{":
                    bracket_count += 1
                    curr_str += c
                    break
                elif c == '':
                    raise EOFError

            while bracket_count > 0:
                c = file.read(1)
                if c == "{":
                    bracket_count += 1
                elif c == "}":
                    bracket_count -= 1

                curr_str += c
            data = json.loads(curr_str)
            curr_str = ""
            yield data
    except:
        file.close()
        return "File Completed Processing"

if __name__ == "__main__":
    fname = sys.argv[1]

    dat = JsonLinesProcessor(fname)
    for data in dat:
        pprint.pprint(data)

