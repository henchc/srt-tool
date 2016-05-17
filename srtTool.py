# Created at UC Berkeley 2015
# Authors: Christopher Hench
# ==============================================================================

"""Library to manipulate .srt subtitle files.
Currently srtTool can shift subtitles by seconds
or change to new frame rates"""


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
        tc_as_num = [[[int(t[0])*60*60, int(t[1])*60,
                     float(t[2].replace(",", "."))]
                     for t in s] for s in tc_as_num]
        tc_as_secs = [(sum(t[0]), sum(t[1])) for t in tc_as_num]

        tc_shifted_secs = [(t[0]+t_shift, t[1]+t_shift) for t in tc_as_secs]

        if rate:
            tc_shifted_secs = [(t[0]*t_shift, t[1]*t_shift)
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
            newFile += str(i+1) + "\n"
            newFile += s_tcs[i][0] + " --> " + s_tcs[i][1] + "\n"
            for x in s:
                newFile += x + "\n"
            newFile += "\n"

        with open("shifted_subs.srt", "w") as f:
            f.write(newFile)

    # ratio input is old rate divided by new rate
    def shift_subs_rate(self, ratio):
        s_tcs = self.shift_tcs(ratio, rate=True)
        newFile = ""
        for i, s in enumerate(self.sub_text):
            newFile += str(i+1) + "\n"
            newFile += s_tcs[i][0] + " --> " + s_tcs[i][1] + "\n"
            for x in s:
                newFile += x + "\n"
            newFile += "\n"

        with open("new_rate_subs.srt", "w") as f:
            f.write(newFile)

if __name__ == '__main__':
    filePath1 = sys.argv[1]  # text file to get onsets from
    action = str(sys.argv[2])
    # num is seconds to shift or ratio of frame rate move
    num = sys.argv[3]

    with open(filePath1, 'r', encoding='utf-8') as f:
        srt = f.read()

    subs = srtLib(srt)

    if action == "shift":
        subs.shift_subs(int(num))

    elif action == "frate":
        subs.shift_subs_rate(float(num))
