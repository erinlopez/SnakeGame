import pygame
from pygame.locals import *
import sys
import random
 
pygame.init()

#create screen
width = 500
height = 400
 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
 
speed = pygame.time.Clock()

#colors
green = (165, 225, 199)
darkgreen = (56, 104, 83)
brightgreen = (20, 150, 54)
blue = (0, 0, 255)
black = (0, 0, 0)

#text fonts
bigfont = pygame.font.SysFont('bookantiqua', 60)
smallfont = pygame.font.SysFont('bookantiqua', 30)
minifont = pygame.font.SysFont('bookantiqua', 25)

########################## screens
#welcome screen
def welcome():
    while welcome:
        screen.fill(green)
        title = bigfont.render('snake game', True, black)
        screen.blit(title, [125, 100])

        line = bigfont.render('~~~~~~~~~~', True, brightgreen)
        screen.blit(line, [125, 150])

        start = smallfont.render('press any key to begin', True, black)
        screen.blit(start, [135, 200])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                difficulty() #open difficulty screen
                welcome == False
        pygame.display.update()

#game mode screen
def difficulty():

    screen.fill(green) #erase welcome message

    while difficulty:
        dif = smallfont.render('choose difficulty...', True, black)
        screen.blit(dif, [50, 100])

        difoptions = smallfont.render('e: easy   m: medium   h: hard', True, black)
        screen.blit(difoptions, [100, 130])

        bonus = smallfont.render('bonus modes...', True, blue)
        screen.blit(bonus, [50, 180])

        bonusoptions = smallfont.render('i - invisible   r - speed roulette', True, blue)
        screen.blit(bonusoptions, [100, 210])

        bonusoptions = smallfont.render('p - poison  v - reverse  l - levels', True, blue)
        screen.blit(bonusoptions, [100, 240])

        instructions = minifont.render('q - instructions', True, black)
        screen.blit(instructions, [20, 20])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #start gameloop with chosen parameters
                if event.key == pygame.K_e:
                    gameloop(4) #slow
                if event.key == pygame.K_m:
                    gameloop(8) #medium
                if event.key == pygame.K_h:
                    gameloop(12) #fast  
                if event.key == pygame.K_i:
                    gameloop(10, 'invisible') #the food block becomes invisible to the player
                if event.key == pygame.K_r:
                    gamespeed = random.randint(2, 20)
                    gameloop(gamespeed, 'roulette') #the player speed changes every time they get the food block
                if event.key == pygame.K_p:
                    gameloop(8, 'poison') #a second poison circle block is added.  the player dies if they hit it
                if event.key == pygame.K_v:
                    gameloop(8, 'reverse') #snake starts long and you have to shorten it
                if event.key == pygame.K_l:
                    gameloop(5, 'levels')  
                if event.key == pygame.K_q:
                    instr()
            difficulty == False
        pygame.display.update()

#instructions screen
def instr():
    while instr:
        screen.fill(green)
        infotit = bigfont.render('information', True, black)
        screen.blit(infotit, [40, 40])

        inv = minifont.render('(i) invisible: hunt for invisible food blocks', True, black)
        screen.blit(inv, [40, 100])

        roul = minifont.render('(r) speed roulette: change speed each time you eat', True, black)
        screen.blit(roul, [40, 130])

        pois = minifont.render('(p) poison: square is food. circle is poison.', True, black)
        screen.blit(pois, [40, 160])

        rev = minifont.render('(v) reverse: start fully grown. eat to get smaller.', True, black)
        screen.blit(rev, [40, 190])

        lev = minifont.render('(l) levels: level up and get faster as you grow', True, black)
        screen.blit(lev, [40, 220])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                difficulty()
                instr == False
        pygame.display.update()

#you win screen
def win():
    while win:
        screen.fill(green)
        youwin = bigfont.render('YOU WIN :)', True, black)
        screen.blit(youwin, [width/4, height/3])
        
        playagain = smallfont.render('n - play again?', True, black)
        screen.blit(playagain, [width/4, height/2])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    difficulty()
                    win == False
        pygame.display.update()

