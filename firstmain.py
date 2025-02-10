import random
from pygame import Rect
from pgzero.actor import Actor
from pgzero.clock import schedule
import pgzrun

# Dimensões da tela
WIDTH, HEIGHT = 900, 600
TITLE = 'Hora de Aventura'

# Classes de Personagens
class Character:
    def __init__(self, game, pos, idle_images, death_anim):
        self.game = game
        self.actor = Actor(idle_images["right"][0])
        self.actor.pos = pos
        self.idle = idle_images
        self.death_anim = death_anim
        self.direction = "right"
        self.is_dead = False

    def draw(self):
        self.actor.draw()

    def reset(self, pos):
        self.actor.pos = pos
        self.is_dead = False
        self.direction = 'right'
        self.actor.image = self.idle[self.direction][0]

class Player(Character):
    def __init__(self, game, pos):
        # Animações do herói
        self.idle = {
            'right': ['hero_idle_right.png'],
            'left':  ['hero_idle_left.png']
        }
        self.run = {
            'right': ['hero_run_right0.png', 'hero_run_right1.png', 'hero_run_right2.png',
                      'hero_run_right3.png', 'hero_run_right4.png', 'hero_run_right5.png'],
            'left':  ['hero_run_left0.png', 'hero_run_left1.png', 'hero_run_left2.png',
                      'hero_run_left3.png', 'hero_run_left4.png', 'hero_run_left5.png']
        }
        self.attack_anim = {
            'right': ['hero_attack_right0.png', 'hero_attack_right1.png', 'hero_attack_right2.png',
                      'hero_attack_right3.png'],
            'left':  ['hero_attack_left0.png', 'hero_attack_left1.png', 'hero_attack_left2.png',
                      'hero_attack_left3.png']
        }
        self.death_anim = {
            'right': ['hero_die_right0.png', 'hero_die_right1.png', 'hero_die_right2.png',
                      'hero_die_right3.png', 'hero_die_right4.png', 'hero_die_right5.png'],
            'left': ['hero_die_left0.png', 'hero_die_left1.png', 'hero_die_left2.png', 'hero_die_left3.png', 'hero_die_left4.png', 'hero_die_left5.png']
            }
        
        # Estados de animação e atributos
        self.run_frame = 0
        self.attack_frame = 0
        self.is_attacking = False
        self.walk_speed = 5
        self.damage = 8
        self.max_health = 100
        self.health = self.max_health

        super().__init__(game, pos, self.idle, self.death_anim)

    def update(self):
        if self.is_dead:
            return

        moving = False

        if keyboard.d and self.actor.right < self.game.WIDTH - self.game.margin:
            self.direction = "right"
            if not self.is_attacking:
                self.actor.image = self.run[self.direction][self.run_frame]
                self.run_frame = (self.run_frame + 1) % len(self.run[self.direction])
            self.actor.x += self.walk_speed
            moving = True

        elif keyboard.a and self.actor.x > self.game.margin:
            self.direction = "left"
            if not self.is_attacking:
                self.actor.image = self.run[self.direction][self.run_frame]
                self.run_frame = (self.run_frame + 1) % len(self.run[self.direction])
            self.actor.x -= self.walk_speed
            moving = True

        if not moving and not self.is_attacking:
            self.actor.image = self.idle[self.direction][0]

        if keyboard.k and not self.is_attacking:
            self.is_attacking = True
            self.animate_attack()

    def animate_attack(self):
        enemy = self.game.enemy
        if enemy.is_dead:
            self.is_attacking = False
            return
        if self.attack_frame == 0 and self.game.sounds_enabled and hasattr(sounds, 'attack_sound'):
            sounds.attack_sound.play()

        if self.attack_frame < len(self.attack_anim[self.direction]):
            self.actor.image = self.attack_anim[self.direction][self.attack_frame]
            self.attack_frame += 1
            schedule(self.animate_attack, 0.1)
        else:
            self.attack_frame = 0
            self.is_attacking = False
            self.actor.image = self.idle[self.direction][0]
            if abs(self.actor.right - enemy.actor.left) < 80:
                enemy.health -= self.damage
                if self.game.sounds_enabled and hasattr(sounds, 'orc_hurt'):
                    sounds.orc_hurt.play()
                if enemy.health <= 0:
                    enemy.health = 0
                    enemy.is_dead = True
                    enemy.death_frame = 0
                    enemy.animate_death()

    def animate_death(self):
        if not hasattr(self, 'death_frame'):
            self.death_frame = 0
        if self.death_frame == 0 and self.game.sounds_enabled and hasattr(sounds, 'hero_die'):
            sounds.hero_die.play()
        if self.death_frame < len(self.death_anim[self.direction]):
            self.actor.image = self.death_anim[self.direction][self.death_frame]
            self.death_frame += 1
            schedule(self.animate_death, 0.2)
        else:
            self.actor.image = self.death_anim[self.direction][-1]
            self.game.game_message = "You Lose!"
            schedule(self.game.return_to_menu, 2)

    def reset(self, pos):
        super().reset(pos)
        self.health = self.max_health
        self.is_attacking = False
        self.run_frame = 0
        self.attack_frame = 0

