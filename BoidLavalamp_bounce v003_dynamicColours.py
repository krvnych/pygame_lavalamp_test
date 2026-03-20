import pygame
import random
import math

# Fenstergröße
WIDTH, HEIGHT = 300, 900
BACKGROUND_COLOR = (0, 0, 81)
BOID_COLOR = (255, 0, 142)
CLOCK_TICK = 60
BORDER_BOUNCE_MARGIN = 20

# Boid-Parameter
NUM_BOIDS = 400 
SIZE_BOID = 10
MAX_SPEED = 6
MAX_FORCE = 0.6
PERCEPTION_RADIUS = 40
COUNT_RADIUS = 100

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

        # Randbehandlung: Abstoßen an den Fensterrändern
        self.edges()

    def edges(self):
        margin = BORDER_BOUNCE_MARGIN  # Abstand zum Rand, innerhalb dessen die Boids abgelenkt werden

        force = pygame.Vector2(0, 0)

        if self.position.x < margin:  # Linker Rand
            force.x = MAX_FORCE
        elif self.position.x > WIDTH - margin:  # Rechter Rand
            force.x = -MAX_FORCE

        if self.position.y < margin:  # Oberer Rand
            force.y = MAX_FORCE
        elif self.position.y > HEIGHT - margin:  # Unterer Rand
            force.y = -MAX_FORCE

        self.apply_force(force)

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

    def draw(self, screen, boids):
        # Zähle die Anzahl der Nachbarn im Wahrnehmungsradius
        neighbor_count = sum(1 for other in boids if other != self and self.position.distance_to(other.position) < COUNT_RADIUS)

        # 2. Wert normalisieren (0.0 bis 1.0)
        max_neighbors = 350  # Maximal erwartete Anzahl von Nachbarn
        t = min(neighbor_count / max_neighbors, 1.0)
        
        # 3. Farben definieren (z.B. von Hellrosa zu Dunkelrosa)
        color_start = pygame.Color(255, 188, 255)  # Hellrosa
        color_end = pygame.Color(255, 0, 255)      # Dunkelrosa
        
        # 4. Dynamische Farbe berechnen
        color = color_start.lerp(color_end, t)
        
        # 5. Größe basierend auf der Anzahl der Nachbarn anpassen
        size = SIZE_BOID + int(t * 10)  # Größe von SIZE_BOID bis SIZE_BOID + 10

        # Zeichne das Boid mit der berechneten Farbe
        pygame.draw.circle(screen, color, self.position, size)


def main():
    # Boid Liste erstellen
    boids = [Boid() for _ in range(NUM_BOIDS)]

    running = True
    while running:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(40)  # Transparenz des Overlays
        overlay.fill(BACKGROUND_COLOR)
        screen.blit(overlay, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update und Zeichnen der Boids
        for boid in boids:
            boid.flock(boids)
            boid.update()
            boid.draw(screen, boids)

        pygame.display.flip()
        clock.tick(CLOCK_TICK)

    pygame.quit()

if __name__ == "__main__":
    main()
