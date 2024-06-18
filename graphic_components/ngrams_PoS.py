import streamlit as st
import sys
import pandas as pd
import numpy as np
import re
import ast
from nltk.util import ngrams
from pandas.plotting import table
from nltk import FreqDist
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from data_manipulation.data_manipulator import DataManipulator
from graphic_components.superComponent import SuperTextComponent

class NgramsPoS(SuperTextComponent):

    def noteClass(self):
        pass
        
    def getTextObj(self, data: Any, t: str) -> Any:
        colorsDict = DataProvider.getUniversalColors()
        cat = [self._cf['categoriesColumn']]
        def color(row, columns, colorFlagHashes):
            formattingLst = []
            for column in columns:
                if column in colorFlagHashes:
                    formattingLst.append('background-color: '+DataProvider.getRephraseAndEmptycolors()['Rephrase'])
                else: 
                    formattingLst.append('background-color: '+colorsDict[row[cat[0]]])
            return formattingLst
        lstOfInOut = []
        restLst = []
        PoSflag = False
        if set(self._cf['inOutLst']) <= set(DataProvider.getInOutColLst()[2]):
            lstOfInOut = [*cat, *DataProvider.getInOutColLst()[2]]
            restLst = DataProvider.getInOutColLst()[0]
            PoSflag = True
        elif set(self._cf['inOutLst']) <= set(DataProvider.getInOutColLst()[3]):
            lstOfInOut = [*cat, *DataProvider.getInOutColLst()[3]]
            restLst = DataProvider.getInOutColLst()[0]
            PoSflag = True
        else:
            st.warning("Wrong list inOut values in n-gram data display.")
        wordLst = []
        if len(data) > 0:
            for inOut in self._cf['inOutLst']:
                tmpLst = []
                for token in data[inOut].tolist():
                    token = " ".join(token)
                    tmpLst.append(token)
                    wordLst.extend(ngrams(token.split(" "), 1))
                data[inOut] = tmpLst
        if len(wordLst) > 0:
            wordLst = FreqDist(wordLst)
            if self._cf['imediatePlot']:
                number = st.slider("Pick top n words/phrases: ", 1, value=10, max_value=len(wordLst), key="Num"+self._cf['prefix']+t)
                ngramType = st.slider("Choose n-gram type: (1-4)",1,value=2, max_value=4, key="n-gramType"+self._cf['prefix']+t)
            else:
                number = 20
                ngramType = self._cf['ngramSliderValue']
            NgramLst = []
            for inOut in self._cf['inOutLst']:
                for token in map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")):
                    NgramLst.extend(ngrams(token.split(" "), ngramType))
            NgramLst = FreqDist(NgramLst)
            common = NgramLst.most_common(number)
            if self._cf['imediatePlot']:
                w2 = [" ".join(item[0])+" : "+str(item[1]) for item in common if item[0] != ('',)]
                word = st.selectbox("Pick "+str(ngramType)+"-gram to analyse: ",w2,index=0,key='Dropdown'+str(ngramType)+'-gram_'+t)
                regexpStr = re.sub(r"^(.*)\s:\s[0-9]+$", r"\1", word)
                regExpCode = r"\s"+regexpStr+r"\s|^"+regexpStr+r"\s|\s"+regexpStr+r"$|^"+regexpStr+r"$"
                st.subheader("Selected phrase is marked in text below between stars: \*\*"+regexpStr+"\*\*")
                if lstOfInOut[1] in self._cf['inOutLst'] and lstOfInOut[2] in self._cf['inOutLst']:
                    filteredInputDF = data[data[lstOfInOut[1]].str.contains(regExpCode, case=False, regex=True)]
                    filteredInputDF.reset_index(inplace=True)
                    filterInOutDF = filteredInputDF[filteredInputDF[lstOfInOut[2]].str.contains(regExpCode, case=False, regex=True)]
                    tmpDf = filterInOutDF[[*lstOfInOut,*restLst]]
                    tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                    tmpDf = tmpDf.sort_values(by=cat[0])
                    tmpDf = tmpDf.reset_index(drop=True)
                    tmpDf.index += 1
                    lstOfInOut.remove(cat[0])
                    columns = [*cat,*lstOfInOut,*restLst]
                    return tmpDf[columns].style.apply(color, axis=1, columns=columns, colorFlagHashes=set(lstOfInOut))
                elif lstOfInOut[1] in self._cf['inOutLst']:
                    x = lstOfInOut[2]
                    filteredInputDF = data[data[lstOfInOut[1]].str.contains(regExpCode, case=False, regex=True)]
                    filteredInputDF.reset_index(inplace=True)
                    tmpDf = filteredInputDF[[*lstOfInOut,*restLst]]
                    tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                    tmpDf = tmpDf.sort_values(by=cat[0])
                    tmpDf = tmpDf.reset_index(drop=True)
                    tmpDf.index += 1
                    lstOfInOut.remove(cat[0])
                    columns = [*cat,*lstOfInOut,*restLst]
                    lstOfInOut.remove(x)
                    return tmpDf[columns].style.apply(color, axis=1, columns=columns, colorFlagHashes=set(lstOfInOut))
                elif lstOfInOut[2] in self._cf['inOutLst']:
                    x = lstOfInOut[1]
                    filteredOutputDF = data[data[lstOfInOut[2]].str.contains(regExpCode, case=False, regex=True)]
                    filteredOutputDF.reset_index(inplace=True)
                    tmpDf = filteredOutputDF[[*lstOfInOut,*restLst]]
                    tmpDf = tmpDf.replace("(?i)"+regExpCode," **"+regexpStr+"** ", regex=True)
                    tmpDf = tmpDf.sort_values(by=cat[0])
                    tmpDf = tmpDf.reset_index(drop=True)
                    tmpDf.index += 1
                    lstOfInOut.remove(cat[0])
                    columns = [*cat,*lstOfInOut,*restLst]
                    lstOfInOut.remove(x)
                    return tmpDf[columns].style.apply(color, axis=1, columns=columns, colorFlagHashes=set(lstOfInOut))
                else:
                    st.error("Wrong input-output options for dataframe")
            else:
                ngramsLst, freqLst = [], []
                [ ngramsLst.append(" ".join(item[0])) for item in common if item[0] != ('',)]
                [ freqLst.append(item[1]) for item in common if item[0] != ('',)]
                tmpDict = {'{n}-gram'.format(n=ngramType,rank=number):ngramsLst[:number],'frequency':freqLst[:number]}
                tmpDf = pd.DataFrame(tmpDict)
                tmpDf.index += 1
                axTmp = self._cf['ax'][self._cf['_8x_dims'][self._cf['subChartPosition']][0],
                        self._cf['_8x_dims'][self._cf['subChartPosition']][1]]
                axTmp.title.set_text(t)
                axTmp.xaxis.set_visible(False)  # hide the x axis
                axTmp.yaxis.set_visible(False)  # hide the y axis
                ytable = table(ax=axTmp, data=tmpDf, loc='center')
                ytable.set_fontsize(self._cf['SubTableFontSize'])
                ytable.scale(self._cf['SubTableXscale'], self._cf['SubTableYscale'])
        else:
            st.warning("Not enought data to display in text analysis.")
    
    def dataDisplay(self, data: Any, t: str) -> None:
        tbl = self.getTextObj(data=data, t=t)
        st.table(tbl)