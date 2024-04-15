#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :assignment12_class.py
# @Time      :2024/4/15 22:18
# @Author    :FanZhang

import pandas as pd
import re

class Paper:
    def __init__(self, ut, py, so, sn, di, issn, vl, abstract, title, authors, affiliations, references):
        self.ut = ut
        self.py = py
        self.so = so
        self.sn = sn
        self.di = di
        self.issn = issn
        self.vl = vl
        self.abstract = abstract
        self.title = title
        self.authors = authors
        self.affiliations = affiliations
        self.references = references

    def __str__(self):
        return f"{self.ut}\t{self.py}\t{self.so}\t{self.sn}\t{self.di}\t{self.issn}\t{self.vl}\t{self.abstract}\t{self.title}\t{self.authors}\t{self.affiliations}\t{self.references}"


class PaperRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        self.papers = []

    def load_data(self):
        df = pd.read_csv(self.filepath, sep='\t')
        for index, row in df.iterrows():
            authors = list(zip(row['AU'].split('; '), row['AF'].split('; ')))
            affiliations = [(match[0], match[1].strip()) for x in row['C1'].split('\n') if (match := re.search(r'\[(.*?)\]', x))]
            references = row['CR'].split('; ')
            paper = Paper(row['UT'], row['PY'], row['SO'], row['SN'], row['DI'], row['IS'], row['VL'], row['AB'], row['TI'], authors, affiliations, references)
            self.papers.append(paper)

    def save_to_txt(self, output_path):
        with open(output_path, 'w') as file:
            for paper in self.papers:
                file.write(str(paper) + '\n')

    def load_from_txt(self, input_path):
        with open(input_path, 'r') as file:
            papers = []
            for line in file:
                parts = line.strip().split('\t')
                ut, py, so, sn, di, issn, vl, abstract, title = parts[:9]
                authors = eval(parts[9])
                affiliations = eval(parts[10])
                references = eval(parts[11])
                paper = Paper(ut, py, so, sn, di, issn, vl, abstract, title, authors, affiliations, references)
                papers.append(paper)
        return papers


if __name__ == "__main__":

    repo = PaperRepository('qje2014_2023.txt')
    repo.load_data()
    repo.save_to_txt('papers.txt')

    # 读取文本文件并重建Paper对象
    loaded_papers = repo.load_from_txt('papers.txt')
    for paper in loaded_papers:
        print(paper)
