import pygame
import random
import math

# Fenster
WIDTH, HEIGHT = 300, 900
BACKGROUND_COLOR = (10, 0, 30)
FPS = 60

# Lava-Parameter
NUM_PARTICLES = 350
MAX_SPEED = 2
MAX_FORCE = 0.08
NEIGHBOR_RADIUS = 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Particle:
    def __init__(self):
        self.pos = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(HEIGHT * 0.5, HEIGHT))
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = pygame.Vector2(0, 0)

    def apply_force(self, force):
        self.acc += force

    def update(self):
        # Auftrieb (nach oben)
        self.apply_force(pygame.Vector2(0, -0.03))

        # Oben abkühlen → wieder runter
        if self.pos.y < HEIGHT * 0.2:
            self.apply_force(pygame.Vector2(0, 0.08))

        # leichtes Wabern
        t = pygame.time.get_ticks() * 0.001
        wobble = math.sin(t + self.pos.y * 0.02) * 0.05
        self.apply_force(pygame.Vector2(wobble, 0))

        # Bewegung
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel
        self.acc *= 0

        # Screen Wrap (seitlich)
        if self.pos.x < 0:
            self.pos.x = WIDTH
        elif self.pos.x > WIDTH:
            self.pos.x = 0

        # unten halten
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT

    def interact(self, particles):
        center = pygame.Vector2(0, 0)
        total = 0

        for other in particles:
            dist = self.pos.distance_to(other.pos)
            if other != self and dist < NEIGHBOR_RADIUS:
                center += other.pos
                total += 1

        if total > 0:
            center /= total
            direction = center - self.pos

            if direction.length() > 0:
                direction = direction.normalize() * MAX_SPEED

            steer = direction - self.vel
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)

            # starke Anziehung → Blobs!
            self.apply_force(steer * 1.8)

    def draw(self, surface, particles):
        # Nachbarn zählen → Größe & Intensität
        neighbors = sum(
            1 for p in particles
            if p != self and self.pos.distance_to(p.pos) < NEIGHBOR_RADIUS
        )

        size = 6 + neighbors * 0.08

        # Glow zeichnen
        glow = pygame.Surface((int(size * 6), int(size * 6)), pygame.SRCALPHA)

        for i in range(3):
            alpha = 40 - i * 10
            pygame.draw.circle(
                glow,
                (255, 0, 180, alpha),
                (glow.get_width() // 2, glow.get_height() // 2),
                int(size * (2 - i * 0.5))
            )

        surface.blit(glow, (self.pos.x - glow.get_width() // 2,
                            self.pos.y - glow.get_height() // 2))


def main():
    particles = [Particle() for _ in range(NUM_PARTICLES)]

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulation
        for p in particles:
            p.interact(particles)
            p.update()
            p.draw(screen, particles)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()