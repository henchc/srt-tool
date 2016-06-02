# Created at UC Berkeley 2015
# Authors: Christopher Hench
# ==============================================================================

'''Library to manipulate .srt subtitle files. Currently srtTool can shift
subtitles by seconds or change to new frame rates. It also can match film
script files to spotted timecodes. PAL uses a frame rate of 25, while NTSC
uses a frame rate of 29.97. 35mm videos have a frame rate of 24. But transfer
from telecining for PAL is 23.976.'''


from datetime import datetime
import sys


class srtLib:

    def __init__(self, srtFile):
        self.subs = srtFile.split("\n\n")
        self.tcs = [s.split("\n")[1].split(" --> ")
                    for s in self.subs if len(s) > 0]
        self.sub_text = [s.split("\n")[2:] for s in self.subs if len(s) > 0]

    # shift all subs by seconds
    def shift_tcs(self, t_shift, rate=False):

        tc_as_num = [[t.split(":") for t in s] for s in self.tcs]
        tc_as_num = [[[int(t[0]) * 60 * 60, int(t[1]) * 60,
                       float(t[2].replace(",", "."))]
                      for t in s] for s in tc_as_num]
        tc_as_secs = [(sum(t[0]), sum(t[1])) for t in tc_as_num]

        tc_shifted_secs = [(t[0] + t_shift, t[1] + t_shift)
                           for t in tc_as_secs]

        if rate:
            tc_shifted_secs = [(t[0] * t_shift, t[1] * t_shift)
                               for t in tc_as_secs]

        shifted_tcs = []
        for s in tc_shifted_secs:
            new_tc = []
            for t in s:
                if t < 60:
                    if len(str(t)) == 1:
                        new_tc.append("00:00:0" +
                                      format(t, ".3f").replace(".", ","))
                    else:
                        new_tc.append("00:00:" +
                                      format(t, ".3f").replace(".", ","))

                if 60 <= t < 60 * 60:
                    if len(str(int(t / 60))) == 1:
                        if len(str(int(t % 60))) == 1:
                            new_tc.append("00:0" + str(int(t / 60)) + ":0" +
                                          format(t % 60, ".3f")
                                          .replace(".", ","))
                        else:
                            new_tc.append("00:0" + str(int(t / 60)) + ":" +
                                          format(t % 60, ".3f")
                                          .replace(".", ","))

                    else:
                        if len(str(int(t % 60))) == 1:
                            new_tc.append("00:" + str(int(t / 60)) + ":0" +
                                          format(t % 60, ".3f")
                                          .replace(".", ","))
                        else:
                            new_tc.append("00:" + str(int(t / 60)) + ":" +
                                          format(t % 60, ".3f")
                                          .replace(".", ","))

                if 60 * 60 <= t <= 60 * 60 * 60:
                    if len(str(int(t % 60))) == 1:
                        if len(str(int(t / 60 / 60))) == 1:
                            tc = ""
                            if len(str(int(t / 60) % 60)) == 1:
                                new_tc.append("0" + str(int(t / 60 / 60)) +
                                              ":0" + str(int(t / 60) % 60) +
                                              ":0" + format(t % 60, ".3f")
                                              .replace(".", ","))
                            else:
                                new_tc.append("0" + str(int(t / 60 / 60)) +
                                              ":" + str(int(t / 60) % 60) +
                                              ":0" + format(t % 60, ".3f")
                                              .replace(".", ","))
                        else:
                            if len(str(int(t / 60) % 60)) == 1:
                                new_tc.append(str(int(t / 60 / 60)) +
                                              ":0" + str(int(t / 60) % 60) +
                                              ":0" + format(t % 60, ".3f")
                                              .replace(".", ","))
                            else:
                                new_tc.append(str(int(t / 60 / 60)) +
                                              ":" + str(int(t / 60) % 60) +
                                              ":0" + format(t % 60, ".3f")
                                              .replace(".", ","))
                    else:
                        if len(str(int(t / 60 / 60))) == 1:
                            tc = ""
                            if len(str(int(t / 60) % 60)) == 1:
                                new_tc.append("0" + str(int(t / 60 / 60)) +
                                              ":0" +
                                              str(int(t / 60) % 60) + ":" +
                                              format(t % 60, ".3f")
                                              .replace(".", ","))
                            else:
                                new_tc.append("0" + str(int(t / 60 / 60)) +
                                              ":" +
                                              str(int(t / 60) % 60) + ":" +
                                              format(t % 60, ".3f")
                                              .replace(".", ","))
                        else:
                            if len(str(int(t / 60) % 60)) == 1:
                                new_tc.append(str(int(t / 60 / 60)) + ":0" +
                                              str(int(t / 60) % 60) + ":" +
                                              format(t % 60, ".3f")
                                              .replace(".", ","))
                            else:
                                new_tc.append(str(int(t / 60 / 60)) + ":" +
                                              str(int(t / 60) % 60) + ":" +
                                              format(t % 60, ".3f")
                                              .replace(".", ","))

            shifted_tcs.append((new_tc[0], new_tc[1]))

        return (shifted_tcs)

    def shift_subs(self, secs):
        s_tcs = self.shift_tcs(secs)
        newFile = ""
        for i, s in enumerate(self.sub_text):
            newFile += str(i + 1) + "\n"
            newFile += s_tcs[i][0] + " --> " + s_tcs[i][1] + "\n"
            for x in s:
                newFile += x + "\n"
            newFile += "\n"

        with open("shifted_subs.srt", "w") as f:
            f.write(newFile)

    def script(self):
        with open("script.txt", "w") as f:
            f.write("\n".join([i for s in self.sub_text for i in s]))

    # ratio input is old rate divided by new rate
    def shift_subs_rate(self, ratio):
        s_tcs = self.shift_tcs(ratio, rate=True)
        newFile = ""
        for i, s in enumerate(self.sub_text):
            newFile += str(i + 1) + "\n"
            newFile += s_tcs[i][0] + " --> " + s_tcs[i][1] + "\n"
            for x in s:
                newFile += x + "\n"
            newFile += "\n"

        with open("new_rate_subs.srt", "w") as f:
            f.write(newFile)

    def match_new(self, new_subs):
        '''This method matches subtitle text formatted in .srt without any
        timecode to a blank srt file with only time codes. This is helpful
        for spotters who happen to have a script.'''

        new_text = [[l for l in sub.split("\n") if len(l) > 0]
                    for sub in new_subs.split("\n\n")]
        assert len(new_text) == len(self.tcs)
        new_srt = ""
        for i, x in enumerate(new_text):
            new_srt += str(x[0]) + "\n"
            new_srt += self.tcs[i][0] + " --> " + self.tcs[i][1] + "\n"
            new_srt += "\n".join(x[1:]) + "\n\n"
        with open("newly_matched.srt", "w") as f:
            f.write(new_srt)


if __name__ == '__main__':
    filePath1 = sys.argv[1]
    action = str(sys.argv[2])

    with open(filePath1, 'r', encoding='utf-8') as f:
        srt = f.read()

    subs = srtLib(srt)

    if action == "shift":
        # num is seconds to shift or ratio of frame rate move
        num = sys.argv[3]
        subs.shift_subs(int(num))

    elif action == "frate":
        orig = sys.argv[3]
        new = sys.argv[4]
        if orig == "NTSC" and new == "PAL":
            subs.shift_subs_rate(23.976/25)
        elif orig == "PAL" and new == "NTSC":
            subs.shift_subs_rate(25/23.976)
        elif orig == "FILM" and new == "PAL":
            subs.shift_subs_rate(24/25)
        elif orig == "FILM" and new == "NTSC":
            subs.shift_subs_rate(25/24)

    elif action == "script":
        subs.script()

    elif action == "match_new":
        new_srt = sys.argv[3]
        with open(new_srt, 'r', encoding='utf-8') as f:
            new_text = f.read()
        subs.match_new(new_text)
