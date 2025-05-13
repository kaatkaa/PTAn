import streamlit as st
import sys
from typing import Tuple, List, Dict, Any
from wordcloud import STOPWORDS
from streamlit_modal import Modal


sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator

class FilterInterface:

    __debug = False

    __config: Dict[str, Any]={
    }

    def __init__(self, config: Dict[str, Any]) -> None:
        self.__cf=FilterInterface.__config
        self.__keyCtr = 0
        for cfg in config.items():
            self.__cf[cfg[0]] = cfg[1]
        self.__stop_words_set = set()
        for word in DataProvider.getCustomStopWords():
            self.__stop_words_set.add(word)
        for word in list(STOPWORDS):
            self.__stop_words_set.add(word)
        self.__cf['StopwordsSet'] = self.__stop_words_set
        self.__filterInterface()

    def getConfig(self) -> Dict[str, Any]:
        return self.__cf

    def __filterInterface(self) -> Tuple[Any, list[str]]:
        col_radio1, col_radio2, col_user_sel= st.columns(3)

        if self.__cf['showPercentageNumber']:
            with col_radio1:
                self.__units()
            
        if self.__cf['showCategoriesInterface']:
            self.__categories(col_radio2)

        if self.__cf['imediatePlot']:
            if self.__cf['unitTextOrSpeaker'] == "Text":
                with col_user_sel:
                    st.write("Selected unit: \"Text\"")
            else:
                with col_user_sel:
                    st.session_state[st.session_state['cfgId']]['unitSpeakerSel'] = st.selectbox("Pick user to analyse: ",
                        st.session_state[st.session_state['cfgId']]['unitSpeakerLst'],
                        key="Speaker_mode_sel"                                                                  
                    )

        if self.__cf['showStopWordsInterface']:
            self.__stopWords()

    def __updateConfig(self, dict: Dict[str,Any]):
        for item in dict.items():
            self.__cf[item[0]] = item[1]

    def __units(self):
        def update_unit_radio(x):
            self.__cf['unitPercentNumberIndex'] = int(not bool(x))
        self.__cf['unitPercentNumber'] = st.radio("Choose units",
            self.__cf['unitsPercentageNumber'],
            index=self.__cf['unitPercentNumberIndex'],
            on_change=update_unit_radio,
            args=(self.__cf['unitPercentNumberIndex'],),                                          
            key=self.__cf['prefix']+"_Units"+str(self.__keyCtr))
        self.__keyCtr += 1

    def __categories(self, col) -> str:
        if self.__cf['showRelationalRadiobutton']:
            with col:
                display_complexity = st.radio("Choose rel/non_rel subject / predicate",
                    ("non Relational",
                        "Relational",
                    ),
                    index=self.__cf['categoryIndex'],                                              
                    key=self.__cf['prefix']+"_Rephrase_4-6cat"+str(self.__keyCtr))
                self.__keyCtr += 1
            if display_complexity == 'non Relational':
                self.__cf['categoryIndex'] = 0
                # sortDict = {key: i for i, key in enumerate(DataProvider.getDynRephDimentions())}
                self.__cf['categoriesLst'] = st.multiselect("Select non relational tags: ",
                                            sorted(DataProvider.getPTA_NrelSP_Dims()), 
                                            self.__cf['categoriesLst'],
                                            key = self.__cf['prefix']+"_multi_sel"+str(self.__keyCtr))
                self.__keyCtr += 1
                self.__cf['categoriesColumn'] = DataProvider.getSubPredColumnName()
                self.__cf['palette'] = DataProvider.getPTA_NrelSP_Colors()
                self.__cf['text_color'] = DataProvider.getPTA_NrelSP_ColorsText()
            elif display_complexity == 'Relational':
                self.__cf['categoryIndex'] = 1
                self.__cf['categoriesLstRel'] = st.multiselect("Select relational tags: ", 
                                            sorted(DataProvider.getPTA_RelSP_Dims()), 
                                            self.__cf['categoriesLstRel'],
                                            key = self.__cf['prefix']+"_multi_selRel"+str(self.__keyCtr))
                self.__keyCtr += 1
                # self.__cf['categoriesLstRel'] = sorted(self.__cf['categoriesLstWS'], key=lambda d: sortDict[d])
                self.__cf['categoriesColumn'] = DataProvider.getSubPredColumnNameRel()
                self.__cf['palette'] = DataProvider.getPTA_RelSP_Colors()
                self.__cf['text_color'] = DataProvider.getPTA_RelSP_ColorsText()
        else:
            self.__cf['categoryIndex'] = 0
            self.__cf['categoriesLst'] = st.multiselect("Select VFPo tags: ", 
                                        sorted(self.__cf['categoriesLst']), 
                                        self.__cf['categoriesLst'],
                                        key = self.__cf['prefix']+"_multi_selRel"+str(self.__keyCtr))
            self.__keyCtr += 1
        # else:
        #     st.error("Oprion not implemented in __filterInterface, class: WordCloudOfEmotions")

    def __stopWords(self):
        col1, col2 = st.columns([2,2])
        with col1:
            useStopWords = st.checkbox(label="Enable stop_words",
                                        value=self.__cf['useStopwords'],
                                        key=self.__cf['prefix']+"_StopWordsChck"+str(self.__keyCtr),
                                        )
            self.__keyCtr += 1
        with col2:
            showStopWords = st.checkbox(label="Show stop_words",
                                        value=self.__cf['showStopwords'],
                                        key=self.__cf['prefix']+"_ShowWordsChck"+str(self.__keyCtr)
                                        )
            self.__keyCtr += 1
        if showStopWords:
            st.write(self.__stop_words_set)
        self.__cf['useStopwords'] = useStopWords