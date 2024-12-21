import pygame,os
from pygame.locals import *

pygame.init()
# variaveis iniciais
largura, altura = 1000, 500
largura_chao,altura_chao = largura, (altura/4)*3
G = 300 # Gravidade
G_objeto = 300
tempo = pygame.time.Clock()
imagemLogo = pygame.image.load(os.path.join("./imagem/icon.png"))
sT = False
recorde = 0


# config inicio de pygame e tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo Massa")
pygame.display.set_icon(imagemLogo)

# variaveis do jogador
personagem_x, personagem_y = largura//2, altura
tamanho_x_personagem, tamanho_y_personagem = 30,50
personagem = pygame.draw.rect(tela,(255,0,0), (personagem_x,personagem_y,tamanho_x_personagem,tamanho_y_personagem))
jumping = False
altura_pulo = 20
jumpPlace = pygame.draw.rect(tela,(0,0,255), (0,0,0,0))
jumping_obj = False
altura_pulo_obj = 30
agachado = False
agachadoV = 25
level = 1

# variaveis objetos
tamanho_x_carro = 25
tamanho_y_carro = 25
carro_x, carro_y = largura, altura_chao-tamanho_y_carro
carro = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
carros = []

tamanho_x_aviao = 70
tamanho_y_aviao = 50
aviao_x, aviao_y = largura+100, altura_chao-tamanho_y_carro-tamanho_y_aviao
aviao = pygame.draw.rect(tela,(255,255,0), (aviao_x,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
avioes = []
pygame.time.Clock()

# fontes
pygame.font.init()
font_padrao = pygame.font.get_default_font()
font_menu = pygame.font.SysFont(font_padrao, 30)
font_menu_menor = pygame.font.SysFont(font_padrao, 15)
acabou = pygame.font.SysFont(font_padrao, 100)
# textos
piorar = font_menu.render('Voce achou que tava ruim?',1,(255,255,255))
piorar_rect = piorar.get_rect(center=(largura/2,altura/2-110))
vaiPiorar = acabou.render('VAI PIORAR',1,(255,0,0))
vaiPiorar_rect = vaiPiorar.get_rect(center=(largura/2,altura/2-70))

bomzinho = font_menu.render('VOCE ATE QUE AGUENTOU ATE',1,(255,255,255))
bomzinho_rect = bomzinho.get_rect(center=(largura/2,altura/2-110))

aqui = font_menu.render('AQUI',1,(255,0,0))
aqui_rect = aqui.get_rect(topleft=(bomzinho_rect.topright[0] + 5, bomzinho_rect.topright[1]))

aguenta = font_menu.render('VAMOS VER ATE AONDE VOCE AGUENTA',1,(255,255,255))
aguenta_rect = aguenta.get_rect(center=(largura/2,altura/2-90))
# tempo 
tempo_inicial = None
duracao = 5000


# sons
pygame.mixer.init()
som_pulo = pygame.mixer.Sound(os.path.join("./audio/jump.wav"))
som_pulo.set_volume(1)
som_morte = pygame.mixer.Sound(os.path.join("./audio/morte.wav"))
som_morte.set_volume(1)

pygame.mixer.music.load(os.path.join("./audio/trilha.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# dev configs
win = False
hack = False
run = False
alive = False
Start_Menu = True
menu_tryagain = False

# posicao centro
jogar=None
sair=None
while Start_Menu:
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Start_Menu = False
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if jogar_rect.collidepoint(pos):
                run = True
                alive = True
                Start_Menu = False
            if sair_rect.collidepoint(pos):
                run = False
                Start_Menu = False
                
    pos = pygame.mouse.get_pos()
    jogar = font_menu.render('JOGAR', 1,(255,0,0))
    jogar_rect = jogar.get_rect(center=(largura/2,altura/2))
    if jogar_rect.collidepoint(pos):
        jogar = font_menu.render('JOGAR', 1,(255,255,0))
    else:
        jogar = font_menu.render('JOGAR', 1,(255,0,0))
    sair = font_menu.render('SAIR', 1, (255,0,0))
    sair_rect = sair.get_rect(center=(largura/2,altura/2+20))

    if sair_rect.collidepoint(pos):
        sair = font_menu.render('SAIR', 1,(255,255,0))
    else:
        sair = font_menu.render('SAIR', 1,(255,0,0))
    tela.blit(jogar,jogar_rect)
    tela.blit(sair,sair_rect)
    
    pygame.display.update()


while run:
    if alive:
        agachadoV = tamanho_y_personagem/2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    alive = False
                    run = False
                if event.key == K_s:
                    tamanho_y_personagem = agachadoV
                    personagem_y += tamanho_y_personagem
                if event.key == K_w or event.key == K_SPACE:
                    if encostando_no_chao:
                        jumping = True
                        som_pulo.play()
            if event.type == KEYUP:
                if event.key == K_s:
                    personagem_y -= tamanho_y_personagem
                    tamanho_y_personagem = tamanho_y_personagem*2
        if personagem_y >= altura_chao-tamanho_y_personagem:
            encostando_no_chao = True
        else:
            encostando_no_chao = False
        # gravidade vertical
        T = tempo.get_time()/1000
        F = G * T
        personagem_y += F
        # gravidade horizontal
        F = G_objeto * T
        carro_x -= F
        aviao_x -= F
        
        # COLISAO
        if personagem_x >= largura-tamanho_x_personagem:
            personagem_x = largura-tamanho_x_personagem
        if personagem_y >= altura_chao-tamanho_y_personagem:
            personagem_y = altura_chao-tamanho_y_personagem
            tempo = pygame.time.Clock()
        if personagem_x <= 0:
            personagem_x = 0
        if personagem_y <= 0:
            personagem_y = 0

        for aviao in avioes:
            if personagem.colliderect(aviao):
                menu_tryagain = True
                alive = False
                som_morte.play()
        for carro in carros:
            if personagem.colliderect(carro):
                menu_tryagain = True
                alive = False
                som_morte.play()
        if jumping:
            personagem_y -= altura_pulo
            altura_pulo -= 1
            if altura_pulo < 0:
                jumping = False
                altura_pulo = 20

        keys = pygame.key.get_pressed()
        if keys[K_a]:
            personagem_x -= 10
        if keys[K_d]:
            personagem_x += 10

        tela.fill((255,255,255))
        # checar se passou level
        personagem = pygame.draw.rect(tela,(255,0,0), (personagem_x,personagem_y,tamanho_x_personagem,tamanho_y_personagem))
        if level == 1:
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+200,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+500,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+700,carro_y,tamanho_x_carro,tamanho_y_carro))
            carros = [carro1,carro2,carro3,carro4]
            if carro_x+700 <= 0-tamanho_x_carro:
                carro_x = largura
                aviao_x = largura
                level = 2
        elif level == 2:
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+170,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+340,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+700,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro5 = pygame.draw.rect(tela,(255,255,0), (carro_x+900,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+1200,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carros = [carro1,carro2,carro3,carro4,carro5]
            avioes = [aviao1]
            if aviao_x+1200 <=0-tamanho_x_aviao:
                carro_x=largura
                aviao_x=largura
                level = 3
        elif level == 3:
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+170,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+400,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+650,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao2 = pygame.draw.rect(tela,(255,255,0), (aviao_x+850,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carros = [carro1,carro2,carro3]
            avioes = [aviao1,aviao2]
            if aviao_x+850 <=0-tamanho_x_aviao:
                carro_x=largura
                aviao_x=largura
                level = 4
        elif level == 4:
            G_objeto = 450
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x+500,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+690,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+1200,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao2 = pygame.draw.rect(tela,(255,255,0), (aviao_x+1390,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+1800,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao3 = pygame.draw.rect(tela,(255,255,0), (aviao_x+2000,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+2400,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao4 = pygame.draw.rect(tela,(255,255,0), (aviao_x+2560,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carros = [carro1,carro2,carro3,carro4]
            avioes = [aviao1,aviao2,aviao3,aviao4]
            if aviao_x+2550 <=0-tamanho_x_aviao:
                carro_x=largura+100
                aviao_x=largura+100
                level = 5
        elif level == 5:
            G_objeto = 475
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x+500,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+700,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+1000,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+1200,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+1500,carro_y,tamanho_x_carro+20,tamanho_y_carro))
            carros = [carro1,carro2,carro3,carro4]
            avioes = [aviao1]
            if carro_x+1500<=0-tamanho_x_carro+20:
                carro_x=largura
                aviao_x=largura
                level = 6
        elif level == 6:
            G_objeto = 500
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+200,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            aviao2 = pygame.draw.rect(tela,(255,255,0), (aviao_x+210,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+500,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+520,carro_y,tamanho_x_carro,tamanho_y_carro))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+900,carro_y,tamanho_x_carro,tamanho_y_carro))
            aviao3 = pygame.draw.rect(tela,(255,255,0), (aviao_x+1120,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro5 = pygame.draw.rect(tela,(255,255,0), (carro_x+1420,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            carro6 = pygame.draw.rect(tela,(255,255,0), (carro_x+1820,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            carros = [carro1,carro2,carro3,carro4,carro5,carro6]
            avioes = [aviao1,aviao2,aviao3]
            if aviao_x+1820 <= 0-tamanho_x_aviao:
                carro_x = largura+3000
                aviao_x = largura+3000
                level = 7
        elif level == 7:
            tela.fill((0,0,0))
            personagem = pygame.draw.rect(tela,(255,0,0), (personagem_x,personagem_y,tamanho_x_personagem,tamanho_y_personagem))
            tempo_atual = pygame.time.get_ticks()
            if tempo_inicial is None:
                tempo_inicial = pygame.time.get_ticks()
            if tempo_atual - tempo_inicial < duracao:
                tela.blit(piorar, piorar_rect)
                tela.blit(vaiPiorar,vaiPiorar_rect)
            G_objeto = 650
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x-20,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+400,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+700,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+1100,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            carro4 = pygame.draw.rect(tela,(255,255,0), (carro_x+1450,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            aviao2 = pygame.draw.rect(tela,(255,255,0), (aviao_x+1700,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro5 = pygame.draw.rect(tela,(255,255,0), (carro_x+2100,carro_y-20,tamanho_x_carro+50,tamanho_y_carro+20))
            aviao3 = pygame.draw.rect(tela,(255,255,0), (aviao_x+2400,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro6 = pygame.draw.rect(tela,(255,255,0), (carro_x+2700,carro_y,tamanho_x_carro+70,tamanho_y_carro+20))
            carros = [carro1,carro2,carro3,carro4,carro5,carro6]
            avioes = [aviao1,aviao2,aviao3]
            if carro_x+5000 <= 0-tamanho_x_carro:
                carro_x = largura+5000
                aviao_x = largura+5000
                level = 8
                tempo_inicial = None
        elif level == 8:
            G_objeto = 700
            tela.fill((0,0,0))
            personagem = pygame.draw.rect(tela,(255,0,0), (personagem_x,personagem_y,tamanho_x_personagem,tamanho_y_personagem))
            tempo_atual = pygame.time.get_ticks()
            if tempo_inicial is None:
                tempo_inicial = pygame.time.get_ticks()
            if tempo_atual - tempo_inicial < duracao:
                tela.blit(bomzinho,bomzinho_rect)
                tela.blit(aqui,aqui_rect)
                tela.blit(aguenta,aguenta_rect)
            carro1 = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y-20,tamanho_x_carro+20,tamanho_y_carro+20))
            aviao1 = pygame.draw.rect(tela,(255,255,0), (aviao_x+200,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro2 = pygame.draw.rect(tela,(255,255,0), (carro_x+600,carro_y-20,tamanho_x_carro+70,tamanho_y_carro+20))
            aviao2 = pygame.draw.rect(tela,(255,255,0), (aviao_x+900,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
            carro3 = pygame.draw.rect(tela,(255,255,0), (carro_x+1300,carro_y-20,tamanho_x_carro+70+tamanho_x_carro+70,tamanho_y_carro+20))
            obstaculoAlto = pygame.draw.rect(tela,(255,255,0), (carro_x+2850,carro_y-100,tamanho_x_carro,tamanho_y_carro+100))
                    
            if carro_x+1300<0-tamanho_x_carro and not carro_x+2600<0-tamanho_x_carro:
                jumpPlace = pygame.draw.rect(tela,(0,0,255), (largura/2,altura_chao-20,50,20))
                if jumpPlace.colliderect(personagem):
                    jumping_obj = True
                if jumping_obj:
                    personagem_y -= altura_pulo_obj
                    altura_pulo_obj -= 1
                    if altura_pulo_obj <= 0:
                        jumping_obj = False
                        altura_pulo_obj = 30
            carros = [carro1,carro2,carro3,obstaculoAlto]
            avioes = [aviao1,aviao2]
            if carro_x+2850 <= 0-tamanho_x_carro:
                win = True
                alive = False
                menu_tryagain = False
        mostrarLevel = font_menu.render(f'Level: {level}',1,(0,0,0))
        if level>=7:
            mostrarLevel = font_menu.render(f'Level: {level}',1,(255,255,255))
        mostrarLevel_rect = mostrarLevel.get_rect(center=(50,50 ))
        tela.blit(mostrarLevel,mostrarLevel_rect)
        if sT:
            levelRecorde = font_menu.render(f"Level Recorde: {recorde}",1,(0,0,0))
            if level>=7:
                levelRecorde = font_menu.render(f"Level Recorde: {recorde}",1,(255,255,255))
            levelRecorde_rect = levelRecorde.get_rect(center=(80,70))
            tela.blit(levelRecorde,levelRecorde_rect)
        pygame.draw.rect(tela,(0,255,0), (0,altura_chao,largura_chao,altura_chao))
        if hack:
            encostando_no_chao == True
            personagem_x,personagem_y = 0,0
        pygame.display.update()
        tempo.tick(30)
    if menu_tryagain:
        sT = True
        tela.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_tryagain = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if tryAgain_rect.collidepoint(pos):
                    # variaveis iniciais
                    ultimo_level = level
                    if ultimo_level > recorde:
                        recorde = ultimo_level
                    largura, altura = 1000, 500
                    largura_chao,altura_chao = largura, (altura/4)*3
                    G = 300 # Gravidade
                    G_objeto = 300
                    tempo = pygame.time.Clock()
                    # variaveis do jogador
                    personagem_x, personagem_y = largura//2, altura
                    tamanho_x_personagem, tamanho_y_personagem = 30,50
                    personagem = pygame.draw.rect(tela,(255,0,0), (personagem_x,personagem_y,tamanho_x_personagem,tamanho_y_personagem))
                    jumping = False
                    altura_pulo = 20
                    agachado = False
                    agachadoV = tamanho_y_personagem/2
                    level = 1

                    # variaveis objetos
                    tamanho_x_carro = 25
                    tamanho_y_carro = 25
                    carro_x, carro_y = largura, altura_chao-tamanho_y_carro
                    carro = pygame.draw.rect(tela,(255,255,0), (carro_x,carro_y,tamanho_x_carro,tamanho_y_carro))
                    carros = []

                    tamanho_x_aviao = 70
                    tamanho_y_aviao = 50
                    aviao_x, aviao_y = largura+100, altura_chao-tamanho_y_carro-tamanho_y_aviao
                    aviao = pygame.draw.rect(tela,(255,255,0), (aviao_x,aviao_y,tamanho_x_aviao,tamanho_y_aviao))
                    avioes = []
                    pygame.time.Clock()

                    # outras variaveis necessarias
                    encostando_no_chao = True  # Resetar condição de estar no chão

                    level = 1
                    alive = True
                    menu_tryagain = False
                if sair_ta_rect.collidepoint(pos):
                    menu_tryagain = False
                    run = False
        ultimo_level = level
        if ultimo_level > recorde:
            recorde = ultimo_level
        pos = pygame.mouse.get_pos()
        tryAgain = font_menu.render('Tentar Novamente', 1, (255,0,0))
        tryAgain_rect = tryAgain.get_rect(center=(largura/2,altura/2))
        if tryAgain_rect.collidepoint(pos):
            tryAgain = font_menu.render('Tentar Novamente', 1, (255,255,0))
        else: 
            tryAgain = font_menu.render('Tentar Novamente', 1, (255,0,0))
        sair_ta = font_menu.render('Sair', 1, (255,0,0))
        sair_ta_rect = sair_ta.get_rect(center=(largura/2,altura/2+20))
        if sair_ta_rect.collidepoint(pos):
            sair_ta = font_menu.render('Sair', 1, (255,255,0))
        else:
            sair_ta = font_menu.render('Sair', 1, (255,0,0))
        tela.blit(tryAgain,tryAgain_rect)
        tela.blit(sair_ta,sair_ta_rect)
        fim = acabou.render('fim', 1, (255,255,255))
        fim_rect = fim.get_rect(center=(largura/2,altura/2-120))
        tela.blit(fim,fim_rect)
        # pontuacao
        pontuacaoAtual = font_menu.render(f'Pontuacao: {level}',1,(255,255,255))
        pontuacaoAtual_rect = pontuacaoAtual.get_rect(center=(largura/2,altura/2-90))
        pontuacaoRecorde = font_menu.render(f'Recorde: {recorde}',1,(255,255,255))
        pontuacaoRecorde_rect = pontuacaoRecorde.get_rect(center=(largura/2,altura/2-70))
        tela.blit(pontuacaoAtual,pontuacaoAtual_rect)
        tela.blit(pontuacaoRecorde,pontuacaoRecorde_rect)

        pygame.display.update()
    if win:
        tela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, KEYDOWN]:
                run = False
                win = False
        text = font_menu.render("Parabéns, você ganhou!", True, (0, 200, 0))
        text2 = font_menu_menor.render("Pressione qualquer botao para sair.", True, (255, 255, 255))
        text_rect = text.get_rect(center=(largura // 2, altura // 2))
        text2_rect = text.get_rect(center=(largura // 2, (altura // 2) + 20))
        tela.blit(text, text_rect)
        tela.blit(text2, text2_rect)
        pygame.display.update()
pygame.quit()

