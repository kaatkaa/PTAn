import streamlit as st
import sys
import pandas as pd
import re
import ast
from operator import itemgetter
from typing import Tuple, List, Dict, Any, Set
from streamlit_modal import Modal


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class DataFilter:

    __debug = False

    __config: Dict[str, Any]={
        # 'generalConfig':DataProvider.getDynRephrESconfig()['DynRephAn for Sentiment'],
        'prefix':'no_prefix_set_',
        # imediatePlot - set to True if plotting single corpora charts 
        # - to False if plotting in comparative analysis charts
        'imediatePlot': True,
        'showPercentageNumber': False,
        'unitPercentNumber': 'Percentage',
        'unitsPercentageNumber': ('Percentage','Number'),
        'showCategoriesInterface': False,
        'categoriesColumn': '',
        'categoriesLst': DataProvider.getPTA_NrelSP_Dims(),
        'Units': '',
        'showStopWordsInterface':False,
        'showStopwords':False,
        'useStopwords':False,
        'StopwordsSet': set(),
    }

    def __RemoveStopWordsFromDf(self, dataF: Any, columns: List[str], stopwords_set: Set[str]) -> None:
        for stop_phrase in stopwords_set:
            p1 = re.compile(r"\s+"+stop_phrase+r"\s+", flags=re.I|re.S)
            p2 = re.compile(r"^"+stop_phrase+r"\s+|\s+"+stop_phrase+r"$|^"+stop_phrase+r"$", flags=re.I|re.S)
            for column in columns:
                dataF[column] = dataF[column].str.replace(p1, " ", regex=True)
                dataF[column] = dataF[column].str.replace(p2, "", regex=True)
        self.__outputData = dataF

    def __init__(self, data: Any, config: Dict[str, Any], prefix: str='') -> None:
        self.__prefix = prefix
        self.__cf=DataFilter.__config
        self.__stop_words_set = self.__cf['StopwordsSet']
        self.__ngramLst = []
        if DataFilter.__debug:
            open_modal = False
            open_modal = st.button(key="debug config button", label='debuf_fData')
            modal = Modal(key="Debugger_fData", title="Check config selected settings")
        if len(data) > 0:
            if DataFilter.__debug and open_modal:
                with modal.container():
                    st.markdown("config['showPOSInterface'] = "+str(config['showPOSInterface']))
                    open_modal = st.button(key="modal_debug_closer", label='Close debug info')
            for cfg in config.items():
                self.__cf[cfg[0]] = cfg[1]
            self.__d = data
            self.__outputData = data.copy(deep=True)
            self.__outDict = dict()
            self.__filterInterface()
        else:
            self.__outputData = data
            self.__outDict = data

    def getDataDict(self) -> Dict[str, Any]:
        return self.__outDict
    
    def getNgramLst(self) -> List[Tuple[str, int]]:
        return self.__ngramLst
        
    def __filterInterface(self) -> Tuple[Any, list[str]]:        
        if self.__cf['showCategoriesInterface'] and len(self.__outputData) > 0:
            if self.__cf['categoryIndex'] == 0:
                #print("self.__cf['categoriesColumn']=",self.__cf['categoriesColumn']," self.__cf['categoriesLst']=",self.__cf['categoriesLst'])
                self.__outputData = self.__outputData.loc[self.__outputData[self.__cf['categoriesColumn']].isin(self.__cf['categoriesLst'])]
            elif self.__cf['categoryIndex'] == 1:
                #print("self.__cf['categoriesColumnRel']=",self.__cf['categoriesColumnRel'],"self.__cf['categoriesLstRel']=",)
                self.__outputData = self.__outputData.loc[self.__outputData[self.__cf['categoriesColumnRel']].isin(self.__cf['categoriesLstRel'])]
        else:
            self.__outputData = self.__d

        # if self.__cf['showStopWordsInterface'] and self.__cf['useStopwords'] and len(self.__outputData) > 0:
        #     self.__RemoveStopWordsFromDf(self.__outputData, self.__cf['content'], self.__stop_words_set)

        if self.__cf['imediatePlot']:
            if self.__cf['unitTextOrSpeaker'] == "Text":
                pass
            elif self.__cf['unitTextOrSpeaker'] == "Speaker":
                # not refreshing in filterInterface!!!
                self.__outputData = self.__outputData.loc[
                    self.__outputData[DataProvider.getSpeakerColumnName()] == st.session_state[st.session_state['cfgId']]['unitSpeakerSel']
                ]

            self.__outDict["whole Text"] = self.__outputData
            if self.__cf['categoryIndex'] == 0:
                    self.__outDict["grupped Text"] = self.__distributionData(self.__outputData, self.__cf['categoriesColumn'])
                    #print("self.__outDict=",self.__outDict)

            elif self.__cf['categoryIndex'] == 1:
                self.__outDict["grupped Text"] = self.__distributionData(self.__outputData, self.__cf['categoriesColumnRel'])

    def __distributionData(self, data, column):
        if self.__cf['unitPercentNumber'] == "Percentage":
            return DataManipulator.getGruppedPercentages(d=data, 
                denominator=len(data),
                groupBy=column,
                col_name="Percentage")
        elif self.__cf['unitPercentNumber'] == "Number":
            return DataManipulator.getGruppedData(d=data,
                groupBy=column,
                col_name="Number")
        else:
            st.error("Wrong option: "+self.__cf['unitPercentNumber']+" for __distributionData!")