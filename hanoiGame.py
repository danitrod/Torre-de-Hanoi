import pygame as pg
import sys
import random
from time import sleep

# por Daniel Rodrigues

# versão final: 3/12/2018

pg.init()

# Inicialização da tela.
size = [600, 600]
screen = pg.display.set_mode(size)
pg.display.set_caption('Torre de Hanoi')
screen.fill((0, 0, 0))
fonte = pg.font.SysFont('Times New Roman', 30)
text = fonte.render('Digite um número de peças de 1 a 7', True, (122, 122, 255))
screen.blit(text, ((size[0]//2) - (text.get_rect().width//2), (size[1]//2) - (text.get_rect().height//2)))
pg.display.flip()

# Loop para escolher o número de discos para o jogo
escolhido = False
while not escolhido:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key in range(49, 56):
                numDiscos = event.key - 48
                escolhido = True

# Cores
ceu = (100, 200, 255)
clarezaNuvens = random.randrange(200, 256)
corNuvem = (clarezaNuvens, clarezaNuvens, clarezaNuvens)
pino = (100, 50, 30)
ganhar = (150, 255, 150)
discos = [None] * numDiscos
for i in range(numDiscos):
    # Cores aleatórias para os discos.
    if i == 0:
        discos[i] = (random.randrange(0,126), random.randrange(0,126), random.randrange(0,126))
    discos[i] = (random.randrange(0,256), random.randrange(0,256), random.randrange(0,180))

# Váriaveis
posicoesDiscos = [0] * numDiscos
clock = pg.time.Clock()
jogando = True
fonteMovimentos = pg.font.SysFont('Times New Roman', 20)
numMovimentos = 0

# Gerar nuvens aleatórias
numNuvens = random.randrange(3,9)
nuvens = []
for i in range(numNuvens):
    yNuvem = random.randrange(0, size[1]//6)
    xNuvem = random.randrange(0, size[0]-100)
    tamNuvem = random.randrange(2,5)
    nuvens.append((xNuvem, yNuvem, tamNuvem))
        
# Funções
def printMenu():
    # Printa o menu no início do jogo.
    text = fonte.render('Bem vindo/a!', True, discos[0])
    screen.blit(text, (size[0]//2-(text.get_rect().width//2),size[1]//5-(text.get_rect().height//2)))
    text = fonte.render('Jogar ou assistir a resolução?', True, discos[0])
    screen.blit(text, (size[0]//2-(text.get_rect().width//2),size[1]//3-(text.get_rect().height//2)))
    text = fonte.render('Jogar', True, discos[0])
    opcao1 = pg.draw.rect(screen, discos[0], ((size[0]//4) - ((text.get_rect().width//2)+10), (size[1]//2) - ((text.get_rect().height//2)+10), \
                                         text.get_rect().width + 20, text.get_rect().height + 20), 5)
    screen.blit(text, ((size[0]//4) - (text.get_rect().width//2), (size[1]//2) - (text.get_rect().height//2)))
    text = fonte.render('Assistir', True, discos[0])
    opcao2 = pg.draw.rect(screen, discos[0], ((3*(size[0]//4)) - ((text.get_rect().width//2)+10), (size[1]//2) - ((text.get_rect().height//2)+10), \
                                         text.get_rect().width + 20, text.get_rect().height + 20), 5)
    screen.blit(text, ((3*(size[0]//4)) - (text.get_rect().width//2), (size[1]//2) - (text.get_rect().height//2)))
    pg.display.update()
    return opcao1, opcao2
       
def printFundo():
    # Printa o cenário.

    # Céu
    screen.fill(ceu)
    for i in range(len(nuvens)):
        for n in range(nuvens[i][2]):
            pg.draw.circle(screen, corNuvem, (nuvens[i][0] + (n*30), nuvens[i][1]), 30)

    # Pinos
    xPino = (size[0]//4) - 5
    yPino = (size[1]-10) - (size[1]//6)
    yBase = size[1]-15
    for i in range(3):
        pg.draw.rect(screen, pino, (xPino, yPino, 10, size[1]//6))
        pg.draw.rect(screen, pino, (xPino-15, yBase, 40, 5))
        xPino += size[0]//4

    pg.display.update()

def printDiscos(posicoesDiscos):
    # Printa os discos nas posições desejadas.
    
    global numDiscos
    for i in range(numDiscos):
        tamDisco = (size[0]//8) - (8*i)
        if posicoesDiscos[i] == -1:
            xDisco = (size[0]//2) - (tamDisco//2)
            yDisco = (size[1]//2) - 7
        else: 
            xDisco = ((size[0]//4) - (tamDisco//2)) + (posicoesDiscos[i]*(size[0]//4))
            cont = 0
            for posAnteriores in range(0, i):
                if posicoesDiscos[posAnteriores] == posicoesDiscos[i]:
                    cont += 1
            yDisco = (size[1] - 30) - (cont * 15)
        pg.draw.rect(screen, discos[i], (xDisco, yDisco, tamDisco, 15))
    pg.display.update()

def printMovimentos(mov):
    # Printa o número de movimentos atual na tela.
    text = fonteMovimentos.render(('Movimentos: %d'%mov), True, (155, 0, 0))
    screen.blit(text, (size[0]-(text.get_rect().width), size[1]-text.get_rect().height))
    pg.display.update()

def buscarPinoClicado():
    # Busca o pino em que o mouse clicou.
    posMouse = pg.mouse.get_pos()
    if posMouse[1] in range(size[1] - ((size[1]//6) + 10), size[1] - 10):
        for x in range(1,4):
            if posMouse[0] in range((x*(size[0]//4)) - (size[0]//16), (x*(size[0]//4) + (size[0]//16))):
                return x

def buscarOpcaoClicada(jogar, assistir):
    # Busca a opção no menu clicada.
    posMouse = pg.mouse.get_pos()
    if posMouse[1] in range((size[1]//2)-(jogar.height//2), (size[1]//2)+(jogar.height//2)):
        if posMouse[0] in range((size[0]//4) - (jogar.width//2), (size[0]//4)+(jogar.width//2)):
            return 1
        elif posMouse[0] in range((3*(size[0]//4)) - (assistir.width//2), (3*(size[0]//4))+(assistir.width//2)):
            return 2

        
def ganhou(movimentos):
    # Printa as mensagens de fim de jogo.
    text = fonte.render('Parabéns! :)', True, ganhar)
    screen.blit(text, (size[0]//2-(text.get_rect().width//2), size[1]//2-(text.get_rect().height//2)))
    pg.display.update()
    
    if movimentos == movimentosHanoi(numDiscos):
        # Se o jogo foi resolvido com o número mínimo de movimentos, printa um "perfeito".
        string = "P E R F E I T O !"
        tmp = fonte.render(string, True, ceu) # Variável penas para pegar o tamanho da string na fonte
        posX = (size[0]//2) - (tmp.get_rect().width//2)
        string = string.split()
        for i in range(len(string)):
            pg.event.pump()
            pg.time.wait(250)
            text = fonte.render(string[i] + ' ', True, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 180)))
            screen.blit(text, (posX, 2*(size[1]//3)))
            posX += text.get_rect().width
            pg.display.update()
            
    return False

def hanoi(discos, origem, destino, aux):
    # Resolve o jogo em passos.
    if discos == 1:
        posicoesDiscos[numDiscos-discos] = destino
        yield posicoesDiscos

    else:
        yield from hanoi(discos-1, origem, aux, destino)
        
        posicoesDiscos[numDiscos-discos] = destino
        yield posicoesDiscos
        
        yield from hanoi(discos-1, aux, destino, origem)

def movimentosHanoi(n):
    # Retorna o mínimo número de movimentos necessário para um jogo com n discos
    if n == 1:
        return 1
    else:
        return (2*movimentosHanoi(n-1))+1

# Loop do menu
printFundo()
printDiscos(posicoesDiscos)
op1, op2 = printMenu()
menu = True
while menu:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            modo = buscarOpcaoClicada(op1, op2)
            if modo != None:
                menu = False

printFundo()
printDiscos(posicoesDiscos)
printMovimentos(numMovimentos)

if modo == 1:
    # Loop do jogo
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and jogando:
                pinoClicado = buscarPinoClicado()
                if pinoClicado != None:
                    if -1 not in posicoesDiscos:       
                            for i in range(numDiscos-1, -1, -1):
                                if posicoesDiscos[i] == pinoClicado-1:
                                    posicoesDiscos[i] = -1
                                    discoSuspenso = i
                                    break
                    else:
                        temMenor = False
                        for i in range(numDiscos-1, discoSuspenso, -1):
                            if posicoesDiscos[i] == pinoClicado-1:
                                # Não coloca um disco na posição se houver um disco menor nela.
                                temMenor = True
                                break
                        if not temMenor:
                            posicoesDiscos[discoSuspenso] = pinoClicado-1
                            numMovimentos += 1
                printFundo()
                printDiscos(posicoesDiscos)
                printMovimentos(numMovimentos)
                if 0 not in posicoesDiscos and 1 not in posicoesDiscos and -1 not in posicoesDiscos:
                    jogando = ganhou(numMovimentos)

else:
    # Loop da demonstração
    movimentos = hanoi(numDiscos, 0, 2, 1)
    rodando = True
    ticks = pg.time.get_ticks()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
        if rodando:
            if pg.time.get_ticks() - ticks >= 1000:
                posicoesAtuais = next(movimentos)
                numMovimentos += 1
                printFundo()
                printDiscos(posicoesAtuais)
                printMovimentos(numMovimentos)
                pg.display.update()
                if posicoesAtuais == [2] * numDiscos:
                    rodando = False
                ticks = pg.time.get_ticks()

    
