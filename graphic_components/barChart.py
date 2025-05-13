import streamlit as st
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any
import io

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Barchart2(SuperChartComponent):

    def getChartObj(self, data: Any, t: str) -> sns.barplot():
        columnLst = list(data.columns.values)
        if len(columnLst) > 0:
            if self._cf['unitSpeakerSel'] == None:
                unit = "Text"
            else:
                unit = self._cf['unitSpeakerSel']
            if self._cf['imediatePlot']:
                fig, z = plt.subplots(figsize=(7, 8))
                z = sns.barplot(data = data, x = columnLst[0], y = columnLst[1], 
                    palette = self._cf['palette'])
            else:
                axTmp = self._cf['ax'][self._cf['_8x_dims'][self._cf['subChartPosition']][0],
                        self._cf['_8x_dims'][self._cf['subChartPosition']][1]]
                z = sns.barplot(data = data, x = columnLst[1], y = columnLst[0], 
                    palette = self._cf['palette'], ax=axTmp)
            if self._cf['unitPercentNumber'] == "Percentage":
                z.bar_label(z.containers[0], fmt='%d%%')
            elif self._cf['unitPercentNumber'] == "Number":
                z.bar_label(z.containers[0], fmt='#%d')
            z.grid(b=True, which='major', color='black', linewidth=0.075)
            if self._cf['imediatePlot']:
                z.axes.set_title(label=unit,fontsize=14)
            else:
                z.axes.set_title(label=t,fontsize=24)
            z.set_xlabel(columnLst[0],fontsize=14)
            z.set_ylabel(columnLst[1], fontsize=14)
            z.tick_params(labelsize=14)
            if self._cf['imediatePlot']:
                return fig
            else:
                return z
        else:
            return None

    def dataDisplay(self, data: Any, t: str) -> Any:
        if len(data) > 0:
            fig = self.getChartObj(data, t)
            fn = "BarChart_"+"_"+t
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300)
            left_co, cent_co, right_co = st.columns([1,2,1])
            with cent_co:
                st.image(buf)
            with left_co:
                btn = st.download_button(
                    label="Download as PNG",
                    data=buf,
                    file_name=fn,
                    mime="image/png")
        #st.pyplot(fig=fig.get_figure(), config=DataProvider.getSaveConfig())
        #fig.containers.pop()
        #fig.cla()