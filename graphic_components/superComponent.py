import streamlit as st
import sys
import re
import pandas as pd
import seaborn as sns
import numpy as np
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")

class dataHandlerDisplayInterface:

    def dataDisplay(self, dataDic: Any, t: str) -> None:
        st.write("This is SuperChartComponent method that should be overlapped.")

    def getChartObj(self, dataDic: Any, t: str) -> Any:
        st.write("This is SuperChartComponent method that should be overlapped.")

    def getChartsDic() -> Dict[str, Any]:
        st.write("This is SuperChartComponent method that should be overlapped.")

class SuperChartComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        self.__data = {}
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                #print(key)
                if not key.startswith("whole"):
                    title = re.sub("gruppedAll|grupped","",key)
                    self.dataDisplay(dataDic[key],title)
        else:
            for ctr, key in enumerate(dataDic.keys()):
                self._cf['subChartPosition'] = ctr
                self.__data[key] = self.getChartObj(dataDic[key],key)

    def getChartsDic(self) -> Dict[str, Any]:
        return self.__data

# class SuperPoSTextComponent(dataHandlerDisplayInterface):

#     def __init__(self, dataPoS_Dict: Dict[str, Any], config: Dict[str, Any]) -> None:
#         self._cf = config
#         if self._cf['imediatePlot']:
#             for key in dataPoS_Dict.keys():
#                 if not key.startswith("CMP"):
#                     self.dataDisplay(dataPoS_Dict[key],key)
    
class SuperTextComponent(dataHandlerDisplayInterface):

    def __init__(self, dataDic: Dict[str, Any], config: Dict[str, Any]) -> None:
        self._cf = config
        self.__chartDict = {}
        self.__textDict = {}
        if self._cf['imediatePlot']:
            for key in dataDic.keys():
                if not key.startswith("grupped"):
                    title = re.sub("wholeAll|whole","",key)
                    self.dataDisplay(dataDic[key],title)
        else:
            for ctr, key in enumerate(dataDic.keys()):
                self._cf['subChartPosition'] = ctr
                if self._cf['objectToEnable'] == "Chart":
                    self.__chartDict[key] = self.getChartObj(dataDic[key],key)
                elif self._cf['objectToEnable'] == "Text":
                    self.__textDict[key] = self.getTextObj(dataDic[key],key)

    def getTextObj(self, data: Any, t: str) -> Any:
        st.write("This is SuperChartComponent method that should be overlapped.")

    def getTextDic(self) -> Dict[str, Any]:
        return self.__textDict
    
    def getChartsDic(self) -> Dict[str, Any]:
        return self.__chartDict