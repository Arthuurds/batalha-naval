"""Loop principal do jogo: eventos, atualização do estado e desenho na tela."""

import pygame

from src.config import (
    LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO,
    TAMANHO_TABULEIRO, TAMANHO_CASA, ORIGEM_JOGADOR, ORIGEM_CPU, LETRAS, FROTA,
    CHANCE_ACERTO_IA, VERIFICACOES_POR_PARTIDA,
    PONTOS_ACERTO, PONTOS_AFUNDAR, PENALIDADE_IA_ERRADA, ESPERA_CPU_MS,
    BRANCO, CINZA, AZUL_MAR, AZUL_LINHA, AZUL_FUNDO, CINZA_NAVIO,
    VERMELHO, VERMELHO_ESCURO, AMARELO, VERDE, LARANJA,
    CAMINHO_RECORDE,
)
from src.tabuleiro import (
    criar_tabuleiro, posicionar_frota_aleatoria, atirar, frota_destruida,
    navios_restantes, tem_navio, casa_de_navio_afundado,
)
from src.assistente import gerar_sugestao, verificar_sugestao
from src.cpu import escolher_tiro_cpu
from src.funcoes import (
    calcular_pontos, pontos_do_tiro, pixel_para_casa, nome_da_casa, calcular_precisao,
)
from src.dados import salvar_recorde, carregar_recorde


# ---------------------------------------------------------------------------
# Estado da partida
# ---------------------------------------------------------------------------

def novo_estado(recorde):
    """Cria o dicionário com todo o estado de uma nova partida."""
    tab_jogador = criar_tabuleiro()
    tab_cpu = criar_tabuleiro()
    posicionar_frota_aleatoria(tab_jogador, FROTA)
    posicionar_frota_aleatoria(tab_cpu, FROTA)

    estado = {
        "tab_jogador": tab_jogador,
        "tab_cpu": tab_cpu,
        "vez": "jogador",            # "jogador", "cpu" ou "fim"
        "resultado": None,           # "vitoria" ou "derrota" quando a partida acaba
        "momento_cpu": 0,            # instante (ms) em que a CPU vai atirar
        "sugestao": None,            # sugestão atual do Radar IA
        "verificacoes": VERIFICACOES_POR_PARTIDA,
        "casas_desmentidas": set(),  # casas que o sonar mostrou serem água
        "casas_confirmadas": set(),  # casas que o sonar mostrou terem navio
        "pontos": 0,
        "recorde": recorde,
        "novo_recorde": False,
        "mensagem": "Sua vez! Clique no tabuleiro inimigo para atirar.",
        "mensagem_cpu": "",
        "estatisticas": {
            "tiros": 0,
            "acertos": 0,
            "seguiu_ia": 0,       # tiros feitos na casa sugerida pela IA
            "ia_errou": 0,        # vezes em que seguiu a IA e era água
            "sonar_usado": 0,
        },
    }
    nova_sugestao(estado)
    return estado


def nova_sugestao(estado):
    """Pede ao Radar IA uma nova sugestão para o turno do jogador."""
    estado["sugestao"] = gerar_sugestao(estado["tab_cpu"], CHANCE_ACERTO_IA)


def encerrar_partida(estado, resultado):
    """Finaliza a partida e salva o recorde, se for o caso."""
    estado["vez"] = "fim"
    estado["resultado"] = resultado
    if estado["pontos"] > estado["recorde"]:
        estado["recorde"] = estado["pontos"]
        estado["novo_recorde"] = True
        salvar_recorde(CAMINHO_RECORDE, estado["recorde"])


# ---------------------------------------------------------------------------
# Jogadas
# ---------------------------------------------------------------------------

