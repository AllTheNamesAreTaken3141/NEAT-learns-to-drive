import pygame
import os
import neat

WIN_WIDTH = 800
WIN_HEIGHT = 500

WHITE = (255, 255, 255)
CAR_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "carsprite.png")), (80, 80))

class Car:
    pass

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        win.fill(WHITE)
        """
        rotated_image = pygame.transform.rotate(CAR_IMG, angle)
        new_rect = rotated_image.get_rect(center = CAR_IMG.get_rect(topleft = (400, 250)).center)
        win.blit(rotated_image, new_rect.topleft)
        """
        pygame.display.update()

main()