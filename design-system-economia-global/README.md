# Atlas — Design System para Economia Global

Sistema visual aplicado ao dashboard Streamlit de indicadores econômicos. Abra [index.html](index.html) no navegador para ver a prévia e os componentes; execute `app.py` para usar o painel com dados e filtros interativos.

## Direção

- **Finex:** precisão visual, contraste e acentos luminosos em dados.
- **Monolith:** superfícies escuras, tipografia de destaque e composição editorial.
- **SaaS Developer:** componentes densos, navegação clara e estados de interface.
- **Atlas:** combinação própria voltada à leitura analítica, sem animações ou dependências das referências.

## Arquivos

- `tokens.css`: cores semânticas, tipografia, espaçamento, raios e foco.
- `components.css`: layout e componentes reutilizáveis.
- `index.html`: prévia do dashboard e catálogo de componentes.

## Regras de uso no dashboard

1. Use a superfície escura para navegação e painéis; reserve o ciano para ação primária, foco e série em destaque.
2. Mostre unidade, ano e comparação junto de cada indicador. Não comunique desempenho econômico apenas pela cor.
3. Mantenha rótulos e valores fora das cores dos gráficos; use legendas e tabelas para leitura precisa.
4. Use `--color-chart-1` a `--color-chart-5` sempre na mesma ordem em gráficos comparáveis.
5. Em telas estreitas, empilhe cartões e permita rolagem horizontal na tabela; não comprima números.
6. Preserve os estados hover, focus, disabled, loading, empty, warning e error previstos neste molde.

## Especificações

| Elemento | Regra |
| --- | --- |
| Canvas / superfície | `#090E16` / `#111C2A` |
| Ação e série em foco | `#67DDD2` |
| Texto principal / secundário | `#F2F7F7` / `#B1C1CB` |
| Fontes | Display: Space Grotesk com fallback de sistema. Corpo: Inter com fallback de sistema. Nenhuma fonte externa é necessária. |
| Espaçamento | Escala de 4, 8, 12, 16, 20, 24, 32, 40 e 48 px. |
| Raios | 8 px nos controles, 14 px nos painéis e 20 px em superfícies maiores. |
| Responsividade | Três colunas de KPI no desktop, duas abaixo de 1050 px e uma abaixo de 510 px. Navegação horizontal no celular. |
| Gráficos | Ciano para o país em foco; azul, âmbar, roxo e verde para comparadores, sempre com legenda e unidade explícitas. |

### Componentes previstos

Navegação lateral, cabeçalho, filtros, botões primário e secundário, cartões KPI, painéis de gráfico, barras de composição, tabela de dados, etiquetas de contexto, notas metodológicas e feedback de sucesso, aviso, erro, vazio e carregamento.

## Integração com Streamlit

`app.py` carrega `tokens.css` junto com `style.css`. O tema em `.streamlit/config.toml` e a versão Stlite em `dist/mount-cdn.js` usam as mesmas cores. `charts.py` e `analytics.py` usam a paleta Atlas nos gráficos. O HTML continua sendo um catálogo visual; os dados e a lógica interativa ficam no app Python. A prévia usa valores reais do Brasil em 2021 presentes na base do projeto, mas não é um painel interativo.

## Acessibilidade

Contraste forte para texto e controles, foco visível, elementos semânticos, tabela de apoio ao gráfico e suporte a `prefers-reduced-motion`. Verifique novamente o contraste se trocar qualquer token de cor.
