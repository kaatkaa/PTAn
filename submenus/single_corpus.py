import streamlit as st
import pandas as pd
from typing import Tuple, List, Dict, Any
import ast

import sys
sys.path.insert(0,"..")
from graphic_components.filterInterface import FilterInterface
from data_manipulation.data_filter import DataFilter
from graphic_components.pieChart import Piechart2
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2
from graphic_components.textAnalysis import Cases2
from graphic_components.wordCloudFreq import WordCloudOfFreq
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from submenus.tweaker import st_tweaker
# from st_ant_tree import st_ant_tree
from streamlit_modal import Modal

class SingleCorpusMenu:

    __debug = False

    def __init__(self, dataDic: dict[str : pd.DataFrame()], prefix: str="0_") -> None:
        #dictionary containing all possible data with corpora indexed by name
        self.__dataDic = dataDic
        #Prefix to distinguish between different data sets
        self.__prefix = prefix
        #loading config file for ethos and sentiment
        # tmp = DataProvider.getPTAnCfgJson()

        self.__ptan_df = pd.DataFrame()
        self.__ptanStatements_df = pd.DataFrame()
        self.__ptan_old = pd.DataFrame()

        if self.__checkSessionState():
            self.__update_corpora_checkbox
        else:
            # ADU or Speaker
            st.session_state[self.__prefix + 'Units'] = ""
            # Speaker type: "Text" or "Speaker", default is ""
            st.session_state[self.__prefix + 'unitChoice'] = ""
        # print("Reloaded!!!")

    def __checkSessionState(self) -> bool:
        for key in self.__dataDic:
            if self.__prefix + key not in st.session_state:
                return False
        # if self.__prefix + 'Units' not in st.session_state:
        #     return False
        # if self.__prefix + 'unitChoice' not in st.session_state:
        #     return False
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
        subjectDict = dict()
        colsToMerge = DataProvider.getTagColumnsLstToMerge()
        colsRel = DataProvider.getTagColumnsLstToMergeRel()
        relLst = DataProvider.getPTA_RelSP_Dims()
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
                return relLst[0].replace("_noRel","") + checkRel()
            elif args[1] == 1:
                return relLst[1].replace("_noRel","") + checkRel()
            elif args[2] == 1:
                return relLst[2].replace("_noRel","") + checkRel()
            else:
                return "Rel--Error"
            
        def concattContents(*args) -> str:
            if args[0] == 1:
                if args[1] != "no_relation":
                    subjectDict[args[1]] = True
                    return ' '.join(self.__ptan_df['content'].loc[self.__ptan_df["mid"] == args[1]].values) + " " + args[2]
                else:
                    return "??predicate??" + " " + args[2]
            else:
                return "£§£====§§"
            
        def subjectAdder(*args) -> str:
            if args[0] == 0:
                if args[1] not in subjectDict:
                    return 1
                else:
                    return 0
            return 0

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
            self.__ptan_df[DataProvider.getSubPredColumnName()] = \
                self.__ptan_df[colsToMerge].apply(lambda x: logicFunc(x[colsToMerge[0]], x[colsToMerge[1]], x[colsToMerge[2]]), axis=1)
            self.__ptan_df[DataProvider.getSubPredColumnNameRel()] = \
                self.__ptan_df[colsRel].apply(lambda x: logicFuncRel(x[colsRel[0]], x[colsRel[1]], x[colsRel[2]], x[colsRel[3]]), axis=1)
            self.__ptanStatements_df = self.__ptan_df.copy(deep=True)
            self.__ptanStatements_df[DataProvider.getStatementName()] = \
                self.__ptan_df[["Predicate", "Links", "content"]].apply(lambda x: concattContents(x["Predicate"], x["Links"], x["content"]), axis=1)
            # The below loads subjectDict
            self.__ptanStatements_df = self.__ptanStatements_df[self.__ptanStatements_df[DataProvider.getStatementName()] != "£§£====§§"]
            # The below only works if subjectDict is properly loaded
            self.__ptan_df['xxx'] = self.__ptan_df[["Predicate", "mid"]].apply(lambda x: subjectAdder(x["Predicate"], x["mid"]), axis=1)
            self.__ptan_df[DataProvider.getStatementName()] = "??Subject?? " + self.__ptan_df['content'] 
            self.__ptanStatements_df = pd.concat([self.__ptanStatements_df, self.__ptan_df.loc[self.__ptan_df['xxx'] == 1]])
                
        self.__iat_df = prepareDf(iat_dfLst)
        self.__ptan_old = self.__ptan_df.copy(deep=True)
        #self.__iat_old = self.__iat_df.copy(deep=True)

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
        def unitUpdate():
            st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] = int(
                not bool(st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'])
            )
            if st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] == 1:
                st.session_state[st.session_state['cfgId']]['unitSpeakerLst'] = self.__ptan_df[DataProvider.getSpeakerColumnName()].unique().tolist()
                if st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] == None:
                    st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] = st.session_state[st.session_state['cfgId']]['unitSpeakerLst'][0]
                elif st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] == "Text":
                    st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] = st.session_state[st.session_state['cfgId']]['unitSpeakerSelOld']
            elif st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] == 0:
                st.session_state[st.session_state['cfgId']]['unitSpeakerLst'] = None
                st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] = "Text"
            else:
                st.error("Wrong units option: ",st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'],
                    "Must be Text or Speaker.")
            
        with st.sidebar:
            st.subheader("Choose Corpora: ")
            st.button("Clean selection",key=self.__prefix+"clear_corpo_button",on_click=self.cleanSelections)
            self.__corporaPickerChckBox()
            st.write("****************************")
            st.subheader("Analysis Units")
            st.session_state[st.session_state['cfgId']]['unitTextOrSpeaker'] = st.radio("Unit picker",
                st.session_state[st.session_state['cfgId']]['unitTextSpeakerOptions'],
                key=self.__prefix+"Text-Based",
                index=0,
                on_change=unitUpdate,
                label_visibility='hidden'
            )
            st.write("****************************")
            st.subheader("Statictical module")
            st.write("Distribution")
            module_choice = st.radio("An. Module", \
                                        ("Subjects_WordCloud","SP","FVPo","SP->FVPo"), \
                                        key=self.__prefix+"post", label_visibility="hidden"
                                    )
        st.markdown("""
        <style>
        #US2016G1tv0,#US2016G1tv1 {
            margin-left: 50px;
        }
        </style>
        """,unsafe_allow_html=True)
        if module_choice == "Subjects_WordCloud":
            __DistribCfg = {
                'prefix':'WordCloud_Subjects',
                'imediatePlot': True,
                'showRelationalRadiobutton': False,
                'categoriesColumn': DataProvider.getSubPredColumnName(),
                'categoriesColumnRel': "",
                'categoriesLst': DataProvider.getPTA_NrelS_Dims(),
                'categoriesLstRel': [],
                'showPercentageNumber': False,
                'showCategoriesInterface': True,
                'showStopWordsInterface':False,
                'textColumnToShow': DataProvider.getContentColumnName()
            }
            DataProvider.updateGlobalConfig(config=__DistribCfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__ptan_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            if len(self.__ptan_df) > 0:
                WordCloudOfFreq(dataDic=DataManipulator.getDictFreq(d=dataDict['whole Text'],colLst=[DataProvider.getContentColumnName()]), 
                                config=st.session_state[st.session_state['cfgId']],title="Wordcloud of selected subjects:")
        elif module_choice == "SP":
            __DistribCfg = {
                'prefix':'distributionsSP_',
                'imediatePlot': True,
                'showRelationalRadiobutton': True,
                'categoriesColumn': DataProvider.getSubPredColumnName(),
                'categoriesColumnRel': DataProvider.getSubPredColumnNameRel(),
                'categoriesLst': DataProvider.getPTA_NrelSP_Dims(),
                'categoriesLstRel': DataProvider.getPTA_RelSP_Dims(),
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'showStopWordsInterface':False,
                'textColumnToShow': DataProvider.getContentColumnName()
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
        elif module_choice == "FVPo":
            __DistribCfg = {
                'prefix':'distributionsSPVo_',
                'categoryIndex': 0,
                # 'categories': DataProvider.getFVPoDims(),
                'categoriesLst': DataProvider.getFVPoDims(),
                'categoriesColumn': DataProvider.getFVPoColumnName(),
                'palette': DataProvider.getFVPoColors(),
                'text_color': DataProvider.getFVPoTextColors(),
                'imediatePlot': True,
                'showPercentageNumber': True,
                'showCategoriesInterface': True,
                'showRelationalRadiobutton': False,
                'showStopWordsInterface':False,
                'textColumnToShow': DataProvider.getStatementName(),
            }
            DataProvider.updateGlobalConfig(config=__DistribCfg)
            st.session_state[st.session_state['cfgId']] = \
                FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
            dataDict = DataFilter(data=self.__ptanStatements_df,config=st.session_state[st.session_state['cfgId']]).getDataDict()
            pieTab, barTab, tableTab, casesTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table",":speech_balloon: Cases"])
            with pieTab:
                Piechart2(dataDic=dataDict,config=st.session_state[st.session_state['cfgId']])
            with barTab:
                Barchart2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with tableTab:
                Table2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
            with casesTab:
                Cases2(dataDic=dataDict, config=st.session_state[st.session_state['cfgId']])
        elif module_choice == "SP->FVPo":
            prefixesLst = ["distributionsPred-SPVo_","distributionsSubject-SPVo_","distributionsImplicitSubject-SPVo_"]
            SPISlst = DataProvider.getPTA_NrelSP_Dims()
            descLst = ["Predicates derived statements","Subject derived statements","Implicit Subject derived statements"]
            for i in range(len(prefixesLst)):
                __DistribCfg = {
                    'prefix':prefixesLst[i],
                    'categoryIndex': 0,
                    # 'categories': DataProvider.getFVPoDims(),
                    'categoriesLst': DataProvider.getFVPoDims(),
                    'categoriesColumn': DataProvider.getFVPoColumnName(),
                    'palette': DataProvider.getFVPoColors(),
                    'text_color': DataProvider.getFVPoTextColors(),
                    'imediatePlot': True,
                    'showPercentageNumber': True,
                    'showCategoriesInterface': True,
                    'showRelationalRadiobutton': False,
                    'showStopWordsInterface':False,
                    'textColumnToShow': DataProvider.getStatementName(),
                }
                DataProvider.updateGlobalConfig(config=__DistribCfg)
                st.session_state[st.session_state['cfgId']] = \
                    FilterInterface(config=st.session_state[st.session_state['cfgId']]).getConfig()
                tmpDf = self.__ptanStatements_df.copy(deep=True)
                tmpDf = tmpDf.loc[tmpDf[SPISlst[i]] == 1]
                dataDict = DataFilter(data=tmpDf,config=st.session_state[st.session_state['cfgId']]).getDataDict()
                pieTab, barTab, tableTab, casesTab = st.tabs([":pizza: PieChart",":bar_chart: BarChart",":black_square_button: Table",":speech_balloon: Cases"])
                st.header(descLst[i])
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
            if st.session_state[st.session_state['cfgId']]['unitTextOrSpeaker'] == "Speaker":
                if self.__prefix + 'unitSpeakerSel' in st.session_state[st.session_state['cfgId']]:
                    newLst = ['Speaker: '+st.session_state[self.__prefix+'unitSpeakerSel']]
                else:
                    newLst = ['error']
            else:
                newLst = ['Text']
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
        def unitUpade():
            # to be adapted
            st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] = int(
                not bool(st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'])
            )
            if st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] == 1:
                st.session_state[st.session_state['cfgId']]['unitSpeakerLst'] = self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]].unique().tolist()
                if st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] == None:
                    st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] = st.session_state[st.session_state['cfgId']]['unitSpeakerLst'][0]
                self.__ptan_df = self.__ptan_df.loc[self.__ptan_df[DataProvider.getSpeakerColumnNamesLst()[0]] == st.session_state[st.session_state['cfgId']][self.__prefix+'unitSpeakerSel']]
            elif st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'] == 0:
                pass
            else:
                st.error("Wrong units option: ",st.session_state[st.session_state['cfgId']]['unitTextSpeakerIndex'],
                    "Must be Text or Speaker.")
            # self.__ptan_df = self.__ptan_old.copy(deep=True)
            # self.__iat_df = self.__iat_old.copy(deep=True)
        st.subheader("Choose Corpora: ")
        self.__corporaPickerChckBox()
        if len(self.__ptan_old) > 0:
            st.session_state[st.session_state['cfgId']]['unitTextOrSpeaker'] = st.radio("Choose Unit Type: ",
                ("Text","Speaker"),
                on_change=unitUpade,
                index=1,
                key=self.__prefix+"Text_Cmp_Speaker")
                # self.__iat_df = self.__iat_df.loc[
                #     (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[1]] == speaker) | 
                #     (self.__iat_df[DataProvider.getSpeakerColumnNamesLst()[2]] == speaker)]

    #Returns data for diagrams
    def getDF(self) -> List[pd.DataFrame]:
        return [self.__ptan_df, self.__iat_df, self.__prefix]