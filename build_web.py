"""Atualiza os arquivos da aplicação servidos pelo runtime Stlite empacotado."""
from pathlib import Path
import shutil,json
root=Path(__file__).resolve().parent;dist=root/'dist';dist.mkdir(exist_ok=True)
for name in ['app.py','analytics.py','charts.py','style.css']:
    shutil.copyfile(root/name,dist/name)
(dist/'dados').mkdir(exist_ok=True)
shutil.copyfile(root/'dados/global_economy_indicators.csv',dist/'dados/global_economy_indicators.csv')
print('Arquivos Python e dados atualizados na versão web.')
