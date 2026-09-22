"""Preparação reproduzível: uma observação por país/economia e ano."""
from pathlib import Path
import numpy as np
import pandas as pd

MAPA = {
    'Country': 'pais', 'Year': 'ano', 'Population': 'populacao',
    'Per capita GNI': 'rnb_pc_informada',
    'Agriculture, hunting, forestry, fishing (ISIC A-B)': 'agricultura',
    'Construction (ISIC F)': 'construcao',
    'Exports of goods and services': 'exportacoes',
    'Final consumption expenditure': 'consumo_final',
    'General government final consumption expenditure': 'consumo_governo',
    'Gross capital formation': 'formacao_capital',
    'Household consumption expenditure (including Non-profit institutions serving households)': 'consumo_familias',
    'Imports of goods and services': 'importacoes', 'Manufacturing (ISIC D)': 'manufatura',
    'Total Value Added': 'vab', 'Transport, storage and communication (ISIC I)': 'transportes',
    'Wholesale, retail trade, restaurants and hotels (ISIC G-H)': 'comercio',
    'Gross National Income(GNI) in USD': 'rnb', 'Gross Domestic Product (GDP)': 'pib',
}
SETORES = ['agricultura', 'manufatura', 'construcao', 'comercio', 'transportes', 'outros_setores']
ROTULOS = ['Agro, silvicultura e pesca', 'Manufatura', 'Construção', 'Comércio e hospedagem', 'Transportes e comunicação', 'Outros setores']
CORES = ['#67DDD2', '#8DB9FF', '#F4B86A', '#BC9CEB', '#8FC79C', '#426073']
NOMES = {'Brazil':'Brasil','Germany':'Alemanha','United States':'Estados Unidos','India':'Índia','China':'China','France':'França','Italy':'Itália','Spain':'Espanha','Japan':'Japão','South Africa':'África do Sul','Argentina':'Argentina','Portugal':'Portugal','Canada':'Canadá','Mexico':'México','United Kingdom':'Reino Unido','Russian Federation':'Rússia','Republic of Korea':'Coreia do Sul','Australia':'Austrália','Switzerland':'Suíça'}

def nome(pais): return NOMES.get(pais, pais)
def numero(valor, casas=1):
    if pd.isna(valor) or not np.isfinite(valor): return '—'
    return f'{valor:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')
def razao(a,b): return a.div(b.where(b > 0))

def carregar(caminho=None):
    caminho = Path(caminho) if caminho else Path(__file__).parent / 'dados/global_economy_indicators.csv'
    bruta = pd.read_csv(caminho, encoding='utf-8-sig')
    bruta.columns = bruta.columns.str.strip()
    faltam = set(MAPA) - set(bruta.columns)
    if faltam: raise ValueError(f'Colunas ausentes: {sorted(faltam)}')
    d = bruta[list(MAPA)].rename(columns=MAPA).copy()
    d['pais'] = d.pais.astype('string').str.strip()
    for c in d.columns.drop('pais'):
        novo = pd.to_numeric(d[c], errors='coerce')
        if (d[c].notna() & novo.isna()).any() or np.isinf(novo).any():
            raise ValueError(f'Valores inválidos na coluna {c}.')
        d[c] = novo
    if d[['pais','ano']].isna().any().any() or d.pais.eq('').any() or d.ano.mod(1).ne(0).any():
        raise ValueError('Chave país-ano inválida.')
    if d.duplicated(['pais','ano']).any(): raise ValueError('Chave país-ano duplicada.')
    d['ano'] = d.ano.astype(int)
    d = d.sort_values(['pais','ano']).reset_index(drop=True)
    d['rnb_pc'] = razao(d.rnb,d.populacao)
    d['pib_pc'] = razao(d.pib,d.populacao)
    d['saldo_externo'] = d.exportacoes-d.importacoes
    for k,v in {'investimento':d.formacao_capital,'consumo_final':d.consumo_final,
                'consumo_familias':d.consumo_familias,'consumo_governo':d.consumo_governo,
                'exportacoes':d.exportacoes,'importacoes':d.importacoes,
                'abertura':d.exportacoes+d.importacoes,'saldo_externo':d.saldo_externo}.items():
        d[k+'_pct'] = 100*razao(v,d.pib)
    d['outros_setores'] = d.vab-d[SETORES[:-1]].sum(axis=1,min_count=5)
    for s in SETORES: d[s+'_pct'] = 100*razao(d[s],d.vab)
    d['ajuste_demanda'] = d.pib-(d.consumo_familias+d.consumo_governo+d.formacao_capital+d.exportacoes-d.importacoes)
    d['ajuste_demanda_pct'] = 100*razao(d.ajuste_demanda,d.pib)
    ant = d.groupby('pais').pib.shift()
    consecutivo = d.ano.sub(d.groupby('pais').ano.shift()).eq(1)
    d['variacao_pib_base_pct'] = (100*(razao(d.pib,ant)-1)).where(consecutivo)
    d['nome'] = d.pais.map(nome)
    return d

