# Batalha Naval: Radar IA

Projeto final da disciplina de Introdução a Algoritmos/Programação, do curso de Engenharia de Software da PUC Minas (Coração Eucarístico), desenvolvido com **Python e Pygame**.

Tema da disciplina: **Inteligência Artificial no Cotidiano: Aplicações e Uso Responsável**.
Recorte do grupo: **confiabilidade de sistemas inteligentes**, ou seja, assistentes de IA podem errar mesmo quando parecem confiantes.

## Integrantes do grupo

| Nome | Matrícula |
|------|-----------|
| Arthur Filipe Silva Dornas | 930592 |
| Diego Emanuel Oliveira Marques | 931449 |
| Wyatt Nicolas Sperber Lopes de Carvalho | 931271 |

Engenharia de Software – 1º período – Noturno.

## Descrição do jogo

Uma Batalha Naval contra o computador. A tela mostra dois tabuleiros 10×10: à esquerda a sua frota, à direita a frota inimiga, escondida. Os lados se alternam disparando até que uma das frotas seja afundada.

O diferencial é o **Radar IA**. A cada turno, um assistente de IA simulado sugere uma casa (marcada em amarelo) e mostra um percentual de confiança. A sugestão **nem sempre está certa**, e uma confiança alta não garante acerto. Você pode:

- **seguir a IA** (ESPAÇO): é rápido, mas se ela errar e você não tiver conferido, perde pontos;
- **verificar com o sonar** (V): descobre se a sugestão está certa sem gastar o tiro, mas só tem 3 usos por partida;
- **ignorar a IA** e escolher a casa você mesmo (clique).

No final, o jogo mostra quantas vezes você seguiu a IA e quantas vezes ela errou.

## Objetivo do jogador

Afundar os 5 navios da CPU antes que ela afunde os seus, fazendo a maior pontuação possível.

## Regras do jogo

- Cada lado tem 5 navios: porta-aviões (5 casas), encouraçado (4), cruzador (3), submarino (3) e destróier (2), posicionados automaticamente.
- Os turnos se alternam, com um tiro por vez. Não é possível atirar duas vezes na mesma casa.
- Acerto: **+10 pontos**. Afundar um navio: **+20 de bônus**.
- Seguir a sugestão da IA **sem verificar** e cair na água: **−10 pontos**.
- O sonar tem **3 usos** por partida.
- **Vitória:** afundar toda a frota da CPU. **Derrota:** ter toda a sua frota afundada.
- O recorde de pontos fica salvo em `data/recorde.txt`.

## Controles

| Ação | Comando |
|------|---------|
| Atirar | Clique esquerdo em uma casa do tabuleiro inimigo |
| Seguir a sugestão da IA | `ESPAÇO` |
| Verificar a sugestão com o sonar | `V` |
| Jogar de novo (tela final) | `R` |
| Sair | `ESC` |

**Legenda do tabuleiro inimigo:** quadrado amarelo com `?` = sugestão da IA; borda laranja = sonar confirmou navio; círculo cinza = sonar mostrou água; bolinha branca = tiro na água; vermelho com X = acerto; vermelho escuro = navio afundado.

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/config.py`: constantes (tela, tabuleiro, frota, regras da IA, pontuação, cores, caminhos).
- `src/jogo.py`: loop principal, eventos, atualização do estado e desenho.
- `src/tabuleiro.py`: regras do tabuleiro (posicionar, atirar, afundar, fim de jogo).
- `src/assistente.py`: Radar IA simulado (sugestão, confiança, sonar).
- `src/cpu.py`: jogadas da CPU.
- `src/funcoes.py`: funções auxiliares (pontuação, conversão de clique, precisão).
- `src/dados.py`: leitura e gravação do recorde.
- `src/sprites.py`: função do template para recortar sprites (ainda não usada).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde e ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação, incluindo a proposta (`docs/proposta.MD`).

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

## Recursos externos

- [Pygame](https://www.pygame.org/) (licença LGPL) e [pytest](https://pytest.org/) (licença MIT).
- Fonte padrão do Pygame. Nenhuma imagem, som ou fonte externa foi usada até agora: tudo é desenhado com formas geométricas.

## Divisão do trabalho

| Integrante | Frente | Arquivos |
|------------|--------|----------|
| Arthur Filipe Silva Dornas | Interface e loop do jogo | `main.py`, `src/jogo.py`, `src/config.py` |
| Diego Emanuel Oliveira Marques | Regras do tabuleiro e CPU | `src/tabuleiro.py`, `src/cpu.py`, `tests/test_tabuleiro.py` |
| Wyatt Nicolas Sperber Lopes de Carvalho | Radar IA, pontuação e dados | `src/assistente.py`, `src/funcoes.py`, `src/dados.py`, `tests/test_assistente.py`, `tests/test_logica.py` |

O detalhamento (o que cada um já entregou e as próximas tarefas) está na seção 18 de `docs/proposta.MD`.

## Andamento

- [x] Proposta inicial (`docs/proposta.MD`)
- [x] **PC04 (Semana 2 – protótipo executável):** janela do Pygame, loop principal, controles (mouse, ESPAÇO, V, R, ESC), tabuleiros, tiros, CPU, Radar IA com sonar e penalidade (mecânica temática), vitória/derrota, recorde e 30 testes com `pytest`
- [ ] Posicionamento manual dos navios (Diego)
- [ ] CPU nível médio (Diego) e menu inicial com dificuldade (Arthur)
- [ ] Ranking com nome do jogador (Wyatt) e sons (Arthur)
