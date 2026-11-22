"""Regras do tabuleiro da Batalha Naval.

Este módulo não usa Pygame: só listas, dicionários, tuplas e conjuntos.
Assim as funções podem ser testadas com pytest.

Um tabuleiro é um dicionário com:
- "grade": matriz (lista de listas) em que cada casa guarda o índice do navio
  que está nela, ou -1 se for água;
- "navios": lista de dicionários, um para cada navio;
- "tiros": conjunto de tuplas (linha, coluna) que já receberam tiro.
"""

import random

from src.config import TAMANHO_TABULEIRO

AGUA = -1


def criar_tabuleiro(tamanho=TAMANHO_TABULEIRO):
    """Cria um tabuleiro vazio, só com água e sem tiros."""
    grade = []
    for _ in range(tamanho):
        grade.append([AGUA] * tamanho)

    return {
        "grade": grade,
        "navios": [],
        "tiros": set(),
    }


def calcular_casas(linha, coluna, tamanho, horizontal):
    """Retorna a lista de casas (linha, coluna) que um navio ocupa a partir da casa inicial."""
    casas = []
    for i in range(tamanho):
        if horizontal:
            casas.append((linha, coluna + i))
        else:
            casas.append((linha + i, coluna))
    return casas


def dentro_do_tabuleiro(tabuleiro, linha, coluna):
    """Indica se a casa (linha, coluna) existe no tabuleiro."""
    tamanho = len(tabuleiro["grade"])
    return 0 <= linha < tamanho and 0 <= coluna < tamanho


def posicao_valida(tabuleiro, linha, coluna, tamanho, horizontal):
    """Indica se um navio cabe na posição: dentro do tabuleiro e sem sobrepor outro navio."""
    for l, c in calcular_casas(linha, coluna, tamanho, horizontal):
        if not dentro_do_tabuleiro(tabuleiro, l, c):
            return False
        if tabuleiro["grade"][l][c] != AGUA:
            return False
    return True


def posicionar_navio(tabuleiro, nome, linha, coluna, tamanho, horizontal):
    """Coloca um navio no tabuleiro se a posição for válida. Retorna True se conseguiu."""
    if not posicao_valida(tabuleiro, linha, coluna, tamanho, horizontal):
        return False

    indice = len(tabuleiro["navios"])
    casas = calcular_casas(linha, coluna, tamanho, horizontal)

    for l, c in casas:
        tabuleiro["grade"][l][c] = indice

    tabuleiro["navios"].append({
        "nome": nome,
        "tamanho": tamanho,
        "casas": casas,
        "acertos": set(),
    })
    return True


def posicionar_frota_aleatoria(tabuleiro, frota, gerador=random):
    """Posiciona todos os navios da frota em posições aleatórias válidas."""
    tamanho_tab = len(tabuleiro["grade"])
    for nome, tamanho in frota:
        colocado = False
        while not colocado:
            horizontal = gerador.choice([True, False])
            linha = gerador.randrange(tamanho_tab)
            coluna = gerador.randrange(tamanho_tab)
            colocado = posicionar_navio(tabuleiro, nome, linha, coluna, tamanho, horizontal)


def tem_navio(tabuleiro, linha, coluna):
    """Indica se existe navio na casa (linha, coluna)."""
    return tabuleiro["grade"][linha][coluna] != AGUA


def navio_afundado(navio):
    """Um navio afunda quando todas as suas casas foram atingidas."""
    return len(navio["acertos"]) == navio["tamanho"]


def atirar(tabuleiro, linha, coluna):
    """Registra um tiro na casa e retorna uma tupla (resultado, nome_do_navio).

    resultado pode ser:
    - "invalido": casa fora do tabuleiro;
    - "repetido": já houve tiro nessa casa (o tiro não conta);
    - "agua": não havia navio;
    - "acerto": acertou um navio que ainda não afundou;
    - "afundou": esse tiro afundou o navio.
    nome_do_navio só é preenchido em "acerto" e "afundou".
    """
    if not dentro_do_tabuleiro(tabuleiro, linha, coluna):
        return "invalido", None

    casa = (linha, coluna)
    if casa in tabuleiro["tiros"]:
        return "repetido", None

    tabuleiro["tiros"].add(casa)

    indice = tabuleiro["grade"][linha][coluna]
    if indice == AGUA:
        return "agua", None

    navio = tabuleiro["navios"][indice]
    navio["acertos"].add(casa)

    if navio_afundado(navio):
        return "afundou", navio["nome"]
    return "acerto", navio["nome"]


def frota_destruida(tabuleiro):
    """Indica se todos os navios do tabuleiro foram afundados (fim de jogo)."""
    for navio in tabuleiro["navios"]:
        if not navio_afundado(navio):
            return False
    return True


