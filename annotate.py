#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Annotate.py

> python annotate.py
"""

import pandas as pd

import re
import os

import argparse
from pathlib import Path
import ntpath


def get_args_parser():
    parser = argparse.ArgumentParser("K400", add_help=False)

    parser.add_argument(
        "--input_file",
        default="/data/i5O/kinetics-dataset/annotations/val.csv",
        help="path to the .csv or .json from the kinetics website",
    )
    parser.add_argument(
        "--dataset_root",
        default="/data/i5O/kinetics400/",
        help="path to the dataset folder. Should be something like ./kinetics400/",
    )

    return parser


def main(args):
    basename = ntpath.basename(args.input_file)
    assert bool(
        re.search("csv", basename)
    ), "for now (for MVD model), only .csv is supported"

    split = re.search(
        "train|val|test", basename
    ).group()  # train, val or test depending on which split we are working with.
    folder = os.path.join(args.dataset_root, split)

    df = pd.read_csv(args.input_file)

    df.youtube_id = (
        folder
        + "/"
        + df.youtube_id
        + "_"
        + df.time_start.astype("string").str.zfill(6)
        + "_"
        + df.time_end.astype("string").str.zfill(6)
        + ".mp4"
    ).values

    df = df[["youtube_id", "label"]]

    # some videos seem to be missing, so we remove.
    df = df[df.apply(lambda x: os.path.isfile(x.youtube_id), axis=1)]

    # TODO: populate df with the video clips.
    # For example, --07WQ2iBlw (the full video) is what is listed in val.csv, but we want the address of the 10-sec clip,
    # for example from 1 to 11 seconds --07WQ2iBlw_000001_000011.mp4, and the rest of clips from --07WQ2iBlw, for this we will need to check the dataset folder.

    # Store the output file

    output_dir = os.path.dirname(args.input_file)  # we use the same folder as input
    basename_f, basename_ext = os.path.splitext(basename)
    output_file = os.path.join(output_dir, basename_f + "_mvd" + basename_ext)

    df.to_csv(output_file, index=False, header=False)


# val_csv = pd.read_csv('/Users/chrisindris/Documents/MSc/Projects/i-5O/kinetics-dataset/annotations/val.csv')

# dataset_root = "/data/cindris/data/i5O/kinetics400/" + "val/"

# val_csv = val_csv[["youtube_id", "label"]]
# val_csv.youtube_id = (dataset_root + val_csv.youtube_id + ".csv").values

# # Should look like
# # dataset_root/split/video_1.mp4  label_1
# # dataset_root/split/video_2.mp4  label_2
# # dataset_root/split/video_3.mp4  label_3
# # ...
# # dataset_root/video_N.mp4  label_N

# val_csv.to_csv("/Users/chrisindris/Documents/MSc/Projects/i-5O/kinetics-dataset/annotations/val_mvd.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("K400", parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)
