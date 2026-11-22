from src.dados import (
    salvar_recorde,
    carregar_recorde,
    carregar_ranking,
    salvar_ranking,
    entra_no_ranking,
    inserir_no_ranking,
)


def test_recorde_salva_e_carrega(tmp_path):
    """O recorde gravado deve ser lido de volta."""
    caminho = tmp_path / "recorde.txt"
    salvar_recorde(caminho, 120)
    assert carregar_recorde(caminho) == 120


def test_recorde_arquivo_inexistente_ou_invalido(tmp_path):
    """Sem arquivo ou com conteudo invalido, o recorde e 0."""
    assert carregar_recorde(tmp_path / "nao_existe.txt") == 0
    caminho = tmp_path / "recorde.txt"
    caminho.write_text("abc", encoding="utf-8")
    assert carregar_recorde(caminho) == 0


def test_ranking_arquivo_inexistente(tmp_path):
    """Sem arquivo, o ranking comeca vazio."""
    assert carregar_ranking(tmp_path / "nao_existe.txt") == []


def test_ranking_salva_e_carrega(tmp_path):
    """O ranking gravado deve ser lido igual."""
    caminho = tmp_path / "ranking.txt"
    ranking = [
        {"nome": "Arthur", "pontos": 150, "precisao": 50},
        {"nome": "Diego", "pontos": 90, "precisao": 40},
    ]
    salvar_ranking(caminho, ranking)
    assert carregar_ranking(caminho) == ranking


def test_ranking_ignora_linhas_invalidas(tmp_path):
    """Linhas vazias ou mal formatadas nao quebram a leitura."""
    caminho = tmp_path / "ranking.txt"
    caminho.write_text("Wyatt;130;47\n\nlinha errada\nAna;abc;10\nDiego;90;40\n", encoding="utf-8")
    assert carregar_ranking(caminho) == [
        {"nome": "Wyatt", "pontos": 130, "precisao": 47},
        {"nome": "Diego", "pontos": 90, "precisao": 40},
    ]


def test_inserir_mantem_ordem():
    """O novo resultado entra na posicao certa (mais pontos primeiro)."""
    ranking = [
        {"nome": "A", "pontos": 200, "precisao": 60},
        {"nome": "B", "pontos": 100, "precisao": 40},
    ]
    novo = inserir_no_ranking(ranking, "C", 150, 50)
    assert [item["nome"] for item in novo] == ["A", "C", "B"]


def test_inserir_desempata_pela_precisao():
    """Com os mesmos pontos, fica na frente quem teve maior precisao."""
    ranking = [{"nome": "A", "pontos": 100, "precisao": 40}]
    novo = inserir_no_ranking(ranking, "B", 100, 55)
    assert [item["nome"] for item in novo] == ["B", "A"]


def test_inserir_respeita_limite():
    """O ranking nunca passa do limite; o pior resultado sai."""
    ranking = []
    for pontos in [50, 40, 30, 20, 10]:
        ranking = inserir_no_ranking(ranking, f"J{pontos}", pontos, 0, limite=5)
    ranking = inserir_no_ranking(ranking, "Novo", 35, 0, limite=5)
    assert len(ranking) == 5
    assert [item["pontos"] for item in ranking] == [50, 40, 35, 30, 20]


def test_entra_no_ranking():
    """Entra se ha vaga ou se supera o ultimo; pontos zero ou negativos nao entram."""
    cheio = [{"nome": f"J{i}", "pontos": p, "precisao": 0} for i, p in enumerate([50, 40, 30, 20, 10])]
    assert entra_no_ranking([], 10, 0) is True
    assert entra_no_ranking([], 0, 0) is False
    assert entra_no_ranking(cheio, 15, 0) is True
    assert entra_no_ranking(cheio, 5, 0) is False
