import random
import time
from pygame import Rect
from pgzero.actor import Actor
from pgzero.clock import schedule
from pgzero.clock import clock
import pgzrun

WIDTH, HEIGHT = 800, 700
state = 'MENU'
sounds_habilitate = True 

TITLE = 'Hora de Aventura'
background = Actor('background.png')
player = Actor('hero_idle_right.png')
orc_enemy = Actor('orc_idle.png', anchor=('center', 'bottom'))

last_attack_time = time.time()
player.pos = (80, 800)
orc_enemy.pos = (500, 500)

button_start = Rect(300, 200, 200, 60) 
button_sound = Rect(300, 275, 200, 60)
button_restart = Rect(300, 350, 200, 60)
button_exit = Rect(300, 425, 200, 60)


player_dead= False 
orc_dead= False 
is_attacking = False 
orc_attack = False 
message = None

attackFrame = 0
playerDeathFrame = 0
OrcDeathFrame = 0
runFrame = 0
orcAttackFrame = 0
 
player_life = 100
orc_life = 100
player_damage = 10
orc_damage = 8
orcAttackCooldown = 5.0
walkSpeed = 5000

playerDirection = "right"
canOrcAttack = True
animationOff = True
orcDirection = "left"


playerIdle = {'right': ['hero_idle_right.png'],
              'left': ['hero_idle_left.png']}

playerRun = {'right': ['hero_run_right0.png', 'hero_run_right1.png', 'hero_run_right2.png', 'hero_run_right3.png', 'hero_run_right4.png', 'hero_run_right5.png'],
             'left': ['hero_run_left0.png', 'hero_run_left1.png', 'hero_run_left2.png', 'hero_run_left3.png', 'hero_run_left4.png', 'hero_run_left5.png']}

playerAttack = {'right': ['hero_attack_right0.png', 'hero_attack_right1.png', 'hero_attack_right2.png', 'hero_attack_right3.png'],
                'left': ['hero_attack_left0.png', 'hero_attack_left1.png', 'hero_attack_left2.png', 'hero_attack_left3.png']}

playerDeath = {'right': ['hero_die_right0.png', 'hero_die_right1.png', 'hero_die_right2.png', 'hero_die_right3', 'hero_die_right4', 'hero_die_right5']}

orcIdle = {'left': ['orc_idle.png']}

orcAttack = {'left': ['orc_attack0.png', 'orc_attack1.png', 'orc_attack2.png', 'orc_attack3.png']}

orcDeath = {'left': ['orc_dead0.png', 'orc_dead1.png', 'orc_dead2.png', 'orc_dead3.png']}

def update():
    global state
    clock.tick(60)#SE REMOVER MEU ORC NÃO COMPLETA A ANIMAÇÃO

    if state == 'MENU':
        return  

    elif state == 'PLAY':
        move_player()
        orc_guard_mode()
        
        if keyboard.ESCAPE:  
            state = 'MENU'
            sounds.background.stop()  

def toggle_sounds():
    global sounds_habilitate

    sounds_habilitate = not sounds_habilitate

    if sounds_habilitate:
        sounds.background.play(-1)  
    else:
        sounds.background.stop()  

def on_mouse_down(pos):
    global state, sounds_habilitate

    if state == 'MENU':  
        if button_start.collidepoint(pos):
            print("Botão 'Começar' pressionado!")  #verificar clique
            state = 'PLAY'  
            reset_game()  # Garante que o jogo inicia corretamente
            if sounds_habilitate:  
                sounds.background.play(-1)
                
        elif button_sound.collidepoint(pos):
            toggle_sounds()  
        elif button_restart.collidepoint(pos):  
            reset_game() 
        elif button_exit.collidepoint(pos):
            exit()  

def draw():
    screen.clear()

    button_color = (87, 59, 46) #marrom claro

    if state == 'MENU':
       screen.fill((33, 19, 13))  # Cor do fundo: marrom 
       screen.draw.text("Hora de Aventura", center=(WIDTH / 2, 100), fontsize=50, color="white")
       screen.draw.filled_rect(button_start, button_color)
       screen.draw.filled_rect(button_sound, button_color)
       screen.draw.filled_rect(button_restart, button_color)
       screen.draw.filled_rect(button_exit, button_color)

       screen.draw.text("JOGAR", center=button_start.center, fontsize=40, color="white")
       screen.draw.text("MÚSICA: " + ("ON" if sounds_habilitate else "OFF"), center=button_sound.center, fontsize=40, color="white")
       screen.draw.text("RECOMEÇAR", center=button_restart.center, fontsize=40, color="white")
       screen.draw.text("SAIR", center=button_exit.center, fontsize=40, color="white")

    elif state == 'PLAY':
        background.draw()
        orc_enemy.draw()
        player.draw()
        draw_life_bars()

    if message:
        screen.fill((33, 19, 13))
        screen.draw.text(message, center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="white")
        

def move_player():
    global playerDirection, is_attacking, runFrame

    if player_dead:
        return
    
     
    moving = False

    if keyboard.RIGHT and player.x < WIDTH:
        playerDirection = "right"
        if not is_attacking:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            clock.schedule_interval(lambda: move_player(), 3000)
        player.x += 5
        moving = True

    elif keyboard.LEFT and player.x > 0:
        playerDirection = "left"
        if not is_attacking:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            schedule(lambda: move_player(), 5000)
        player.x -= 5
        moving = True

    if not moving and not is_attacking:
        player.image = playerIdle[playerDirection][0]

    if keyboard.k and not is_attacking:
        attack = True
        animate_attack()

