"""Gráficos Plotly; todos recebem dados já revisados e recortados."""
import numpy as np
import plotly.graph_objects as go
from analytics import nome, numero, SETORES, ROTULOS, CORES, serie_pais
AZUL='#67DDD2'; CINZA='#F2F7F7'; OCRE='#F4B86A'; TEAL='#8DB9FF'
PALETA=[AZUL,TEAL,OCRE,'#BC9CEB','#8FC79C','#C3D3E7']

def base(fig,altura=425):
    fig.update_layout(template='plotly_dark',height=altura,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=15,r=30,t=25,b=35),font=dict(family='Inter, Segoe UI, sans-serif',size=14,color=CINZA),
        separators=',.',hoverlabel=dict(bgcolor='#172536',bordercolor='#426073',font=dict(color='#F2F7F7',size=14)),
        legend=dict(orientation='h',yanchor='bottom',y=1.03,x=0,font_size=12),
        hovermode='closest')
    fig.update_xaxes(showgrid=False,zeroline=False,linecolor='#426073',automargin=True)
    fig.update_yaxes(gridcolor='#294052',zeroline=False,automargin=True)
    return fig

def evolucao(d,paises,inicio,fim,modo):
    fig=go.Figure();faltantes=[]
    for i,p in enumerate(paises):
        s=serie_pais(d,p,inicio,fim);v=s.pib.copy()
        if modo=='Índice (início = 100)':
            if not np.isfinite(v.iloc[0]) or v.iloc[0]<=0:
                faltantes.append(nome(p));continue
            v=100*v/v.iloc[0]
        elif modo=='Variação anual (%)': v=s.variacao_pib_base_pct
        else:v=v/1e9
        fig.add_trace(go.Scatter(x=s.index.tolist(),y=v.tolist(),mode='lines+markers',name=nome(p),
            line=dict(color=PALETA[i%len(PALETA)],width=3 if i==0 else 2),
            marker_size=5,connectgaps=False,hovertemplate='%{x}<br>%{y:,.1f}<extra>%{fullData.name}</extra>'))
    base(fig);fig.update_layout(hovermode='x unified')
    fig.update_yaxes(title_text={'PIB registrado':'Bilhões de u.m. da base','Índice (início = 100)':f'Índice · {inicio} = 100','Variação anual (%)':'Variação do valor registrado (%)'}[modo])
    fig.update_xaxes(dtick=max(1,round((fim-inicio)/7)),tickformat='d')
    if modo!='Variação anual (%)':fig.update_yaxes(rangemode='tozero')
    else:fig.add_hline(y=0,line_color='#91A8B6',line_width=1)
    return fig,faltantes

def estrutura(partes):
    # Somar explicitamente os limites evita que Plotly trate anos ausentes como zero.
    fig=go.Figure();limite=partes.cumsum(axis=1)
    for i,c in enumerate(partes.columns):
        fig.add_trace(go.Scatter(x=partes.index.tolist(),y=limite[c].tolist(),name=ROTULOS[i],
            fill='tozeroy' if i==0 else 'tonexty',fillcolor=CORES[i],
            line=dict(width=.5,color=CORES[i]),connectgaps=False,
            customdata=partes[c].tolist(),hovertemplate='%{x}<br>%{customdata:.1f}% do VAB<extra>%{fullData.name}</extra>'))
    base(fig,455);fig.update_yaxes(range=[0,100],ticksuffix='%',title_text='Participação no valor adicionado')
    fig.update_layout(legend=dict(y=-.28,yanchor='top',font_size=12),margin=dict(b=95))
    return fig

def demanda(f):
    valores=[f.consumo_familias_pct,f.consumo_governo_pct,f.investimento_pct,f.exportacoes_pct,-f.importacoes_pct,f.ajuste_demanda_pct,0]
    fig=go.Figure(go.Waterfall(x=['Famílias','Governo','Formação de<br>capital','Exportações','Importações','Ajuste','PIB'],
        y=valores,measure=['relative']*6+['total'],
        text=[numero(v)+'%' for v in valores[:-1]]+['100,0%'],textposition='outside',
        increasing=dict(marker_color=AZUL),decreasing=dict(marker_color=OCRE),totals=dict(marker_color=CINZA),
        connector=dict(line=dict(color='#426073',width=1)),
        hovertemplate='%{x}<br>%{text}<extra></extra>'))
    base(fig,440);fig.update_yaxes(title_text='Componentes (% do PIB)');fig.update_layout(showlegend=False)
    return fig

def exterior(a):
    fig=go.Figure()
    for k,rot,c in [('exportacoes_pct','Exportações',AZUL),('importacoes_pct','Importações',OCRE)]:
        fig.add_trace(go.Bar(x=a[k].tolist(),y=a.nome.tolist(),name=rot,orientation='h',marker_color=c,
            text=[numero(v)+'%' for v in a[k]],textposition='outside',cliponaxis=False,
            hovertemplate='%{y}<br>%{x:.1f}% do PIB<extra>%{fullData.name}</extra>'))
    base(fig,max(380,len(a)*68));fig.update_layout(barmode='group',bargap=.32)
    fig.update_xaxes(title_text='Fluxo de bens e serviços (% do PIB)',showgrid=True,gridcolor='#294052',rangemode='tozero')
    fig.update_yaxes(showgrid=False)
    if len(a):fig.update_xaxes(range=[0,max(a.exportacoes_pct.max(),a.importacoes_pct.max())*1.22])
    return fig

def renda(a,pais,log=True):
    fig=go.Figure()
    outros=a[~a.pais.eq(pais)];foco=a[a.pais.eq(pais)]
    for x,rot,cor,tam in [(outros,'Demais economias','#91A8B6',9),(foco,nome(pais),AZUL,15)]:
        if x.empty:continue
        fig.add_trace(go.Scatter(x=x.rnb_pc.tolist(),y=x.agricultura_pct.tolist(),mode='markers',name=rot,
            marker=dict(color=cor,size=tam,opacity=.78,line=dict(color='white',width=.8)),text=x.nome.tolist(),
            hovertemplate='<b>%{text}</b><br>RNB por habitante: USD %{x:,.0f}<br>Agro: %{y:.1f}% do VAB<extra></extra>'))
    base(fig,465);fig.update_xaxes(type='log' if log else 'linear',title_text='RNB por habitante (USD)'+(' · escala logarítmica' if log else ''),tickformat=',.0f')
    fig.update_yaxes(title_text='Agro, silvicultura e pesca (% do VAB)',rangemode='tozero')
    return fig
