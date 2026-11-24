# Simple3D AI

Aplicacao local e gratuita para criar videos 3D simples com personagens estilo bonequinho.

## Recursos

- Interface web em Portugues.
- Prompt, duracao de 5, 10 ou 15 segundos e formato 16:9 ou 9:16.
- Processamento local para cenas conhecidas: caminhar, conversar e futebol.
- Renderizacao real via Blender.
- Exportacao como MP4.
- Nenhuma API paga ou dependencia externa de IA.

O gerador nao simula sucesso. Cenas nao suportadas ou a ausencia do Blender retornam uma mensagem explicita de erro.

## Requisitos

- Python 3.10 ou superior.
- Blender 3.x ou 4.x disponivel no PATH.
- Navegador moderno.

No Windows, instale o Python pela Microsoft Store ou python.org e confirme:

```powershell
python --version
blender --version
```

## Executar localmente

Na raiz do projeto:

```powershell
python app/server.py
```

Acesse `http://127.0.0.1:8000`.

## Estrutura

- `index.html`, `style.css`, `script.js`: interface web.
- `app/server.py`: servidor HTTP local e API.
- `app/processing.py`: validacao e classificacao deterministica das cenas.
- `app/blender_render.py`: integracao de subprocesso com o Blender.
- `blender/render_scene.py`: construcao e animacao da cena no Blender.
- `tests/test_processing.py`: testes focados do processamento.

## Testes

```powershell
python -m unittest discover -s tests -v
```
