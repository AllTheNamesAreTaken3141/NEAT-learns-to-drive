from re import L
import pygame
import os
from math import sin, cos, radians
import neat

WIN_WIDTH = 800
WIN_HEIGHT = 500

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CAR_SIZE = 80
CAR_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "carsprite.png")), (CAR_SIZE, CAR_SIZE))
TRACK_IMG = pygame.image.load(os.path.join("imgs", "track.png"))\

RAY_COLLIDE_SURFACE = pygame.Surface((8,8))
pygame.draw.circle(RAY_COLLIDE_SURFACE, WHITE, (4,4), 4)
RAY_COLLIDE_MASK = pygame.mask.from_surface(RAY_COLLIDE_SURFACE)

clamp = lambda n, minn, maxn: max(min(maxn, n), minn) #i totally stole this from the internet

class Track:
    IMG = TRACK_IMG
    MASK = pygame.mask.from_surface(TRACK_IMG)

    def __init__(self):
        pass

    def draw(self, win):
        win.blit(self.IMG, (0, 0))

    def collide(self, car):
        car_mask = car.mask
        
        car_rect = car_mask.get_rect(center = (car.position.x, car.position.y))
        self_rect = self.MASK.get_rect(center = (400, 250))

        offset_x = self_rect.x - car_rect.x
        offset_y = self_rect.y - car_rect.y

        if car_mask.overlap(self.MASK, (offset_x, offset_y)):
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
        self.rays = [[0, 0], [-45, 0], [-90, 0], [-135, 0], [-180, 0]]

    def draw(self, win):
        rotated_image = pygame.transform.rotate(CAR_IMG, self.angle)
        new_rect = rotated_image.get_rect(center = CAR_IMG.get_rect(topleft = (self.position.x - CAR_SIZE / 2, self.position.y - CAR_SIZE / 2)).center)
        self.mask = pygame.mask.from_surface(rotated_image)
        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        self.position = self.position + self.velocity

    def turn(self, strength):
        """strength is between -1 and 1 and determines the amount the car turns. Negative values turn _ and positive values turn _"""
        self.velocity.rotate_ip(self.ROT_VEL * strength)
        self.angle -= self.ROT_VEL * strength

    def raycast(self, track):
        for r in range(len(self.rays)):
            for i in range(0, 500, 2):
                if self.collide_ray(self.rays[r][0] + self.angle, i, track):
                    self.rays[r][1] = i
                    break

    def collide_ray(self, angle, distance, track):
        position = ((sin(radians(angle)) * distance) + self.position.x, (cos(radians(angle)) * distance) + self.position.y)

        ray_rect = RAY_COLLIDE_MASK.get_rect(center = (position[0], position[1]))
        track_rect = track.MASK.get_rect(center = (400, 250))

        offset_x = track_rect.x - ray_rect.x
        offset_y = track_rect.y - ray_rect.y

        if RAY_COLLIDE_MASK.overlap(track.MASK, (offset_x, offset_y)):
            return True

        return False

    def get_distances(self):
        distances = []
        for i in self.rays:
            distances.append(i[1])
        return distances

def draw_window(win, track, cars):
    win.fill(WHITE)

    track.draw(win)
    for car in cars:
        car.draw(win)

    pygame.display.update()

def main(genomes, config):
    nets = [] #contains all the neural networks
    ge = [] #contains all the genomes
    cars = [] #contains all the ai cars

    #fill lists and generate cars
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car(400,425,180))
        g.fitness = 0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    track = Track()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(cars) <= 0:
            run = False
            break

        for x, car in enumerate(cars):
            car.move()
            car.raycast(track)
            ge[x].fitness += 0.1

            output = nets[x].activate(car.get_distances())

            car.turn(clamp((output[0] - 0.5) * 2, -1, 1))

            if track.collide(car):
                ge[x].fitness -= 1
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, track, cars)
        

def run(config_path):
    #create a config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    #create a population
    p = neat.Population(config)

    #add some stat reporters
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    #training montage time
    winner = p.run(main, 50)

#finds the file path for the NEAT config
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)