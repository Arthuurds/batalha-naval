# Batalha Naval

Projeto final da disciplina de Introdução a Algoritmos/Programação, do curso de Engenharia de Software da PUC Minas (Coração Eucarístico), desenvolvido com **Python e Pygame**.

O jogo é uma versão da clássica Batalha Naval em que o jogador enfrenta o computador (CPU).

## Integrantes do grupo

| Nome | Matrícula |
|------|-----------|
| Arthur Filipe Silva Dornas | 930592 |
| Diego Emanuel Oliveira Marques | 931449 |
| Wyatt Nicolas Sperber Lopes de Carvalho | 931271 |

Engenharia de Software – 1º período – Noturno.

## Descrição do jogo

A tela mostra dois tabuleiros 10×10: à esquerda, o tabuleiro com a frota do jogador; à direita, o tabuleiro da CPU, cujos navios ficam escondidos. Antes da partida, o jogador posiciona seus navios (ou usa o posicionamento automático) e a CPU posiciona os dela aleatoriamente.

Depois, os dois lados se alternam disparando em casas do tabuleiro adversário. A cada tiro o jogo indica se foi **água**, **acerto** ou se o navio foi **afundado**. A CPU tem dois níveis: no fácil ela atira ao acaso; no médio, depois de acertar um navio ela passa a atirar nas casas vizinhas até afundá-lo.

## Objetivo do jogador

Afundar todos os navios da CPU antes que ela afunde todos os seus, usando o menor número de tiros possível para entrar no ranking.

## Regras do jogo

- Cada lado tem 5 navios: porta-aviões (5 casas), encouraçado (4), cruzador (3), submarino (3) e destróier (2).
- Os navios ficam na horizontal ou na vertical, não podem sair do tabuleiro nem se sobrepor.
- O jogador começa atirando e depois os turnos se alternam.
- Não é possível atirar duas vezes na mesma casa; o clique é ignorado e o turno continua.
- Um navio afunda quando todas as suas casas são atingidas.
- **Vitória:** afundar toda a frota da CPU. **Derrota:** ter toda a sua frota afundada.
- Ao final são exibidos tiros, acertos e precisão; os melhores resultados vão para o ranking.

## Controles

| Ação | Comando |
|------|---------|
| Posicionar navio | Clique esquerdo no seu tabuleiro |
| Girar navio (horizontal/vertical) | Tecla `R` ou clique direito |
| Posicionamento automático | Tecla `A` |
| Iniciar partida | `Enter` |
| Atirar | Clique esquerdo em uma casa do tabuleiro da CPU |
| Voltar ao menu / sair | `ESC` |

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde e ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo a proposta inicial (`docs/proposta.MD`).

## Como executar o projeto

É necessário ter o **Python 3** instalado.

```bash
git clone https://github.com/Arthuurds/batalha-naval.git
cd batalha-naval
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Andamento

- [x] Repositório criado a partir do template da disciplina
- [x] Proposta inicial (`docs/proposta.MD`)
- [ ] Tabuleiros e posicionamento da frota
- [ ] Turnos, tiros e detecção de navio afundado
- [ ] CPU nível fácil
- [ ] Telas de vitória/derrota e estatísticas
- [ ] Ranking salvo em `data/ranking.txt`
- [ ] CPU nível médio
- [ ] Testes das regras do jogo
