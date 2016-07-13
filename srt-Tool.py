# Created at UC Berkeley 2015
# Authors: Christopher Hench
# ==============================================================================

'''Library to manipulate .srt subtitle files. Currently srtTool can shift
subtitles by seconds or change to new frame rates. It also can match film
script files to spotted timecodes. PAL uses a frame rate of 25, while NTSC
uses a frame rate of 29.97. 35mm videos have a frame rate of 24. But transfer
from telecining for PAL is 23.976.'''


import datetime
import sys
import time


class srtLib:

    def __init__(self, srtFile):
        self.subs = srtFile.split("\n\n")
        self.tcs = [s.split("\n")[1].split(" --> ")
                    for s in self.subs if len(s) > 0]
        self.sub_text = [s.split("\n")[2:] for s in self.subs if len(s) > 0]

    def to_seconds(self, timecode):
        x = time.strptime(timecode.split(',')[0], '%H:%M:%S')
        secs = float(datetime.timedelta(
            hours=x.tm_hour,
            minutes=x.tm_min,
            seconds=x.tm_sec).total_seconds())
        return(secs)

    def to_tc(self, seconds):
        m, s = divmod(seconds, 60)
        sd = "%.3f" % s
        sd = "," + sd[-3:]
        h, m = divmod(m, 60)
        tc = "%02d:%02d:%02d" % (h, m, s)
        tc += sd
        return(tc)

    # shift all subs by seconds
    def shift_tcs(self, t_shift, rate=False):
        secs = [(self.to_seconds(x[0]), self.to_seconds(x[1]))
                for x in self.tcs]
        if not rate:
            secs = [(x[0] + t_shift, x[1] + t_shift) for x in secs]
        elif rate:
            secs = [(x[0] * t_shift, x[1] * t_shift) for x in secs]
        s_tcs = [(self.to_tc(x[0]), self.to_tc(x[1])) for x in secs]
        newFile = ""
        for i, s in enumerate(self.sub_text):
            newFile += str(i + 1) + "\n"
            newFile += s_tcs[i][0] + " --> " + s_tcs[i][1] + "\n"
            for x in s:
                newFile += x + "\n"
            newFile += "\n"

        with open("shifted_subs.srt", "w") as f:
            f.write(newFile)
        return (s_tcs)

    def script(self):
        with open("script.txt", "w") as f:
            f.write("\n".join([i for s in self.sub_text for i in s]))

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
        sec_or_rate = sys.argv[3]
        num = sys.argv[4]
        if sec_or_rate == "seconds":
            subs.shift_tcs(float(num))
        elif sec_or_rate == "rate":
            subs.shift_tcs(float(num), rate=True)

    # elif action == "frate":
    #     orig = sys.argv[3]
    #     new = sys.argv[4]
    #     if orig == "NTSC" and new == "PAL":
    #         subs.shift_subs_rate(23.976 / 25)
    #     elif orig == "PAL" and new == "NTSC":
    #         subs.shift_subs_rate(25 / 23.976)
    #     elif orig == "FILM" and new == "PAL":
    #         subs.shift_subs_rate(24 / 25)
    #     elif orig == "FILM" and new == "NTSC":
    #         subs.shift_subs_rate(25 / 24)

    elif action == "script":
        subs.script()

    elif action == "match_new":
        new_srt = sys.argv[3]
        with open(new_srt, 'r', encoding='utf-8') as f:
            new_text = f.read()
        subs.match_new(new_text)
