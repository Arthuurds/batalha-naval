"""Funções auxiliares de regra e lógica (pontuação, limites e conversões)."""


def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def pontos_do_tiro(resultado, seguiu_ia, ia_verificada, pontos_acerto, pontos_afundar, penalidade_ia):
    """Calcula quantos pontos um tiro do jogador vale.

    - acerto: ganha pontos_acerto;
    - afundou: ganha pontos_acerto + pontos_afundar;
    - água: 0 ponto, mas se o jogador seguiu a IA SEM verificar, perde penalidade_ia
      (penaliza a confiança cega no sistema automatizado).
    """
    if resultado == "acerto":
        return pontos_acerto
    if resultado == "afundou":
        return pontos_acerto + pontos_afundar
    if resultado == "agua" and seguiu_ia and not ia_verificada:
        return -penalidade_ia
    return 0


def pixel_para_casa(x, y, origem, tamanho_casa, tamanho_tabuleiro):
    """Converte um clique (x, y) em pixels para (linha, coluna) do tabuleiro.

    origem é a tupla (x, y) do canto superior esquerdo do tabuleiro.
    Retorna None se o clique foi fora do tabuleiro.
    """
    coluna = (x - origem[0]) // tamanho_casa
    linha = (y - origem[1]) // tamanho_casa

    if x < origem[0] or y < origem[1]:
        return None
    if linha >= tamanho_tabuleiro or coluna >= tamanho_tabuleiro:
        return None
    return (linha, coluna)


def nome_da_casa(linha, coluna, letras="ABCDEFGHIJ"):
    """Converte (linha, coluna) para o formato do jogo, por exemplo (0, 0) -> "A1"."""
    return f"{letras[linha]}{coluna + 1}"


def calcular_precisao(acertos, tiros):
    """Retorna a precisão em porcentagem (inteiro). Sem tiros, a precisão é 0."""
    if tiros == 0:
        return 0
    return round(acertos * 100 / tiros)


def limpar_nome(texto, tamanho_maximo=12):
    """Prepara o nome digitado para o ranking.

    Remove espaços das pontas e o caractere ";" (usado como separador no arquivo),
    corta no tamanho máximo e usa "Jogador" se o nome ficar vazio.
    """
    nome = texto.replace(";", "").strip()
    nome = nome[:tamanho_maximo].strip()
    if nome == "":
        return "Jogador"
    return nome
