

import pygame
import cv2
import random
import numpy as np

class SmokeParticle:
    '''
    Docstring for SmokeParticle

    class to draw particles and make them fade away when we we press a specific key

    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(4, 8)
        self.life = 255  
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-3, -1)
        self.growth = 0.12 

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius += self.growth
        self.life -= 2  


    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((int(self.radius*2), int(self.radius*2)), pygame.SRCALPHA)

            pygame.draw.circle(s, (250, 0, 0, self.life), (self.radius, self.radius), int(self.radius))
            
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

def main():
    # 1. Initialize Pygame
    pygame.init()
    screen = pygame.display.set_caption("Smoke Particle Test")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    particles = []
    running = True

    while running:
        # Fill screen with black
        screen.fill((30, 30, 30))

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Key Press logic mentioned in docstring
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Spawn a burst of 20 particles at center
                    for _ in range(20):
                        particles.append(SmokeParticle(400, 500))

        # 3. Continuous Spawn at Mouse Position
        mx, my = pygame.mouse.get_pos()
        particles.append(SmokeParticle(mx, my))

        # 4. Update and Draw Particles
        # We iterate backwards to safely remove dead particles from the list
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            
            # Remove particle if it is invisible
            if particle.life <= 0:
                particles.remove(particle)

        # 5. Refresh Display
        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()