def navios_restantes(tabuleiro):
    """Conta quantos navios ainda não afundaram."""
    total = 0
    for navio in tabuleiro["navios"]:
        if not navio_afundado(navio):
            total += 1
    return total


def casas_sem_tiro(tabuleiro):
    """Retorna a lista de casas que ainda não receberam tiro."""
    livres = []
    tamanho = len(tabuleiro["grade"])
    for linha in range(tamanho):
        for coluna in range(tamanho):
            if (linha, coluna) not in tabuleiro["tiros"]:
                livres.append((linha, coluna))
    return livres


def casa_de_navio_afundado(tabuleiro, linha, coluna):
    """Indica se a casa pertence a um navio que já afundou (usado no desenho)."""
    indice = tabuleiro["grade"][linha][coluna]
    if indice == AGUA:
        return False
    return navio_afundado(tabuleiro["navios"][indice])


# ---------------------------------------------------------------------------
# Posicionamento manual dos navios (melhoria 1 da proposta)
#
# O estado do posicionamento é um dicionário com:
# - "frota": lista de tuplas (nome, tamanho), na ordem em que serão colocados;
# - "indice": qual navio da frota é a vez de colocar;
# - "horizontal": True para horizontal, False para vertical (tecla R gira).
#
# No jogo.py:
# - para desenhar a "sombra" do navio sob o mouse: previa_posicionamento();
# - no clique: confirmar_posicionamento();
# - na tecla R: girar_navio().
# ---------------------------------------------------------------------------

def criar_posicionamento(frota):
    """Cria o estado do posicionamento manual para a frota informada."""
    return {
        "frota": list(frota),
        "indice": 0,
        "horizontal": True,
    }


def posicionamento_concluido(posicionamento):
    """Indica se todos os navios da frota já foram colocados."""
    return posicionamento["indice"] >= len(posicionamento["frota"])


def navio_atual(posicionamento):
    """Retorna a tupla (nome, tamanho) do navio da vez, ou None se já acabou."""
    if posicionamento_concluido(posicionamento):
        return None
    return posicionamento["frota"][posicionamento["indice"]]


def girar_navio(posicionamento):
    """Alterna o navio da vez entre horizontal e vertical."""
    posicionamento["horizontal"] = not posicionamento["horizontal"]


def previa_posicionamento(tabuleiro, posicionamento, linha, coluna):
    """Mostra onde o navio da vez ficaria se fosse colocado em (linha, coluna).

    Retorna uma tupla (casas, valido):
    - casas: as casas que o navio ocuparia, só as que estão dentro do tabuleiro;
    - valido: True se o navio pode ser colocado ali (desenhar em verde)
      ou False se não pode (desenhar em vermelho).
    """
    atual = navio_atual(posicionamento)
    if atual is None:
        return [], False

    _, tamanho = atual
    horizontal = posicionamento["horizontal"]

    casas = []
    for l, c in calcular_casas(linha, coluna, tamanho, horizontal):
        if dentro_do_tabuleiro(tabuleiro, l, c):
            casas.append((l, c))

    valido = posicao_valida(tabuleiro, linha, coluna, tamanho, horizontal)
    return casas, valido


def confirmar_posicionamento(tabuleiro, posicionamento, linha, coluna):
    """Coloca o navio da vez em (linha, coluna) e passa para o próximo.

    Retorna True se conseguiu colocar. Se a posição for inválida, nada muda.
    """
    atual = navio_atual(posicionamento)
    if atual is None:
        return False

    nome, tamanho = atual
    colocado = posicionar_navio(tabuleiro, nome, linha, coluna, tamanho,
                                posicionamento["horizontal"])
    if colocado:
        posicionamento["indice"] += 1
    return colocado


def remover_ultimo_navio(tabuleiro):
    """Tira do tabuleiro o último navio colocado. Retorna o navio ou None.

    Só deve ser usado antes de a partida começar (sem tiros).
    """
    if not tabuleiro["navios"]:
        return None

    navio = tabuleiro["navios"].pop()
    for l, c in navio["casas"]:
        tabuleiro["grade"][l][c] = AGUA
    return navio


def desfazer_posicionamento(tabuleiro, posicionamento):
    """Volta um passo: remove o último navio colocado. Retorna True se voltou."""
    if posicionamento["indice"] == 0:
        return False

    remover_ultimo_navio(tabuleiro)
    posicionamento["indice"] -= 1
    return True


def completar_aleatorio(tabuleiro, posicionamento, gerador=random):
    """Posiciona aleatoriamente os navios que ainda faltam."""
    faltando = posicionamento["frota"][posicionamento["indice"]:]
    posicionar_frota_aleatoria(tabuleiro, faltando, gerador)
    posicionamento["indice"] = len(posicionamento["frota"])
