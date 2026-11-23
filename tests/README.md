# Testes

Esta pasta contém os testes automatizados do projeto.

## Arquivos

- `test_tabuleiro.py`: regras do tabuleiro em `src/tabuleiro.py` (posicionar, atirar, afundar, fim de jogo).
- `test_assistente.py`: Radar IA em `src/assistente.py` (sugestão, confiança, sonar, histórico).
- `test_logica.py`: funções auxiliares em `src/funcoes.py` (pontuação, conversão de clique, precisão).
- `test_dados.py`: recorde e ranking em `src/dados.py`.

## Como executar

```bash
python -m pytest
```
