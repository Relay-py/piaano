import pygame
import random


WIDTH, HEIGHT = 800, 600

class Spark:
    """Fast, small particles that fly out from the click point."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-7, 0.2) 
        self.life = 255
        self.color = color
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  
        self.life -= 3 

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.life), (self.size, self.size), self.size)
            surface.blit(s, (self.x, self.y), special_flags=pygame.BLEND_ADD)
class RisingNote:
    """Neon bars that float upwards starting from the click Y position."""
    def __init__(self, x, y, w,color):
        self.x = x
        self.y = y  
        self.w = w
        self.h = 0 
        self.color = color
        self.speed = 7
        self.is_active = True 

    def update(self):
        if self.is_active:
            # The bottom stays at the click Y, the top moves up
            self.h += self.speed 
            self.y -= self.speed
        else:
            # Once released, the whole block floats away
            self.y -= self.speed 

    def draw(self, surface):
        if self.h <= 0: return
        
        # Create a surface for the note and its neon glow
        note_surf = pygame.Surface((self.w + 20, self.h + 20), pygame.SRCALPHA)
        
        # 1. Outer Glow (Lower Alpha, BLEND_ADD makes it look like light)
        pygame.draw.rect(note_surf, (*self.color, 80), (5, 5, self.w + 10, self.h + 10), border_radius=8)
        
        # 2. Core Note (Full Brightness)
        pygame.draw.rect(note_surf, self.color, (10, 10, self.w, self.h), border_radius=5)
        
        surface.blit(note_surf, (self.x - 10, self.y - 10), special_flags=pygame.BLEND_ADD)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Synthesia Mode: Sparks Behind Notes")
    clock = pygame.time.Clock()

    active_note = None
    finished_notes = []
    particles = []

    running = True
    while running:
        # Step 1: Draw Background
        screen.fill((5, 5, 15)) 

        mx, my = pygame.mouse.get_pos()

        # Step 2: Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                color = random.choice([
                    (0, 255, 150), (0, 220, 255), (255, 100, 255), (255, 255, 100)
                ])
                active_note = RisingNote(mx - 20, my,40,color)

            if event.type == pygame.MOUSEBUTTONUP:
                if active_note:
                    active_note.is_active = False
                    finished_notes.append(active_note)
                    active_note = None

        # Step 3: Logic - Continuous Generation
        if active_note:
            for _ in range(3): 
                particles.append(Spark(mx, my, active_note.color))

        # --- STEP 4: DRAWING (ORDER MATTERS HERE) ---

        # FIRST: Draw Sparks (They go behind)
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)
        
        # SECOND: Draw Notes (They appear on top of sparks)
        all_notes = finished_notes + ([active_note] if active_note else [])
        for note in all_notes[:]:
            note.update()
            note.draw(screen)
            if note.y + note.h < -100:
                if note in finished_notes: finished_notes.remove(note)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()