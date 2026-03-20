# 🌋 Pygame Boid-Lavalamp Simulation

Diese Simulation kombiniert Craig Reynolds' **Boids-Algorithmus** (Schwarmverhalten) mit einer dynamischen Dichteberechnung, um den organischen Effekt einer **Lavalampe** zu erzeugen. Die Partikel verhalten sich wie zähflüssiges Wachs, das bei hoher Dichte die Farbe und Größe ändert.

## 🚀 Features

- **Schwarmintelligenz:** Implementierung der drei Grundregeln (Alignment, Cohesion, Separation).
- **Dynamisches Farb-Morphing:** Partikel ändern ihre Farbe flüssig von Hellrosa zu Lava-Rot, basierend auf der Anzahl der Nachbarn.
- **Zähflüssige Optik (Motion Trails):** Durch ein halbtransparentes Overlay entstehen weiche Schweife, die den Eindruck von viskosem Wachs verstärken.
- **Performance-Optimierung:** Nutzt ein **Spatial Partitioning Grid** (Gitter-System), um die Berechnungen auch bei hohen Partikelzahlen (400+) flüssig zu halten.
- **Memory-Effizient:** Manuelle RGB-Interpolation verhindert Speicherlecks und schont den RAM.

## 🛠 Installation

1. Stelle sicher, dass **Python 3.x** installiert ist.
2. Installiere die benötigte Bibliothek **Pygame**:
   ```bash
   pip install pygame


## TODO

1. smoother visualasiation