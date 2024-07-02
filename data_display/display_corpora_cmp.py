import streamlit as st
import io
import sys
import pandas as pd
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px

from typing import Dict, Any, Tuple, TypeVar
sys.path.insert(0,"..")
from graphic_components.barChart import Barchart2
from graphic_components.table import Table2
from graphic_components.wordCoud import WordCloudOfRephrase
from graphic_components.filterInterface import FilterInterface
from graphic_components.ngrams import Ngrams
from config.config_data_colector import DataProvider
from data_manipulation.data_filter import DataFilter


class ComparativeCorporaSimple:

    def noteClass(self):
        pass

    def __init__(self, data_dic: dict[str,pd.DataFrame()], config: Dict[str,Any]):
        self.prefixCtr = 1
        self.__dataDic = data_dic
        self.__cf = config
        with st.sidebar:
            st.header("Statistical module")
            module = st.radio("Choose module: ", ("Distribution",),
                            label_visibility='collapsed', key=str(self.prefixCtr)+"CMP_module_")
            self.prefixCtr += 1
        if module == "Distribution" and len(self.__dataDic) > 0:
            self.Distribution()
        # elif module == "Wordcloud" and len(self.__dataDic) > 0:
        #     self.WordCloud()
        # elif module == "n-grams" and len(self.__dataDic) > 0:
        #     self.Ngrams()
        # elif module == "PoS" and len(self.__dataDic) > 0:
        #     self.PoS()
        else:
            st.error("Unknown option for comparative analysis.")

    def __Display(self, data_dic: dict[str,pd.DataFrame()], classType: Any, prefix: str) -> Any:
        if len(data_dic) > 1:
            fig, ax = plt.subplots(4, 2, figsize=(10,45), sharex=True)
            fig.subplots_adjust(left=-1, bottom=0.1, right=1.2, top=0.9, wspace=0.2, hspace=0.2)
            sns.set(font_scale=2)
            self.__cf['ax'] = ax
            x = [ k for k in classType(dataDic=data_dic,config=self.__cf).getChartsDic().keys()]
            st.pyplot(fig=fig, config=DataProvider.getSaveConfig())
            fn = 'comparative_analysis.png'
            img = io.BytesIO()
            fig.savefig(img,fig=fig, format='png',height=1080, width=800,bbox_inches="tight")
            st.download_button(
                key=prefix+"_saveBtn",
                label="Download as image",
                data=img,
                file_name=fn,
                mime="image/png"
            )
            return x
        else:
            st.write("**Add More Data to Compara.**")
            return None

    def __updateCfg(self, config: Dict[str,Any]) -> None:
        for item in config.items():
            self.__cf[item[0]] = item[1]
    
    def __loadFilteredDataToDic(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        gruppedDataDic = {}
        wholeDataDic = {}
        for key in self.__dataDic.keys():
            tmpDic = DataFilter(data=self.__dataDic[key][0],config=self.__cf,prefix=self.__dataDic[key][2]).getDataDict()
            if len(tmpDic) > 0:
                gruppedDataDic[key] = tmpDic['gruppedAll']
                wholeDataDic[key] = tmpDic['wholeAll']
        return gruppedDataDic, wholeDataDic

    def Distribution(self):
        overrideConfig = {
            'prefix':'CmpDistribution',
            'imediatePlot': False,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'showStopWordsInterface':False,
            'showStopwords':False,
            'useStopwords':False,
        }
        self.__updateCfg(config=overrideConfig)
        self.__cf = FilterInterface(config=self.__cf).getConfig()
        gruppedDataDic, wholeDataDic = self.__loadFilteredDataToDic()
        chart, table = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
        with chart:
            self.__Display(data_dic=gruppedDataDic, classType=Barchart2, prefix="BarCmpDistribution")
            self.prefixCtr +=1
        with table:
            self.__cf['SubTableXscale'] = .9
            self.__cf['SubTableYscale'] = 6.5
            self.__cf['SubTableFontSize'] = 24
            self.__Display(data_dic=gruppedDataDic, classType=Table2, prefix="TableCmpDistribution")
            self.prefixCtr += 1

    def Ngrams(self):
        overrideConfig = {
            'prefix':'CmpNgrams',
            'imediatePlot': False,
            'objectToEnable': "Text",
            'showPercentageNumber': False,
            'showCategoriesInterface': True,
            'ADU_or_Speaker':"",
            'SS rephrase': False,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False,
            'showNgramSlider': True
        }
        self.__updateCfg(config=overrideConfig)
        self.__cf = FilterInterface(config=self.__cf).getConfig()
        gruppedDataDic, wholeDataDic = self.__loadFilteredDataToDic()
        st.header("The most frequent ngrams")
        self.__cf['SubTableXscale'] = .9
        self.__cf['SubTableYscale'] = 2
        self.__cf['SubTableFontSize'] = 18
        self.__classNote0 = self.__Display(data_dic=wholeDataDic, classType=Ngrams, prefix="CmpNgrams")
        self.prefixCtr += 1

    def WordCloud(self):
        overrideConfig = {
            'prefix':'CmpWordcloud',
            'imediatePlot': False,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'ADU_or_Speaker':"",
            'SS rephrase': False,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showStopWordsInterface':True,
            'showStopwords':False,
            'useStopwords':True,
            'showPOSInterface':False,
            'showNgramSlider': False
        }
        self.__updateCfg(config=overrideConfig)
        self.__cf = FilterInterface(config=self.__cf).getConfig()
        gruppedDataDic, wholeDataDic = self.__loadFilteredDataToDic()
        wordcloud, top20words = st.tabs([":rain_cloud: Wordcloud",":top: Top_20_Words"])
        with wordcloud:
            self.__cf['objectToEnable'] = "Chart"
            self.__classNote0 = self.__Display(data_dic=wholeDataDic, classType=WordCloudOfRephrase, prefix="CmpWordcloud")
            self.prefixCtr += 1
        with top20words:
            self.__cf['objectToEnable'] = "Text"
            self.__cf['SubTableXscale'] = .9
            self.__cf['SubTableYscale'] = 2
            self.__cf['SubTableFontSize'] = 18
            self.__Display(data_dic=wholeDataDic, classType=WordCloudOfRephrase, prefix="Top20CmpWordcloud")
            self.prefixCtr += 1

    def PoS(self):
        overrideConfig = {
            'prefix':'CmpPoS',
            'imediatePlot': False,
            'showPercentageNumber': True,
            'unitPercentNumber': 'Percentage',
            'showCategoriesInterface': True,
            'ADU_or_Speaker':"",
            'SS rephrase': False,
            'OS rephrase': False,
            'showInOutInterface': True,
            'showStopWordsInterface':False,
            'showStopwords':False,
            'useStopwords':False,
            'showPOSInterface':True,
            'showNgramSlider': False
        }
        self.__updateCfg(config=overrideConfig)
        self.__cf = FilterInterface(config=self.__cf).getConfig()
        gruppedDataDic, wholeDataDic = self.__loadFilteredDataToDic()
        chart, table, = st.tabs([":bar_chart: Barchart",":black_square_button: Table"])
        with chart:
            self.__Display(data_dic=gruppedDataDic, classType=Barchart2, prefix="ChartCmpPoS")
            self.prefixCtr +=1
        with table:
            self.__cf['SubTableXscale'] = .9
            self.__cf['SubTableYscale'] = 2
            self.__cf['SubTableFontSize'] = 18
            self.__Display(data_dic=gruppedDataDic, classType=Table2, prefix="TableCmpPoS")
            self.prefixCtr += 1
        self.prefixCtr += 1


# Save to file first or an image file has already existed.
# fn = 'scatter.png'
# plt.savefig(fn)
# with open(fn, "rb") as img:
#     btn = st.download_button(
#         label="Download image",
#         data=img,
#         file_name=fn,
#         mime="image/png"
#     )
