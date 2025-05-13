import streamlit as st
import sys
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import dataframe_image as dfi
from typing import Tuple, List, Dict, Any
from pandas.plotting import table

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Table2(SuperChartComponent):

    def getChartObj(self, df: Any, t: str) -> Any:
        columnLst = list(df.columns.values)
        if self._cf['unitSpeakerSel'] == None:
            unit = "Text"
        else:
            unit = self._cf['unitSpeakerSel']
        def make_pretty(styler):
            styler.set_caption(unit)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        tmpDf = df.copy(deep=True)
        tmpDf = tmpDf.sort_values(by=columnLst[1], ascending=False)
        tmpDf.reset_index(drop=True,inplace=True)
        tmpDf.index += 1
        if len(columnLst) == 3:
            tmpDf = tmpDf[[columnLst[2],columnLst[1]]]
        if self._cf['imediatePlot']:
            return make_pretty(tmpDf.style)
        elif len(tmpDf) > 0:
            axTmp = self._cf['ax'][self._cf['_8x_dims'][self._cf['subChartPosition']][0],
                    self._cf['_8x_dims'][self._cf['subChartPosition']][1]]
            axTmp.title.set_text(unit)
            axTmp.xaxis.set_visible(False)  # hide the x axis
            axTmp.yaxis.set_visible(False)  # hide the y axis
            ytable = table(ax=axTmp, data=tmpDf, loc='center')
            ytable.set_fontsize(self._cf['SubTableFontSize'])
            ytable.scale(self._cf['SubTableXscale'], self._cf['SubTableYscale'])

    def dataDisplay(self, data: Any, t: str) -> Any:
        if len(data) > 0:
            tbl = self.getChartObj(data, t)
            st.table(tbl)
        # data = BytesIO()
        # fn = "Table.png"
        # dfi.export(tbl, data, dpi=200)
        # btn = st.download_button(
        #     label="Download as PNG",
        #     data=data,
        #     file_name=fn,
        #     mime="image/png")