#gameover screen
def gameover():
    while gameover:
        screen.fill(green)
        over = bigfont.render('game over :(', True, black) #message
        screen.blit(over, [125, height/3]) #put message on screen at coordinates
    
        restart = smallfont.render('n - new game     q - quit', True, black)
        screen.blit(restart, [135, height/2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    welcome() #restarts game at welcome screen
                    gameover == False
                if event.key == pygame.K_q:
                    quit()
                    gameover == False

######################### game functions
#scoreboard ftn
def score(snakelength):
    score = (snakelength - 1) * 10
    scoreboard = smallfont.render(f'score: {score}', True, black)
    screen.blit(scoreboard, [5, 5])

#quit ftn
def quit():
    pygame.quit() #close window
    sys.exit() #end script

#snake ftn
def snake(blocksize, snakelst, mode, snakelength):
    #draw snake
    for s in snakelst:
        pygame.draw.rect(screen, darkgreen, [s[0], s[1], blocksize, blocksize])
    #gameover if snake head hits body
    for s in snakelst[1:]:
        if mode == 'reverse' and snakelength > 49:
                pass
        elif snakelst[0][0] == s[0] and snakelst[0][1] == s[1]:
            gameover()

##################### main gameloop
def gameloop(gamespeed, mode=''): #take gamespeed and optional mode from difficulty()
    #snake position (x, y)
    snakepos = (250, 200)
    snakechange = (0,0)
    
    blocksize = 25
    
    snakelst = [] #list of snake coordinates
    
    #starting snake length
    snakelength = 1

    if mode == 'reverse':
        snakelength = 50

    #food position (x, y)
    foodpos = (random.randrange(0, 500, blocksize), random.randrange(0, 400, blocksize))
    
    #poison position - POISON MODE
    poisonpos = (600, 600)
    
    #random color generator
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rgb = (r, g, b)
        
    while True:    
        #move snake
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snakechange =  (-blocksize, 0)
                if event.key == pygame.K_RIGHT:
                    snakechange =  (blocksize, 0)
                if event.key == pygame.K_UP:
                    snakechange = (0, -blocksize)
                if event.key == pygame.K_DOWN:
                    snakechange = (0, blocksize)

        #change snake positions
        snakepos = ((snakepos[0]+snakechange[0]), (snakepos[1]+snakechange[1]))
        screen.fill(green)

        #gameover if hit boundary
        if snakepos > (width, height) or snakepos < (0,0):
            gameover()
        
        #when snake eats food
        if snakepos == foodpos:
            #food color
            if mode == 'invisible':
                rgb = green
            else:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb = (r, g, b)
            #change speed in roulette mode
            if mode == 'roulette':
                gamespeed = random.randint(2, 20)
            
            #poison mode
            if mode == 'poison':
                poisonpos = (random.randrange(0, 500, blocksize), random.randrange(0, 400, blocksize))

            #new foodpos
            foodpos = (random.randrange(0, 500, blocksize), random.randrange(0, 400, blocksize))
            
            snakelength += 1

            #reverse mode remove block
            if mode == 'reverse':
                snakelength = snakelength - 2
                screen.fill(green)
                snakelst = snakelst[2:]
                if snakelength == 1:
                    win()
            
            #levels mode increase speed every 5 blocks
            if mode == 'levels':
                if snakelength % 5 == 0:
                    gamespeed += 1

        #put blacks on screen
        #snake
        snake(blocksize, snakelst, mode, snakelength)
        #food
        pygame.draw.rect(screen, rgb, (foodpos[0], foodpos[1], blocksize, blocksize))
        #poison
        if mode == 'poison':
            pygame.draw.rect(screen, rgb, (poisonpos[0], poisonpos[1], blocksize, blocksize), border_radius = 10)
            if snakepos == poisonpos:
                gameover()
        
        #record snake position coordinates
        snakehead = []
        snakehead.append(snakepos[0])
        snakehead.append(snakepos[1])
        snakelst.append(snakehead)

        if len(snakelst) > snakelength:
            snakelst = snakelst[1:]

        #update scoreboard
        score(snakelength)

        speed.tick(gamespeed)
 
        pygame.display.update()

#start game
welcome()