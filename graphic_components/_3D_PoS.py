import streamlit as st
import sys
import pandas as pd
import numpy as np
import re
from functools import cmp_to_key
from typing import Dict, Any, List
#from data_display.barchart3d import barchart3d
from typing import Tuple
sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_display.display_data_in_3d import ThreeD_Charts
from data_manipulation.data_filter import DataFilter
from data_display.display_data_in_3d import ThreeD_Charts

class _3D_PoS:

    def __prepareData(self, allCorpora_dataDic: Any) -> Dict[str, pd.DataFrame]:
        initialCorporaDic = dict()
        for item in DataProvider.get3DcorpoDic().items():
            tmp = pd.DataFrame()
            for ddf in allCorpora_dataDic.items():
                if ddf[0] in item[1]:
                    tmp = pd.concat([ddf[1], tmp])
            tmp.reset_index(inplace=True)
            initialCorporaDic[item[0]] = tmp
        return initialCorporaDic
    
    def __fillEmptyMatrixFields(self, matrix: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
        sortDict = {key: i for i, key in enumerate(DataProvider.getPoSlst())}
        for item in self.__cfg['posCategories']:
            if item not in matrix:
                matrix[item] = {'Frequency': 0}
        return dict(sorted(matrix.items(), key=lambda d: sortDict[d[0]]))

    def __init__(self, dataDic: Any, config: Dict[str, Any]) -> None:

        self.__cfg = config
        self.__allSpeakersDic = {}
        for item in self.__prepareData(dataDic).items():
            tmpDic = DataFilter(data=item[1],config=config).getDataDict()
            if len(tmpDic) > 0:
                for filteredItem in tmpDic.items():
                    if not filteredItem[0].startswith("whole"):
                        title = re.sub("gruppedAll|grupped","",filteredItem[0])
                        tmpDf = filteredItem[1]
                        columnLst = list(tmpDf.columns.values)
                        tmpDf.rename(columns = {columnLst[1]:'Frequency'}, inplace = True)
                        tmpDf = tmpDf.set_index('PoS_type')
                        tmpDict = self.__fillEmptyMatrixFields(matrix=tmpDf.to_dict('index'))
                        self.__allSpeakersDic[title] = self.__allSpeakersDic.get(title, {})
                        if item[0] not in self.__allSpeakersDic[title]:
                            self.__allSpeakersDic[title][item[0]] = tmpDict
                        else:
                            st.error("Item already in 3D dictionary!")

    def plot3D(self):    
        with st.form("Form: "+self.__cfg['prefix']):
            if st.form_submit_button("Show 3D PoS "+self.__cfg['generalConfig']['anName']):
                for speaker in self.__allSpeakersDic.items():
                    # st.write(matrix)
                    ThreeD_Charts.CorporaVsDynRephrasePlot(matrix=speaker[1],
                        threshold=[0,0],
                        title="3D "+self.__cfg['generalConfig']['anName']+" PoS "+str(speaker[0]))