class Enemy(Character):
    def __init__(self, game, pos):
        # Animações do inimigo
        self.idle = {
            'right': ['orc_idle.png'],
            'left':  ['orc_idle.png']
        }
        self.attack_anim = {
            'right': ['orc_attack0.png', 'orc_attack1.png', 'orc_attack2.png', 'orc_attack3.png'],
            'left':  ['orc_attack0.png', 'orc_attack1.png', 'orc_attack2.png', 'orc_attack3.png']
        }
        self.death_anim = {
            'right': ['orc_dead0.png', 'orc_dead1.png', 'orc_dead2.png', 'orc_dead3.png'],
            'left':  ['orc_dead0.png', 'orc_dead1.png', 'orc_dead2.png', 'orc_dead3.png']
        }
        self.attack_frame = 0
        self.is_attacking = False
        self.can_attack = True
        self.damage = 5
        self.attack_cooldown = 1.0
        self.max_health = 50
        self.health = self.max_health

        super().__init__(game, pos, self.idle, self.death_anim)

    def update(self):
        if self.is_dead:
            return

        if self.game.player.actor.x < self.actor.x:
            self.direction = "left"
        else:
            self.direction = "right"

        # Se o herói estiver próximo, o inimigo ataca
        if abs(self.actor.left - self.game.player.actor.right) < 80 and not self.game.player.is_dead:
            if not self.is_attacking and self.can_attack:
                self.is_attacking = True
                self.can_attack = False
                self.animate_attack()
                self.game.player.health -= self.damage
                if self.game.sounds_enabled and hasattr(sounds, 'hero_hurt'):
                    sounds.hero_hurt.play()
                if self.game.player.health <= 0:
                    self.game.player.health = 0
                    self.game.player.is_dead = True
                    self.game.player.animate_death()
                schedule(self.reset_attack, self.attack_cooldown)
        else:
            self.actor.image = self.idle[self.direction][0]

    def animate_attack(self):
        if self.attack_frame < len(self.attack_anim[self.direction]):
            self.actor.image = self.attack_anim[self.direction][self.attack_frame]
            self.attack_frame += 1
            schedule(self.animate_attack, 0.15)
        else:
            self.attack_frame = 0
            self.is_attacking = False
            self.actor.image = self.idle[self.direction][0]

    def animate_death(self):
        if not hasattr(self, 'death_frame'):
            self.death_frame = 0
        if self.death_frame == 0 and self.game.sounds_enabled and hasattr(sounds, 'orc_die'):
            sounds.orc_die.play()
        if self.death_frame < len(self.death_anim[self.direction]):
            self.actor.image = self.death_anim[self.direction][self.death_frame]
            self.death_frame += 1
            schedule(self.animate_death, 0.2)
        else:
            self.actor.image = self.death_anim[self.direction][-1]
            self.game.game_message = "You Win!"
            schedule(self.game.return_to_menu, 2)

    def reset_attack(self):
        self.can_attack = True

    def reset(self, pos):
        super().reset(pos)
        self.health = self.max_health
        self.is_attacking = False
        self.attack_frame = 0

