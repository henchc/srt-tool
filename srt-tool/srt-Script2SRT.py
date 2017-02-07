import time
from nltk.parse import stanford
from nltk import sent_tokenize, Tree
from string import punctuation

punctuation = punctuation.replace("'", "")

line_limit = 34

with open("script_eng.txt") as f:
    raw_script = f.read()

# prepare stanford parser
parser = stanford.StanfordParser(
    path_to_jar="/Users/chench/Documents/stanford-parser-full-2015-12-09/stanford-parser.jar",
    path_to_models_jar="/Users/chench/Documents/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar")

sentences = parser.raw_parse_sents(sent_tokenize(raw_script))


def get_all_nodes(parent):
    '''
    extracts all chunk and word relations
    '''

    for node in parent:
        if isinstance(node, Tree):
            label_leaves = (node.label(), node.leaves())
            all_results.append(label_leaves)

            get_all_nodes(node)


all_results = []
for t in sentences:
    get_all_nodes(t)

# build subtitle lines
st_line = ""
all_lines = []

for tup in all_results:

    # rename elements
    label = tup[0]
    word_list = tup[1]
    word_string = " ".join(word_list)

    # clean st_line
    for p in punctuation:
        st_line = st_line.replace(" " + p, p)
    st_line = st_line.replace(" n't", "n't")
    st_line = st_line.replace(" 's", "'s")
    st_line = st_line.replace("I 'm", "I'm")

    # identify beginning of sentence
    if label == "ROOT":
        ROOT = word_list
        count = 0

    # iterate through chunks and words
    if len(word_list) > 1 and label[-1] == "P":
        if len(
                word_string +
                st_line) <= line_limit and word_list[0] == ROOT[count]:
            st_line += word_string + " "
            count += len(word_list)

    elif len(word_list) == 1 and word_list[0] == ROOT[count]:
        if len(st_line + word_string) <= line_limit:
            st_line += word_string + " "
            count += len(word_list)
        else:

            p_bin = 0

            for i, char in enumerate(st_line.strip()[::-1][1:]):
                if i < 10 and char in punctuation:
                    all_lines.append(st_line[:-i - 1].strip())
                    st_line = st_line[-i - 1:] + word_string + " "
                    p_bin = 1
                    break
                elif i < 20 and char in ".!?":
                    all_lines.append(st_line[:-i - 1].strip())
                    st_line = st_line[-i - 1:] + word_string + " "
                    p_bin = 1
                    break

            if p_bin == 0:
                all_lines.append(st_line.strip())
                st_line = word_string + " "

            count += len(word_list)


# fix and add final line
for p in punctuation + "'":
    st_line = st_line.replace(" " + p, p)

st_line = st_line.replace(" n't", "n't")
st_line = st_line.replace(" 's", "'s")
st_line = st_line.replace("I 'm", "I'm")
all_lines.append(st_line.strip())

for i in range(len(all_lines)):
    if all_lines[i][0] in punctuation:
        all_lines[i - 1] = all_lines[i - 1] + all_lines[i][0]
        all_lines[i] = all_lines[i][1:].strip()

count = 0

all_subs = []
sub = []
for l in all_lines:
    if count == 2:
        all_subs.append(sub)
        sub = []
        count = 0

    if count != 2:
        if l[-1] == ".":
            sub.append(l)
            all_subs.append(sub)
            sub = []
            count = 0
        else:
            sub.append(l)
            count += 1

ks = input("Press 'Enter' to start:")

time_stamps = []
for i in range(len(all_subs)):
    print()
    ks = input("\n".join(all_subs[i]))
    begin = time.time()
    ks = input()
    end = time.time()
    time_stamps.append((begin, end))

start_time = time_stamps[0][0]

for i in range(len(time_stamps)):
    time_stamps[i] = (
        time_stamps[i][0] -
        start_time,
        time_stamps[i][1] -
        start_time)


def to_tc(seconds):
    '''Converts seconds to timecode strings HH:MM:SS,SSS'''

    m, s = divmod(seconds, 60)
    sd = "%.3f" % s
    sd = "," + sd[-3:]
    h, m = divmod(m, 60)
    tc = "%02d:%02d:%02d" % (h, m, s)
    tc += sd
    return(tc)

#assert len(new_text) == len(self.tcs)

new_srt = ""
for i, x in enumerate(all_subs):
    new_srt += str(i + 1) + "\n"
    new_srt += to_tc(time_stamps[i][0]) + " --> " + \
        to_tc(time_stamps[i][1]) + "\n"
    new_srt += "\n".join(all_subs[i]) + "\n\n"

with open("newly_matched.srt", "w") as f:
    f.write(new_srt)
