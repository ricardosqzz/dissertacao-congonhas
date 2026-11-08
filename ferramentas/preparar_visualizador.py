"""Prepara as prévias para o site e para a leitura sem conexão."""
from pathlib import Path
import json,zipfile,shutil
root=Path(__file__).resolve().parents[1];source=root/'visualizador';target=root/'_visualizador'
target.mkdir(exist_ok=True)
parts=sorted((source/'partes').glob('imagens-*.zip'))
assert parts, 'Volumes de imagens não encontrados'
for part in parts:
    with zipfile.ZipFile(part) as z:
        for item in z.infolist():
            destination=(target/item.filename).resolve()
            assert destination.is_relative_to(target.resolve()) and item.filename.startswith('imagens/') and item.filename.endswith('.webp'),item.filename
            assert item.file_size<4_000_000,item.filename
        z.extractall(target)
for name in ['index.html','dados.js','README.md']:shutil.copy2(source/name,target/name)
data=json.loads((source/'catalogo.json').read_text(encoding='utf8'))
assert len([x for x in data['catalog'] if x['mode']=='direcional'])==144
for item in data['catalog']:assert (target/item['src']).is_file(),item['src']
print('Visualizador preparado:',len(data['catalog']),'figuras')
