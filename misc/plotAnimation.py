import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def update(idx):
    pt.set_data(x[idx],y[idx])
    return pt


x = np.linspace(0,2*np.pi,200)
y = np.sin(x)


fig, ax = plt.subplots()
ln, = ax.plot(x,y)
pt, = ax.plot(x[0], y[0], marker='o', markersize=5, color='r')
ax.grid()
ani = animation.FuncAnimation(fig,update,frames=np.arange(0,len(x)), interval=10, repeat=False)
ani.save('test.mp4',dpi=600)
plt.show()
