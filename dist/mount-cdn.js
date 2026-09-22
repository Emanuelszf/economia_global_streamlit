import { mount } from 'https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js';
const local=(path)=>new URL(path,document.baseURI).href;
const observer=new MutationObserver(()=>{if(document.querySelector('#root [data-testid=\"stAppViewContainer\"] h1')){document.getElementById('loading')?.remove();observer.disconnect();}});
observer.observe(document.getElementById('root'),{childList:true,subtree:true});
setTimeout(()=>{const r=document.getElementById('retry');if(r)r.hidden=false},90000);
const files={};
for(const path of ['app.py','analytics.py','charts.py','style.css','design-system-economia-global/tokens.css','dados/global_economy_indicators.csv'])files[path]={url:local(path)};
mount({entrypoint:'app.py',files,pyodideUrl:'https://cdn.jsdelivr.net/pyodide/v0.27.6/full/pyodide.mjs',requirements:['https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/wheels/streamlit-1.45.1-cp312-none-any.whl','https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/wheels/stlite_lib-0.1.0-py3-none-any.whl',local('runtime/wheels/plotly-5.24.1-py3-none-any.whl')],streamlitConfig:{'theme.base':'dark','theme.primaryColor':'#67DDD2','theme.backgroundColor':'#090E16','theme.secondaryBackgroundColor':'#111C2A','theme.textColor':'#F2F7F7','theme.font':'sans serif','client.toolbarMode':'viewer','browser.gatherUsageStats':false}},document.getElementById('root'));
