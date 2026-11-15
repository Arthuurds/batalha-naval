# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com **Python e Pygame** dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

## 1. Nome provisório do jogo

Informe o nome provisório do jogo.

**Nome:**

> Batalha Naval

## 2. Integrantes do grupo

- Nome 1: Arthur Filipe Silva Dornas – 930592
- Nome 2: Diego Emanuel Oliveira Marques – 931449
- Nome 3: Wyatt Nicolas Sperber Lopes de Carvalho – 931271

## 3. Tema escolhido

Indique qual tema específico o grupo escolheu **dentro do eixo temático definido no enunciado**.

**Tema:**

> [PREENCHER: tema dentro do eixo temático do enunciado]

**Como esse tema se relaciona com o jogo?** Explique brevemente (2 a 4 linhas) como ele aparecerá nos objetivos, nas regras ou nos desafios, e não apenas nas imagens ou no cenário.

> [PREENCHER após definir o tema]

## 4. Tipo de jogo

Indique o estilo do jogo. Exemplos: desviar de obstáculos, coleta de itens, labirinto, perguntas e respostas, memória, Pong, Snake, Breakout, corrida ou sobrevivência simples.

**Tipo escolhido:**

> Jogo de estratégia por turnos (tabuleiro), jogador contra o computador.

## 5. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará. O que aparece na tela? O que o jogador controla? O que ele precisa fazer e quais desafios encontrará?

**Descrição:**

> A tela mostra dois tabuleiros 10×10: à esquerda, a frota do jogador; à direita, o tabuleiro da CPU, com os navios escondidos. Primeiro o jogador posiciona seus 5 navios com o mouse (ou de forma automática) e a CPU posiciona os dela aleatoriamente. Depois, os dois se alternam clicando/disparando em casas do tabuleiro adversário. Cada tiro mostra se foi água, acerto ou se o navio foi afundado. O desafio é descobrir onde estão os navios inimigos usando o mínimo de tiros, enquanto a CPU tenta fazer o mesmo.

## 6. Objetivo do jogador

Descreva o objetivo principal. Por exemplo: coletar itens, sobreviver por determinado tempo, chegar ao final de um percurso ou completar desafios.

**Objetivo:**

> Afundar todos os navios da CPU antes que ela afunde todos os navios do jogador.

## 7. Regras principais

Liste até cinco regras que expliquem o funcionamento do jogo. Exemplos: o jogador começa com três vidas; acertos somam pontos; colisões retiram vidas.

- Regra 1: Cada lado tem 5 navios (tamanhos 5, 4, 3, 3 e 2), posicionados na horizontal ou vertical, sem sair do tabuleiro e sem se sobrepor.
- Regra 2: O jogador começa atirando e depois os turnos se alternam, um tiro por vez.
- Regra 3: Não é permitido atirar duas vezes na mesma casa; o clique é ignorado e o turno continua.
- Regra 4: Um navio afunda quando todas as suas casas são atingidas.
- Regra 5: Cada tiro conta para as estatísticas (tiros, acertos e precisão), usadas no ranking.

## 8. Condição de vitória

Explique como o jogador vence ou conclui a partida. Exemplos: alcançar uma pontuação, finalizar uma fase ou completar todas as tarefas.

**Condição de vitória:**

> O jogador vence ao afundar os 5 navios da CPU.

## 9. Condição de derrota ou encerramento

Explique quando a partida termina ou como o jogador perde. Exemplos: esgotar as vidas, acabar o tempo ou atingir o limite de erros.

**Condição de derrota ou encerramento:**

> O jogador perde quando a CPU afunda todos os seus navios. A partida também pode ser encerrada a qualquer momento com a tecla ESC (contada como desistência).

## 10. Elementos previstos no jogo

Descreva brevemente os elementos mais importantes, sem precisar detalhar a implementação.

- **Personagem ou elemento principal:** a frota do jogador e a mira (cursor do mouse) sobre o tabuleiro inimigo.
- **Obstáculos ou desafios:** a frota escondida da CPU e a própria CPU, que também ataca (nível fácil: tiros aleatórios; nível médio: após acertar, ataca as casas vizinhas).
- **Itens ou objetos de interação (se houver):** casas dos tabuleiros e marcadores de tiro (água, acerto, afundado).
- **Pontuação, vidas, tempo ou progresso:** navios restantes de cada lado (funcionam como "vidas"), número de tiros, acertos e precisão; ranking salvo em `data/ranking.txt`.

## 11. Controles previstos

Informe como o jogador vai interagir com o jogo (por exemplo, setas para movimentar, espaço para agir ou mouse para selecionar).

**Controles:**

> Mouse: clique esquerdo para posicionar navios no próprio tabuleiro e para atirar no tabuleiro da CPU. Tecla R (ou clique direito) para girar o navio, A para posicionamento automático, Enter para iniciar a partida e ESC para voltar ao menu/sair.

## 12. Principais dificuldades esperadas

Cite até três dificuldades que o grupo espera enfrentar. Exemplos: movimentação, colisões, controle de tempo, testes ou uso do GitHub.

- Dificuldade 1: Converter o clique do mouse (pixels) em linha e coluna do tabuleiro e desenhar os dois tabuleiros corretamente com Pygame.
- Dificuldade 2: Programar a CPU do nível médio (escolher casas vizinhas após um acerto, sem repetir tiros e sem sair do tabuleiro).
- Dificuldade 3: Organizar o código em módulos testáveis e integrar o trabalho dos três integrantes pelo GitHub.

## 13. Escopo mínimo para a entrega final

Descreva a **versão mais simples que já seria jogável**, com as interações e regras essenciais. Evite planejar funcionalidades demais.

**Escopo mínimo:**

> Dois tabuleiros 10×10 desenhados na tela; posicionamento automático da frota do jogador e da CPU; turnos alternados com tiro pelo clique do mouse; indicação de água/acerto/afundado; CPU atirando aleatoriamente sem repetir casas; tela de vitória ou derrota com o número de tiros; testes com `pytest` para validação de posição dos navios, tiro repetido e fim de jogo.

## 14. Possíveis melhorias, caso haja tempo

Liste até três funcionalidades extras para implementar somente depois que a versão mínima estiver funcionando. Exemplos: sons, fases, ranking, animações ou menu inicial.

- Melhoria 1: CPU nível médio (ataca as casas vizinhas após um acerto) e escolha de dificuldade no menu.
- Melhoria 2: Posicionamento manual dos navios com o mouse e rotação pela tecla R.
- Melhoria 3: Ranking salvo em arquivo, sons de tiro/explosão e menu inicial.
