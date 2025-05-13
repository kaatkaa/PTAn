import streamlit as st
import sys
from typing import Tuple, List, Dict, Any

sys.path.insert(0,"..")
from config.config_data_colector import DataProvider
from graphic_components.superComponent import SuperTextComponent

class Cases2(SuperTextComponent):

    def getTextObj(self, data: Any, t: str) -> Any:
        if self._cf['unitSpeakerSel'] == None:
            unit = "Text"
        else:
            unit = self._cf['unitSpeakerSel']
        backgroundColor = self._cf['palette']
        textColor = self._cf['text_color']
        def color(row):
            return ['background-color: '+backgroundColor[row[self._cf['categoriesColumn']]]+";"
                'color: '+textColor[row[self._cf['categoriesColumn']]]+";"
                ] * len(row)
        def make_pretty(styler):
            styler.set_caption(unit)
            styler.set_table_styles(DataProvider.getTableFormat())
            styler.apply(color, axis=1)
            return styler
        lst = [self._cf['categoriesColumn']] + [self._cf['textColumnToShow']] + ['mid','Links']
        data = data[lst].sort_values(by=self._cf['categoriesColumn'])
        data.reset_index(drop=True,inplace=True)
        data.index += 1
        return make_pretty(data.style)

    def dataDisplay(self, df: Any, title: str):
        if len(df) > 0:
            stylesed = self.getTextObj(df,title)
            #st.dataframe(stylesed, height=800, column_config={self._cf['categoriesColumn']: None})
            st.table(stylesed)