import streamlit as st
import pandas as pd

import sys

from typing import Dict, Any
from submenus.single_corpus import SingleCorpusMenu
from config.config_data_colector import DataProvider
from data_display.display_corpora_cmp import ComparativeCorporaSimple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components._3D_EthosPathos import _3D_EthosPathos
from graphic_components.filterInterface import FilterInterface
from graphic_components._3D_PoS import _3D_PoS

class CmpCorpusMenu:

    def __init__(self, dataDict: pd):

        self.__anCf = {
            'prefix':'no_prefix_set_',
            # imediatePlot - set to True if plotting single corpora charts 
            # - to False if plotting in comparative analysis charts
            'imediatePlot': False,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False
        }

        #Below are tab labels
        self.__tabLabels: list[str] = ["Data("+str(x)+")" for x in range(1,9,1)]
        #Below is loaded SingleCorpusMenu for each tab
        self.__dataLoaders: list[SingleCorpusMenu] = [SingleCorpusMenu(dataDic=dataDict, prefix=str(ctr)+"0_") for ctr in range(1,9,1)]
        self.__tabLabels.append("Comparative Analysis PTAn")
        # In dictionary below all __dataDic keys are stored for Data(1)-(8)
        self.__keyDic = {}
        # In dictionary below all data_frames will be stored for comparison
        self.__dataDic = {}

    def display(self):
        st.markdown("""
            <style>
            .stRadio [role=radiogroup]{
                display: flex;
                justify-content: space-between;
            }
            </style>
        """,unsafe_allow_html=True)
        st.divider()
        tabs = st.tabs(tabs=self.__tabLabels)
        for ctr, i in enumerate(tabs):
            if ctr < (len(tabs)-1):
                with i:
                    st.subheader("**Pick your data set "+str(ctr+1)+".**")
                    self.__dataLoaders[ctr].tab()
                    # if __dataDic was previously filled, now new data will be stored in it so it has to be cleared.
                    if str(ctr)+"_" in self.__keyDic:
                        #st.text(self.__keyDic[str(ctr)+'_'])
                        del self.__dataDic[self.__keyDic[str(ctr)+"_"]]
                        del self.__keyDic[str(ctr)+"_"]
                    self.__keyDic[str(ctr)+"_"] = self.__tabLabels[ctr]+" |"+self.__dataLoaders[ctr].getCriteria()
                    st.write(self.__keyDic[str(ctr)+"_"])
                    self.__dataDic[self.__keyDic[str(ctr)+"_"]] = self.__dataLoaders[ctr].getDF()
            else:
                with i:
                    st.subheader(self.__tabLabels[ctr])
                    self.__display = ComparativeCorporaSimple(data_dic=self.__dataDic, config=st.session_state[st.session_state['cfgId']])
        self.__display.noteClass()

    def clearTabsSelections(self) -> None:
        for tab in self.__dataLoaders:
            tab.cleanSelections()