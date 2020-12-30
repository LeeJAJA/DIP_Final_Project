import os
import random

import pandas as pd
from tqdm import tqdm
from shutil import copyfile

ROOT_DOR = r'../../data/trainData/slice-level'
csv_name = 'Slice_level_label.csv'
slice_roots = ['Cap', 'Covid-19']

TRAIN_RATE = 0.6
VAL_RATE = 0.3
TEST_RATE = 0.1
assert TRAIN_RATE + VAL_RATE + TEST_RATE - 1.0 < 0.0001


def get_slice_path_labels():
    image_labels = []

    df = pd.read_csv(os.path.join(ROOT_DOR, csv_name), index_col=0)
    for slice_root in slice_roots:
        person_root = os.path.join(ROOT_DOR, slice_root)
        person_names = os.listdir(person_root)

        i = 0
        while i < len(person_names):
            if not person_names[i].startswith('cap') and not person_names[i].startswith('P'):
                person_names.pop(i)
                i -= 1
            i += 1

        for pname in tqdm(person_names):
            try:
                assert pname.startswith('cap') or pname.startswith('P')
            except:
                print(person_names)
                raise

            image_root = os.path.join(person_root, pname)
            image_names = os.listdir(image_root)

            i = 0
            while i < len(image_names):
                if not image_names[i].startswith('CT'):
                    image_names.pop(i)
                    i -= 1
                i += 1

            for iname in image_names:
                assert len(iname) == 10
                imindex = int(iname[2:6])

                label = int(df.loc[pname][imindex])
                ifullname = os.path.join(image_root, iname)

                if pname.startswith('P') and label:
                    label = 2

                image_labels.append((ifullname, label))

    return image_labels


def shuffle_save():
    image_labels = get_slice_path_labels()
    random.shuffle(image_labels)

    for i, (name, label) in tqdm(enumerate(image_labels)):
        if i <= len(image_labels) * TRAIN_RATE:
            root = 'train'
        elif i <= len(image_labels) * (TRAIN_RATE + VAL_RATE):
            root = 'val'
        else:
            root = 'test'
        s = name.split(os.path.sep)
        s[-1]='img'+str(i).rjust(5,'0')+'_'+str(label)+'.png'
        s = s[:3] + [s[-1]]
        s.insert(-1, 'first_classifier')
        s.insert(-1, root)
        newname = os.path.sep.join(s)

        copyfile(name,newname)

shuffle_save()