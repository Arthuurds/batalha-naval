# Proposta Inicial do Jogo

Proposta do grupo para o projeto final, desenvolvido com **Python e Pygame**.
*Atualizada no ponto de controle 04 (Semana 2 – protótipo inicial executável): tema definido, mecânica do Radar IA incluída, controles ajustados ao protótipo e divisão de tarefas entre os integrantes (seção 18).*

## 1. Nome provisório do jogo

**Nome:**

> Batalha Naval: Radar IA

## 2. Integrantes do grupo

- Nome 1: Arthur Filipe Silva Dornas – 930592
- Nome 2: Diego Emanuel Oliveira Marques – 931449
- Nome 3: Wyatt Nicolas Sperber Lopes de Carvalho – 931271

## 3. Tema escolhido

**Tema:**

> Confiabilidade de sistemas inteligentes: assistentes de IA podem errar, inclusive quando mostram alta confiança, e por isso é importante conferir os resultados antes de agir (uso responsável, transparência e análise crítica).

**Como esse tema se relaciona com o jogo?**

> A cada turno, um assistente de IA (o "Radar IA") sugere uma casa do tabuleiro inimigo e mostra um percentual de confiança. A sugestão erra com frequência, e a confiança alta não garante acerto. O jogador escolhe entre seguir a IA, conferir com o sonar (usos limitados) ou decidir sozinho. Seguir a IA sem verificar e cair na água tira pontos, e a tela final mostra quantas vezes o jogador confiou na IA e quantas vezes ela errou.

## 4. Tipo de jogo

**Tipo escolhido:**

> Estratégia por turnos em tabuleiro (Batalha Naval), jogador contra o computador.

## 5. Descrição geral do jogo

**Descrição:**

> A tela mostra dois tabuleiros 10×10: à esquerda, a frota do jogador; à direita, o tabuleiro da CPU, com os navios escondidos. As frotas são posicionadas automaticamente. Na sua vez, o jogador clica em uma casa do tabuleiro inimigo para atirar, ou segue a sugestão do Radar IA, destacada em amarelo com o percentual de confiança. Antes de atirar, ele pode usar o sonar para conferir se a sugestão está certa. Depois a CPU atira no tabuleiro do jogador. Cada tiro mostra se foi água, acerto ou se o navio afundou.

## 6. Objetivo do jogador

**Objetivo:**

> Afundar todos os navios da CPU antes que ela afunde os seus, fazendo a maior pontuação possível e usando a IA de forma crítica.

## 7. Regras principais

- Regra 1: Cada lado tem 5 navios (tamanhos 5, 4, 3, 3 e 2), na horizontal ou vertical, sem sair do tabuleiro e sem se sobrepor.
- Regra 2: Os turnos se alternam, com um tiro por vez. Não é permitido atirar duas vezes na mesma casa.
- Regra 3: Acertar um navio vale +10 pontos, e afundar um navio dá +20 de bônus.
- Regra 4: A cada turno o Radar IA sugere uma casa com um percentual de confiança. Seguir a sugestão sem verificar e cair na água custa −10 pontos.
- Regra 5: O sonar confere se a sugestão da IA está certa, sem gastar o tiro. Ele tem apenas 3 usos por partida.

## 8. Condição de vitória

**Condição de vitória:**

> O jogador vence ao afundar os 5 navios da CPU. Se a pontuação superar o recorde, ela é salva em `data/recorde.txt`.

## 9. Condição de derrota ou encerramento

**Condição de derrota ou encerramento:**

> O jogador perde quando a CPU afunda todos os seus navios. A tecla ESC encerra o jogo a qualquer momento. Ao fim da partida aparece um resumo (pontos, precisão, vezes que seguiu a IA e quantas vezes ela errou), e a tecla R começa uma nova partida.

## 10. Elementos previstos no jogo

- **Personagem ou elemento principal:** a frota do jogador e a mira (mouse) sobre o tabuleiro inimigo.
- **Obstáculos ou desafios:** a frota escondida da CPU, a CPU que também ataca e o Radar IA, que ajuda mas nem sempre acerta.
- **Itens ou objetos de interação (se houver):** casas dos tabuleiros, sugestão da IA (marcador amarelo) e sonar (marcador laranja para navio confirmado, círculo cinza para água confirmada).
- **Pontuação, vidas, tempo ou progresso:** pontos, recorde, tiros, acertos, precisão, navios restantes de cada lado e usos de sonar restantes.

## 11. Controles previstos

**Controles:**

> Clique esquerdo no tabuleiro inimigo: atirar. ESPAÇO: atirar na casa sugerida pela IA. V: verificar a sugestão com o sonar. R: jogar de novo (na tela final). ESC: sair.

## 12. Principais dificuldades esperadas