def jogada_do_jogador(estado, casa, agora):
    """Executa o tiro do jogador na casa (linha, coluna) do tabuleiro da CPU."""
    sugestao = estado["sugestao"]
    seguiu_ia = sugestao is not None and casa == sugestao["casa"]
    ia_verificada = seguiu_ia and sugestao["verificada"]

    resultado, nome_navio = atirar(estado["tab_cpu"], casa[0], casa[1])
    if resultado in ("repetido", "invalido"):
        estado["mensagem"] = "Você já atirou nessa casa. Escolha outra."
        return

    stats = estado["estatisticas"]
    stats["tiros"] += 1
    if seguiu_ia:
        stats["seguiu_ia"] += 1

    ganho = pontos_do_tiro(resultado, seguiu_ia, ia_verificada,
                           PONTOS_ACERTO, PONTOS_AFUNDAR, PENALIDADE_IA_ERRADA)
    estado["pontos"] = calcular_pontos(estado["pontos"], ganho)

    texto_casa = nome_da_casa(casa[0], casa[1], LETRAS)
    if resultado == "agua":
        if seguiu_ia:
            stats["ia_errou"] += 1
        if ganho < 0:
            estado["mensagem"] = f"{texto_casa}: água! Você confiou na IA sem verificar ({ganho} pontos)."
        else:
            estado["mensagem"] = f"{texto_casa}: água."
    elif resultado == "acerto":
        stats["acertos"] += 1
        estado["mensagem"] = f"{texto_casa}: acertou um navio! (+{ganho})"
    else:
        stats["acertos"] += 1
        estado["mensagem"] = f"{texto_casa}: você afundou o {nome_navio}! (+{ganho})"

    if frota_destruida(estado["tab_cpu"]):
        encerrar_partida(estado, "vitoria")
        return

    # Passa a vez para a CPU, que vai "pensar" um pouco antes de atirar.
    estado["vez"] = "cpu"
    estado["momento_cpu"] = agora + ESPERA_CPU_MS
    estado["sugestao"] = None


def jogada_da_cpu(estado):
    """Executa o tiro da CPU no tabuleiro do jogador."""
    casa = escolher_tiro_cpu(estado["tab_jogador"])
    if casa is None:
        return

    resultado, nome_navio = atirar(estado["tab_jogador"], casa[0], casa[1])
    texto_casa = nome_da_casa(casa[0], casa[1], LETRAS)

    if resultado == "agua":
        estado["mensagem_cpu"] = f"CPU atirou em {texto_casa}: água."
    elif resultado == "acerto":
        estado["mensagem_cpu"] = f"CPU atirou em {texto_casa}: acertou seu {nome_navio}!"
    else:
        estado["mensagem_cpu"] = f"CPU atirou em {texto_casa}: afundou seu {nome_navio}!"

    if frota_destruida(estado["tab_jogador"]):
        encerrar_partida(estado, "derrota")
        return

    estado["vez"] = "jogador"
    nova_sugestao(estado)


def usar_sonar(estado):
    """Confere a sugestão atual da IA usando uma verificação do sonar."""
    resultado, restantes = verificar_sugestao(estado["sugestao"], estado["verificacoes"])
    estado["verificacoes"] = restantes

    if resultado == "sem_sonar":
        estado["mensagem"] = "Sem sonar! Agora você decide sozinho se confia na IA."
    elif resultado == "ja_verificada":
        estado["mensagem"] = "Essa sugestão já foi verificada."
    elif resultado in ("confirmada", "desmentida"):
        estado["estatisticas"]["sonar_usado"] += 1
        casa = estado["sugestao"]["casa"]
        texto_casa = nome_da_casa(casa[0], casa[1], LETRAS)
        if resultado == "confirmada":
            estado["casas_confirmadas"].add(casa)
            estado["mensagem"] = f"Sonar: há um navio em {texto_casa}. A IA estava certa."
        else:
            estado["casas_desmentidas"].add(casa)
            estado["mensagem"] = f"Sonar: {texto_casa} é água. A IA errou, mesmo confiante!"


# ---------------------------------------------------------------------------
# Eventos e atualização
# ---------------------------------------------------------------------------

def processar_evento(estado, evento, agora):
    """Trata um evento do Pygame. Retorna False quando o jogo deve fechar."""
    if evento.type == pygame.QUIT:
        return False

    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
            return False

        if estado["vez"] == "fim" and evento.key == pygame.K_r:
            estado.clear()
            estado.update(novo_estado(carregar_recorde(CAMINHO_RECORDE)))
            return True

        if estado["vez"] == "jogador":
            if evento.key == pygame.K_SPACE and estado["sugestao"] is not None:
                jogada_do_jogador(estado, estado["sugestao"]["casa"], agora)
            elif evento.key == pygame.K_v:
                usar_sonar(estado)

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if estado["vez"] == "jogador":
            casa = pixel_para_casa(evento.pos[0], evento.pos[1], ORIGEM_CPU,
                                   TAMANHO_CASA, TAMANHO_TABULEIRO)
            if casa is not None:
                jogada_do_jogador(estado, casa, agora)

    return True


def atualizar(estado, agora):
    """Atualiza o que depende do tempo: a CPU atira depois da espera."""
    if estado["vez"] == "cpu" and agora >= estado["momento_cpu"]:
        jogada_da_cpu(estado)


# ---------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------

def carregar_fontes():
    """Cria as fontes usadas no jogo (fonte padrão do Pygame, sem arquivos externos)."""
    return {
        "titulo": pygame.font.Font(None, 40),
        "normal": pygame.font.Font(None, 24),
        "pequena": pygame.font.Font(None, 20),
        "grande": pygame.font.Font(None, 72),
    }


