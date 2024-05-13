import gymnasium as gym
from gymnasium import spaces
import random
import time
import pygame
import numpy as np

class FlappyBird(gym.Env):
    def __init__(self):
        self.width = 360
        self.height = 600
        self.velocity = 0
        self.max_valocity = 7
        self.start = True
        self.gravity = 0.5
        self.fps = 60
        self.horizontal_velocity = 3
        self.vertical_pillar_gap = 150
        self.pillar_width = 60
        self.pillar_height = self.height
        self.render_mode = ""
        self.done = False

        pygame.init()
        pygame.display.set_caption('')
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('Arial_bold', 36)
        self.clock = pygame.time.Clock()

        low = -1
        high = 1
        
        self.observation_space=spaces.Box(low=low, high=high, shape=(3,), dtype = np.float32)
        self.action_space=spaces.Discrete(2)

    def step(self, action):
        if action == 0:
            self.velocity = -10
            self.start = True
        if self.start:
            self.bird.y += self.velocity
            if self.velocity < self.max_valocity:
                self.velocity += self.gravity

        self.pillar_logic()

        self.observation = self.get_obs()
        self.reward = 1

        self.collution_check()

        if self.render_mode == "human":
            self.render()
        self.clock.tick(self.fps)

        return self.observation, self.reward , self.done , False,  {}
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)

        self.bird = pygame.Rect(25 , self.width //2 , 30 , 30)
        self.pillars = list(self.get_pillars())
        self.points = 0
        self.done = False
        
        return self.get_obs() , {}
    
    def render(self, render_mode = "human"): 
        self.display.fill((37, 150, 190))
        pygame.draw.rect(self.display , (200,200,0) , self.bird)
        for pillar in self.pillars:
            pygame.draw.rect(self.display , (0,125,0) , pillar)
        str1 = str(self.points)
        text = self.font.render(str1, True, (255, 255, 255))
        self.display.blit(text, (self.width // 2 - (len(str1) * 36 / 2), 0))
        pygame.display.update()

        if self.done:
            time.sleep(0.5)
        
    def close(self):
        pygame.quit()
    
    def pillar_logic(self):
        if self.pillars[0].x + self.pillar_width < 0:
            self.pillars.pop(0)
            self.pillars.pop(0)
            p1 , p2 = self.get_pillars()
            self.pillars.append(p1)
            self.pillars.append(p2)
            self.points +=1 

        if self.start:
            for pillar in self.pillars:
                pillar.x -= self.horizontal_velocity

    def collution_check(self):
        collide = False
        for pillar in self.pillars:
            collide = pygame.Rect.colliderect(pillar, self.bird)
            if collide or self.bird.y < 0 or self.bird.y > self.height:
                self.run = False
                self.done = True
                self.reward = -abs(self.bird.y - self.pillars[0].y + self.vertical_pillar_gap//2)
                break


    def get_pillars(self):
        num = random.randint(1,self.height // self.vertical_pillar_gap)
        p_d = pygame.Rect(self.width, num * self.vertical_pillar_gap, self.pillar_width, self.pillar_height)
        p_u_y = p_d.y - self.vertical_pillar_gap - self.pillar_height
        p_u = pygame.Rect(self.width, p_u_y, self.pillar_width, self.pillar_height)
        return p_d , p_u
    
    def get_obs(self):
        h = self.bird.y / self.height
        d = (self.pillars[0].x - self.bird.x) /self.width
        h_p = (self.bird.y - self.pillars[0].y + self.vertical_pillar_gap//2 ) / self.height

        return np.array([h, d ,h_p])

