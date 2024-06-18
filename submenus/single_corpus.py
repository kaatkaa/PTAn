import streamlit as st
import pandas as pd
from typing import Tuple, List, Dict, Any

import sys
sys.path.insert(0,"..")
from graphic_components.filterInterface import FilterInterface
from data_manipulation.data_filter import DataFilter
from graphic_components.pieChart import Piechart2
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2
from graphic_components.textAnalysis import Cases2
from config.config_data_colector import DataProvider
from submenus.tweaker import st_tweaker
from st_ant_tree import st_ant_tree
from streamlit_modal import Modal

class SingleCorpusMenu:

    __debug = False

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="0_") -> None:
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
        #Prefix to distinguish between different data sets
        self.__prefix = prefix
        #loading config file for ethos and sentiment
        tmp = DataProvider.getPTAnCfgJson()

        self.__ptan_df = pd.DataFrame()
        self.__ptan_old = pd.DataFrame()

        if self.__checkSessionState():
            self.__update_corpora_checkbox
        else:
            # ADU or Speaker
            st.session_state[self.__prefix + 'Units'] = ""
            # Speaker type: "Text" or "Speaker", default is ""
            st.session_state[self.__prefix + 'unitChoice'] = ""
        print("Reloaded!!!")

    def __checkSessionState(self) -> bool:
        for key in self.__dataDic:
            if self.__prefix + key not in st.session_state:
                return False
        if self.__prefix + 'Units' not in st.session_state:
            return False
        if self.__prefix + 'unitChoice' not in st.session_state:
            return False
        return True

    def cleanSelections(self):
        for key in self.__dataDic:
            st.session_state[self.__prefix + key] = False
        #st.session_state[self.__prefix + "ElectionsSM"] = False
        st.session_state[self.__prefix + "US2016G1tv"] = False
        self.__ptan_df = pd.DataFrame()
        self.__ptan_old = self.__ptan_df.copy(deep=True)
        self.__iat_df = pd.DataFrame()
        self.__iat_old = self.__ptan_df.copy(deep=True)

    def __update_corpora_checkbox(self):
        colsToMerge = DataProvider.getTagColumnsLstToMerge()
        colsRel = DataProvider.getTagColumnsLstToMergeRel()
        def prepareDf(lst):
            if len(lst) > 1:
                result = pd.concat(lst,ignore_index=True)        
            elif len(lst) == 1:
                result = lst[0]
            else:
                result = pd.DataFrame()
            return result
        def logicFunc(*args) -> str:
            if args[0] == 1:
                return colsToMerge[0]
            elif args[1] == 1:
                return colsToMerge[1]
            elif args[2] == 1:
                return colsToMerge[2]
            else:
                return "Error"
        def logicFuncRel(*args) -> str:
            def checkRel() -> str:
                if args[3] == "no_relation":
                    return "_noRel"
                else:
                    return "_Rel"
            if args[0] == 1:
                return colsToMerge[0] + checkRel()
            elif args[1] == 1:
                return colsToMerge[1] + checkRel()
            elif args[2] == 1:
                return colsToMerge[2] + checkRel()
            else:
                return "Rel--Error"
        ptan_dfLst = []
        iat_dfLst = []
        for key in self.__dataDic:
            if st.session_state[self.__prefix + key]:
                if key.endswith("PTA"):
                    ptan_dfLst.append(self.__dataDic[key])
                elif key.endswith("IAT"):
                    iat_dfLst.append(self.__dataDic[key])
                
        self.__ptan_df = prepareDf(ptan_dfLst)
        if len(self.__ptan_df) > 0:
            self.__ptan_df[DataProvider.getTagColumnName()] = \
                self.__ptan_df[colsToMerge].apply(lambda x: logicFunc(x[colsToMerge[0]], x[colsToMerge[1]], x[colsToMerge[2]]), axis=1)
            self.__ptan_df[DataProvider.getTagColumnNameRel()] = \
                self.__ptan_df[colsRel].apply(lambda x: logicFuncRel(x[colsRel[0]], x[colsRel[1]], x[colsRel[2]], x[colsRel[3]]), axis=1)
        self.__iat_df = prepareDf(iat_dfLst)
        self.__ptan_old = self.__ptan_df.copy(deep=True)
        self.__iat_old = self.__iat_df.copy(deep=True)

    def __update_block(self, name: str):
        for key in self.__dataDic:
            if key.find(name) != -1:
                #print("Block:", self.__prefix + name," Updates: ",self.__prefix + key)
                st.session_state[self.__prefix + key] = st.session_state[self.__prefix + name]
                self.__update_corpora_checkbox()

    def __corporaPickerChckBox(self):
        us2016G1tv = False
        for ctr, key in enumerate(self.__dataDic):
            if key.find("US2016G1tv") != -1:
                if not us2016G1tv:
                    us2016G1tv = True
                    st.checkbox("US2016G1tv", \
                        key = self.__prefix + "US2016G1tv",
                        help = self.__prefix + "US presidential elections 2016 Hillary vs Trump",
                        value = False,
                        on_change=self.__update_block,
                        kwargs = {"name": "US2016G1tv"},
                        disabled=False
                    )           
                st_tweaker.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False,
                    id = "US2016G1tv" + str(ctr)
                )              
            else:
                st.checkbox(key, \
                    key = self.__prefix + key,
                    help = self.__prefix + key,
                    value = False,
                    on_change=self.__update_corpora_checkbox,
                    kwargs = {},
                    disabled=False
                )
        self.__update_corpora_checkbox()
        st.markdown("""
        <style>
        #US2016G1tv0,#US2016G1tv1 {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
            

    def sidebar(self):       
        with st.sidebar:
            st.subheader("Choose Corpora: ")           
            st.button("Clean selection",key=self.__prefix+"clear_corpo_button",on_click=self.cleanSelections)
            self.__corporaPickerChckBox()
            st.write("****************************")
            st.subheader("Analysis Units")
            Text_or_Speaker = st.radio("Unit picker",("Text","Speaker"),
                     key=self.__prefix+"Text-Based",
                     index=0,
                     label_visibility='hidden')
            if Text_or_Speaker == "Text":
                st.session_state[self.__prefix + 'unitChoice'] = None
            elif Text_or_Speaker == "Speaker":
                if len(self.__ptan_df) > 0:
                    speakersLst = self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]].unique().tolist()
                    speaker = st.radio("Choose Speaker: ",
                        speakersLst,
                        key=self.__prefix+"Choose_Speaker")
                    self.__ptan_df = self.__ptan_df.loc[self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]] == speaker]
                    self.__iat_df = self.__iat_df.loc[
                        (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[1]] == speaker) | 
                        (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[2]] == speaker)]
                    st.session_state[self.__prefix + 'unitChoice'] = speaker
                    st.session_state[st.session_state['cfgId']]['unitChoice'] = speaker
                else:
                    st.session_state[self.__prefix + 'unitChoice'] = None
                    st.session_state[st.session_state['cfgId']]['unitChoice'] = None
            st.write("****************************")
            st.subheader("Statictical module")
            module_choice = st.radio("An. Module", \
                                        ("Distribution",), \
                                        key=self.__prefix+"post", label_visibility="hidden"
                                    )
        st.markdown("""
        <style>
        #US2016G1tv0,#US2016G1tv1 {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
        if module_choice == "Distribution":
            __DistribCfg = {
                'prefix':'distributions_',
                'imediatePlot': True,
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'showStopWordsInterface':True
            }
            DataProvider.updateGlobalConfig(config=__DistribCfg)
            if SingleCorpusMenu.__debug:
                st.button(key="Session_state..", label='Session_state')
                modal = Modal(key="session_st", title="showPOSInterface check")
                if modal.is_open():
                    with modal.container():
                        st.write(st.session_state[st.session_state['cfgId']])
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__ptan_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            #st.write(dataDict)
            pieTab, barTab, tableTab, casesTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table",":speech_balloon: Cases"])
            with pieTab:
                Piechart2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
            with barTab:
                Barchart2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with tableTab:
                Table2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with casesTab:
                Cases2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
        else:
            raise NotImplementedError("Unsupported option of Analytical module in single_corpus.py .")
        
    #Returns criteria to which data is selected
    def getCriteria(self) -> str:
        if len(self.__dataDic) > 0:
            newLst = []
            # if st.session_state[self.__prefix + 'Units'] == "Text-Based Analysis":
            if self.__prefix + 'unitChoice' in st.session_state:
                newLst = ['Unit: '+st.session_state[self.__prefix + 'unitChoice']]
            else:
                newLst = ['error']
            ctr = 1
            for key in self.__dataDic:
                if key.endswith("PTA"):
                    if st.session_state[self.__prefix + key]:
                        ctr += 1
                        newLst.append(key)
                        if ctr == 2:
                            newLst.append("\n")
                            ctr = 0
            self.criteria = "|".join(newLst)
        else:
            self.criteria = ""
        return self.criteria

    def tab(self):
        st.subheader("Choose Corpora: ")
        self.__corporaPickerChckBox()
        if len(self.__ptan_old) > 0:
            unitChoice = st.radio("Choose Unit Type: ",
                ("Text","Speaker"),
                key=self.__prefix+"Text_Cmp_Speaker")
            if unitChoice == "Text":
                self.__ptan_df = self.__ptan_old.copy(deep=True)
                self.__iat_df = self.__iat_old.copy(deep=True)
                speaker = "Text"
            elif unitChoice == "Speaker":
                self.__ptan_df = self.__ptan_old.copy(deep=True)
                self.__iat_df = self.__iat_old.copy(deep=True)
                speakersLst = self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]].unique().tolist()
                speaker = st.radio("Choose Speaker: ",
                    speakersLst,
                    key=self.__prefix+"Choose_Cmp_Speaker")
                self.__ptan_df = self.__ptan_df.loc[self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]] == speaker]
                self.__iat_df = self.__iat_df.loc[
                    (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[1]] == speaker) | 
                    (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[2]] == speaker)]
            st.session_state[self.__prefix + 'unitChoice'] = speaker

    #Returns data for diagrams
    def getDF(self) -> List[pd.DataFrame]:
        return [self.__ptan_df, self.__iat_df]