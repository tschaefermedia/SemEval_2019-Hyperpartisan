import itertools

import pandas as pd
import xml.etree.ElementTree as ET
import io
import re


def content(element):
    return (element.text or '') + ''.join(ET.tostring(e, 'unicode') for e in element)


def iter_data(data):
    nprocessed = 0
    all = 0
    debug = True
    tree = ET.iterparse(data)
    for event, element in tree:
        if element.tag == "article":
            doc_dict = element.attrib
            content_text = content(element)
            doc_dict['content'] = content_text
            yield doc_dict


def remove_links(df):
    for index, row in df.iterrows():
        cleaner = re.compile('<.*?>')
        cleantext = re.sub(cleaner, '', row['content'])
        row['content'] = cleantext
    return df




def iter_truth(data):
    pass


def parse_xml_files(data, truth, save, outfile):
    columns_data = ['id', 'published-at', 'title', 'content']
    columns_truth = ['hyp', 'bias', 'url']
    bias = {'left': -1, 'left-center': -0.5, 'least': 0, 'right-center': 0.5, 'right': 1}
    data_df = pd.DataFrame(columns=columns_data)

    for file in data:
        with open(file, encoding="utf8") as f:
            print("Starting with file: " + file)
            df = pd.DataFrame.from_records(list(iter_data(f)))
            data_df = data_df.append(df, sort=True)
            print("Finished file: " + file)
    data_df = remove_links(data_df)
    if save:
        data_df.to_csv(outfile)

