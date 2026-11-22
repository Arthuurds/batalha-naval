"""Jogadas do adversário controlado pelo computador (CPU)."""

import random

from src.tabuleiro import casas_sem_tiro


def escolher_tiro_cpu(tabuleiro_jogador, gerador=random):
    """Nível fácil: a CPU escolhe aleatoriamente uma casa onde ainda não atirou.

    Retorna a tupla (linha, coluna) ou None se não houver casas livres.
    """
    livres = casas_sem_tiro(tabuleiro_jogador)
    if not livres:
        return None
    return gerador.choice(livres)