# Classe Principal do Jogo
class Game:
    def __init__(self):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.margin = 50
        self.state = 'menu'
        self.sounds_enabled = True
        self.game_message = None
        self.vertical_offset = 200

        # Background único
        self.background = Actor('background.png')

        # Instancia o herói e o inimigo:
        self.player = Player(self, (self.margin, self.HEIGHT/2 + self.vertical_offset))
        self.enemy = Enemy(self, (self.WIDTH - self.margin, self.HEIGHT/2 + self.vertical_offset))

        # Botões do Menu Principal
        self.button_start   = Rect(350, 200, 200, 50)
        self.button_sound   = Rect(350, 275, 200, 50)
        self.button_exit    = Rect(350, 350, 200, 50)
        self.button_restart = Rect(350, 425, 200, 50)

    def update(self):
        if self.state == 'menu':
            return
        elif self.state == 'play':
            self.player.update()
            self.enemy.update()
            if keyboard.ESCAPE:
                self.state = 'menu'
                if hasattr(sounds, 'background'):
                    sounds.background.stop()

    def draw(self):
        screen.clear()
        if self.state == 'menu':
            screen.draw.text("Hora da aventura", center=(self.WIDTH/2, 100), fontsize=50, color="white")
            screen.draw.filled_rect(self.button_start, "gray")
            screen.draw.filled_rect(self.button_sound, "gray")
            screen.draw.filled_rect(self.button_exit, "gray")
            screen.draw.filled_rect(self.button_restart, "gray")
            screen.draw.text("start game", center=self.button_start.center, fontsize=30, color="white")
            screen.draw.text("sounds: " + ("ON" if self.sounds_enabled else "OFF"), center=self.button_sound.center, fontsize=30, color="white")
            screen.draw.text("exit", center=self.button_exit.center, fontsize=30, color="white")
            screen.draw.text("restart game", center=self.button_restart.center, fontsize=30, color="white")
        elif self.state == 'play':
            self.background.draw()
            self.player.draw()
            self.enemy.draw()
            self.draw_health_bars()

        if self.game_message:
            screen.fill((0, 0, 0))
            screen.draw.text(self.game_message, center=(self.WIDTH/2, self.HEIGHT/2), fontsize=50, color="white")

    def on_mouse_down(self, pos):
        if self.state == 'menu':
            if hasattr(sounds, 'background'):
                sounds.background.stop()
            if self.button_start.collidepoint(pos):
                self.state = 'play'
                if self.sounds_enabled and hasattr(sounds, 'background'):
                    sounds.background.play(-1)
            elif self.button_sound.collidepoint(pos):
                self.toggle_sounds()
            elif self.button_exit.collidepoint(pos):
                exit()
            elif self.button_restart.collidepoint(pos):
                self.reset_game()

    def toggle_sounds(self):
        self.sounds_enabled = not self.sounds_enabled
        if self.sounds_enabled:
            if hasattr(sounds, 'background'):
                sounds.background.play(-1)
        else:
            if hasattr(sounds, 'background'):
                sounds.background.stop()

    def draw_health_bars(self):
        max_player_health = self.player.max_health
        max_enemy_health  = self.enemy.max_health

        player_bar_width = (self.player.health / max_player_health) * 200
        enemy_bar_width  = (self.enemy.health  / max_enemy_health) * 200

        screen.draw.filled_rect(Rect((10, 10), (player_bar_width, 20)), "green")
        screen.draw.rect(Rect((10, 10), (200, 20)), "white")
        screen.draw.filled_rect(Rect((self.WIDTH - 210, 10), (enemy_bar_width, 20)), "red")
        screen.draw.rect(Rect((self.WIDTH - 210, 10), (200, 20)), "white")

        screen.draw.text(f"Player: {self.player.health}/100", (10, 35), fontsize=20, color="white")
        screen.draw.text(f"Enemy: {self.enemy.health}/50", (self.WIDTH - 210, 35), fontsize=20, color="white")

    def reset_game(self):
        self.state = 'menu'
        self.game_message = None
        self.player.reset((self.margin, self.HEIGHT/2 + self.vertical_offset))
        self.enemy.reset((self.WIDTH - self.margin, self.HEIGHT/2 + self.vertical_offset))
        if hasattr(sounds, 'background'):
            sounds.background.stop()
        self.state = 'play'
        if self.sounds_enabled and hasattr(sounds, 'background'):
            sounds.background.play(-1)


    def return_to_menu(self):
        self.reset_game()
        self.game_message = None


# Funções globais para o pgzrun
# Instância global do jogo
game = Game()

def update():
    game.update()

def draw():
    game.draw()

def on_mouse_down(pos):
    game.on_mouse_down(pos)

pgzrun.go()
