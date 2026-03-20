import pygame
import random
import math

# Fenstergröße
WIDTH, HEIGHT = 400, 1200
BACKGROUND_COLOR = (217, 170, 219)
BOID_COLOR = (255, 0, 142)

# Boid-Parameter
NUM_BOIDS = 700 
SIZE_BOID = 20
MAX_SPEED = 5
MAX_FORCE = 0.4
PERCEPTION_RADIUS = 20

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)

    def update(self):
        # Geschwindigkeit und Position aktualisieren
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

        # Randbehandlung: Wrap-around Effekt
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

    def apply_force(self, force):
        self.acceleration += force

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_vector = pygame.Vector2(0, 0)
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                avg_vector += other.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = avg_vector.normalize() * MAX_SPEED
            steering = avg_vector - self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def cohesion(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        center_of_mass = pygame.Vector2(0, 0)
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                center_of_mass += other.position
                total += 1
        if total > 0:
            center_of_mass /= total
            direction = center_of_mass - self.position
            if direction.length() > 0:
                direction = direction.normalize() * MAX_SPEED
            steering = direction - self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def separation(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < PERCEPTION_RADIUS / 2:
                diff = self.position - other.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * MAX_SPEED
            steering -= self.velocity
            if steering.length() > MAX_FORCE:
                steering.scale_to_length(MAX_FORCE)
        return steering

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        # Gewichte für die verschiedenen Verhaltensregeln
        self.apply_force(alignment * 1.0)
        self.apply_force(cohesion * 1.0)
        self.apply_force(separation * 1.5)

    def draw(self, screen):
        pygame.draw.circle(screen, BOID_COLOR, self.position, SIZE_BOID)

def main():
    # Boid Liste erstellen
    boids = [Boid() for _ in range(NUM_BOIDS)]

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update und Zeichnen der Boids
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
