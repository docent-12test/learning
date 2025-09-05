# python



import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.collections import LineCollection
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation
from datetime import datetime
import random

# ---------- Model ----------
def lissajous(a, b, delta, n=2000, t0=0.0):
    t = np.linspace(0, 2 * np.pi, n)
    x = np.sin(a * (t + t0) + delta)
    y = np.sin(b * (t + t0))
    return x, y, t

def make_segments(x, y):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    return np.concatenate([points[:-1], points[1:]], axis=1)

# ---------- Figure layout ----------
plt.rcParams["figure.figsize"] = (10, 7)
fig = plt.figure(constrained_layout=False)
gs = fig.add_gridspec(3, 3, height_ratios=[10, 1, 1])

ax_main = fig.add_subplot(gs[0, :])
ax_main.set_aspect("equal", adjustable="datalim")
ax_main.set_xticks([])
ax_main.set_yticks([])
ax_main.set_title("Lissajous Playground — frequenties, fase en animatie")

# Sliders-axes
ax_a = fig.add_subplot(gs[1, 0])
ax_b = fig.add_subplot(gs[1, 1])
ax_delta = fig.add_subplot(gs[1, 2])

ax_speed = fig.add_subplot(gs[2, 0])
ax_points = fig.add_subplot(gs[2, 1])
ax_lw = fig.add_subplot(gs[2, 2])

# ---------- Initial parameters ----------
a0, b0 = 3, 2
delta0 = np.pi / 4
speed0 = 0.2        # animatiesnelheid
n_points0 = 2000
lw0 = 2.0
t0 = 0.0
paused = False

# ---------- Data + plot ----------
x, y, t = lissajous(a0, b0, delta0, n_points0, t0)
segs = make_segments(x, y)
colors = t[:-1] / t[-1]  # gradient langs de curve (0..1)

lc = LineCollection(segs, cmap="plasma", array=colors, linewidth=lw0, alpha=0.95)
ax_main.add_collection(lc)
ax_main.set_xlim(-1.1, 1.1)
ax_main.set_ylim(-1.1, 1.1)

# ---------- Sliders ----------
slider_a = Slider(ax=ax_a, label="a (fx)", valmin=1, valmax=15, valinit=a0, valstep=1)
slider_b = Slider(ax=ax_b, label="b (fy)", valmin=1, valmax=15, valinit=b0, valstep=1)
slider_delta = Slider(ax=ax_delta, label="delta (fase)", valmin=0, valmax=2*np.pi, valinit=delta0)
slider_speed = Slider(ax=ax_speed, label="snelheid", valmin=0.0, valmax=1.0, valinit=speed0)
slider_points = Slider(ax=ax_points, label="# punten", valmin=300, valmax=6000, valinit=n_points0, valstep=100)
slider_lw = Slider(ax=ax_lw, label="lijndikte", valmin=0.5, valmax=5.0, valinit=lw0)

def rebuild_curve():
    a = int(slider_a.val)
    b = int(slider_b.val)
    delta = slider_delta.val
    n = int(slider_points.val)
    x, y, t = lissajous(a, b, delta, n, t0)
    segs = make_segments(x, y)
    colors = t[:-1] / t[-1]
    lc.set_segments(segs)
    lc.set_array(colors)
    lc.set_linewidth(slider_lw.val)
    # autoscale netjes op [-1.1, 1.1]
    ax_main.set_xlim(-1.1, 1.1)
    ax_main.set_ylim(-1.1, 1.1)
    fig.canvas.draw_idle()

for s in [slider_a, slider_b, slider_delta, slider_points, slider_lw]:
    s.on_changed(lambda _evt: rebuild_curve())

# snelheid slider hoeft alleen animatie te beïnvloeden; geen rebuild nodig

# ---------- Buttons ----------
btn_ax_pause = fig.add_axes([0.12, 0.92, 0.1, 0.05])
btn_pause = Button(btn_ax_pause, "Pauzeer")

btn_ax_play = fig.add_axes([0.24, 0.92, 0.1, 0.05])
btn_play = Button(btn_ax_play, "Speel")

btn_ax_rand = fig.add_axes([0.36, 0.92, 0.1, 0.05])
btn_rand = Button(btn_ax_rand, "Random")

btn_ax_save = fig.add_axes([0.48, 0.92, 0.1, 0.05])
btn_save = Button(btn_ax_save, "Opslaan")

def on_pause(_):
    global paused
    paused = True

def on_play(_):
    global paused
    paused = False

def on_random(_):
    # willekeurige maar “mooie” combinaties
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    delta = random.choice([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, np.pi*0.7])
    slider_a.set_val(a)
    slider_b.set_val(b)
    slider_delta.set_val(delta)

def on_save(_):
    fname = f"lissajous_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    ax_main.set_title(f"Opgeslagen: {fname}", color="tab:green")
    fig.canvas.draw_idle()
    fig.savefig(fname, dpi=200, facecolor="white", bbox_inches="tight")
    # titel terugzetten
    ax_main.set_title("Lissajous Playground — frequenties, fase en animatie", color="black")
    fig.canvas.draw_idle()

btn_pause.on_clicked(on_pause)
btn_play.on_clicked(on_play)
btn_rand.on_clicked(on_random)
btn_save.on_clicked(on_save)

# ---------- Animatie ----------
def update(_frame):
    global t0
    if not paused:
        t0 += slider_speed.val * 0.03  # frissere beweging met kleine stapjes
        rebuild_curve()
    return (lc,)

ani = animation.FuncAnimation(fig, update, interval=20, blit=False)

plt.show()