import pandas as pd
import numpy as np
import streamlit as st
import ast
from typing import Dict, Set, List

class DataManipulator:

    @staticmethod
    def getGruppedPercentages(d: pd, denominator: int, groupBy: str="", col_name: str="Percentage"):
        d = d.groupby([groupBy]).size().reset_index(name = col_name)
        d[col_name] = d[col_name] / denominator
        d[col_name] = d[col_name] * 100
        d[col_name] = d[col_name].round().astype(int)
        return d
    
    @staticmethod
    def getGruppedData(d: pd, groupBy: str="", col_name: str="Number"):
        d = d.groupby([groupBy]).size().reset_index(name = col_name)
        return d
    
    @staticmethod
    def getTagsFreq(d: pd, colLst: List[str], PSPset: Set[str]) -> Set[str]:
        tags = dict()
        for column in colLst:
            for tag in d[column].tolist():
                for t in ast.literal_eval(tag):
                    if t in PSPset:
                        tags[t] = tags.get(t, 0) + 1
        return tags

    @staticmethod
    def getDictFreq(d: pd, colLst: List[str]):
        tags = dict()
        for column in colLst:
            for tag in d[column].tolist():
                tag = str(tag).strip()
                tags[tag] = tags.get(tag, 0) + 1
        return tags
    
    @staticmethod
    def getTagsPercentageFreq(d: pd, colLst: List[str], PSPset: Set[str]) -> Dict[str, int]:
        tags = dict()
        ctr = 0
        for column in colLst:
            for tag in d[column].tolist():
                for t in ast.literal_eval(tag):
                    if t in PSPset:
                        tags[t] = tags.get(t, 0) + 1
                        ctr += 1
        for tag in tags.keys():
            tags[tag] /=  ctr
            tags[tag] *= 100
            tags[tag] = int(round(tags[tag]))
        return tags