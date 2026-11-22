import random

from src.config import FROTA
from src.tabuleiro import criar_tabuleiro, posicionar_frota_aleatoria, tem_navio, atirar
from src.assistente import (
    gerar_sugestao,
    verificar_sugestao,
    chance_real_de_acerto,
    sonar_apos_tiro,
    criar_historico_ia,
    registrar_revelacao,
    taxa_acerto_ia,
    CONFIANCA_MINIMA,
    CONFIANCA_MAXIMA,
)


def tabuleiro_de_teste():
    """Cria um tabuleiro com a frota posicionada de forma repetivel."""
    tab = criar_tabuleiro()
    posicionar_frota_aleatoria(tab, FROTA, random.Random(1))
    return tab


def test_sugestao_campo_correta_bate_com_o_tabuleiro():
    """O campo 'correta' deve indicar se ha mesmo navio na casa sugerida."""
    tab = tabuleiro_de_teste()
    gerador = random.Random(3)
    for _ in range(50):
        sugestao = gerar_sugestao(tab, 0.5, gerador)
        linha, coluna = sugestao["casa"]
        assert sugestao["correta"] == tem_navio(tab, linha, coluna)


def test_chance_real_sobe_com_a_confianca():
    """Confianca maior deve significar chance real maior (a confianca tem algum valor)."""
    assert chance_real_de_acerto(0.45, 95) > chance_real_de_acerto(0.45, 50)


def test_chance_real_e_menor_que_a_confianca_exibida():
    """A IA e superconfiante: a chance real fica sempre abaixo do percentual exibido."""
    for confianca in range(CONFIANCA_MINIMA, CONFIANCA_MAXIMA + 1):
        assert chance_real_de_acerto(0.45, confianca) < confianca / 100


def test_chance_real_fica_entre_0_e_1():
    """Mesmo com valores extremos a chance real e uma probabilidade valida."""
    assert chance_real_de_acerto(1.0, 95) == 1.0
    assert chance_real_de_acerto(0.0, 50) == 0.0


def test_ia_erra_mesmo_com_confianca_alta():
    """Em muitas sugestoes, a IA erra algumas vezes mesmo com 85% ou mais."""
    tab = tabuleiro_de_teste()
    gerador = random.Random(11)
    erros_confiantes = 0
    for _ in range(500):
        sugestao = gerar_sugestao(tab, 0.45, gerador)
        if sugestao["confianca"] >= 85 and not sugestao["correta"]:
            erros_confiantes += 1
    assert erros_confiantes > 0


def test_acerto_medio_abaixo_da_confianca_media():
    """Na media, a IA acerta menos do que a confianca que ela mostra."""
    tab = tabuleiro_de_teste()
    gerador = random.Random(12)
    acertos = 0
    soma_confianca = 0
    total = 2000
    for _ in range(total):
        sugestao = gerar_sugestao(tab, 0.45, gerador)
        soma_confianca += sugestao["confianca"]
        if sugestao["correta"]:
            acertos += 1
    assert acertos / total < (soma_confianca / total) / 100


def test_ia_nao_sugere_casa_ja_atirada():
    """A sugestao deve ser sempre uma casa que ainda nao recebeu tiro."""
    tab = tabuleiro_de_teste()
    for linha in range(10):
        for coluna in range(9):
            atirar(tab, linha, coluna)
    sugestao = gerar_sugestao(tab, 0.5, random.Random(2))
    assert sugestao["casa"][1] == 9


def test_confianca_entre_0_e_100():
    """A confianca exibida e um percentual valido."""
    tab = tabuleiro_de_teste()
    gerador = random.Random(9)
    for _ in range(50):
        confianca = gerar_sugestao(tab, 0.5, gerador)["confianca"]
        assert CONFIANCA_MINIMA <= confianca <= CONFIANCA_MAXIMA


def test_verificar_gasta_sonar_e_revela_resultado():
    """Verificar uma sugestao gasta 1 sonar e diz se a IA estava certa."""
    certa = {"casa": (0, 0), "correta": True, "confianca": 90, "verificada": False}
    errada = {"casa": (1, 1), "correta": False, "confianca": 90, "verificada": False}
    assert verificar_sugestao(certa, 3) == ("confirmada", 2)
    assert verificar_sugestao(errada, 2) == ("desmentida", 1)


def test_verificar_sem_sonar_ou_repetido():
    """Sem sonar nao verifica; verificar de novo nao gasta sonar."""
    sugestao = {"casa": (0, 0), "correta": True, "confianca": 70, "verificada": False}
    assert verificar_sugestao(sugestao, 0) == ("sem_sonar", 0)
    verificar_sugestao(sugestao, 3)
    assert verificar_sugestao(sugestao, 2) == ("ja_verificada", 2)
    assert verificar_sugestao(None, 2) == ("sem_sugestao", 2)


def test_afundar_devolve_um_sonar_ate_o_maximo():
    """Afundar navio devolve 1 sonar; nunca passa do maximo; outros tiros nao mudam."""
    assert sonar_apos_tiro("afundou", 1, 3) == 2
    assert sonar_apos_tiro("afundou", 3, 3) == 3
    assert sonar_apos_tiro("acerto", 1, 3) == 1
    assert sonar_apos_tiro("agua", 0, 3) == 0


def test_historico_da_ia():
    """O historico conta as sugestoes reveladas e calcula a taxa de acerto."""
    historico = criar_historico_ia()
    assert taxa_acerto_ia(historico) is None
    registrar_revelacao(historico, True)
    registrar_revelacao(historico, False)
    registrar_revelacao(historico, True)
    registrar_revelacao(historico, False)
    assert historico == {"reveladas": 4, "corretas": 2}
    assert taxa_acerto_ia(historico) == 50
