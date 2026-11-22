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
