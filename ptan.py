# imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from submenus.single_corpus import SingleCorpusMenu
from submenus.comparative_corpus import CmpCorpusMenu
from config.config_data_colector import DataProvider

pd.set_option("max_colwidth", 300)
sns.set_theme(style="whitegrid")
plt.style.use("seaborn-talk")

__AnConfigId = "DynRephAnCfgId"
__AnConfig = {
    'prefix':'no_prefix_set_',
    # imediatePlot - set to True if plotting single corpora charts 
    # - to False if plotting in comparative analysis charts
    'imediatePlot': True,
    # For tables wit text, how much lines has to be shown from table
    'textInstances': 1,
    # Dimentions of comparative analysis chart:
    '_8x_dims': [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]],
    # The position (0-7) of current chart in subplot for comparative analysis
    'subChartPosition': 0,
    # ax of subplot
    'ax': None,
    # subplot table customalisation paremeters
    'SubTableXscale': .9,
    'SubTableYscale': 6.5,
    'SubTableFontSize': 24,
    # end of subplot Table configuration
    # Variable below enables "Chart" or "Text" component in SuperTextComponent superclass
    'objectToEnable': "Chart",
    #Text or Speaker
    'unitTextSpeakerOptions': ['Text','Speaker'],
    'unitTextSpeakerIndex': 0,
    'unitTextOrSpeaker': "Text",
    'unitSpeakerLst': None,
    'unitSpeakerSel': None,
    'unitSpeakerSelOld': None,
    #Number or percentage
    'showPercentageNumber': False,
    'unitPercentNumberIndex': 0,
    'unitPercentNumber': 'Percentage',
    'unitsPercentageNumber': ('Percentage','Number'),
    #categories interface
    'showCategoriesInterface': False,
    'categoryIndex': 0,
    'categoriesColumn': '',
    'categoriesLst': DataProvider.getPTA_NrelSP_Dims(),
    'categoriesLstRel': DataProvider.getPTA_RelSP_Dims(),
    'categoriesLstFVPo': DataProvider.getFVPoDims(),
    # Color palette
    'palette': DataProvider.getPTA_NrelSP_Colors(),
    'text_color': DataProvider.getPTA_NrelSP_ColorsText(),
    # use stopwords interface
    'content': [DataProvider.getContentColNames()[0]],
    'showStopWordsInterface':False,
    'showStopwords':False,
    'useStopwords':False,
    'StopwordsSet': set(DataProvider.getCustomStopWords()),
}

st.set_page_config(layout="wide")

# ******************* path to file **************************************

__PTAn_xlsx = r"./data_xlsx/PTAn.xlsx"

# ********************** functions **************************************

def __style_css(file):
    with open(file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def __load_data(dir_address: str) -> dict[str : pd.DataFrame()]:
    tmpDic = pd.read_excel(dir_address, sheet_name=None)
    # for corpoName in DataProvider.getCorporaSkipLst():
    #     if corpoName in tmpDic:
    #         del tmpDic[corpoName]
    return tmpDic

# ******************* multi pages functions **************************************

def __MainPage():
    st.title("Periodic Table of Arguments analytic")
    DataProvider.addSpacelines(2)
    st.write("PTAn_ver_0.1")
    with st.expander("Read abstract"):
        DataProvider.addSpacelines(1)
        st.write("""
            First PTAn implementation...
            """
        )

    with st.container():
        DataProvider.addSpacelines(3)

        st.write("**[The New Ethos Lab](https://newethos.org/)**")
        st.write(" ************************** ")

    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;font-size=18px;}</style>', unsafe_allow_html=True)

def __SingleCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()], submenu_prefix: str) -> SingleCorpusMenu:
    return SingleCorpusMenu(dataDic = dataDic, prefix = submenu_prefix)

def __ComparativeCorporaMenuLoader(dataDic: dict[str:pd.DataFrame()]) -> CmpCorpusMenu:
    return CmpCorpusMenu(dataDict=dataDic)

# def __resetData(single_corpus: SingleCorpusMenu, comparative_corpora: CmpCorpusMenu) -> None:
#     single_corpus.cleanSelections()
#     comparative_corpora.clearTabsSelections()
if __AnConfigId not in st.session_state:
    st.session_state['cfgId'] = __AnConfigId
    st.session_state[st.session_state['cfgId']] = __AnConfig
with st.sidebar:
    st.write('<style>div[class="css-1siy2j7 e1fqkh3o3"] > div{background-color: #d2cdcd;}</style>', unsafe_allow_html=True)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:column;}</style>', unsafe_allow_html=True)
    dataDic = __load_data(__PTAn_xlsx)
        
    __single_corpora_menu = __SingleCorporaMenuLoader(dataDic=dataDic, submenu_prefix="0_")
    __cmp_corpora_menu = __ComparativeCorporaMenuLoader(dataDic=dataDic)
    st.title("Contents")
    contents_radio = st.radio("Choose: ", ("Main Page", "Single Corpus Analysis", "Comparative Corpora Analysis"),label_visibility='collapsed')

if contents_radio == "Main Page":
    __MainPage()
elif contents_radio == "Single Corpus Analysis":
    __single_corpora_menu.sidebar()
elif contents_radio == "Comparative Corpora Analysis":
    with st.sidebar:
        st.button("Clear All Tabs",key="tabs_clear",on_click=__cmp_corpora_menu.clearTabsSelections)
    __cmp_corpora_menu.display()
else:
    st.error("Wrong option of main sidemenu radiobitton.")