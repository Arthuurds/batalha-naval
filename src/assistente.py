"""Assistente de IA simulado (mecânica temática do jogo).

Tema: confiabilidade de sistemas inteligentes.
A cada turno, o "Radar IA" sugere uma casa do tabuleiro inimigo e mostra um
percentual de confiança. A sugestão NÃO é sempre correta:

- confiança mais alta indica uma chance um pouco maior de acerto, mas
- a IA é "superconfiante": o percentual mostrado é sempre MAIOR do que a
  chance real de acerto. Uma sugestão com 90% pode errar com frequência.

O jogador precisa decidir se confia, se confere com o sonar (usos limitados)
ou se ignora a sugestão. O histórico de acertos da IA fica visível na tela
(transparência), para o jogador avaliar o sistema com base em resultados.

Não há IA real aqui: a "decisão" é simulada com sorteio e condicionais,
como o enunciado permite.
"""

import random

from src.funcoes import limitar_valor
from src.tabuleiro import casas_sem_tiro, tem_navio

CONFIANCA_MINIMA = 50   # menor percentual de confiança que a IA exibe
CONFIANCA_MAXIMA = 95   # maior percentual de confiança que a IA exibe
CONFIANCA_MEDIA = (CONFIANCA_MINIMA + CONFIANCA_MAXIMA) / 2


def chance_real_de_acerto(chance_media, confianca):
    """Calcula a chance REAL de a sugestão estar certa a partir da confiança exibida.

    A chance real fica em torno de chance_media e sobe ou desce 1 ponto
    percentual para cada ponto de confiança acima ou abaixo da média.
    Exemplo com chance_media = 0.45: confiança 95% -> chance real de 0.675;
    confiança 50% -> chance real de 0.225. O resultado fica entre 0 e 1.
    """
    chance = chance_media + (confianca - CONFIANCA_MEDIA) / 100
    return limitar_valor(chance, 0.0, 1.0)


def gerar_sugestao(tabuleiro_inimigo, chance_acerto, gerador=random):
    """Gera uma sugestão de tiro do assistente de IA.

    chance_acerto é a chance MÉDIA de a IA acertar (configurada em config.py).

    Retorna um dicionário com:
    - "casa": tupla (linha, coluna) sugerida;
    - "correta": True se realmente há navio na casa (o jogador não vê isso);
    - "confianca": percentual exibido na tela;
    - "verificada": se o jogador já conferiu a sugestão com o sonar.
    Retorna None se não houver casas disponíveis.
    """
    livres = casas_sem_tiro(tabuleiro_inimigo)
    if not livres:
        return None

    com_navio = []
    sem_navio = []
    for linha, coluna in livres:
        if tem_navio(tabuleiro_inimigo, linha, coluna):
            com_navio.append((linha, coluna))
        else:
            sem_navio.append((linha, coluna))

    # 1. A IA "anuncia" uma confiança.
    confianca = gerador.randint(CONFIANCA_MINIMA, CONFIANCA_MAXIMA)

    # 2. Sorteia se, desta vez, a IA vai acertar, usando a chance REAL.
    vai_acertar = gerador.random() < chance_real_de_acerto(chance_acerto, confianca)

    if vai_acertar and com_navio:
        casa = gerador.choice(com_navio)
    elif sem_navio:
        casa = gerador.choice(sem_navio)
    else:
        casa = gerador.choice(com_navio)

    return {
        "casa": casa,
        "correta": tem_navio(tabuleiro_inimigo, casa[0], casa[1]),
        "confianca": confianca,
        "verificada": False,
    }


def verificar_sugestao(sugestao, verificacoes_restantes):
    """Usa o sonar para conferir a sugestão.

    Retorna uma tupla (resultado, verificacoes_restantes), em que resultado é:
    - "sem_sugestao": não há sugestão para verificar;
    - "ja_verificada": a sugestão já foi conferida (não gasta sonar);
    - "sem_sonar": acabaram as verificações;
    - "confirmada": há navio na casa sugerida;
    - "desmentida": a casa sugerida é água.
    """
    if sugestao is None:
        return "sem_sugestao", verificacoes_restantes
    if sugestao["verificada"]:
        return "ja_verificada", verificacoes_restantes
    if verificacoes_restantes <= 0:
        return "sem_sonar", verificacoes_restantes

    sugestao["verificada"] = True
    if sugestao["correta"]:
        return "confirmada", verificacoes_restantes - 1
    return "desmentida", verificacoes_restantes - 1


def sonar_apos_tiro(resultado, verificacoes, maximo):
    """Recompensa: afundar um navio devolve 1 uso de sonar, sem passar do máximo."""
    if resultado == "afundou":
        return min(verificacoes + 1, maximo)
    return verificacoes


# ---------------------------------------------------------------------------
# Histórico da IA (transparência): quantas sugestões já se mostraram certas
# ---------------------------------------------------------------------------

def criar_historico_ia():
    """Cria o histórico vazio de sugestões cujo resultado já foi revelado."""
    return {"reveladas": 0, "corretas": 0}


def registrar_revelacao(historico, correta):
    """Registra uma sugestão cujo resultado o jogador descobriu (por tiro ou sonar)."""
    historico["reveladas"] += 1
    if correta:
        historico["corretas"] += 1


def taxa_acerto_ia(historico):
    """Percentual de acerto da IA nas sugestões reveladas, ou None se ainda não há dados."""
    if historico["reveladas"] == 0:
        return None
    return round(historico["corretas"] * 100 / historico["reveladas"])
