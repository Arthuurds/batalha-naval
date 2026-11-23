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

O diferencial é o **Radar IA**. A cada turno, um assistente de IA simulado sugere uma casa (marcada em amarelo) e mostra um percentual de confiança. A sugestão **nem sempre está certa**. A IA é *superconfiante*: confiança maior indica uma chance um pouco maior de acerto, mas a chance real é sempre menor do que o percentual exibido. Você pode:

- **seguir a IA** (ESPAÇO): é rápido, mas se ela errar e você não tiver conferido, perde pontos;
- **verificar com o sonar** (V): descobre se a sugestão está certa sem gastar o tiro, mas só tem 3 usos (afundar um navio devolve 1);
- **ignorar a IA** e escolher a casa você mesmo (clique).

Durante a partida, o painel mostra o **histórico da IA**, ou seja, quantas das sugestões reveladas (por tiro ou sonar) estavam certas. Assim você avalia o sistema pelos resultados, e não pela confiança que ele anuncia. No final aparecem o resumo do uso da IA e o **ranking** com os 5 melhores resultados.

## Objetivo do jogador

Afundar os 5 navios da CPU antes que ela afunde os seus, fazendo a maior pontuação possível.

## Regras do jogo

- Cada lado tem 5 navios: porta-aviões (5 casas), encouraçado (4), cruzador (3), submarino (3) e destróier (2), posicionados automaticamente.
- Os turnos se alternam, com um tiro por vez. Não é possível atirar duas vezes na mesma casa.
- Acerto: **+10 pontos**. Afundar um navio: **+20 de bônus**.
- Seguir a sugestão da IA **sem verificar** e cair na água: **−10 pontos**.
- O sonar tem **3 usos**; afundar um navio devolve 1 uso (máximo de 3).
- **Vitória:** afundar toda a frota da CPU. **Derrota:** ter toda a sua frota afundada.
- O recorde de pontos fica salvo em `data/recorde.txt` ao fim de qualquer partida (vitória ou derrota).
- Se a pontuação entrar no top 5, você digita seu nome e o resultado vai para `data/ranking.txt` (desempate pela precisão).

## Controles

| Ação | Comando |
|------|---------|
| Atirar | Clique esquerdo em uma casa do tabuleiro inimigo |
| Seguir a sugestão da IA | `ESPAÇO` |
| Verificar a sugestão com o sonar | `V` |
| Digitar nome no ranking (tela final) | Teclado + `ENTER` |
| Jogar de novo (tela final) | `R` |
| Sair | `ESC` |

**Legenda do tabuleiro inimigo:** quadrado amarelo com `?` = sugestão da IA; borda laranja = sonar confirmou navio; círculo cinza = sonar mostrou água; bolinha branca = tiro na água; vermelho com X = acerto; vermelho escuro = navio afundado.

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/config.py`: constantes (tela, tabuleiro, frota, regras da IA, pontuação, cores, caminhos).
- `src/jogo.py`: loop principal, eventos, atualização do estado e desenho.
- `src/tabuleiro.py`: regras do tabuleiro (posicionar, atirar, afundar, fim de jogo).
- `src/assistente.py`: Radar IA simulado (sugestão, confiança superconfiante, sonar, histórico da IA).
- `src/cpu.py`: jogadas da CPU.
- `src/funcoes.py`: funções auxiliares (pontuação, conversão de clique, precisão, nome do ranking).
- `src/dados.py`: leitura e gravação do recorde e do ranking.
- `src/sprites.py`: função do template para recortar sprites (ainda não usada).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde e ranking).
- `tests/`: testes unitários com `pytest`.
- `pytest.ini`: configuração para rodar os testes com `pytest` a partir da raiz.
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

| Integrante | Frente |
|------------|--------|
| Arthur Filipe Silva Dornas | Repositório, documentação e interface das melhorias (menu, posicionamento manual, sons) |
| Diego Emanuel Oliveira Marques | Regras do tabuleiro e CPU (`src/tabuleiro.py`, `src/cpu.py`) |
| Wyatt Nicolas Sperber Lopes de Carvalho | Protótipo, Radar IA, pontuação e dados (`src/jogo.py`, `src/assistente.py`, `src/funcoes.py`, `src/dados.py`, `tests/`) |

O detalhamento (o que cada um entregou e as próximas tarefas) está na seção 18 de `docs/proposta.MD`.

## Andamento

- [x] Proposta inicial (`docs/proposta.MD`)
- [x] **PC02 (Semana 2 – protótipo executável):** janela do Pygame, loop principal, controles (mouse, ESPAÇO, V, R, ESC), tabuleiros, tiros, CPU, Radar IA com sonar e penalidade (mecânica temática), vitória/derrota, recorde e testes com `pytest`
- [x] Ranking com nome do jogador (top 5 em arquivo)
- [x] Equilíbrio da IA: confiança superconfiante, histórico de acertos visível e sonar extra ao afundar navio
- [ ] Posicionamento manual dos navios (lógica pronta em `src/tabuleiro.py`, falta a tela no jogo)
- [ ] CPU nível médio (lógica pronta em `src/cpu.py`) e menu inicial para escolher a dificuldade
- [ ] Sons
