"""Jogadas do adversário controlado pelo computador (CPU)."""

import random

from src.tabuleiro import (
    casa_de_navio_afundado,
    casas_sem_tiro,
    dentro_do_tabuleiro,
    tem_navio,
)


def escolher_tiro_cpu(tabuleiro_jogador, gerador=random):
    """Nível fácil: a CPU escolhe aleatoriamente uma casa onde ainda não atirou.

    Retorna a tupla (linha, coluna) ou None se não houver casas livres.
    """
    livres = casas_sem_tiro(tabuleiro_jogador)
    if not livres:
        return None
    return gerador.choice(livres)


# ---------------------------------------------------------------------------
# Nível médio (melhoria 2 da proposta)
#
# A CPU usa só o que ela mesma já sabe pelos tiros que deu: onde acertou
# e quais navios já afundaram (isso é anunciado na tela). Não "espia"
# navios escondidos. Por isso não precisa guardar estado: tudo é calculado
# a partir do tabuleiro do jogador.
#
# 1. Se há acertos em navios que ainda não afundaram, ataca perto deles.
#    Com 2 ou mais acertos em linha, continua nessa direção.
# 2. Se não há alvo, procura em "xadrez" (linha + coluna par): o menor
#    navio tem 2 casas, então sempre ocupa pelo menos uma dessas casas.
# ---------------------------------------------------------------------------

FACIL = "facil"
MEDIO = "medio"


def acertos_pendentes(tabuleiro_jogador):
    """Casas onde a CPU acertou um navio que ainda não afundou."""
    pendentes = set()
    for linha, coluna in tabuleiro_jogador["tiros"]:
        if tem_navio(tabuleiro_jogador, linha, coluna) and \
                not casa_de_navio_afundado(tabuleiro_jogador, linha, coluna):
            pendentes.add((linha, coluna))
    return pendentes


def vizinhos(tabuleiro, linha, coluna):
    """Casas acima, abaixo, à esquerda e à direita que existem no tabuleiro."""
    candidatos = [(linha - 1, coluna), (linha + 1, coluna),
                  (linha, coluna - 1), (linha, coluna + 1)]
    resultado = []
    for l, c in candidatos:
        if dentro_do_tabuleiro(tabuleiro, l, c):
            resultado.append((l, c))
    return resultado


def pontas_das_linhas(pendentes):
    """Para acertos alinhados, retorna as casas logo antes e depois da linha.

    Ex.: acertos em (3, 4) e (3, 5) -> {(3, 3), (3, 6)}.
    """
    pontas = set()
    for linha, coluna in pendentes:
        # Linha horizontal começando nesta casa
        if (linha, coluna + 1) in pendentes and (linha, coluna - 1) not in pendentes:
            fim = coluna
            while (linha, fim + 1) in pendentes:
                fim += 1
            pontas.add((linha, coluna - 1))
            pontas.add((linha, fim + 1))
        # Linha vertical começando nesta casa
        if (linha + 1, coluna) in pendentes and (linha - 1, coluna) not in pendentes:
            fim = linha
            while (fim + 1, coluna) in pendentes:
                fim += 1
            pontas.add((linha - 1, coluna))
            pontas.add((fim + 1, coluna))
    return pontas


def alvos_cpu(tabuleiro_jogador):
    """Casas que a CPU média quer atacar agora (lista vazia se não há alvo)."""
    pendentes = acertos_pendentes(tabuleiro_jogador)
    if not pendentes:
        return []

    livres = set(casas_sem_tiro(tabuleiro_jogador))

    # 1º: continuar uma linha de acertos
    alvos = pontas_das_linhas(pendentes) & livres
    if alvos:
        return sorted(alvos)

    # 2º: qualquer vizinho livre de um acerto
    alvos = set()
    for linha, coluna in pendentes:
        for casa in vizinhos(tabuleiro_jogador, linha, coluna):
            if casa in livres:
                alvos.add(casa)
    return sorted(alvos)


def escolher_tiro_cpu_medio(tabuleiro_jogador, gerador=random):
    """Nível médio: caça os navios depois de acertar e procura em xadrez.

    Retorna a tupla (linha, coluna) ou None se não houver casas livres.
    """
    livres = casas_sem_tiro(tabuleiro_jogador)
    if not livres:
        return None

    alvos = alvos_cpu(tabuleiro_jogador)
    if alvos:
        return gerador.choice(alvos)

    xadrez = [casa for casa in livres if (casa[0] + casa[1]) % 2 == 0]
    if xadrez:
        return gerador.choice(xadrez)
    return gerador.choice(livres)


def escolher_tiro(tabuleiro_jogador, dificuldade=FACIL, gerador=random):
    """Escolhe o tiro da CPU de acordo com a dificuldade ("facil" ou "medio")."""
    if dificuldade == MEDIO:
        return escolher_tiro_cpu_medio(tabuleiro_jogador, gerador)
    if dificuldade == FACIL:
        return escolher_tiro_cpu(tabuleiro_jogador, gerador)
    raise ValueError(f"Dificuldade inválida: {dificuldade}")