def escrever(tela, fonte, texto, cor, x, y, centralizado=False):
    """Desenha um texto na tela."""
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    if centralizado:
        retangulo.midtop = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(imagem, retangulo)


def retangulo_da_casa(origem, linha, coluna):
    """Retorna o pygame.Rect de uma casa do tabuleiro."""
    x = origem[0] + coluna * TAMANHO_CASA
    y = origem[1] + linha * TAMANHO_CASA
    return pygame.Rect(x, y, TAMANHO_CASA, TAMANHO_CASA)


def desenhar_coordenadas(tela, fontes, origem):
    """Desenha os números das colunas e as letras das linhas ao redor do tabuleiro."""
    for i in range(TAMANHO_TABULEIRO):
        x_centro = origem[0] + i * TAMANHO_CASA + TAMANHO_CASA // 2
        escrever(tela, fontes["pequena"], str(i + 1), CINZA, x_centro, origem[1] - 18, True)
        y = origem[1] + i * TAMANHO_CASA + 9
        escrever(tela, fontes["pequena"], LETRAS[i], CINZA, origem[0] - 18, y)


def desenhar_tabuleiro(tela, fontes, tabuleiro, origem, mostrar_navios, estado=None):
    """Desenha um tabuleiro. Os navios só aparecem se mostrar_navios for True.

    Quando estado é informado (tabuleiro da CPU), desenha também a sugestão da
    IA, as marcas do sonar e o destaque da casa sob o mouse.
    """
    desenhar_coordenadas(tela, fontes, origem)
    posicao_mouse = pygame.mouse.get_pos()

    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            ret = retangulo_da_casa(origem, linha, coluna)
            casa = (linha, coluna)
            navio_aqui = tem_navio(tabuleiro, linha, coluna)

            cor = AZUL_MAR
            if mostrar_navios and navio_aqui:
                cor = CINZA_NAVIO
            if casa in tabuleiro["tiros"] and navio_aqui:
                cor = VERMELHO_ESCURO if casa_de_navio_afundado(tabuleiro, linha, coluna) else VERMELHO
            pygame.draw.rect(tela, cor, ret)
            pygame.draw.rect(tela, AZUL_LINHA, ret, 1)

            if casa in tabuleiro["tiros"]:
                if navio_aqui:
                    # "X" sobre o acerto
                    pygame.draw.line(tela, BRANCO, ret.inflate(-12, -12).topleft, ret.inflate(-12, -12).bottomright, 2)
                    pygame.draw.line(tela, BRANCO, ret.inflate(-12, -12).topright, ret.inflate(-12, -12).bottomleft, 2)
                else:
                    # bolinha branca = tiro na água
                    pygame.draw.circle(tela, BRANCO, ret.center, 4)

            if estado is None:
                continue

            # Marcas do sonar (só no tabuleiro inimigo)
            if casa in estado["casas_desmentidas"] and casa not in tabuleiro["tiros"]:
                pygame.draw.circle(tela, CINZA, ret.center, 6, 1)
            if casa in estado["casas_confirmadas"] and casa not in tabuleiro["tiros"]:
                pygame.draw.rect(tela, LARANJA, ret.inflate(-4, -4), 3)

            # Destaque da casa sob o mouse na vez do jogador
            if estado["vez"] == "jogador" and ret.collidepoint(posicao_mouse):
                pygame.draw.rect(tela, BRANCO, ret, 2)

    # Sugestão do Radar IA
    if estado is not None and estado["sugestao"] is not None and estado["vez"] == "jogador":
        casa = estado["sugestao"]["casa"]
        ret = retangulo_da_casa(origem, casa[0], casa[1])
        pygame.draw.rect(tela, AMARELO, ret, 3)
        escrever(tela, fontes["normal"], "?", AMARELO, ret.centerx, ret.y + 8, True)


