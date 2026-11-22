# Configurações centrais do jogo (tela, tabuleiro, regras, cores e caminhos de arquivos).

# --- Janela ---
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TITULO_JOGO = "Batalha Naval: Radar IA"

# --- Tabuleiro ---
TAMANHO_TABULEIRO = 10          # 10 x 10 casas
TAMANHO_CASA = 32               # tamanho de cada casa em pixels
ORIGEM_JOGADOR = (40, 110)      # canto superior esquerdo do tabuleiro do jogador
ORIGEM_CPU = (440, 110)         # canto superior esquerdo do tabuleiro da CPU
LETRAS = "ABCDEFGHIJ"

# Frota de cada jogador: lista de tuplas (nome, tamanho)
FROTA = [
    ("Porta-aviões", 5),
    ("Encouraçado", 4),
    ("Cruzador", 3),
    ("Submarino", 3),
    ("Destróier", 2),
]

# --- Regras do assistente de IA (tema: confiabilidade de sistemas inteligentes) ---
CHANCE_ACERTO_IA = 0.45         # probabilidade de a sugestão da IA estar correta
VERIFICACOES_POR_PARTIDA = 3    # quantas vezes o jogador pode usar o sonar para conferir a IA

# --- Pontuação ---
PONTOS_ACERTO = 10              # acertar uma casa de navio
PONTOS_AFUNDAR = 20             # bônus por afundar um navio
PENALIDADE_IA_ERRADA = 10       # seguir a sugestão da IA sem conferir e ela estar errada

# --- Tempo ---
ESPERA_CPU_MS = 700             # tempo (ms) que a CPU "pensa" antes de atirar

# --- Cores (R, G, B) ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
AZUL_MAR = (24, 64, 112)
AZUL_LINHA = (60, 110, 170)
AZUL_FUNDO = (12, 28, 52)
CINZA_NAVIO = (130, 140, 150)
VERMELHO = (220, 50, 50)
VERMELHO_ESCURO = (120, 20, 20)
AMARELO = (250, 210, 60)
VERDE = (70, 200, 110)
LARANJA = (245, 150, 50)

# --- Arquivos ---
CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"
