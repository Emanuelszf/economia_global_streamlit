# Economia Global — dashboard Streamlit

Painel acadêmico com seis páginas: panorama, evolução econômica, estrutura produtiva, composição da demanda, setor externo e renda versus estrutura. Seleção inicial: Brasil, 2021. Dados fornecidos ao projeto: 1970–2021.

## Rodar no computador

Requer Python 3.10 ou superior e navegador atualizado. Extraia o ZIP inteiro, mantendo a pasta `dados` junto ao arquivo `app.py`.

Abra o terminal na pasta extraída:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```powershell
.venv\Scripts\activate
```

No macOS/Linux:

```bash
source .venv/bin/activate
```

Instale e abra:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Acesse o endereço que aparecer no terminal, normalmente `http://localhost:8501`. O terminal deve permanecer aberto. `Ctrl+C` encerra o painel. Em alguns sistemas use `python3` no lugar de `python`.

Após instalar as dependências, os dados e gráficos são locais. Não é necessário acessar uma API. Os atalhos `iniciar_windows.bat` e `iniciar_mac_linux.sh` iniciam a aplicação quando o Python com as dependências já estiver disponível.

## Navegar

- Escolha a análise no menu lateral ou use Anterior/Próxima ao final da página.
- O país e ano persistem durante a navegação. Ao mudar para um país sem o ano escolhido, o painel seleciona seu último ano disponível.
- Evolução e estrutura permitem escolher o início do intervalo; o ano de referência define o final.
- Em Evolução, abra o controle de comparação e ative os comparadores. O índice exige PIB positivo no mesmo ano-base para todas as séries.
- No Setor externo, até sete comparadores podem ser adicionados ao país em foco.
- Em Renda e estrutura, todas as economias válidas do ano permanecem visíveis. O país em foco aparece destacado.
- Passe o mouse nos gráficos para ler valores. A barra de ferramentas do gráfico oferece zoom e exportação de imagem.
- O expansor de dados permite consultar e baixar o recorte exibido. A base original pode ser baixada no expansor metodológico.

## Estrutura do código

- `app.py`: interface, navegação, filtros, textos e exportações.
- `analytics.py`: leitura, validação e cálculo dos indicadores.
- `charts.py`: figuras Plotly.
- `style.css` e `.streamlit/config.toml`: estilo e tema claro.
- `dados/global_economy_indicators.csv`: base original, sem alterações.

O notebook anterior continua útil como material de estudo. O dashboard usa as mesmas definições e preserva valores ausentes.

## Interpretação econômica

A unidade e base de preços do PIB não estão documentadas no CSV. Por isso exibimos **PIB registrado**, em **u.m. da base**; suas variações não medem crescimento real. Razões entre componentes monetários pressupõem que suas unidades e bases sejam compatíveis.

- RNB por habitante = RNB em USD / população; não equivale a salário nem está ajustada por PPC.
- Formação de capital / PIB: investimento bruto.
- Abertura = (exportações + importações) / PIB.
- Saldo = (exportações − importações) / PIB.
- Composição setorial usa VAB como denominador. Outros setores é o resíduo, não apenas serviços.
- Demanda inclui um ajuste calculado para conciliar os componentes com o PIB; ausência de componente impede a decomposição.
- A amostra internacional é descritiva. A correlação usa log10 da renda e não tem interpretação causal.
- Não calculamos totais mundiais com cobertura territorial variável.

## Versão acessível por link

A edição web usa **Stlite**, que executa o código Streamlit em Python dentro do navegador por meio de Pyodide. Ela usa os mesmos arquivos `app.py`, `analytics.py` e `charts.py` e a mesma base. A primeira abertura transfere o ambiente Python; as interações seguintes reutilizam a sessão. Recarregar a página reinicia as seleções.

A aplicação local usa o servidor Streamlit convencional e tende a iniciar mais rapidamente depois da instalação. A edição web carrega o Stlite e o Pyodide pelas distribuições oficiais no primeiro acesso; o código Python, a base e o wheel do Plotly permanecem no pacote do painel.

Referências: [Streamlit](https://docs.streamlit.io/), [Plotly](https://plotly.com/python/), [Stlite](https://github.com/whitphx/stlite).