def serie_pais(d,pais,inicio,fim):
    """Reindexar preserva lacunas temporais em todos os gráficos."""
    return d[d.pais.eq(pais)].set_index('ano').reindex(range(inicio,fim+1))

def composicao(serie):
    p = serie[[s+'_pct' for s in SETORES]].copy()
    ok = p.notna().all(axis=1) & p.ge(0).all(axis=1)
    return p.where(ok, np.nan),ok

def amostra_renda(d,ano):
    a=d[d.ano.eq(ano)].copy()
    ok=a.rnb_pc.gt(0)&a.agricultura_pct.between(0,100)&a[['rnb_pc','agricultura_pct']].notna().all(axis=1)
    return a.loc[ok].copy(),int((~ok).sum())

def comparadores_proximos(d,pais,ano,indicador,limite=4):
    """Ordena economias pelo indicador escolhido no mesmo ano."""
    if indicador not in ('rnb_pc','abertura_pct'):
        raise ValueError('Indicador de comparação inválido.')
    a=d.loc[d.ano.eq(ano),['pais',indicador]].dropna().copy()
    a=a.loc[a[indicador].gt(0) if indicador=='rnb_pc' else a[indicador].ge(0)]
    foco=a.loc[a.pais.eq(pais),indicador]
    if foco.empty:return []
    valor=float(foco.iloc[0])
    outros=a.loc[a.pais.ne(pais)].copy()
    if indicador=='rnb_pc':
        outros['distancia']=np.abs(np.log(outros[indicador]/valor))
    else:
        outros['distancia']=(outros[indicador]-valor).abs()
    return outros.sort_values(['distancia','pais']).pais.head(limite).tolist()

def cobertura_ano(d,pais,ano):
    """Cobertura dos indicadores usados nas seis análises."""
    a=d.loc[d.ano.eq(ano)]
    setores=[s+'_pct' for s in SETORES]
    demanda=['consumo_familias_pct','consumo_governo_pct','investimento_pct',
             'exportacoes_pct','importacoes_pct','ajuste_demanda_pct']
    disponiveis={
        'PIB registrado':a.pib.notna(),
        'RNB por habitante positiva':a.rnb_pc.gt(0),
        'Estrutura produtiva completa':a[setores].notna().all(axis=1)&a[setores].ge(0).all(axis=1),
        'Demanda completa':a[demanda].notna().all(axis=1),
        'Exportações e importações':a[['exportacoes_pct','importacoes_pct']].notna().all(axis=1),
    }
    foco=a.pais.eq(pais)
    tabela=pd.DataFrame([
        {'Indicador':rotulo,'Economias com dados':int(ok.sum()),
         'País em foco':'Disponível' if bool(ok.loc[foco].iloc[0]) else 'Indisponível'}
        for rotulo,ok in disponiveis.items()
    ])
    return tabela,len(a)
