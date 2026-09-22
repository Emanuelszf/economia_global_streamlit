"""Análise econômica global: interface Streamlit para o seminário de Economia.
Execute: python -m streamlit run app.py
"""
from pathlib import Path
from html import escape
import numpy as np
import pandas as pd
import streamlit as st
from analytics import (carregar, nome, numero, serie_pais, composicao, amostra_renda,
                       comparadores_proximos, cobertura_ano, SETORES, ROTULOS)
import charts

st.set_page_config(page_title='Análise econômica global',page_icon='◈',layout='wide',initial_sidebar_state='expanded')
RAIZ = Path(__file__).resolve().parent
tokens = RAIZ.joinpath('design-system-economia-global/tokens.css').read_text(encoding='utf-8')
estilos = RAIZ.joinpath('style.css').read_text(encoding='utf-8')
st.markdown(f'<style>{tokens}\n{estilos}</style>',unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def dados_revisados(): return carregar()

try:
    d=dados_revisados()
except (ValueError,FileNotFoundError) as erro:
    st.error(f'Não foi possível carregar a base: {erro}');st.stop()

PAGINAS=['01  Panorama','02  Evolução econômica','03  Estrutura produtiva','04  Composição da demanda','05  Setor externo','06  Renda e estrutura']
ss=st.session_state
if 'pagina' not in ss: ss.pagina=PAGINAS[0]
if 'pais' not in ss: ss.pais='Brazil'
if 'ano' not in ss: ss.ano=2021
if 'periodo_inicio' not in ss: ss.periodo_inicio=2000
if 'comparadores' not in ss: ss.comparadores=['China','India','United States','Germany']
# Preserve os filtros de páginas que ficam temporariamente fora da tela.
for chave in ['periodo_inicio','comparadores','modo_evolucao']:
    if chave in ss: ss[chave] = ss[chave]

def resetar():
    ss.pais='Brazil';ss.ano=2021;ss.periodo_inicio=2000
    ss.comparadores=['China','India','United States','Germany']

def mudar_pagina(indice): ss.pagina=PAGINAS[indice]

def aplicar_sugestao(indicador):
    ss.comparadores=comparadores_proximos(d,ss.pais,int(ss.ano),indicador)

with st.sidebar:
    st.markdown('<div class="sidebar-brand"><span class="brand-mark" aria-hidden="true">◈</span><div><div class="sidebar-title">Análise econômica global</div></div></div><div class="sidebar-section">NAVEGAÇÃO</div>',unsafe_allow_html=True)
    st.radio('Análises',PAGINAS,key='pagina',label_visibility='collapsed')
    st.divider()
    st.markdown('<div class="sidebar-section">SOBRE A BASE</div>',unsafe_allow_html=True)
    st.caption(f'Base histórica: {d.ano.min()}–{d.ano.max()}\n\n{d.pais.nunique()} países/economias · {numero(len(d),0)} registros')

anos=sorted(d.loc[d.pais.eq(ss.pais),'ano'].unique().tolist(),reverse=True)
if ss.ano not in anos:ss.ano=anos[0]
pais=ss.pais;ano=int(ss.ano);idx=PAGINAS.index(ss.pagina)
f=d.loc[d.pais.eq(pais)&d.ano.eq(ano)].iloc[0]
prev=d.loc[d.pais.eq(pais)&d.ano.eq(ano-1)]
prev=prev.iloc[0] if len(prev) else None

TITULOS=['Panorama econômico','A trajetória da economia','Transformação da estrutura produtiva','O PIB pela ótica da demanda','A economia e o comércio exterior','Renda e estrutura econômica']
PERGUNTAS=['Tamanho, renda e inserção internacional em uma visão conjunta.',
           'Como o valor registrado do PIB evoluiu ao longo do tempo?',
           'Como a participação das atividades no valor adicionado mudou?',
           'Como consumo, investimento e comércio exterior se conciliam com o PIB?',
           'Qual é o peso dos fluxos comerciais nas economias selecionadas?',
           'Como a renda por habitante se relaciona com a participação agrícola?']
st.markdown(f'<div class="dashboard-topbar"><span>Análise econômica global <span class="topbar-divider">/</span> <strong>{TITULOS[idx]}</strong></span><span class="topbar-status"><span class="status-dot"></span> BASE HISTÓRICA {d.ano.min()}–{d.ano.max()}</span></div>',unsafe_allow_html=True)
st.markdown(f'<div class="page-eyebrow"><span class="eyebrow-line"></span> INTELIGÊNCIA ECONÔMICA <span class="eyebrow-separator">/</span> ANÁLISE {idx+1:02d}</div>',unsafe_allow_html=True)
st.title(TITULOS[idx])
st.markdown(f'<div class="question">{PERGUNTAS[idx]}</div>',unsafe_allow_html=True)
with st.container(border=True,key='dashboard_filters'):
    filtro_pais,filtro_ano,filtro_reset=st.columns([2.2,1.1,1.3],vertical_alignment='bottom')
    with filtro_pais:
        st.selectbox('País em foco',sorted(d.pais.unique(),key=nome),format_func=nome,key='pais')
    with filtro_ano:
        st.selectbox('Ano de referência',anos,key='ano',help='Apenas anos disponíveis para o país em foco. Nas comparações, todas as economias usam este mesmo ano.')
    with filtro_reset:
        st.button('Restaurar Brasil · 2021',on_click=resetar,use_container_width=True)
st.markdown(f'<div class="context"><span class="context-label">RECORTE ATUAL</span><span class="context-pill">{escape(nome(pais))}</span><span class="context-pill">{ano}</span><small>VISÃO {idx+1:02d} / 06</small></div>',unsafe_allow_html=True)

def leitura(texto): st.markdown('<div class="reading">'+texto+'</div>',unsafe_allow_html=True)
def desenhar(fig,key):
    st.plotly_chart(fig,use_container_width=True,key=key,config={'displaylogo':False,'scrollZoom':False,'toImageButtonOptions':{'format':'png','scale':2},'modeBarButtonsToRemove':['lasso2d','select2d']},theme=None)
def tabela_exportacao(tabela,arquivo):
    with st.expander('Consultar e baixar os dados desta análise'):
        st.dataframe(tabela,use_container_width=True,hide_index=True)
        st.download_button('Baixar CSV',tabela.to_csv(index=False,sep=';',decimal=',').encode('utf-8-sig'),file_name=arquivo,mime='text/csv',key='download_'+arquivo)
def intervalo():
    mi=int(d.ano.min());ma=ano
    if ss.periodo_inicio>ma:ss.periodo_inicio=ma
    if mi==ma:return mi,ma
    st.slider('Início da série',mi,ma,key='periodo_inicio',help='O final do intervalo é o ano de referência selecionado acima.')
    return int(ss.periodo_inicio),ma

def grupo_comparacao():
    st.multiselect('Economias para comparar',sorted(d.pais.unique(),key=nome),key='comparadores',format_func=nome,max_selections=7,help='O país em foco sempre participa. Selecione até sete comparadores.')
    renda=comparadores_proximos(d,pais,ano,'rnb_pc')
    abertura=comparadores_proximos(d,pais,ano,'abertura_pct')
    sugerir_renda,sugerir_abertura=st.columns(2)
    with sugerir_renda:
        st.button('Sugerir por renda',on_click=aplicar_sugestao,args=('rnb_pc',),
                  disabled=not renda,use_container_width=True,
                  help='Seleciona até quatro economias com RNB por habitante mais próxima no ano escolhido.')
    with sugerir_abertura:
        st.button('Sugerir por abertura',on_click=aplicar_sugestao,args=('abertura_pct',),
                  disabled=not abertura,use_container_width=True,
                  help='Seleciona até quatro economias com abertura comercial mais próxima no ano escolhido.')
    st.caption('As sugestões usam um indicador por vez e o mesmo ano. Você pode editar a seleção acima.')
    return list(dict.fromkeys([pais]+ss.comparadores))

def spark(col):
    s=serie_pais(d,pais,max(int(d.ano.min()),ano-9),ano)[col]
    if s.notna().sum()<2:return ''
    lo,hi=s.min(),s.max();amp=hi-lo if hi>lo else 1
    paths=[];p=[]
    for i,v in enumerate(s):
        if pd.isna(v):
            if p:paths.append(' '.join(p));p=[]
        else:p.append(f'{i*76/max(len(s)-1,1):.1f},{23-(v-lo)/amp*21:.1f}')
    if p:paths.append(' '.join(p))
    lines=''.join(f'<polyline points="{x}" fill="none" stroke="#67DDD2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' for x in paths)
    return '<svg class="kpi-spark" viewBox="0 0 78 25" aria-hidden="true">'+lines+'</svg>'

def delta(col,percent=False):
    if prev is None or pd.isna(prev[col]) or pd.isna(f[col]):return 'Sem comparação anual'
    if percent:return f'{numero(f[col]-prev[col]):s} p.p. ante {ano-1}'
    if prev[col]<=0:return 'Sem comparação anual'
    return f'{numero((f[col]/prev[col]-1)*100)}% ante {ano-1}'

if idx==0:
    st.markdown('<div class="dashboard-section-heading"><h2>Comece por uma pergunta</h2><span>EXPLORE OS DADOS</span></div>',unsafe_allow_html=True)
    with st.container(key='guided_questions'):
        perguntas=st.columns(3)
        with perguntas[0]:
            st.markdown('<div class="guided-label">TRAJETÓRIA</div><div class="guided-title">Como o PIB registrado mudou?</div>',unsafe_allow_html=True)
            st.button('Ver evolução →',on_click=mudar_pagina,args=(1,),use_container_width=True)
        with perguntas[1]:
            st.markdown('<div class="guided-label">ESTRUTURA</div><div class="guided-title">Como a produção se transformou?</div>',unsafe_allow_html=True)
            st.button('Ver setores →',on_click=mudar_pagina,args=(2,),use_container_width=True)
        with perguntas[2]:
            st.markdown('<div class="guided-label">COMPARAÇÃO</div><div class="guided-title">Como o comércio se compara?</div>',unsafe_allow_html=True)
            st.button('Ver setor externo →',on_click=mudar_pagina,args=(4,),use_container_width=True)
    st.markdown(f'<div class="dashboard-section-heading"><h2>Indicadores principais</h2><span>{escape(nome(pais))} / {ano}</span></div>',unsafe_allow_html=True)
    cards=[('PIB registrado',numero(f.pib/1e9),'bilhões de u.m. da base','pib',False),
           ('População',numero(f.populacao/1e6),'milhões de habitantes','populacao',False),
           ('RNB por habitante',numero(f.rnb_pc,0),'USD por habitante','rnb_pc',False),
           ('Formação de capital',numero(f.investimento_pct)+'%','do PIB · investimento bruto','investimento_pct',True),
           ('Abertura comercial',numero(f.abertura_pct)+'%','do PIB · exportações + importações','abertura_pct',True),
           ('Saldo de bens e serviços',numero(f.saldo_externo_pct)+'%','do PIB · exportações − importações','saldo_externo_pct',True)]
    html='<div class="kpi-grid">'
    for rot,val,unit,col,pp in cards:
        html+=f'<div class="kpi"><div class="kpi-label">{rot}</div><div class="kpi-value">{val}</div><div class="kpi-unit">{unit}</div><div class="kpi-change">{delta(col,pp)}</div>{spark(col)}</div>'
    st.markdown(html+'</div>',unsafe_allow_html=True)
    leitura('<strong>Como ler os indicadores.</strong> Os valores situam o país no ano escolhido; as variações comparam com o ano imediatamente anterior. As pequenas linhas mostram até dez anos de histórico. Abertura e investimento são razões em relação ao PIB, e não notas de desempenho.')
    st.caption('u.m. = unidade monetária. O CSV não documenta a unidade nem a base de preços do PIB. Variações monetárias não representam crescimento real; as razões pressupõem componentes comparáveis.')
    tabela_exportacao(f[['nome','ano','pib','populacao','rnb_pc','investimento_pct','abertura_pct','saldo_externo_pct']].to_frame().T,'panorama.csv')

elif idx==1:
    inicio,fim=intervalo()
    with st.expander('Comparar com outras economias'):
        grupo=grupo_comparacao()
        comparar=st.checkbox('Mostrar comparadores no gráfico',value=False)
    modo=st.radio('Forma de comparação',['PIB registrado','Índice (início = 100)','Variação anual (%)'],horizontal=True,key='modo_evolucao')
    exibidos=grupo if comparar else [pais]
    fig,sem_base=charts.evolucao(d,exibidos,inicio,fim,modo)
    desenhar(fig,'evolucao')
    if sem_base:st.warning('Sem PIB positivo no ano-base; não exibidos no índice: '+', '.join(sem_base))
    s=serie_pais(d,pais,inicio,fim)
    leitura(f'<strong>{escape(nome(pais))}:</strong> há PIB observado em {s.pib.notna().sum()} dos {len(s)} anos do intervalo. A variação registrada em {ano} é {numero(f.variacao_pib_base_pct)}%. O índice usa o mesmo ano-base para todas as economias; lacunas permanecem sem interpolação.')
    st.caption('O CSV não documenta unidade monetária e base de preços do PIB. Não interprete a série como crescimento real ou como comparação por poder de compra.')
    partes_exportacao=[]
    for economia in exibidos:
        if nome(economia) in sem_base: continue
        t=serie_pais(d,economia,inicio,fim)[['pib','variacao_pib_base_pct']].copy()
        t['valor_exibido']=(100*t.pib/t.pib.iloc[0] if modo=='Índice (início = 100)' else t.variacao_pib_base_pct if modo=='Variação anual (%)' else t.pib/1e9)
        t['medida']=modo;t['país']=nome(economia);partes_exportacao.append(t.reset_index())
    t=pd.concat(partes_exportacao,ignore_index=True) if partes_exportacao else pd.DataFrame(columns=['país','ano','valor_exibido','medida'])
    tabela_exportacao(t,'evolucao.csv')

elif idx==2:
    inicio,fim=intervalo();s=serie_pais(d,pais,inicio,fim);p,ok=composicao(s)
    if ok.any():
        desenhar(charts.estrutura(p),'estrutura')
        completos=p.loc[ok];ini,ult=completos.index[[0,-1]]
        v0=completos.loc[ini,'manufatura_pct'];v1=completos.loc[ult,'manufatura_pct']
        leitura(f'<strong>Manufatura no VAB:</strong> {numero(v0)}% em {ini} e {numero(v1)}% em {ult}, uma diferença de {numero(v1-v0)} pontos percentuais. Participações em valor refletem preços e quantidades; a mudança não comprova queda ou expansão do volume produzido.')
    else:st.info('Não há composição setorial completa e não negativa neste intervalo. Selecione outro período ou país.')
    st.caption(f'{int(ok.sum())} de {len(ok)} anos com composição válida. Outros setores = VAB menos os cinco grupos selecionados; inclui atividades industriais e de serviços. Manufatura não corresponde à indústria total.')
    out=p.rename(columns=dict(zip(p.columns,ROTULOS))).reset_index();out.insert(0,'País',nome(pais))
    tabela_exportacao(out,'estrutura_produtiva.csv')

elif idx==3:
    cols=['consumo_familias_pct','consumo_governo_pct','investimento_pct','exportacoes_pct','importacoes_pct','ajuste_demanda_pct']
    if f[cols].isna().any():st.info('Há componentes ausentes para este país e ano; a conciliação não pode ser exibida.')
    else:
        desenhar(charts.demanda(f),'demanda')
        leitura(f'<strong>O ajuste de conciliação é {numero(f.ajuste_demanda_pct)}% do PIB.</strong> Ele é calculado como PIB − (famílias + governo + formação de capital + exportações − importações). Seu papel é mostrar o resíduo da base, sem ocultá-lo.')
        if abs(f.ajuste_demanda_pct)>1:st.warning('O ajuste ultrapassa 1% do PIB, limite exploratório adotado no MVP. Investigue definições e compatibilidade da fonte antes de interpretar a decomposição.')
    st.caption('Famílias inclui instituições sem fins lucrativos. Governo representa consumo final, não gasto público total. Subtrair importações evita contabilizar produção externa; não demonstra um efeito causal negativo.')
    st.latex(r'PIB = C_{famílias} + C_{governo} + FBC + X - M + Ajuste')
    t=pd.DataFrame({'Componente':['Famílias','Governo','Formação de capital','Exportações','Importações (subtração)','Ajuste'],'% do PIB':[f.consumo_familias_pct,f.consumo_governo_pct,f.investimento_pct,f.exportacoes_pct,-f.importacoes_pct,f.ajuste_demanda_pct]})
    tabela_exportacao(t,'composicao_demanda.csv')

elif idx==4:
    grupo=grupo_comparacao();a=d[d.ano.eq(ano)&d.pais.isin(grupo)].dropna(subset=['exportacoes_pct','importacoes_pct']).copy()
    a=a.sort_values('abertura_pct')
    ausentes=[nome(p) for p in grupo if p not in set(a.pais)]
    if len(a):
        desenhar(charts.exterior(a),'exterior')
        leitura(f'<strong>Abertura comercial de {escape(nome(pais))}: {numero(f.abertura_pct)}% do PIB.</strong> O saldo de bens e serviços é {numero(f.saldo_externo_pct)}% do PIB. As barras estão ordenadas pela soma de exportações e importações em relação ao PIB.')
    else:st.info('Nenhuma economia selecionada tem ambos os fluxos disponíveis neste ano.')
    if ausentes:st.warning('Sem dados completos no ano: '+', '.join(ausentes))
    st.caption('Maior abertura não é automaticamente melhor. Tamanho, estrutura e posição nas cadeias produtivas afetam os fluxos; a soma pode ultrapassar 100% do PIB.')
    tabela_exportacao(a[['nome','ano','exportacoes_pct','importacoes_pct','abertura_pct','saldo_externo_pct']],'setor_externo.csv')

elif idx==5:
    a,excluidos=amostra_renda(d,ano)
    log=st.toggle('Escala logarítmica da renda',value=True,help='Distâncias iguais representam razões iguais, facilitando a leitura de países com rendas muito diferentes.')
    if len(a):
        desenhar(charts.renda(a,pais,log),'renda')
        corr=np.log10(a.rnb_pc).corr(a.agricultura_pct) if len(a)>=3 and a.rnb_pc.nunique()>1 and a.agricultura_pct.nunique()>1 else np.nan
        leitura(f'<strong>{len(a)} economias na comparação.</strong> A correlação entre log₁₀ da RNB por habitante e a participação agrícola é {numero(corr,2)}. É uma associação descritiva, sem ponderação por população; não permite concluir que reduzir a agricultura eleva a renda.')
        if pais not in set(a.pais):st.info('O país em foco não tem renda positiva e participação agrícola válida para aparecer nesta comparação.')
    else:st.info('Não há observações válidas neste ano.')
    st.caption(f'{excluidos} observações do ano excluídas por ausência ou valores inválidos. RNB por habitante = RNB / população, em USD, sem ajuste por paridade do poder de compra. Cada ponto representa uma economia com o mesmo peso visual.')
    tabela_exportacao(a[['nome','ano','rnb_pc','agricultura_pct']],'renda_estrutura.csv')

with st.expander('Cobertura e lacunas dos dados'):
    cobertura,total=cobertura_ano(d,pais,ano)
    st.caption(f'Em {ano}, a base contém registros para {total} economias. As contagens abaixo consideram apenas essas economias.')
    st.dataframe(cobertura,use_container_width=True,hide_index=True)
    st.caption('Disponível indica que os campos necessários à análise estão presentes e atendem às condições indicadas. A cobertura varia entre países e anos.')

with st.expander('Fonte, definições e limites da análise'):
    st.markdown('**Fonte:** Global Economy Indicators.csv, arquivo fornecido ao projeto. O produtor e os metadados originais não foram confirmados. Unidade de observação: **país/economia × ano**. Países e territórios seguem os nomes e a cobertura da fonte.')
    st.markdown('**Comparabilidade:** a coluna de RNB total identifica USD; o CSV não documenta a unidade/base de preços do PIB e dos componentes. As razões entre valores monetários pressupõem unidades e bases compatíveis. Não há ajuste de preços, câmbio ou PPC nesta versão.')
    st.markdown('**Tratamento:** espaços removidos, chaves e tipos validados, denominadores não positivos tratados como indisponíveis. Valores ausentes são preservados; a cobertura varia por ano. Nenhum total mundial é calculado com conjuntos mutáveis de países.')
    st.markdown('**Estrutura:** participação setorial = setor / VAB. Outros setores é o resíduo dos cinco grupos e não pode ser chamado apenas de serviços. **Demanda:** não somamos consumo final novamente aos seus componentes. **Renda:** RNB per capita não equivale a salário médio.')
    st.markdown('**Uso:** comparações descritivas para o seminário. Alterações de fronteiras, metodologias e cobertura histórica podem afetar comparações; associações e identidades contábeis não identificam causalidade.')
    st.download_button('Baixar base original',Path(__file__).parent.joinpath('dados/global_economy_indicators.csv').read_bytes(),file_name='global_economy_indicators.csv',mime='text/csv')

st.divider()
a,b,c=st.columns([1,2,1])
with a:st.button('← Anterior',disabled=idx==0,on_click=mudar_pagina,args=(max(0,idx-1),),use_container_width=True)
with b:st.caption(f'Página {idx+1} de 6 · {nome(pais)} · {ano}')
with c:st.button('Próxima →',disabled=idx==5,on_click=mudar_pagina,args=(min(5,idx+1),),use_container_width=True)
st.markdown('<div class="footer">Análise econômica global · Dados históricos até 2021 · Cálculos próprios para fins acadêmicos</div>',unsafe_allow_html=True)
