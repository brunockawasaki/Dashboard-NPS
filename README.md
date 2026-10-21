# Dashboard NPS – Pesquisa de Satisfação (Processos)

Painel em HTML com os indicadores da pesquisa de satisfação da área de Processos e Melhoria Contínua do Grupo Gadens.

**Abra `index.html` no navegador.** Ele abre com **dados de exemplo (fictícios)**, só para mostrar como o painel funciona.

## O que o painel mostra
- NPS (promotores, neutros, detratores) e distribuição das notas de 0 a 10
- Concordância com as frases (respostas 4 e 5) e média por frase
- NPS por frequência de uso dos documentos
- Comentários dos detratores
- Tempo no Grupo, frequência de uso, identificação e setor (só de quem se identificou)
- Setores mais indicados para mapear nas próximas fases
- Botão **Acessibilidade**: aparência Clara, Escura ou para Daltonismo

## Como ver as respostas reais
1. Baixe a planilha de respostas do Forms (Exibir respostas → Abrir no Excel) e salve numa pasta.
2. Rode o script, passando a pasta (ou defina a variável `PASTA_NPS`):

```
python gerar_dashboard_nps.py "caminho\da\pasta"
```

O script lê a planilha **mais recente** da pasta (`.xlsx` ou `.csv`) e grava `Dashboard NPS.html` na mesma pasta, já com os dados dentro. Precisa de Python 3 e da biblioteca `openpyxl`.

`Atualizar Dashboard NPS.bat` roda o script com dois cliques.

## Cuidado com os dados
**Não suba para o GitHub o `Dashboard NPS.html` gerado nem as planilhas de respostas.** Eles contêm respostas reais. O `.gitignore` já evita isso.
