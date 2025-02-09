import random
from pygame import Rect
from pgzero.actor import Actor
from pgzero.clock import schedule
import pgzrun

#Constantes do Jogo
WIDTH, HEIGHT = 900, 600
State = 'MENU'
sounds_habilitate = True 

#Elementos Visuais do Jogo
TITLE = 'Hora de Aventura'
background = Actor('battleground3.png')
floor = Actor('chao.png')
player = Actor('hero_idle_0.png')
orc_enemy = Actor('enemy_idle0.png', anchor=('center', 'bottom'))

floor.pos = (450, 550)
player.pos = (50, 440)
orc_enemy.pos = (800, 500)

#Menu principal
button_start = Rect(350, 200, 200, 50) 
button_sound = Rect(350, 275, 200, 50)
button_exit = Rect(350, 350, 200, 50)
button_restart = Rect(350, 425, 200, 50)

#Estados do Jogo

player_dead= False #jogador morto
orc_dead= False #monstro morto
jump = False #pular
player_attack = False #ataque do jogador
orc_attack = False #ataque do monstro
message = None

#Parâmetros de Animação e Mecânicas

attackFrame = 0
playerDeathFrame = 0
OrcDeathFrame = 0
runFrame = 0
orcWalkFrame = 0
orcAttackFrame = 0

#caractefisticas dos personagens 
player_life = 100
orc_life = 100
player_damage = 10
enemy_damage = 5
jumps = 2
orcAttackCooldown = 1.0
walkSpeed = 0.05

#Controle de Animação e Direções
playerDirection = "right"
canOrcAttack = True
animationOff = True
orcDirection = "left"

playerIdle = {'right': ['hero_idle_0.png', 'hero_idle_1.png', 'hero_idle_2.png', 'hero_idle_3.png', 'hero_idle_4.png', 'hero_idle_5.png'],
              'left': ['hero_idle_left0.png', 'hero_idle_left1.png', 'hero_idle_left2.png', 'hero_idle_left3.png', 'hero_idle_left4.png', 'hero_idle_left5.png']}

playerRun = {'right': ['hero_run_0.png', 'hero_run_1.png', 'hero_run_2.png', 'hero_run_3.png', 'hero_run_4.png', 'hero_run_5.png', 'hero_run_6.png', 'hero_run_7.png'],
             'left': ['hero_run_left0.png', 'hero_run_left1.png', 'hero_run_left2.png', 'hero_run_left3.png', 'hero_run_left4.png', 'hero_run_left5.png', 'hero_run_left6.png', 'hero_run_left7.png']}

playerJump = {'right': ['hero_jump_0.png', 'hero_jump_1.png', 'hero_jump_2.png', 'hero_jump_3.png', 'hero_jump_4.png', 'hero_jump_5.png', 'hero_jump_6.png', 'hero_jump_7.png', 'hero_jump_8.png', 'hero_jump_9.png', 'hero_jump_10.png', 'hero_jump_11.png' ],
              'left': ['hero_jump_left0.png', 'hero_jump_left1.png', 'hero_jump_left2.png', 'hero_jump_left3.png', 'hero_jump_left4.png', 'hero_jump_left5.png', 'hero_jump_left6.png', 'hero_jump_left7.png', 'hero_jump_left8.png', 'hero_jump_left9.png', 'hero_jump_left10.png', 'hero_jump_left11.png']}

playerAttack = {'right': ['hero_attack_0.png', 'hero_attack_1.png', 'hero_attack_2.png', 'hero_attack_3.png', 'hero_attack_4.png', 'hero_attack_5.png'],
                'left': ['hero_attack_left0.png', 'hero_attack_left1.png', 'hero_attack_left2.png', 'hero_attack_left3.png', 'hero_attack_left4.png', 'hero_attack_left5.png']}

playerDeath = {'right': ['hero_die_0.png', 'hero_die_1.png', 'hero_die_2.png'],
                'left': ['hero_die_left0.png', 'hero_die_left1.png', 'hero_die_left2.png']}

enemyIdle = {'right': ['enemy_idle0.png', 'enemy_idle1.png', 'enemy_idle2.png', 'enemy_idle3.png', 'enemy_idle4.png'],
             'left': ['enemy_idle_left0.png', 'enemy_idle_left1.png', 'enemy_idle_left2.png', 'enemy_idle_left3.png', 'enemy_idle_left4.png']}

orcAttack = {'right': ['orc_attack0.png', 'orc_attack1.png', 'orc_attack2.png', 'orc_attack3.png', 'orc_attack4.png', 'orc_attack5.png', 'orc_attack6.png', 'orc_attack7.png', 'orc_attack8.png'],
               'left': ['orc_attack_left0.png', 'orc_attack_left1.png', 'orc_attack_left2.png', 'orc_attack_left3.png', 'orc_attack_left4.png', 'orc_attack_left5.png', 'orc_attack_left6.png', 'orc_attack_left7.png', 'orc_attack_left8.png']}

