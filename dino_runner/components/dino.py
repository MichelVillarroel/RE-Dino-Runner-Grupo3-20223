import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING, DUCKING_SHIELD, JUMPING, JUMPING_SHIELD, RUNNING, RUNNING_SHIELD, SHIELD_TYPE

class Dino(Sprite):
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8
    Y_POS_DUCK_VEL = 340

    def __init__(self):
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
    
        self.setup_state_booleans()

    def setup_state_booleans (self):
        self.has_powerup = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
        
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_jump :
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

        if self.step_index >= 10:
            self.step_index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def run(self):
        if self.step_index <= 5:
            self.image = self.run_img[self.type][0]
        else:
            self.image = self.run_img[self.type][1]
        
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.type][self.step_index // 5]
        #self.image = self.run_img[self.type][0] if self.step_index < 5 else self.run_img[self.type][1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK_VEL
        self.step_index += 1


    def jump(self):
        self.image = self.jump_img[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4 # Salto
            self.jump_vel -= 0.8 # Subiendo y cuando es negativo baja
        if self.jump_vel < -self.JUMP_VEL: # CUando llega a JUMP_VEL en negativo se termina el salto
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def check_invincibility (self, screen):
        if self.shield:
            time_to_show = round ((self.shield_time_up - pygame.time.get_ticks())/ 1000 , 2)
            if time_to_show >=0:
                if self.show_text:
                    font = pygame.font.Font('freesansbold.ttf', 18)
                    text = font.render(f'Shield enabled for {time_to_show}',True, (0, 0, 0))
                    textRect = text.get_rect()
                    textRect.center = (500, 40)
                    screen.blit(text, textRect)
            else:
                self.shield = False
                self.update_to_default(SHIELD_TYPE)

    def update_to_default (self, current_type):
        if self.type == current_type:
            self.type = DEFAULT_TYPE
