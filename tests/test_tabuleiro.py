import random

from src.config import FROTA
from src.tabuleiro import (
    criar_tabuleiro,
    calcular_casas,
    posicao_valida,
    posicionar_navio,
    posicionar_frota_aleatoria,
    atirar,
    frota_destruida,
    navios_restantes,
    casas_sem_tiro,
)
from src.cpu import escolher_tiro_cpu


def test_tabuleiro_comeca_vazio():
    """Tabuleiro novo: 10x10, sem navios e sem tiros."""
    tab = criar_tabuleiro()
    assert len(tab["grade"]) == 10
    assert len(tab["grade"][0]) == 10
    assert tab["navios"] == []
    assert tab["tiros"] == set()


def test_calcular_casas_horizontal_e_vertical():
    """Navio horizontal anda nas colunas; vertical anda nas linhas."""
    assert calcular_casas(2, 3, 3, True) == [(2, 3), (2, 4), (2, 5)]
    assert calcular_casas(2, 3, 3, False) == [(2, 3), (3, 3), (4, 3)]


def test_navio_nao_pode_sair_do_tabuleiro():
    """Porta-avioes (5) a partir da coluna 8 nao cabe na horizontal."""
    tab = criar_tabuleiro()
    assert posicao_valida(tab, 0, 8, 5, True) is False
    assert posicionar_navio(tab, "Porta-aviões", 0, 8, 5, True) is False


def test_navios_nao_podem_se_sobrepor():
    """Um navio nao pode ocupar casa de outro navio."""
    tab = criar_tabuleiro()
    assert posicionar_navio(tab, "Cruzador", 2, 2, 3, True) is True
    assert posicionar_navio(tab, "Submarino", 0, 3, 3, False) is False


def test_frota_aleatoria_valida():
    """A frota aleatoria tem 5 navios, 17 casas ocupadas e nenhuma sobreposicao."""
    tab = criar_tabuleiro()
    posicionar_frota_aleatoria(tab, FROTA, random.Random(42))
    assert len(tab["navios"]) == 5

    ocupadas = set()
    for navio in tab["navios"]:
        for casa in navio["casas"]:
            assert casa not in ocupadas
            ocupadas.add(casa)
    assert len(ocupadas) == 17


def test_tiro_na_agua_e_repetido():
    """Tiro na agua retorna 'agua'; repetir a casa retorna 'repetido'."""
    tab = criar_tabuleiro()
    assert atirar(tab, 5, 5) == ("agua", None)
    assert atirar(tab, 5, 5) == ("repetido", None)


def test_tiro_fora_do_tabuleiro():
    """Coordenada inexistente e invalida."""
    tab = criar_tabuleiro()
    assert atirar(tab, 10, 0) == ("invalido", None)
    assert atirar(tab, -1, 3) == ("invalido", None)


def test_acertar_e_afundar_navio():
    """Atingir todas as casas de um navio deve afunda-lo."""
    tab = criar_tabuleiro()
    posicionar_navio(tab, "Destróier", 0, 0, 2, True)
    assert atirar(tab, 0, 0) == ("acerto", "Destróier")
    assert atirar(tab, 0, 1) == ("afundou", "Destróier")


def test_fim_de_jogo_quando_frota_destruida():
    """frota_destruida so e verdadeiro depois de afundar todos os navios."""
    tab = criar_tabuleiro()
    posicionar_navio(tab, "Destróier", 0, 0, 2, True)
    posicionar_navio(tab, "Submarino", 5, 5, 3, False)
    assert frota_destruida(tab) is False
    assert navios_restantes(tab) == 2

    for linha, coluna in [(0, 0), (0, 1), (5, 5), (6, 5), (7, 5)]:
        atirar(tab, linha, coluna)

    assert navios_restantes(tab) == 0
    assert frota_destruida(tab) is True


def test_cpu_nunca_repete_tiro():
    """Em 100 tiros a CPU deve cobrir as 100 casas sem repetir nenhuma."""
    tab = criar_tabuleiro()
    gerador = random.Random(7)
    for _ in range(100):
        casa = escolher_tiro_cpu(tab, gerador)
        resultado, _ = atirar(tab, casa[0], casa[1])
        assert resultado != "repetido"
    assert casas_sem_tiro(tab) == []
    assert escolher_tiro_cpu(tab, gerador) is None