def desenhar_painel(tela, fontes, estado):
    """Desenha as informações da partida abaixo dos tabuleiros."""
    stats = estado["estatisticas"]
    y = 448

    # Coluna da esquerda: Radar IA e mensagens
    sugestao = estado["sugestao"]
    if estado["vez"] == "jogador" and sugestao is not None:
        casa = nome_da_casa(sugestao["casa"][0], sugestao["casa"][1], LETRAS)
        escrever(tela, fontes["normal"],
                 f"Radar IA sugere {casa} com {sugestao['confianca']}% de confiança",
                 AMARELO, 40, y)
        if sugestao["verificada"]:
            texto, cor = ("Sonar: CONFIRMADA", VERDE) if sugestao["correta"] else ("Sonar: DESMENTIDA", VERMELHO)
        else:
            texto, cor = "Sugestão não verificada", CINZA
        escrever(tela, fontes["pequena"], texto, cor, 40, y + 24)
    elif estado["vez"] == "cpu":
        escrever(tela, fontes["normal"], "Vez da CPU...", CINZA, 40, y)

    escrever(tela, fontes["pequena"], f"Sonar restante: {estado['verificacoes']}", LARANJA, 260, y + 24)
    escrever(tela, fontes["normal"], estado["mensagem"], BRANCO, 40, y + 50)
    escrever(tela, fontes["normal"], estado["mensagem_cpu"], CINZA, 40, y + 76)

    # Coluna da direita: desempenho
    precisao = calcular_precisao(stats["acertos"], stats["tiros"])
    x = 560
    escrever(tela, fontes["normal"], f"Pontos: {estado['pontos']}   Recorde: {estado['recorde']}", BRANCO, x, y)
    escrever(tela, fontes["pequena"], f"Tiros: {stats['tiros']}  Acertos: {stats['acertos']}  ({precisao}%)", CINZA, x, y + 24)

    # Controles
    escrever(tela, fontes["pequena"],
             "Clique: atirar   |   ESPAÇO: seguir a IA   |   V: verificar com sonar   |   ESC: sair",
             CINZA, LARGURA_TELA // 2, ALTURA_TELA - 26, True)


def desenhar_fim(tela, fontes, estado):
    """Desenha a tela de fim de partida com o resumo e a reflexão sobre o uso da IA."""
    cobertura = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
    cobertura.fill((0, 0, 0, 190))
    tela.blit(cobertura, (0, 0))

    stats = estado["estatisticas"]
    centro = LARGURA_TELA // 2

    if estado["resultado"] == "vitoria":
        escrever(tela, fontes["grande"], "VITÓRIA!", VERDE, centro, 120, True)
    else:
        escrever(tela, fontes["grande"], "DERROTA", VERMELHO, centro, 120, True)

    precisao = calcular_precisao(stats["acertos"], stats["tiros"])
    linhas = [
        f"Pontos: {estado['pontos']}" + ("   (novo recorde!)" if estado["novo_recorde"] else ""),
        f"Tiros: {stats['tiros']}   Acertos: {stats['acertos']}   Precisão: {precisao}%",
        f"Você seguiu a IA {stats['seguiu_ia']} vezes e ela errou {stats['ia_errou']} delas.",
        f"Sonar usado: {stats['sonar_usado']} de {VERIFICACOES_POR_PARTIDA}.",
    ]
    y = 210
    for linha in linhas:
        escrever(tela, fontes["normal"], linha, BRANCO, centro, y, True)
        y += 32

    escrever(tela, fontes["normal"],
             "Lembre-se: confiança alta não garante resposta certa. Verifique!",
             AMARELO, centro, y + 20, True)
    escrever(tela, fontes["normal"], "R: jogar de novo    ESC: sair", CINZA, centro, y + 70, True)


def desenhar(tela, fontes, estado):
    """Desenha a cena completa."""
    tela.fill(AZUL_FUNDO)
    escrever(tela, fontes["titulo"], "BATALHA NAVAL: RADAR IA", BRANCO, LARGURA_TELA // 2, 14, True)

    escrever(tela, fontes["normal"],
             f"Sua frota  (navios: {navios_restantes(estado['tab_jogador'])})",
             BRANCO, ORIGEM_JOGADOR[0], 58)
    escrever(tela, fontes["normal"],
             f"Frota inimiga  (navios: {navios_restantes(estado['tab_cpu'])})",
             BRANCO, ORIGEM_CPU[0], 58)

    desenhar_tabuleiro(tela, fontes, estado["tab_jogador"], ORIGEM_JOGADOR, True)
    desenhar_tabuleiro(tela, fontes, estado["tab_cpu"], ORIGEM_CPU, False, estado)
    desenhar_painel(tela, fontes, estado)

    if estado["vez"] == "fim":
        desenhar_fim(tela, fontes, estado)


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()
    fontes = carregar_fontes()

    estado = novo_estado(carregar_recorde(CAMINHO_RECORDE))
    rodando = True

    # Loop principal: processa entrada, atualiza estado e desenha a cena.
    while rodando:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if not processar_evento(estado, evento, agora):
                rodando = False

        atualizar(estado, agora)

        # Informações também na barra de título da janela
        pygame.display.set_caption(
            f"{TITULO_JOGO} | Pontos: {estado['pontos']} | Recorde: {estado['recorde']}"
        )

        desenhar(tela, fontes, estado)
        pygame.display.flip()

    pygame.quit()
