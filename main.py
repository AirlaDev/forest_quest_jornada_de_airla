# -*- coding: utf-8 -*-
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "A Jornada de Airla"

game_state = "menu" 
music_on = True

start_button = Rect((WIDTH/2 - 100, 220), (200, 50))
sound_button = Rect((WIDTH/2 - 100, 300), (200, 50))
exit_button = Rect((WIDTH/2 - 100, 380), (200, 50))

play_again_button = Rect((WIDTH/2 - 120, HEIGHT/2 + 70), (240, 50))
exit_button_endgame = Rect((WIDTH/2 - 120, HEIGHT/2 + 130), (240, 50))

class Airla:    
    def __init__(self):
        self.start_pos = (50, HEIGHT / 2)
        self.images_idle = ['airla_idle1']
        self.images_walk = ['airla_walk1', 'airla_walk2']
        self.actor = Actor(self.images_idle[0], self.start_pos)
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.target = self.actor.pos
        self.speed = 3

    def reset(self):        
        self.actor.pos = self.start_pos
        self.target = self.start_pos
        self.actor.image = self.images_idle[0]

    def update(self):
        self.animate()
        self.move_towards_target()

    def animate(self):
        is_moving = self.actor.pos != self.target
        current_images = self.images_walk if is_moving else self.images_idle
        
        if len(current_images) > 1:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % len(current_images)
                self.actor.image = current_images[self.frame]
        else:
            self.actor.image = current_images[0]

    def move_towards_target(self):
        if self.actor.distance_to(self.target) < self.speed:
            self.actor.pos = self.target
            return
        x, y = self.actor.pos
        tx, ty = self.target
        if x < tx: x += self.speed
        elif x > tx: x -= self.speed
        if y < ty: y += self.speed
        elif y > ty: y -= self.speed
        self.actor.pos = (x, y)

class Enemy:    
    def __init__(self, x, y, image_list):
        self.start_pos = (x, y)
        self.images = image_list
        self.actor = Actor(self.images[0], self.start_pos)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 15 

    def reset(self):        
        self.actor.pos = self.start_pos
        self.direction = random.choice([-1, 1])

    def update(self):        
        if len(self.images) > 1:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % len(self.images)
                self.actor.image = self.images[self.frame]
        self.actor.x += self.direction * self.speed
        if self.actor.right > WIDTH or self.actor.left < 0:
            self.direction *= -1

class Fred:    
    def __init__(self):
        self.image_waiting = 'fred_waiting'
        self.images_saved = ['fred_saved1', 'fred_saved2', 'fred_saved3', 'fred_saved4']
        self.actor = Actor(self.image_waiting, (WIDTH - 80, HEIGHT / 2))
        self.frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

    def reset(self):
        self.actor.image = self.image_waiting

    def update(self):
        if game_state == "win":
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.frame = (self.frame + 1) % len(self.images_saved)
                self.actor.image = self.images_saved[self.frame]

airla = Airla()
fred = Fred()

inimigo_galhos_imgs = ['inimigo_galhos']
inimigo_gosma_imgs = ['inimigo_gosma']
inimigo_foguete_imgs = ['inimigo_foguete1', 'inimigo_foguete2']
inimigo_red_imgs = ['inimigo_red1', 'inimigo_red2', 'inimigo_red3', 'inimigo_red4']

enemies = [
    Enemy(200, 100, inimigo_galhos_imgs),
    Enemy(600, 500, inimigo_galhos_imgs),
    Enemy(300, 450, inimigo_gosma_imgs),
    Enemy(700, 150, inimigo_gosma_imgs),
    Enemy(400, 80, inimigo_foguete_imgs),
    Enemy(500, 300, inimigo_red_imgs)
]

def reset_game():
    global game_state
    music.stop()
    airla.reset()
    fred.reset()
    for enemy in enemies:
        enemy.reset()
    game_state = "playing"
    if music_on:
        music.play('forest_theme')
        music.set_volume(0.3)

def draw():
    screen.clear()
    screen.blit('cenario', (0, 0))
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "win":
        draw_win_screen()

def draw_menu():
    screen.draw.text("A Jornada de Airla", center=(WIDTH/2, 100), fontsize=70, color="lightgreen", ocolor="black", owidth=1.5)
    screen.draw.filled_rect(start_button, "green")
    screen.draw.text("Iniciar Jogo", center=start_button.center, fontsize=30, color="white")
    sound_text = "Musica ON" if music_on else "Musica OFF"
    screen.draw.filled_rect(sound_button, "green")
    screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color="white")
    screen.draw.filled_rect(exit_button, "darkred")
    screen.draw.text("Sair", center=exit_button.center, fontsize=30, color="white")

def draw_game():
    airla.actor.draw()
    fred.actor.draw()
    for enemy in enemies:
        enemy.actor.draw()

def draw_game_over():
    draw_game()
    screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2), fontsize=100, color="red", ocolor="white", owidth=2)
    screen.draw.filled_rect(play_again_button, "green")
    screen.draw.text("Jogar Novamente", center=play_again_button.center, fontsize=30, color="white")
    screen.draw.filled_rect(exit_button_endgame, "darkred")
    screen.draw.text("Sair", center=exit_button_endgame.center, fontsize=30, color="white")

def draw_win_screen():
    draw_game()
    screen.draw.text("Voce salvou o Fred!", center=(WIDTH/2, HEIGHT/2), fontsize=50, color="gold", ocolor="black", owidth=2)
    screen.draw.filled_rect(play_again_button, "green")
    screen.draw.text("Jogar Novamente", center=play_again_button.center, fontsize=30, color="white")
    screen.draw.filled_rect(exit_button_endgame, "darkred")
    screen.draw.text("Sair", center=exit_button_endgame.center, fontsize=30, color="white")

def update():
    if game_state == "playing":
        airla.update()
        for enemy in enemies:
            enemy.update()
        check_collisions()
        check_for_win()
    elif game_state == "win":
        fred.update()

def on_mouse_down(pos):
    global game_state, music_on
    if game_state == "menu":
        if start_button.collidepoint(pos):
            sounds.click.play()
            reset_game()
        elif sound_button.collidepoint(pos):
            sounds.click.play()
            music_on = not music_on
            if not music_on:
                music.stop()
        elif exit_button.collidepoint(pos):
            exit()
    elif game_state == "playing":
        airla.target = pos
    elif game_state == "game_over" or game_state == "win":
        if play_again_button.collidepoint(pos):
            sounds.click.play()
            reset_game()
        elif exit_button_endgame.collidepoint(pos):
            exit()

def check_collisions():
    global game_state
    if game_state != "playing":
        return
    for enemy in enemies:
        if airla.actor.colliderect(enemy.actor):
            game_state = "game_over"
            music.stop()
            if music_on:
                try:
                    music.play_once('danger')
                except Exception as e:
                    print(f"AVISO: Nao foi possivel tocar 'danger'. Erro: {e}")

def check_for_win():
    global game_state
    if game_state != "playing":
        return
    if airla.actor.colliderect(fred.actor):
        game_state = "win"
        music.stop()
        if music_on:
            try:
                music.play_once('win')
            except Exception as e:
                print(f"AVISO: Nao foi possivel tocar 'win'. Erro: {e}")