import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Stel wat voorbeelddata in
window_size = 50  # Het aantal datapunten dat zichtbaar is
x_data = list(range(window_size))
y_data = [0] * window_size  # Initieel alle waarden op 0

# Maak een plot
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data, color='blue')

# Stel de grenzen van de grafiek in
ax.set_xlim(0, window_size - 1)
ax.set_ylim(-1, 1)


# Updatefunctie die telkens nieuwe data toevoegt
def update(frame):
    global x_data, y_data

    # Nieuwe waarde toevoegen
    new_y_value = np.sin(frame * 0.1)  # Voorbeelddata (sine wave)
    y_data.append(new_y_value)

    # Oudste waarde verwijderen zodat de grafiek opschuift
    y_data.pop(0)

    # Data bijwerken in de grafiek
    line.set_ydata(y_data)
    return line,


# Maak de animatie
ani = FuncAnimation(fig, update, frames=range(200), blit=True, interval=50)

# Toon de grafiek
plt.show()
