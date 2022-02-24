from re import L
import pygame
import os
import neat

WIN_WIDTH = 800
WIN_HEIGHT = 500

WHITE = (255, 255, 255)
RED = (255, 0, 0)
CAR_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "carsprite.png")), (64, 64))
TRACK_IMG = pygame.image.load(os.path.join("imgs", "track.png"))

class Track:
    IMG = TRACK_IMG

    def __init__(self):
        pass

    def draw(self, win):
        win.blit(self.IMG, (0, 0))

    def collide(self, car):
        car_mask = car.mask
        self_mask = pygame.mask.from_surface(self.IMG)
        
        car_rect = car_mask.get_rect(center = (car.position.x, car.position.y))
        self_rect = self_mask.get_rect(center = (400, 250))

        offset_x = self_rect.x - car_rect.x
        offset_y = self_rect.y - car_rect.y

        if car_mask.overlap(self_mask, (offset_x, offset_y)):
            return True
        
        return False



class Car:
    IMG = CAR_IMG
    VEL = 9
    ROT_VEL = 8

    def __init__(self, x, y, angle):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(-self.VEL, 0)
        self.velocity.rotate_ip(angle)
        self.angle = -angle
        self.mask = pygame.mask.from_surface(CAR_IMG)

    def draw(self, win):
        rotated_image = pygame.transform.rotate(CAR_IMG, self.angle)
        new_rect = rotated_image.get_rect(center = CAR_IMG.get_rect(topleft = (self.position.x - 32, self.position.y - 32)).center)
        win.blit(rotated_image, new_rect.topleft)
        self.mask = pygame.mask.from_surface(rotated_image)

    def move(self):
        self.position = self.position + self.velocity

    def turn(self, strength):
        """strength is between -1 and 1 and determines the amount the car turns. Negative values turn _ and positive values turn _"""
        self.velocity.rotate_ip(self.ROT_VEL * strength)
        self.angle -= self.ROT_VEL * strength


def draw_window(win, track, car, colliding):
    if colliding:
        win.fill(RED)
    else:
        win.fill(WHITE)
        

    track.draw(win)
    car.draw(win)

    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    track = Track()
    car = Car(400, 425, 180)

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.turn(-1)
        elif keys[pygame.K_RIGHT]:
            car.turn(1)

        car.move()

        draw_window(win, track, car, track.collide(car))

main()