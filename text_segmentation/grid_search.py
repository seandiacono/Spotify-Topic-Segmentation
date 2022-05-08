import segeval
from load_transcripts import load_all_transcripts
from load_annotations import load_all_annotations
from algorithms import TextTiling, TextSplit, Baseline

transcripts_as_strings = load_all_transcripts(
    path="../dataset/transcripts/", as_string=True)
annotations = load_all_annotations(
    path=f"../dataset/annotations/", transcript_path="../dataset/transcripts")

# TextSplit
# segment_len = {}


# TextTiling
def grid_search_text_tiling():

    w = [10, 20, 30, 50, 70]
    k = [5, 10, 20, 30]
    policy = [0, 1]

    min_pk = 1
    min_wd = 1

    values_pk = {}
    values_wd = {}

    for p1 in policy:
        for w1 in w:
            for k1 in k:

                segmenter = TextTiling(w1, k1, p1)

                list_pk = []
                list_wd = []

                for t, wc_truth in zip(transcripts_as_strings.values(), annotations.values()):
                    _, wc_pred = segmenter.segment(t)
                    pk = segeval.pk(wc_truth, wc_pred)
                    try:
                        wd = segeval.window_diff(wc_truth, wc_pred)
                    except:
                        wd = 1
                        print("Window diff failed")
                        print("Values were: ", p1, w1, k1)

                    list_pk.append(pk)
                    list_wd.append(wd)

                average_pk = sum(list_pk) / len(list_pk)
                average_wd = sum(list_wd) / len(list_wd)

                if average_pk < min_pk:
                    values_pk['w'] = w1
                    values_pk['k'] = k1
                    values_pk['p'] = p1
                    print(f"New min pk: {average_pk}")
                    print(f"New best pk values: {values_pk}")
                    min_pk = average_pk

                if average_wd < min_wd:
                    values_wd['w'] = w1
                    values_wd['k'] = k1
                    values_wd['p'] = p1
                    print(f"New min wd: {average_wd}")
                    print(f"New best wd values: {values_wd}")
                    min_wd = average_wd
    print('==============================')
    print(f"Best pk values: {values_pk}")
    print(f"Best wd values: {values_wd}")


def grid_search_text_split():

    segment_len = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    min_pk = 1
    min_wd = 1

    values_pk = {}
    values_wd = {}

    for l in segment_len:
        segmenter = TextSplit(segment_len=l)

        list_pk = []
        list_wd = []

        for t, wc_truth in zip(transcripts_as_strings.values(), annotations.values()):
            _, wc_pred = segmenter.segment(t)
            print(f"Equal size: {sum(wc_truth) == sum(wc_pred)}")
            try:
                pk = segeval.pk(wc_truth, wc_pred)
                wd = segeval.window_diff(wc_truth, wc_pred)
                list_pk.append(pk)
                list_wd.append(wd)
            except:
                continue

        average_pk = sum(list_pk) / len(list_pk)
        average_wd = sum(list_wd) / len(list_wd)

        if average_pk < min_pk:
            values_pk['l'] = l
            print(f"New min pk: {average_pk}")
            print(f"New best pk values: {values_pk}")
            min_pk = average_pk

        if average_wd < min_wd:
            values_wd['l'] = l
            print(f"New min wd: {average_wd}")
            print(f"New best wd values: {values_wd}")
            min_wd = average_wd

    print('==============================')
    print(f"Best pk values: {values_pk}")
    print(f"Best wd values: {values_wd}")


# grid_search_text_tiling()
grid_search_text_split()
