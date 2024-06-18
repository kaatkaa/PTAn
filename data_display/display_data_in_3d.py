import plotly.graph_objects as go
from typing import Dict
import streamlit as st
from config.config_data_colector import DataProvider


#from data_display.barchart3d import barchart3d
class ThreeD_Charts:
    @staticmethod
    def CorporaVsDynRephrasePlot(matrix: Dict[str, Dict[str, int]],threshold: list=[int],title: str="Test title", h_title: str="Heat map title",
        width=900, height=900, thikness=0.8, colorscale='Viridis',mixed: bool=False,
        **kwargs) -> None:

        """
        Draws a 3D barchart
        :param labels: Array_like of bar labels
        :param z_data: Array_like of bar heights (data coords)
        :param title: Chart title
        :param z_title: Z-axis title
        :param n_row: Number of x-rows
        :param width: Chart width (px)
        :param height: Chart height (px)
        :param thikness: Bar thikness (0; 1)
        :param colorscale: Barchart colorscale
        :param **kwargs: Passed to Mesh3d()
        :return: 3D barchart figure
        """
        def edgesUpdate(color):
            fig.add_scatter3d(mode='lines',
                x=[x_min, x_min, x_max, x_max, x_min],
                y=[y_min, y_max, y_max, y_min, y_min],
                z=[0, 0, 0, 0, 0],
                showlegend=False,
                line=dict(color='red')
            )

            fig.add_scatter3d(mode='lines',
                x=[x_min, x_min, x_max, x_max, x_min],
                y=[y_min, y_max, y_max, y_min, y_min],
                z=[z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency']],
                showlegend=False,
                line=dict(color=color)
            )

            fig.add_scatter3d(mode='lines',
                x=[x_min, x_min],
                y=[y_max, y_max],
                z=[0, z_dic[1]['Frequency']],
                showlegend=False,
                line=dict(color=color)
            )
            fig.add_scatter3d(mode='lines',
                x=[x_min, x_min],
                y=[y_min, y_min],
                z=[0, z_dic[1]['Frequency']],
                showlegend=False,
                line=dict(color=color)
            )

            fig.add_scatter3d(mode='lines',
                x=[x_max, x_max],
                y=[y_min, y_min],
                z=[0, z_dic[1]['Frequency']],
                showlegend=False,
                line=dict(color=color)
            )
            fig.add_scatter3d(mode='lines',
                x=[x_max, x_max],
                y=[y_max, y_max],
                z=[0, z_dic[1]['Frequency']],
                showlegend=False,
                line=dict(color=color)
            )

        thikness *= 0.5
        ann = []

        colorDic = DataProvider.get3D_ColorMatrix()
        
        fig = go.Figure(
            layout=dict(
                barmode = 'overlay',
                bargap=0,
                bargroupgap=0,
                boxgap = 0,
                boxmode = 'overlay',
                barnorm = 'percent',
                funnelmode = 'overlay'
            )
        )

        ctrX = 0
        ctr = 1
        for y_dic in matrix.items():
            ctrY = 0
            for z_dic in y_dic[1].items():
                x_min, y_min = ctrX - thikness, ctrY - thikness
                x_max, y_max = ctrX + thikness, ctrY + thikness

                #if z_dic[0].find("_Eth") != -1 or mixed:
                fig.add_trace(
                    go.Mesh3d(
                    x=[x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max],
                    y=[y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min],
                    z=[0, 0, 0, 0, z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency']],
                    alphahull=0,
                    flatshading=True,
                    color=colorDic[str(y_dic[0])][str(z_dic[0]).replace("_Eth","").replace("_Sent","")],
                    #intensitymode='vertex',
                    #flatshading=True,
                    #intensity=[0, 0, 0, 0, z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency'], z_dic[1]['Frequency']],
                    #text="x_min"+str(x_min),
                    #coloraxis='coloraxis',
                    hoverinfo='text',
                    **kwargs)
                )             
                
                if z_dic[1]['Frequency'] > matrix['Total'][z_dic[0]]['Frequency']:
                    edgesUpdate('white')
                elif z_dic[1]['Frequency'] < matrix['Total'][z_dic[0]]['Frequency']:
                    edgesUpdate('black')

                ann.append(dict(
                    showarrow=False,
                    x=ctrX, y=ctrY, z=z_dic[1]['Frequency'],
                    text=f'<b>#{ctr}</b>',
                    #text=f'<b>'+labels[iz]+'</b>',
                    font=dict(color='white', size=11),
                    bgcolor='rgba(0, 0, 0, 0.3)',
                    xanchor='center', yanchor='middle',
                    hovertext= str(y_dic[0])+"."+str(z_dic[0])+"="+str(z_dic[1]['Frequency'])))
    
                # mesh3d doesn't currently support showLegend param, so
                # add invisible scatter3d with names to show legend
                #for i, label in enumerate(labels):
                fig.add_trace(go.Scatter3d(
                    x=[None], y=[None], z=[None],
                    opacity=0,
                    name=f'#{ctr} {y_dic[0]}.{z_dic[0]}'))
                ctr += 1
                ctrY +=1
            ctrX += 1

        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            opacity=0,
            name=f'\n')
        )
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            opacity=0,
            name=f'White edges - higher than "Total"')
        )
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            opacity=0,
            name=f'\n')
        )
        fig.add_trace(go.Scatter3d(
            x=[None], y=[None], z=[None],
            opacity=0,
            name=f'Black edges - lower than "Total"')
        )
        #eyeX = st.slider(label="eyeX",value=2.0,min_value=-2.0, max_value=2.0,step=0.01)
        #exeY = st.slider(label="eyeY",value=2.0,min_value=-2.0, max_value=2.0,step=0.01)
        #eyeZ = st.slider(label="eyeZ",value=0.1,min_value=-2.0, max_value=2.0,step=0.01)
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.74, y=-1.01, z=1.20)
        )
        fig.update_layout(
            width=width, height=height,
            title=title, title_x=0.5,
            bargap=0,bargroupgap=0,
            scene_camera=camera,
            scene=dict(
                aspectmode="cube",
                aspectratio=dict(x=1),
                xaxis=dict(showticklabels=True,
                           ticktext = list(matrix.keys()),
                           tickvals = [ ctr for ctr in range(len(matrix))],
                           title='X axis'),
                yaxis=dict(showticklabels=True, 
                           ticktext = list(matrix['Total'].keys()),
                           tickvals = [ ctr for ctr in range(len(matrix['Total']))],
                           title='Y axis'),
                zaxis=dict(title='Z axis'),
                annotations=ann),
            coloraxis=dict(
                colorscale=colorscale,
                colorbar=dict(
                    title=dict(
                        text=h_title,
                        side='right'),
                    xanchor='right', x=1.0,
                    xpad=0,
                    ticks='inside')),
            legend=dict(
                yanchor='top', y=1.0,
                xanchor='left', x=0.0,
                bgcolor='rgba(0, 0, 0, 0)',
                itemclick=False,
                itemdoubleclick=False),
            showlegend=True)
        fig.update_layout(bargap=0.25,bargroupgap=0.0)
        st.plotly_chart(fig, config=DataProvider.getSaveConfig())
        #st.write(fig.to_dict()['layout']['scene']['camera'])

    def __init__(self) -> None:
        pass