- Dificuldade 1: Converter o clique do mouse (pixels) em linha e coluna e desenhar os dois tabuleiros e o painel com Pygame.
- Dificuldade 2: Equilibrar a mecânica da IA (chance de acerto, confiança exibida, penalidade e número de sonares) para que confiar às cegas não compense, mas a IA continue útil.
- Dificuldade 3: Organizar o código em módulos testáveis e integrar o trabalho dos três integrantes pelo GitHub.

## 13. Escopo mínimo para a entrega final

**Escopo mínimo:**

> Dois tabuleiros 10×10; frotas posicionadas automaticamente; turnos alternados com tiro pelo mouse; indicação de água, acerto e afundado; CPU atirando aleatoriamente sem repetir casas; Radar IA com sugestão, confiança, sonar e penalidade; pontuação e recorde salvos em arquivo; tela de vitória ou derrota com resumo do uso da IA; testes com `pytest` para as funções de lógica.

## 14. Possíveis melhorias, caso haja tempo

- Melhoria 1: Posicionamento manual dos navios com o mouse (tecla R para girar).
- Melhoria 2: CPU nível médio, que ataca as casas vizinhas depois de um acerto, e escolha de dificuldade em um menu inicial.
- Melhoria 3: Ranking com nome do jogador em `data/ranking.txt`, além de sons de tiro e explosão.

## 15. Organização inicial do código

| Arquivo | Responsabilidade |
|---------|------------------|
| `main.py` | Ponto de entrada (`python main.py`). |
| `src/config.py` | Constantes: tela, tabuleiro, frota, regras da IA, pontuação, cores e caminhos. |
| `src/jogo.py` | Loop principal do Pygame: eventos, atualização do estado e desenho. |
| `src/tabuleiro.py` | Regras do tabuleiro: posicionar navios, atirar, navio afundado e fim de jogo. |
| `src/assistente.py` | Radar IA simulado: sugestão, confiança e verificação com sonar. |
| `src/cpu.py` | Escolha do tiro da CPU. |
| `src/funcoes.py` | Funções auxiliares: pontuação, conversão de clique em casa e precisão. |
| `src/dados.py` | Leitura e gravação do recorde em arquivo. |
| `tests/` | Testes com `pytest` das funções de lógica. |

Estruturas de dados usadas: matriz (lista de listas) para o tabuleiro, dicionários para o tabuleiro, os navios, a sugestão da IA e o estado da partida, tuplas para as coordenadas, conjuntos para tiros e acertos, e lista de tuplas para a frota.

## 16. Recursos utilizados

- Biblioteca **Pygame** (desenho, eventos e janela) e **pytest** (testes).
- Fonte padrão do Pygame. Não há imagens, sons ou fontes externas até o momento; os elementos são desenhados com formas geométricas.
- Qualquer recurso externo adicionado depois será registrado no `README.md`, com origem e licença.

## 17. Declaração de originalidade

Declaramos que este projeto é de autoria do grupo, desenvolvido a partir do template oficial da disciplina. A ideia da Batalha Naval é um jogo clássico de domínio público, e a mecânica do Radar IA, as regras de pontuação e a implementação foram criadas pelo grupo. Materiais de consulta e recursos externos usados serão citados no `README.md`.

## 18. Divisão de tarefas

O trabalho foi dividido em três frentes, uma por integrante, para que cada um seja responsável por módulos e testes próprios. A integração é feita pelo GitHub, e todos revisam o código dos colegas antes de juntar as mudanças.

| Integrante | Frente | Arquivos sob responsabilidade | O que já foi entregue (PC04) | Próximas tarefas |
|------------|--------|-------------------------------|------------------------------|------------------|
| Arthur Filipe Silva Dornas | Interface e loop do jogo | `main.py`, `src/jogo.py`, `src/config.py` | Janela do Pygame, loop principal, tratamento de eventos (mouse, ESPAÇO, V, R, ESC), desenho dos tabuleiros, do painel e da tela final, integração dos módulos | Menu inicial com escolha de dificuldade, sons de tiro e explosão |
| Diego Emanuel Oliveira Marques | Regras do tabuleiro e CPU | `src/tabuleiro.py`, `src/cpu.py`, `tests/test_tabuleiro.py` | Posicionamento automático da frota, tiro, água/acerto/afundado, fim de jogo, tiro aleatório da CPU sem repetir casas | Posicionamento manual dos navios com o mouse, CPU nível médio (ataca vizinhas após acerto) |
| Wyatt Nicolas Sperber Lopes de Carvalho | Radar IA, pontuação e dados | `src/assistente.py`, `src/funcoes.py`, `src/dados.py`, `tests/test_assistente.py`, `tests/test_logica.py` | Sugestão da IA com confiança, sonar com usos limitados, pontuação e penalidade, conversão de clique em casa, precisão, recorde em arquivo | Ranking com nome do jogador (`data/ranking.txt`), ajuste do equilíbrio da IA (chance de acerto, confiança, penalidade) |
