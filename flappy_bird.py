import pygame
import random

width = 360
height = 600
velocity = 0
max_valocity = 7
start = True
gravity = 0.5
fps = 60
horizontal_velocity = 3
run = True
score = 0

vertical_pillar_gap = 150
pillar_width = 60
pillar_height = height

pygame.init()
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

bird = pygame.Rect(25 , width //2 , 30 , 30)
 
def pillar_logic():
    global pillar_height, pillar_width, horizontal_velocity, score, start
    if pillars[0].x + pillar_width < 0:
        pillars.pop(0)
        pillars.pop(0)
        p1 , p2 = get_pillars()
        pillars.append(p1)
        pillars.append(p2)
        score +=1 

    if start:
        for pillar in pillars:
            pillar.x -= horizontal_velocity

def collution_check():
    global run, bird, height
    collide = False
    for pillar in pillars:
        collide = pygame.Rect.colliderect(pillar, bird)
        if collide or bird.y < 0 or bird.y > height:
            run = False
            pygame.time.delay(500)
            break


def get_pillars():
    global vertical_pillar_gap , height, width, pillar_width, pillar_height
    num = random.randint(1,height // vertical_pillar_gap)
    p_d = pygame.Rect(width, num * vertical_pillar_gap, pillar_width, pillar_height)
    p_u_y = p_d.y - vertical_pillar_gap - pillar_height
    p_u = pygame.Rect(width, p_u_y, pillar_width, pillar_height)
    return p_d , p_u


def render():
    global score
    display.fill((37, 150, 190))
    pygame.draw.rect(display , (200,200,0) , bird)
    for pillar in pillars:
        pygame.draw.rect(display , (0,125,0) , pillar)
    str1 = str(score)
    text = font.render(str1, True, (255, 255, 255))
    display.blit(text, (width // 2 - (len(str1) * 36 / 2), 0))
    pygame.display.update()

pillars = list(get_pillars())

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = -10
                start = True
    if start:
        bird.y += velocity
        if velocity < max_valocity:
            velocity += gravity

    pillar_logic()
    collution_check()
    render()
    clock.tick(fps)
                
pygame.quit()