import streamlit as st
import sys
import pandas as pd
import numpy as np
import plotly.express as px
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperChartComponent

class Piechart2(SuperChartComponent):

    def getChartObj(self, data: Any, t: str) -> px.pie():
        displayer = ""
        namesLst = list(data.columns.values)
        if self._cf['unitPercentNumber'] == "Percentage":
            displayer = 'percent+label'
        elif self._cf['unitPercentNumber'] == "Number":
            displayer = 'text+label'
        if self._cf['unitSpeakerSel'] == None:
            unit = "Text"
        else:
            unit = self._cf['unitSpeakerSel']
        if len(namesLst) == 3:
            labelsDic = {}
            labelsDic[namesLst[2]] = sorted(data[namesLst[2]].tolist())
            fig = px.pie(data, values=self._cf['unitPercentNumber'], names=namesLst[2], color=namesLst[0],
                        color_discrete_map=self._cf['palette'],
                        title=unit,
                        category_orders=labelsDic, width=1080
            )
        else:
            labelsDic = {}
            labelsDic[namesLst[0]] = sorted(data[namesLst[0]].tolist())
            fig = px.pie(data, values=self._cf['unitPercentNumber'], names=namesLst[0], color=namesLst[0],
                        color_discrete_map=self._cf['palette'],
                        title=unit,
                        category_orders=labelsDic, width=1080
            )
        fig.update_traces(textposition='inside', 
                    text=data[self._cf['unitPercentNumber']].map("#{:,}".format),
                    textinfo=displayer)
        fig.update_layout(margin=dict(t=55, b=0, l=0, r=0),
            font=dict(
                family="Arial",
                size=45,  # Set the font size here
                color="black"
            ),
            legend = dict(
                font = dict( family="Arial",
                size = 30
                )
            ),
            title = dict(
                font = dict( family="Arial",
                size = 35
                )
            )
        )
        return fig
        
    def dataDisplay(self, data: Any, t: str) -> None:
        fig = self.getChartObj(data, t)
        st.plotly_chart(fig, config=DataProvider.getSaveConfig())            