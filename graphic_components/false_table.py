import streamlit as st
import sys
import pandas as pd
import numpy as np
from io import BytesIO
import dataframe_image as dfi
from typing import Tuple, List, Dict, Any
from pandas.plotting import table

sys.path.insert(0,"..")
from graphic_components.superComponent import SuperPoSTextComponent
from submenus.tweaker import st_tweaker
from config.config_data_colector import DataProvider

class FalseTable(SuperPoSTextComponent):
    
    def dataDisplay(self, two: Tuple[Dict[str, int], Dict[str, int or float]], t: str) -> None:
        # Data inicjalization
        advPoSdict = two[1]
        if 'posSpecialContentName'+t not in st.session_state[st.session_state['cfgId']]:
            st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t] = st.session_state[st.session_state['cfgId']]['posSpecialContentName']
            st.session_state[st.session_state['cfgId']]['posSpecialContent'+t] = st.session_state[st.session_state['cfgId']]['posSpecialContent']
        def updateSpecialTagType(tagName: str):
            st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t] = tagName
            st.session_state[st.session_state['cfgId']]['posSpecialContent'+t] = advPoSdict[tagName]
        if st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t] != '':
            updateSpecialTagType(st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t])
        posDict = two[0]
        convDict = DataProvider.getPoStagsConverter()

        with st.container():
            st.subheader(st.session_state[st.session_state['cfgId']]['ADU_or_Speaker']+" "+t)

        with st.container():
            colms = st.columns((1, 4, 5, 10))
            if st.session_state[st.session_state['cfgId']]['unitPercentNumber'] == "Percentage":
                info = st.session_state[st.session_state['cfgId']]['unitPercentNumber'] + " (" + str(len(posDict)) + " tags is 100%)"
            else:
                info = "#"+st.session_state[st.session_state['cfgId']]['unitPercentNumber'] + " (number of occurences)"
            fields = ["№", 'PoS_tag', info, 
                      str(convDict[st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t]])]
            # headers of first table 
            for col, field_name in zip(colms, fields):
                # header
                col.write(field_name)

            #First "fake" table data
            markup = "<style>"
            for c, idx in enumerate(posDict.items()):
                if st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t] == idx[0]:
                    buttonBorder = "border: 2px solid #11FE00;"
                else:
                    buttonBorder = "border: 2px dotted #FF7E22;"
                tmpId = st.session_state[st.session_state['cfgId']]['prefix']+"_Btn_"+t.replace(" ","q").replace("+","i")+"_"+idx[0]
                key = st.session_state[st.session_state['cfgId']]['prefix']+"_BtnKey_"+t+"_"+idx[0]
                markup += """
                    #{myButton} {{
                        height: 24px;
                        margin: 0;
                        {border}
                    }}
                """.format(myButton=tmpId, border=buttonBorder)
                with colms[0]:
                    st.markdown("<table><tr><th>"+str(c+1)+"</th></tr></table>",unsafe_allow_html=True)
                with colms[1]:
                    st_tweaker.button(convDict[idx[0]], 
                        id=tmpId, 
                        key=key,
                        on_click=updateSpecialTagType,
                        kwargs={'tagName':idx[0]}
                    )
                with colms[2]:
                    if st.session_state[st.session_state['cfgId']]['unitPercentNumber'] == "Percentage":
                        st.markdown("<table><tr><th>"+str(idx[1])+"%"+"</th></tr></table>",unsafe_allow_html=True)
                    else:
                        st.markdown("<table><tr><th>"+"#"+str(idx[1])+"</th></tr></table>",unsafe_allow_html=True)

            # second #Real table
            if st.session_state[st.session_state['cfgId']]['posSpecialContentName'+t] != '':
                nameLst, valLst = [], []
                if st.session_state[st.session_state['cfgId']]['unitPercentNumber'] == "Percentage":
                    chooseInf = "Choose top n "+st.session_state[st.session_state['cfgId']]['posTagType']+ \
                        " ("+str(len(st.session_state[st.session_state['cfgId']]['posSpecialContent'+t]))+ \
                        " tags is 100%)"
                else:
                    chooseInf = "Choose top n "+st.session_state[st.session_state['cfgId']]['posTagType']+ \
                        " ("+str(len(st.session_state[st.session_state['cfgId']]['posSpecialContent'+t]))+ \
                        " in total)"
                with colms[3]:
                    limiter = st.slider(chooseInf,
                        min_value=1, 
                        value=st.session_state[st.session_state['cfgId']]['posLimittingSliderValue'],
                        max_value=len(st.session_state[st.session_state['cfgId']]['posSpecialContent'+t]),
                        key=st.session_state[st.session_state['cfgId']]['prefix']+"_Slider_"+t)
                    for c, item in enumerate(st.session_state[st.session_state['cfgId']]['posSpecialContent'+t].items()):
                        if c < limiter:
                            nameLst.append(item[0])
                            if st.session_state[st.session_state['cfgId']]['unitPercentNumber'] == "Percentage":
                                valLst.append(str(item[1])+"%")
                            else:
                                valLst.append("#"+str(item[1]))
                        else:
                            break
                    st.session_state[st.session_state['cfgId']]['posLimittingSliderValue'] = limiter
                    slownik = {str(st.session_state[st.session_state['cfgId']]['posTagType']):nameLst, 
                            st.session_state[st.session_state['cfgId']]['unitPercentNumber']:valLst}
                    df = pd.DataFrame(data=slownik)
                    df.index += 1
                    stt = df.style
                    # stt.set_caption()
                    stt.set_table_styles(DataProvider.getTableFormat())
                    st.table(stt)

            st.markdown(
                markup + "</style>",
                unsafe_allow_html=True
            )
