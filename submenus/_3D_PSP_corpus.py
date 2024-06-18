import streamlit as st
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import re
import plotly.data as pdata
from typing import Dict
#from data_display.barchart3d import barchart3d
from wordcloud import STOPWORDS
from pandas.api.types import CategoricalDtype
from typing import Tuple, List
from nltk.util import ngrams
from nltk import FreqDist
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from data_display.display_data_in_3d import ThreeD_Charts

class _3D_PSP_corpus:
    
    def __onFilterChange(self, lst: list[str], key: str) -> None:
        if key in st.session_state:
            st.session_state[key] = lst
        else:
            st.warning("Unknown session state key: ",key)

    def __filterAPNNch(self) -> Tuple[any, list[str]]:
        def get_new_values_list(key: str=""):
            self.__onFilterChange(st.session_state[key], key)
        def prepareSortDict(lst: list[str]) -> Dict[str, int]:
            my_dict = dict()
            for ctr, val in enumerate(lst):
                my_dict[val] = ctr
            return my_dict
        col1, col2 = st.columns([2,2])
        with col1:
            colName = st.multiselect("Choose input(first phrase)/output(rephrase)", 
                                        default=st.session_state[str(self.__prefix)+"filterLst2"],
                                        options=DataProvider.getPSPcolumns1(),
                                        on_change=get_new_values_list,
                                        kwargs={'key': str(self.__prefix)+"filterLst2"},
                                        key = str(self.__prefix)+"filterLst2")
        with col2:
            Computation_type = st.radio("Choose Percentage/Number",
                ("Percentage",
                    "Number"),
                key=self.__prefix+"PercentNumber")
        dyn_rephrase_options = st.multiselect("Choose part of speech", 
                                    default=st.session_state[str(self.__prefix)+"filterLst"],
                                    options=sorted(DataProvider.getPSPlst()),
                                    on_change=get_new_values_list,
                                    kwargs={'key': str(self.__prefix)+"filterLst"},
                                    key = str(self.__prefix)+"filterLst")
        threshold = 7
        sortDic = prepareSortDict(DataProvider.getPSPlst())
        dyn_rephrase_options = sorted(dyn_rephrase_options, key=lambda x: sortDic[x])
        return dyn_rephrase_options, Computation_type, colName, threshold

    def __loader(self, mySet: set[str]):
        tmp = pd.DataFrame()
        for ddf in self.__dataDic.items():
            if ddf[0] in mySet:
                tmp = pd.concat([ddf[1], tmp])
        tmp.reset_index(inplace=True)
        return tmp

    def __prepCorpora_and_DynRephType(self) -> Dict[str, Dict[str, int]]:
        corpus3Ddic = {
             'Total': {'US2016redditD1','US2016redditR1','US2016redditG1','US2016tvD1','US2016tvR1','US2016tvG1','Hansard','PolarIs1vacc'},
             'SocialMedia': {'US2016redditD1','US2016redditR1','US2016redditG1','PolarIs1vacc'},
             'Media': {'US2016tvD1','US2016tvR1','US2016tvG1'},
             'F2F': {'Hansard'}
        }
        filterLst, computation_type, dataColumn, threshold = self.__filterAPNNch()
        dic3D = {}
        for item in corpus3Ddic.items():
            my_data = self.__loader(item[1])
            if computation_type == "Percentage":
                tmpDict = DataManipulator.getTagsPercentageFreq(d=my_data,colLst=dataColumn,PSPset=set(tag for tag in filterLst))
            elif computation_type == "Number":
                tmpDict = DataManipulator.getTagsFreq(my_data,colLst=dataColumn,PSPset=set(tag for tag in filterLst))
            else:
                st.error("Unknown opion: ",computation_type," in __prepCorpora_and_DynRephType")
            dic3D[item[0]] = dict()
            for dyn in filterLst:
                if dyn in tmpDict:
                    dic3D[item[0]][dyn] = {'Frequency': tmpDict[dyn]}
                else:
                    dic3D[item[0]][dyn] = {'Frequency': 0}
        #st.table(dic3D)
        return dic3D, threshold

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="3D_", anType: str="DynRephAn for Ethos") -> None:
        self.__prefix = prefix
        if str(self.__prefix + 'filterLst') not in st.session_state:
            st.session_state[self.__prefix + 'filterLst'] = DataProvider.getPSPlstDefault()
        if str(self.__prefix + 'filterLst2') not in st.session_state:
            st.session_state[self.__prefix + 'filterLst2'] = DataProvider.getPSPcolumns1()
        self.__plotData1 = None
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
    
    def draw3D(self):
        self.__plotData1, threshold = self.__prepCorpora_and_DynRephType()
        #print("*******************************")
        ploter = ThreeD_Charts()
        ploter.CorporaVsDynRephrasePlot(self.__plotData1,
                                        threshold,
                                        "Corpora VS Parts of Speech distribution",
                                        "Color Scale"
                                        )
        #st.write(self.__plotData1)
        #print("*******************************")