orcDeath = {'right': ['orc_die_0.png', 'orc_die_1.png', 'orc_die_2.png', 'orc_die_3.png'],
              'left': ['enemy_die_left0.png', 'enemy_die_left1.png', 'enemy_die_left2.png', 'enemy_die_left3.png']}

orcWalk = {'right': ['orc_walk_0.png', 'orc_walk_1.png', 'orc_walk_2.png', 'orc_walk_3.png', 'orc_walk_4.png', 'orc_walk_5.png'],
             'left': ['orc_walk_left0.png', 'orc_walk_left1.png', 'orc_walk_left2.png', 'orc_walk_left3.png', 'orc_walk_left4.png', 'orc_walk_left5.png']}

def update():
    global State

    if State == 'MENU':
        return  

    elif State == 'PLAY':
        move_player()
        enemy_follow_player()
        if keyboard.ESCAPE:  
            State = 'MENU'
            sounds.background_music.stop()  

def toggle_sounds():
    global sounds_habilitate

    sounds_habilitate = not sounds_habilitate

    if sounds_habilitate:
        sounds.background_music.play(-1)  
    else:
        sounds.background_music.stop()  

def on_mouse_down(pos):
    global State, sounds_habilitate

    if State == 'MENU':  
        sounds.background_music.stop()
        if button_start.collidepoint(pos):
            State = 'PLAY'  
            if sounds_habilitate:  
                sounds.background_music.play(-1)
        elif button_sound.collidepoint(pos):
            toggle_sounds()  
        elif button_exit.collidepoint(pos):
            exit()  
        elif button_restart.collidepoint(pos):  
            reset_game()  

def draw():
    screen.clear()

    if State == 'MENU':
        screen.draw.text("Hora de Aventura", center=(WIDTH / 2, 100), fontsize=50, color="white")
        screen.draw.filled_rect(button_start, "gray")
        screen.draw.filled_rect(button_sound, "gray")
        screen.draw.filled_rect(button_exit, "gray")
        screen.draw.filled_rect(button_restart, "gray")

        screen.draw.text("Começar a jogar", center=button_start.center, fontsize=30, color="white")
        screen.draw.text("Musica: " + ("ON" if sounds_habilitate else "OFF"), center=button_sound.center, fontsize=30, color="white")
        screen.draw.text("sair", center=button_exit.center, fontsize=30, color="white")
        screen.draw.text("Recomeçar", center=button_restart.center, fontsize=30, color="white")

    elif State == 'PLAY':
        background.draw()
        floor.draw()
        player.draw()
        orc_enemy.draw()
        draw_health_bars()

    if message:
        screen.fill((0, 0, 0))
        screen.draw.text(message, center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="white")
        return  

def move_player():
    global jump, jumps, playerDirection, player_attack, runFrame

    if player_dead:
        return


    runSpeed = 0.07  
    moving = False

    if keyboard.d and player.x < WIDTH:
        playerDirection = "right"
        if not attack:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            schedule(lambda: move_player(), runSpeed)
        player.x += 5
        moving = True

    elif keyboard.a and player.x > 0:
        playerDirection = "left"
        if not attack:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            schedule(lambda: move_player(), runSpeed)
        player.x -= 5
        moving = True

    if not moving and not attack and not jump:
        player.image = playerIdle[playerDirection][0]

    if keyboard.k and not attack:
        attack = True
        animate_attack()

    if keyboard.space and not jump:
        jump = True
        jumps -= 1
        if sounds_habilitate:
            sounds.herojump.play() 
        player.image = playerJump[playerDirection][random.randint(0, len(playerJump[playerDirection]) - 1)]
        player.y -= 100
        schedule(land_player, 0.5)

    if not player.colliderect(floor):
        player.y += 5
        jump = True
    else:
        jump= False
        jumps = 2

def animate_attack():
    global attackFrame, attack, orc_life, orc_dead, orcDeathFrame

    if orc_dead: 
        attack = False
        return

    if attackFrame == 0 and sounds_habilitate:
        sounds.heroattack.play()

    if attackFrame < len(player_attack[playerDirection]):
        player.image = player_attack[playerDirection][attackFrame]
        attackFrame += 1
        schedule(animate_attack, 0.05)
    else:
        attackFrame = 0
        attack = False
        player.image = playerIdle[playerDirection][0]

        if abs(player.x - orc_enemy.x) < 50 and not orc_dead:
            orc_life -= player_damage
            if sounds_habilitate:
                sounds.enemyhurt.play()
            if orc_life <= 0:
                orc_life = 0
                orc_dead = True
                orcDeathFrame = 0
                animate_enemy_death()

def land_player():
    global jump
    jump = False
    player.image = playerIdle[playerDirection][0]

