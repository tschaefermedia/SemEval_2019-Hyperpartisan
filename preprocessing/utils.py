import string

import pandas as pd
import xml.etree.ElementTree as ET
import re
from nltk.corpus import stopwords

pd.set_option('display.max_columns', None)

def content(element):
    return (element.text or '') + ''.join(ET.tostring(e, 'unicode') for e in element)


def iter_data(data):
    tree = ET.iterparse(data)
    for event, element in tree:
        if element.tag == "article":
            doc_dict = element.attrib
            content_text = content(element)
            doc_dict['content'] = content_text
            yield doc_dict


def clean_content(df):
    for index, row in df.iterrows():
        cleaner = re.compile('<.*?>')
        cleaned_text = re.sub(cleaner, '', row['content'])
        row['content'] = cleaned_text
        row['content'] = " ".join(clean_text(row['content']))
    return df


def clean_text(text):
        '''
        What will be covered:
        1. Remove punctuation
        2. Remove stopwords
        3. Return list of clean text words
        '''

        # 1
        nopunc = [char for char in text if char not in string.punctuation]
        nopunc = ''.join(nopunc)

        # 2
        clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

        # 3
        return clean_words


def iter_truth(data):
    tree = ET.iterparse(data)
    for event, element in tree:
        if element.tag == "article":
            doc_dict = element.attrib
            yield doc_dict


def parse_xml_files(data, truth, save, outfile):
    columns_data = ['id', 'published-at', 'title', 'content']
    columns_truth = ['id', 'hyp', 'bias', 'url']
    bias = {'left': -1, 'left-center': -0.5, 'least': 0, 'right-center': 0.5, 'right': 1}
    data_df = pd.DataFrame(columns=columns_data)
    truth_df = pd.DataFrame(columns=columns_truth)
    for file in data:
        with open(file, encoding="utf8") as f:
            print("Starting with file: " + file)
            df = pd.DataFrame.from_records(list(iter_data(f)))
            data_df = data_df.append(df, sort=True)
            print("Finished file: " + file)
    data_df = clean_content(data_df)
    for file in truth:
        with open(file, encoding="utf8") as f:
            print("Starting with file: " + file)
            df = pd.DataFrame.from_records(list(iter_truth(f)), columns=columns_truth)
            truth_df = truth_df.append(df, sort=True)
            print("Finished file: " + file)
    print(data_df.head())
    print(truth_df.head())
    if save:
        data_df.to_csv(outfile)

