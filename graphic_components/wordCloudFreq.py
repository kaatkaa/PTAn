import streamlit as st
import sys
import pandas as pd
import io
import re
import matplotlib.pyplot as plt
from typing import Any, Tuple, List, Dict
from wordcloud import WordCloud
from config.config_data_colector import DataProvider

from graphic_components.superComponent import SuperWordCloudFreq
sys.path.insert(0,"..")

class WordCloudOfFreq(SuperWordCloudFreq):

    def getChartObj(self, freqDict: Dict[str,int], t: str) -> Any:

        if len(freqDict) > 0:
            wordcloud = WordCloud(background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                                normalize_plurals=False).generate_from_frequencies(freqDict)
            if self._cf['imediatePlot']:
                fig, ax = plt.subplots(figsize=(5, 4), facecolor=None)
                ax.set_title(t,fontsize=14)
                ax.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)
                return fig
            else:
                axTmp = self._cf['ax'][self._cf['_8x_dims'][self._cf['subChartPosition']][0],
                        self._cf['_8x_dims'][self._cf['subChartPosition']][1]]
                axTmp.title.set_text(t)
                axTmp.xaxis.set_visible(False)  # hide the x axis
                axTmp.yaxis.set_visible(False)  # hide the y axis
                axTmp.imshow(wordcloud)
    
    def dataDisplay(self, freqDict: Dict[str, int], t: str) -> None:
        if len(freqDict) > 0:
            # st.subheader(self._cf['generalConfig']["Wordcloud_display"])
            t = re.sub("wholeAll|whole","",t)
            chart = self.getChartObj(freqDict=freqDict, t=t)
            buf = io.BytesIO()
            chart.savefig(buf, format="png", dpi=300)
            left_co, cent_co = st.columns([1,3])
            with cent_co:
                st.image(buf)
            with left_co:
                btn = st.download_button(
                    label="Download as PNG",
                    data=buf,
                    file_name=t,
                    key=self._cf['prefix']+"_wordCloud",
                    mime="image/png")
        else:
            st.warning("You have to provide corpora for text analysis.")