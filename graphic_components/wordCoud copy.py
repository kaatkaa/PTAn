import streamlit as st
import sys
import pandas as pd
import io
import re
import matplotlib.pyplot as plt
from typing import Any, Tuple, List
from wordcloud import WordCloud
from pandas.plotting import table
from config.config_data_colector import DataProvider

from graphic_components.superComponent import SuperTextComponent
sys.path.insert(0,"..")

class WordCloudOfRephrase(SuperTextComponent):

    def noteClass(self):
        pass

    def getChartObj(self, df: Any, t: str) -> Any:

        if len(df) > 0:        
            joined_set = set()
            for inOut in self._cf['inOutLst']: 
                emo_set = set(",".join(df[inOut].dropna().to_numpy(na_value="")).split(","))
                joined_set = joined_set | emo_set
            lexicon = list(joined_set)
            wordcloud = WordCloud(background_color="#493E38", colormap='YlOrRd', width=500, height=400,
                                normalize_plurals=False).generate(" ".join(lexicon))
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
    
    def getTextObj(self, data: Any, t: str) -> Any:
        def make_pretty(styler):
            styler.set_caption(t)
            styler.set_table_styles(DataProvider.getTableFormat())
            return styler
        text = ""
        for inOut in self._cf['inOutLst']:
            text += " ".join(map(str,",".join(data[inOut].dropna().to_numpy(na_value="")).split(",")))
        if text != "":
            wordLst = sorted(WordCloud().process_text(text).items(), key=lambda x:x[1], reverse=True)
            if self._cf['imediatePlot']:
                self._cf['textInstances'] = st.slider("Pick top n unigrams: ", 1, value=10, max_value=len(wordLst))
            else:
                self._cf['textInstances'] = 20
            index = []
            for i in range(1,self._cf['textInstances']+1):
                index.append(i)
            unigramsDf = pd.DataFrame(wordLst[:self._cf['textInstances']],columns = ['Top word', 'Frequency'],index=pd.Index(index, name='Ranking'))
            unigramsDf.columns.name = unigramsDf.index.name
            #unigramsDf.index += 1
            if self._cf['imediatePlot']:
                return make_pretty(unigramsDf.style)
            else:
                axTmp = self._cf['ax'][self._cf['_8x_dims'][self._cf['subChartPosition']][0],
                        self._cf['_8x_dims'][self._cf['subChartPosition']][1]]
                axTmp.title.set_text(t)
                axTmp.xaxis.set_visible(False)  # hide the x axis
                axTmp.yaxis.set_visible(False)  # hide the y axis
                ytable = table(ax=axTmp, data=unigramsDf, loc='center')
                ytable.set_fontsize(self._cf['SubTableFontSize'])
                ytable.scale(self._cf['SubTableXscale'], self._cf['SubTableYscale'])
                return None
        else:
            return pd.DataFrame()
    
    def dataDisplay(self, data: pd.DataFrame(), t: str) -> None:
        if len(data) > 0 and len(self._cf['inOutLst']) > 0:
            st.subheader(self._cf['generalConfig']["Wordcloud_display"])
            wordcloudTab, tableTab = st.tabs([":cloud: Wordcloud",":black_square_button: Table"])
            with wordcloudTab:
                t = re.sub("wholeAll|whole","",t)
                chart = self.getChartObj(df=data, t=self._cf['ADU_or_Speaker']+" "+t)
                fn = self._cf['prefix']+self._cf['ADU_or_Speaker']+"_"+t
                buf = io.BytesIO()
                chart.savefig(buf, format="png", dpi=300)
                left_co, cent_co,last_co = st.columns([1,3,1])
                with cent_co:
                    st.image(buf)
                with left_co:
                    btn = st.download_button(
                        label="Download as PNG",
                        data=buf,
                        file_name=fn,
                        mime="image/png")                        
            with tableTab:
                left, center, right = st.columns(3)
                with center:
                    df = self.getTextObj(data, t=self._cf['ADU_or_Speaker'])
                    st.table(df)
        else:
            st.warning("You have to provide corpora for text analysis.")