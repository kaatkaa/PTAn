import json
import os
import streamlit as st
from typing import Tuple, List, Dict, Any

class DataProvider:
    __tableFormat = [
        {"selector": "caption","props":[("text-align", "center"),
            ("font-size", "20px"),
            ("color", 'black'),
            ('caption-side','top')]},
        {"selector": "", "props": [("border", "1px solid grey")]},
        {"selector": "tbody td", "props": [("border", "1px solid grey")]},
        {"selector": "th", "props": [("border", "2px solid black")]}
    ]

    __PTAn_file = 'config/PTAnConfig.json'
    __lst_of_subj_pred_NoRel = ['Predicate', 'Subject', 'ImplicitSubject']
    __lst_of_subj_NoRel = ['Subject', 'ImplicitSubject']
    __lst_of_subj_pred_Rel = ['S_noRel', 'P_noRel', 'IS_noRel','S_Rel', 'P_Rel', 'IS_Rel']
    __lst_of_SPVo = ["VALUE","FACT","POLICY",'no_relation','relation']

    __color_SP_noRel = {'Subject':'#008CFF','Predicate':'#E02D00','ImplicitSubject':'#01FCF4'}
    __color_SP_noRel_Text = {'Subject':'#FFFFFF','Predicate':'#FFFFFF','ImplicitSubject':'#000000'}
    
    __color_SP_Rel = {'S_noRel':'#4891FF','P_noRel':'#FF0000','IS_noRel':'#01FCF4'
                     ,'S_Rel':'#0008F5','P_Rel':'#BD0000','IS_Rel':'#00DDFF'}
    __color_SP_Rel_Text = {'S_noRel':'#000000','P_noRel':'#FFFFFF','IS_noRel':'#000000'
                     ,'S_Rel':'#FFFFFF','P_Rel':'#FFFFFF','IS_Rel':'#000000'}
    
    __color_FVP = {"relation":'#00F1F5',"no_relation":'#0008F5',"VALUE":'#FF0000',"FACT":'#f5aa60',"POLICY":'#51FF00'}
    __color_FVP_text = {"relation":'#000000',"no_relation":'#FFFFFF',"VALUE":'#FFFFFF',"FACT":'#000000',"POLICY":'#000000'}
    
    # __color_PoS ={
    #     "PROPN": '#B3B3B3',"AUX": '#47CCD3',"VERB": '#FF0000',"PRON": '#0008FF',"NOUN": '#51FF00',
    #     "CCONJ": '#dcb559',"ADP": '#f5bc6b',"DET": '#f5aa60',"PART": '#f39659',"ADJ": '#FF00FB',
    #     "NUM": '#ec6e55',"PUNCT": '#e65857',"ADV": '#D0FF00',"INTJ": '#501D5B',"SYM": '#2D157B',
    #     "SCONJ": '#2E3390',"SPACE": '#213766',"X": '#2A565C'
    # }

    # __PoS = ["PROPN","AUX","VERB","PRON","NOUN","CCONJ","ADP","DET","PART","ADJ","NUM","PUNCT","ADV","INTJ","SYM","SCONJ","SPACE","X"]

    # __PoS_Converter = {"PROPN":"Proper noun","AUX":"Auxiliary verb",
    #     "VERB":"Verb","PRON":"Pronoun","NOUN":"Noun","CCONJ":"Coordinating conjunction",
    #     "ADP":"Adposition","DET":"Determinative","PART":"Part",
    #     "ADJ":"Adjective","NUM":"Cardinal numbers","PUNCT":"Punctuation","ADV":"Adverb",
    #     "INTJ":"Interjection","SYM":"Symbol","SCONJ":"Subordinating conjunction",
    #     "SPACE":"Space","X":"Unknowx","":"--"}
    
    # __PoS_defalut = ["PROPN","AUX","VERB","PRON","NOUN","CCONJ","NUM"]
        
    __sav_image = {
        'toImageButtonOptions': {
            'format': 'png', # one of png, svg, jpeg, webp
            'filename': 'presentation_image',
            'height': 1080,
            'width': 1180,
            'scale':6 # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    __custom_stop_words = [
            "http", "https", "co", "rt",
            "donald", "trump", "mike", "pence",
            "hillary","hilary", "clinton", "joe", "biden",
            "michael", "bloomberg", "jeb", "bush","nicholas", "ridley",
            "ben", "carson", "lincoln" "chafee",
            "chris", "christie", "ted", "cruz",
            "carly", "fiorina", "obama", "obama",
            "jim", "gilmore",
            "lindsey", "graham"
            "mike", "huckabee",
            "bobby", "jindal",
            "john", "kasich",
            "lawrence", "lessig",
            "martin", "o'malley",
            "george", "pataki",
            "rand", "paul",
            "rick", "perry",
            "marco", "rubio",
            "bernie", "sanders",
            "rick", "santorum",
            "scott", "walker",
            "elizabeth", "warren",
            "jim", "webb","mr"
    ]

    __customSpacyTagTypes = ['text','lemma_','pos_','tag_','dep_','shape_','morph','ent_type_','ent_iob_']

    @staticmethod
    def updateGlobalConfig(config: Dict[str, Any]) -> None:
        for cfg in config.items():
            st.session_state[st.session_state['cfgId']][cfg[0]] = cfg[1]

    @staticmethod
    def addSpacelines(number=2):
        for i in range(number):
            st.write("\n")

    @staticmethod
    def getPTAnCfgJson():
        return DataProvider.__PTAn_file

    @staticmethod
    def getPTA_NrelSP_Dims():
        return DataProvider.__lst_of_subj_pred_NoRel
    
    @staticmethod
    def getPTA_NrelS_Dims():
        return DataProvider.__lst_of_subj_NoRel

    @staticmethod
    def getPTA_RelSP_Dims():
        return DataProvider.__lst_of_subj_pred_Rel
    
    @staticmethod
    def getFVPoDims() -> List[str]:
        return DataProvider.__lst_of_SPVo

    @staticmethod
    def getPTA_NrelSP_Colors():
        return DataProvider.__color_SP_noRel

    @staticmethod
    def getPTA_NrelSP_ColorsText():
        return DataProvider.__color_SP_noRel_Text

    @staticmethod
    def getPTA_RelSP_Colors():
        return DataProvider.__color_SP_Rel

    @staticmethod
    def getPTA_RelSP_ColorsText():
        return DataProvider.__color_SP_Rel_Text
    
    @staticmethod
    def getTableFormat():
        return DataProvider.__tableFormat

    @staticmethod
    def getSpeakerColumnName() -> str:
        return 'speaker'

    @staticmethod
    def getSubPredColumnName() -> str:
        return 'PS_tags'
    
    @staticmethod
    def getSubPredColumnNameRel() -> str:
        return 'PS_tagsRel'
    
    
    @staticmethod
    def getFVPoColumnName() -> str:
        return 'Relations'
    
    @staticmethod
    def getStatementName() -> str:
        return 'Statement'
    
    @staticmethod
    def getFVPoColors() -> Dict:
        return DataProvider.__color_FVP

    @staticmethod
    def getFVPoTextColors() -> Dict:
        return DataProvider.__color_FVP_text
    
    @staticmethod
    def getContentColumnName() -> str:
        return 'content'
    
    @staticmethod
    def getTagColumnsLstToMerge() -> List[str]:
        return DataProvider.__lst_of_subj_pred_NoRel
    
    @staticmethod
    def getTagColumnsLstToMergeRel() -> List[str]:
        return DataProvider.__lst_of_subj_pred_NoRel + ['Relations']
    
    @staticmethod
    def getCustomStopWords() -> List[str]:
        return DataProvider.__custom_stop_words
    
    @staticmethod
    def getSaveConfig() -> dict[str, any]:
        return DataProvider.__sav_image
    
    @staticmethod
    def getSpacyTagTypes() -> List[str]:
        return DataProvider.__customSpacyTagTypes
    
    @staticmethod
    def getContentColNames() -> List[str]:
        return ['content','locution_conclusion','locution_premise']