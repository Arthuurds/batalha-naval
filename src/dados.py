"""Leitura e gravação de dados do jogo em arquivos de texto (recorde e ranking)."""


def salvar_recorde(caminho_arquivo, pontuacao):
    """Salva a pontuação recorde em arquivo texto."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(pontuacao))


def carregar_recorde(caminho_arquivo):
    """Carrega o recorde salvo; retorna 0 se não existir valor válido."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

            if conteudo == "":
                return 0

            return int(conteudo)

    except (FileNotFoundError, ValueError):
        return 0


# ---------------------------------------------------------------------------
# Ranking
# Cada linha do arquivo tem o formato:  nome;pontos;precisao
# Exemplo:                              Wyatt;130;47
# ---------------------------------------------------------------------------

def carregar_ranking(caminho_arquivo):
    """Lê o ranking do arquivo e retorna uma lista de dicionários.

    Cada item é {"nome": str, "pontos": int, "precisao": int}.
    Linhas vazias ou mal formatadas são ignoradas.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    ranking = []
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) != 3:
                    continue
                try:
                    ranking.append({
                        "nome": partes[0],
                        "pontos": int(partes[1]),
                        "precisao": int(partes[2]),
                    })
                except ValueError:
                    continue
    except FileNotFoundError:
        return []
    return ranking


def salvar_ranking(caminho_arquivo, ranking):
    """Grava o ranking no arquivo, uma linha por jogador."""
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        for item in ranking:
            arquivo.write(f"{item['nome']};{item['pontos']};{item['precisao']}\n")


def vem_antes(pontos_a, precisao_a, pontos_b, precisao_b):
    """Indica se o resultado A fica acima do B: mais pontos; em empate, maior precisão."""
    if pontos_a != pontos_b:
        return pontos_a > pontos_b
    return precisao_a > precisao_b


def entra_no_ranking(ranking, pontos, precisao, limite=5):
    """Indica se um resultado entra no ranking (precisa ter pontos positivos)."""
    if pontos <= 0:
        return False
    if len(ranking) < limite:
        return True
    ultimo = ranking[limite - 1]
    return vem_antes(pontos, precisao, ultimo["pontos"], ultimo["precisao"])


def inserir_no_ranking(ranking, nome, pontos, precisao, limite=5):
    """Retorna um NOVO ranking com o resultado inserido na posição certa.

    A lista fica ordenada do melhor para o pior e com no máximo `limite` itens.
    """
    novo_item = {"nome": nome, "pontos": pontos, "precisao": precisao}
    novo_ranking = []
    inserido = False

    for item in ranking:
        if not inserido and vem_antes(pontos, precisao, item["pontos"], item["precisao"]):
            novo_ranking.append(novo_item)
            inserido = True
        novo_ranking.append(item)

    if not inserido:
        novo_ranking.append(novo_item)

    return novo_ranking[:limite]