def animate_attack():
    global attackFrame, attack, orc_life, orc_dead, orcDeathFrame, last_attack_time
    
    current_time = time.time()  # Pega o tempo atual
    frame_duration = current_time - last_attack_time  # Calcula tempo desde último frame
    last_attack_time = current_time  # Atualiza o tempo do último frame

    print(f"Tempo entre frames (ataque): {frame_duration:.4f} segundos")  # Mostra na tela

    if orc_dead: 
        attack = False
        return

    if attackFrame == 0 and sounds_habilitate:
        sounds.attack_sound.play()

    if attackFrame < len(playerAttack[playerDirection]):
        player.image = playerAttack[playerDirection][attackFrame]
        attackFrame += 1
        clock.schedule_interval(animate_attack, 5000)
    else:
        attackFrame = 0
        attack = False
        player.image = playerIdle[playerDirection][0]

        if abs(player.x - orc_enemy.x) < 50 and not orc_dead:
            orc_life -= player_damage
            if sounds_habilitate:
                sounds.orc_hurt.play()
            if orc_life <= 0:
                orc_life = 0
                orc_dead = True
                orcDeathFrame = 0
                animate_orc_death()



def animate_player_death():
    global playerDeathFrame, player_dead, message

    if playerDeathFrame == 0 and sounds_habilitate:
        sounds.hero_die.play()

    if playerDeathFrame < len(playerDeath[playerDirection]):
        player.image = playerDeath[playerDirection][playerDeathFrame]
        playerDeathFrame += 1
        schedule(animate_player_death, 2000)
    else:
        message = "Game over!"
        screen.clear()
        schedule(return_to_menu, 4) 

def animate_orc_attack():
    global orcAttackFrame, orc_attack

    if orc_attack:  # Somente executa se o orc estiver atacando
        if orcAttackFrame < len(orcAttack[orcDirection]):
            orc_enemy.image = orcAttack[orcDirection][orcAttackFrame]
            orcAttackFrame += 1
        else:
            orcAttackFrame = 0
            orc_attack = False  # Finaliza o ataque
            orc_enemy.image = orcIdle[orcDirection][0]  # Volta para a animação de idle do orc

        # Continua animando o ataque
        schedule(animate_orc_attack, 2000)  # 2 seg de intervalo entre os frames da animação
    else:
        orc_enemy.image = orcIdle[orcDirection][0]  # Se não estiver atacando, fica em idle

     

def enable_orc_attack():
    global canOrcAttack
    canOrcAttack = True
    
def orc_guard_mode():
    global orcDirection, player_dead, player_life, orc_attack, canOrcAttack

    if orc_dead:
        return

    if abs(orc_enemy.x - player.x) < 50 and not player_dead:  # Se o jogador estiver perto
        if not orc_attack and canOrcAttack:
            orc_attack = True
            canOrcAttack = False
            animate_orc_attack()  # Chama a animação de ataque
            player_life -= orc_damage
            if sounds_habilitate:
                sounds.hero_die.play()
            if player_life <= 0:
                player_life = 0
                player_dead = True
                animate_player_death()  # Chama a animação de morte do jogador

            schedule(enable_orc_attack, orcAttackCooldown)  # Atraso entre ataques do orc
    else:
        orc_attack = False
        orc_enemy.image = orcIdle[orcDirection][0]  # Retorna à animação de idle do orc se não atacar
    
    
def animate_orc_death():
    global orcDeathFrame, orc_dead, message

    if orcDeathFrame == 0 and sounds_habilitate:
        orc_dead = True
        sounds.orc_die.play() 
        orc_enemy.image = orcDeath[orcDirection][0]

    if  0 <= orcDeathFrame < len(orcDeath[orcDirection]):
        orc_enemy.image = orcDeath[orcDirection][orcDeathFrame]
        orcDeathFrame += 1
        clock.schedule_unique(animate_orc_death, 2000)
    else:
        orc_enemy.image = orcDeath[orcDirection][-1]  
        message = "Victory!!"  
        show_victory_message()  
        
def show_victory_message():
    global message
    message = "Victory!!"
    print("Victory")
    clock.schedule_unique(return_to_menu, 5)

def return_to_menu():
    global message, state
    reset_game()
    state = 'MENU'
    message = None  

def draw_life_bars():
    max_player_life = 100
    max_orc_life = 100

    player_bar_width = (player_life / max_player_life) * 200
    orc_bar_width = (orc_life / max_orc_life) * 200

    screen.draw.filled_rect(Rect((10, 10), (player_bar_width, 20)), "blue")
    screen.draw.rect(Rect((10, 10), (200, 20)), "white")

    screen.draw.filled_rect(Rect((WIDTH - 210, 10), (orc_bar_width, 20)), "green")
    screen.draw.rect(Rect((WIDTH - 210, 10), (200, 20)), "white")

    screen.draw.text(f"Player: {player_life}/100", (10, 35), fontsize=20, color="white")
    screen.draw.text(f"Orc: {orc_life}/50", (WIDTH - 210, 35), fontsize=20, color="white")

def reset_game():
    global state, attack, attackFrame, player_life, orc_life, player_dead, orc_dead
    global  message, playerDeathFrame, orcDeathFrame, orcAttackFrame, orcWalkFrame
    
    if state == 'MENU':
        message = None 
        
    state = 'MENU'
    message = None  
    player.pos = (80, 485)
    orc_enemy.pos = (500, 500)

    player_life, orc_life = 100, 100
    player_dead, orc_dead, attack = False, False, False
    attackFrame = 0

    orc_enemy.pos = (700, 525)
    orc_life = 100
    orc_dead = False  
    orcDeathFrame, orcAttackFrame, orcWalkFrame = 0, 0, 0
    orcDirection = "left"
    orc_enemy.image = orcIdle[orcDirection][0]

    sounds.background.stop()

    state = 'PLAY'  
    if sounds_habilitate:
        sounds.background.play(-1) 
        
pgzrun.go()