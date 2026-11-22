from src.funcoes import (
    calcular_pontos,
    limitar_valor,
    pontos_do_tiro,
    pixel_para_casa,
    nome_da_casa,
    calcular_precisao,
    limpar_nome,
)


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_calcular_pontos_com_penalidade():
    """Deve permitir somar valores negativos (penalidade)."""
    assert calcular_pontos(10, -5) == 5


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


def test_pontos_acerto_e_afundar():
    """Acerto vale os pontos de acerto; afundar soma o bonus."""
    assert pontos_do_tiro("acerto", False, False, 10, 20, 5) == 10
    assert pontos_do_tiro("afundou", False, False, 10, 20, 5) == 30


def test_pontos_agua_sem_seguir_ia():
    """Errar sozinho nao tira pontos."""
    assert pontos_do_tiro("agua", False, False, 10, 20, 5) == 0


def test_penalidade_ao_seguir_ia_sem_verificar():
    """Seguir a IA sem verificar e cair na agua tira pontos (confianca cega)."""
    assert pontos_do_tiro("agua", True, False, 10, 20, 5) == -5


def test_sem_penalidade_se_ia_foi_verificada():
    """Se o jogador verificou a sugestao, nao ha penalidade."""
    assert pontos_do_tiro("agua", True, True, 10, 20, 5) == 0


def test_pixel_para_casa_dentro():
    """Clique dentro do tabuleiro deve virar (linha, coluna)."""
    # origem (100, 50), casas de 30 px: o pixel (165, 85) fica na coluna 2, linha 1
    assert pixel_para_casa(165, 85, (100, 50), 30, 10) == (1, 2)


def test_pixel_para_casa_fora():
    """Clique fora do tabuleiro deve retornar None."""
    assert pixel_para_casa(90, 85, (100, 50), 30, 10) is None
    assert pixel_para_casa(165, 40, (100, 50), 30, 10) is None
    assert pixel_para_casa(100 + 300, 60, (100, 50), 30, 10) is None


def test_nome_da_casa():
    """(0, 0) e A1; (9, 9) e J10."""
    assert nome_da_casa(0, 0) == "A1"
    assert nome_da_casa(9, 9) == "J10"


def test_calcular_precisao():
    """Precisao em porcentagem, sem dividir por zero."""
    assert calcular_precisao(0, 0) == 0
    assert calcular_precisao(1, 4) == 25


def test_limpar_nome():
    """Remove espacos e ';', corta no tamanho maximo e usa 'Jogador' se vazio."""
    assert limpar_nome("  Wyatt  ") == "Wyatt"
    assert limpar_nome("Ana;Maria") == "AnaMaria"
    assert limpar_nome("NomeMuitoGrandeDemais", 12) == "NomeMuitoGra"
    assert limpar_nome("   ") == "Jogador"