def animate_player_death():
    global playerDeathFrame, player_dead, gameMessage

    if playerDeathFrame == 0 and sounds_habilitate:
        sounds.herodie.play()

    if playerDeathFrame < len(playerDeath[playerDirection]):
        player.image = playerDeath[playerDirection][playerDeathFrame]
        playerDeathFrame += 1
        schedule(animate_player_death, 0.12)
    else:
        gameMessage = "you lose!"
        screen.clear()
        schedule(return_to_menu, 2) 

def animate_enemy_attack():
    global orcAttackFrame, orc_attack

    if orcAttackFrame < len(orc_attack[enemyDirection]):
        orc_enemy.image = orc_attack[enemyDirection][orcAttackFrame]
        orcAttackFrame += 1
        schedule(animate_enemy_attack, 0.12)  
    else:
        orcAttackFrame = 0
        orc_attack = False 

        if abs(orc_enemy.x - player.x) > 50:  
            animate_enemy_walk()  
        else:
            orc_enemy.image = enemyIdle[enemyDirection][0] 

def enable_enemy_attack():
    global canEnemyAttack
    canEnemyAttack = True
def enemy_follow_player():
    global enemyDirection, player_dead, player_life, orc_attack, canEnemyAttack

    if orc_dead:
        return

    if abs(orc_enemy.x - player.x) < 50 and not player_dead:
        if not orc_attack and canEnemyAttack:
            orc_attack = True
            canEnemyAttack = False
            animate_enemy_attack()
            player_life -= enemy_damage
            if sounds_habilitate:
                sounds.herodie.play()
            if player_life <= 0:
                player_life = 0
                orc_dead = True
                animate_player_death()

            schedule(enable_enemy_attack, orcAttackCooldown)
    else:
        if orc_enemy.x < player.x:
            enemyDirection = "right"
            orc_enemy.x += 2
        elif orc_enemy.x > player.x:
            enemyDirection = "left"
            orc_enemy.x -= 2
        if not orc_attack and orcWalkFrame == 0:
            animate_enemy_walk()

    orc_enemy.y = floor.pos[1] - 50 

def animate_enemy_walk():
    global orcWalkFrame

    if orc_dead or orc_attack:
        return

    orc_enemy.image = enemyWalk[enemyDirection][enemyWalkFrame]
    enemyWalkFrame = (enemyWalkFrame + 1) % len(enemyWalk[enemyDirection])  
    schedule(animate_enemy_walk, 0.12)

def animate_enemy_death():
    global orcDeathFrame, orc_dead, message

    if orcDeathFrame == 0 and sounds_habilitate:
        orc_dead = True
        sounds.enemydie.play() 
        orc_enemy.image = enemyDeath[enemyDirection][0]

    if orcDeathFrame < len(enemyDeath[enemyDirection]):
        orc_enemy.image = enemyDeath[enemyDirection][orcDeathFrame]
        orcDeathFrame += 1
        schedule(animate_enemy_death, 0.5)
    else:
        orc_enemy.image = enemyDeath[enemyDirection][-1]  
        message = "you win!"  
        schedule(return_to_menu, 2)  

def return_to_menu():
    global message
    reset_game() 
    message = None  

def draw_health_bars():
    max_player_life = 100
    max_orc_life = 50

    player_bar_width = (player_life / max_player_life) * 200
    orc_bar_width = (orc_life / max_orc_life) * 200

    screen.draw.filled_rect(Rect((10, 10), (player_bar_width, 20)), "green")
    screen.draw.rect(Rect((10, 10), (200, 20)), "white")

    screen.draw.filled_rect(Rect((WIDTH - 210, 10), (orc_bar_width, 20)), "red")
    screen.draw.rect(Rect((WIDTH - 210, 10), (200, 20)), "white")

    screen.draw.text(f"Player: {player_life}/100", (10, 35), fontsize=20, color="white")
    screen.draw.text(f"Enemy: {orc_life}/50", (WIDTH - 210, 35), fontsize=20, color="white")

def reset_game():
    global State, jump, jumps, attack, attackFrame, player_life, orc_life, player_dead, orc_dead
    global  message, playerDeathFrame, orcDeathFrame, orcAttackFrame, orcWalkFrame
    
    State = 'MENU'
    message = None  
    player.pos = (50, 440)
    orc_enemy.pos = (800, 500)

    player_life, orc_life = 100,50
    player_dead, orc_dead, jump, attack = False, False, False, False
    attackFrame = 0

    orc_enemy.pos = (800, 500)
    orc_life = 50
    orc_dead = False  
    orcDeathFrame, orcAttackFrame, orcWalkFrame = 0, 0, 0
    enemyDirection = "left"
    orc_enemy.image = enemyIdle[enemyDirection][0]

    sounds.background_music.stop()

    State = 'PLAY'  
    if sounds_habilitate:
        sounds.background_music.play(-1) 

pgzrun.go()