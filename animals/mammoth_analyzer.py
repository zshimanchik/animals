import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from engine.world_constants import WorldConstants

c = WorldConstants()

# def func(n, max_n, b, c):
#     return  6*7*c/n * (0.006*b * min(max_n, n) - 0.007)

def func(n, max_n, c1, mammoth_size_to_energy_ratio):
    time_for_eating = c.APPEAR_FOOD_SIZE_MIN * c.MAMMOTH_BODY_DENSITY * c1 / n
    energy_gain_per_tick = c.EATING_VALUE * mammoth_size_to_energy_ratio * min(max_n, n)
    energy_spend_per_tick = c.ENERGY_FOR_EXIST + (0.2 + 0.2) * c.MOVE_DISTANCE_TO_CONSUMED_ENERGY_RATIO
    return time_for_eating * (energy_gain_per_tick - energy_spend_per_tick)

fig, (ax, ax2) = plt.subplots(2)
plt.subplots_adjust(bottom=0.25)
t = np.arange(1, 40, 1)

s = [func(n, c.MAMMOTH_MAX_ANIMAL_N, 1, c.MAMMOTH_SIZE_TO_ENERGY_RATIO) for n in t]
l, = ax.plot(t, s, lw=2)

s2 = [func(n, c.MAMMOTH_MAX_ANIMAL_N, 1, c.MAMMOTH_SIZE_TO_ENERGY_RATIO) * n for n in t]
l2, = ax2.plot(t, s2, lw=3)

ax.margins(x=0)

axcolor = 'lightgoldenrodyellow'
ax_c2 = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_c1 = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_n = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)

slider_c1 = Slider(ax_c1, 'c1', 0.01, 2, valinit=1, valstep=0.001)
slider_c2 = Slider(ax_c2, 'mster', 1, 4, valinit=c.MAMMOTH_SIZE_TO_ENERGY_RATIO, valstep=0.1)
slider_n = Slider(ax_n, 'N', 5, 40, valinit=c.MAMMOTH_MAX_ANIMAL_N, valstep=1)


def update(val):
    max_n = slider_n.val
    mammoth_size_to_energy_ratio = slider_c2.val
    c1 = slider_c1.val

    l.set_ydata([func(n, max_n, c1, mammoth_size_to_energy_ratio) for n in t])
    l2.set_ydata([func(n, max_n, c1, mammoth_size_to_energy_ratio) *n for n in t])

    # recompute the ax.dataLim
    ax.relim()
    # update ax.viewLim using the new dataLim
    ax.autoscale_view()
    # recompute the ax.dataLim
    ax2.relim()
    # update ax.viewLim using the new dataLim
    ax2.autoscale_view()

    fig.canvas.draw_idle()


slider_c2.on_changed(update)
slider_n.on_changed(update)
slider_c1.on_changed(update)


plt.show()
