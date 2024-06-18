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
from typing import Tuple
from nltk.util import ngrams
from nltk import FreqDist
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from data_display.display_data_in_3d import ThreeD_Charts

class ThreeDCorpusMenu:
    
    def __onFilterChange(self, lst: list[str], colName = "") -> None:
        if colName == self.__anCfg['colName']:
            if str(self.__prefix + 'filterLst') in st.session_state:
                st.session_state[str(self.__prefix + 'filterLst')] = lst
                self.__filterLst = lst
            else:
                st.error("Sesion state not set for function: ",self.__onFilterChange.__name__)
        elif colName == self.__anCfg['colNameWS']:
            if str(self.__prefix + 'filterLstSW') in st.session_state:
                st.session_state[str(self.__prefix + 'filterLstSW')] = lst
                self.__filterLstSW = lst
            else:
                st.error("Sesion state SW not set for function: __onFilterChange")
        else:
            st.error("Wrong column option in __onFilterChange.")

    def __filterAPNNch(self) -> Tuple[any, list[str]]:
        col_radio1, col_radio2 = st.columns(2)
        def get_new_values_list(key: str="", colName: str=""):
            self.__onFilterChange(st.session_state[key],colName=colName)
        def prepareSortDict(lst: list[str]) -> Dict[str, int]:
            my_dict = dict()
            for ctr, val in enumerate(lst):
                my_dict[val] = ctr
            return my_dict
        dyn_rephrase_options = []
        colName = ""
        with col_radio1:
            display_complexity = st.radio("Choose complexity level: WordCloudOfEmotions",
                ("4-categories",
                    "6-categories"),
                key=self.__prefix+"Rephrase_Piechart_ADU_4-6cat")
        with col_radio2:
            Computation_type = st.radio("Choose %percentage/#number",
                ("Percentage",
                    "Number"),
                key=self.__prefix+"PercentNumber")
        # if Computation_type == "Percentage":
        #     threshold = st.slider("Choose +/- tolerance in % (Red edges do not fulfill tolerance)",1,value=7, max_value=100, key=self.__prefix+"HigherSlider") 
        # else:
        #     threshold = 0
            threshold = 7
        sortDic = dict()
        marker = ''
        if display_complexity == '4-categories':
            marker = 'colName'
            colName = self.__anCfg[marker]
            dyn_rephrase_options = st.multiselect(self.__anCfg["Wordcloud_filterInterface"], 
                                        default=list(self.__filterLst),
                                        options=list(DataProvider.getDynRephDimentions()),
                                        on_change=get_new_values_list,
                                        kwargs={'key': str(self.__prefix)+"1multi_sel",'colName':colName},
                                        key = str(self.__prefix)+"1multi_sel")
            sortDic = prepareSortDict(DataProvider.getDynRephDimentions())
        elif display_complexity == '6-categories':
            marker = 'colNameWS'
            colName = self.__anCfg[marker]
            dyn_rephrase_options = st.multiselect(self.__anCfg["Wordcloud_filterInterface"], 
                                        default=list(self.__filterLstSW),
                                        on_change=get_new_values_list,
                                        kwargs={'key': str(self.__prefix)+"2multi_sel",'colName':colName},
                                        options=list(DataProvider.getDynRephDimentionsWS()),
                                        key = str(self.__prefix)+"2multi_sel")
            sortDic = prepareSortDict(DataProvider.getDynRephDimentionsWS())
        else:
            st.warning("Option not implemented in __filterInterface, class: WordCloudOfEmotions")
        #sorts items always in the same order
        dyn_rephrase_options = sorted(dyn_rephrase_options, key=lambda x: sortDic[x])
        return dyn_rephrase_options, Computation_type, colName, marker, threshold

    def __loader(self, mySet: set[str]):
        tmp = pd.DataFrame()
        for ddf in self.__dataDic.items():
            if ddf[0] in mySet:
                tmp = pd.concat([ddf[1], tmp])
        tmp.reset_index(inplace=True)
        return tmp

    def __prepCorpora_and_DynRephType(self, bothEthosPathos: bool=False) -> Dict[str, Dict[str, int]]:
        corpus3Ddic = {
             'Total': {'US2016redditD1','US2016redditR1','US2016redditG1','US2016tvD1','US2016tvR1','US2016tvG1','Hansard','PolarIs1vacc'},
             'SocialMedia': {'US2016redditD1','US2016redditR1','US2016redditG1','PolarIs1vacc'},
             'Media': {'US2016tvD1','US2016tvR1','US2016tvG1'},
             'F2F': {'Hansard'}
        }
        filterLst, computation_type, dataColumn, marker, threshold = self.__filterAPNNch()
        dic3D = {}
        for item in corpus3Ddic.items():
            my_data = self.__loader(item[1])
            my_data = my_data.loc[my_data[dataColumn].isin(filterLst)]
            if computation_type == "Percentage":
                if bothEthosPathos:
                    tmpDf1 = DataManipulator.getGruppedPercentages(my_data,len(my_data),self.__mainCfg['DynRephAn for Ethos'][marker],"Frequency")
                    tmpDf2 = DataManipulator.getGruppedPercentages(my_data,len(my_data),self.__mainCfg['DynRephAn for Sentiment'][marker],"Frequency")
                else:
                    tmpDf = DataManipulator.getGruppedPercentages(my_data,len(my_data),dataColumn,"Frequency")
            elif computation_type == "Number":
                if bothEthosPathos:
                    tmpDf1 = DataManipulator.getGruppedData(my_data,self.__mainCfg['DynRephAn for Ethos'][marker],"Frequency")
                    tmpDf2 = DataManipulator.getGruppedData(my_data,self.__mainCfg['DynRephAn for Sentiment'][marker],"Frequency")
                else:
                    tmpDf = DataManipulator.getGruppedData(my_data,dataColumn,"Frequency")
            else:
                st.error("Unknown opion: ",computation_type," in __prepCorpora_and_DynRephType")
            if bothEthosPathos:
                tmpDf1 = tmpDf1.set_index(self.__mainCfg['DynRephAn for Ethos'][marker])
                tmpDict1 = tmpDf1.to_dict('index')
                tmpDf2 = tmpDf2.set_index(self.__mainCfg['DynRephAn for Sentiment'][marker])
                tmpDict2 = tmpDf2.to_dict('index')
                dic3D[item[0]] = dict()
                for dyn in filterLst:
                    if dyn in tmpDict1:
                        dic3D[item[0]][dyn+"_Eth"] = tmpDict1[dyn]
                    else:
                        dic3D[item[0]][dyn+"_Eth"] = {'Frequency': 0}
                    if dyn in tmpDict2:
                        dic3D[item[0]][dyn+"_Sent"] = tmpDict2[dyn]
                    else:
                        dic3D[item[0]][dyn+"_Sent"] = {'Frequency': 0}
            else:
                tmpDf = tmpDf.set_index(dataColumn)
                tmpDict = tmpDf.to_dict('index')
                dic3D[item[0]] = dict()
                for dyn in filterLst:
                    #st.write(tmpDict)
                    if dyn in tmpDict:
                        dic3D[item[0]][dyn] = tmpDict[dyn]
                    else:
                        dic3D[item[0]][dyn] = {'Frequency': 0}

        return dic3D, threshold

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="3D_", anType: str="DynRephAn for Ethos") -> None:
        self.__prefix = prefix
        self.__stop_words_set = set()
        for word in DataProvider.getCustomStopWords():
            self.__stop_words_set.add(word)
        for word in list(STOPWORDS):
            self.__stop_words_set.add(word)
        if str(self.__prefix + 'filterLst') in st.session_state:
            self.__filterLst = st.session_state[str(self.__prefix + 'filterLst')]
        else:
            self.__filterLst = DataProvider.getDynRephDimentions()
            st.session_state[self.__prefix + 'filterLst'] = self.__filterLst
        if str(self.__prefix + 'filterLstSW') in st.session_state: 
            self.__filterLstSW = st.session_state[str(self.__prefix + 'filterLstSW')]
        else:
            self.__filterLstSW = DataProvider.getDynRephDimentionsWS()
            st.session_state[str(self.__prefix + 'filterLstSW')] = self.__filterLstSW
        self.__plotData1 = None
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
        #Prefix to distinguish between different data sets
        #loading config file for ethos and sentiment
        self.__mainCfg = DataProvider.getDynRephrESconfig()
        #config file with messages and column names for Ethos and Sentiment
        self.__anCfg = self.__mainCfg[anType]
    
    def draw3D(self, bothEthosPathos = False):
        self.__plotData1, threshold = self.__prepCorpora_and_DynRephType(bothEthosPathos=bothEthosPathos)
        #print("*******************************")
        ploter = ThreeD_Charts()
        ploter.CorporaVsDynRephrasePlot(self.__plotData1,
                                        threshold,
                                        "Corpora VS DynamicRephType distribution",
                                        "Color Scale",
                                        mixed=not bothEthosPathos
                                        )
        #st.write(self.__plotData1)
        #print("*******************************")
