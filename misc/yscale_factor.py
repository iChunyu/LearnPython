import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0,2*np.pi,500)
y = 1e-6 * np.sin(x)


plt.figure()
plt.plot(x,y)
plt.grid()
plt.show()


plt.figure()
plt.plot(x,y)
plt.ticklabel_format(useMathText=True)
plt.grid()
plt.show()


plt.rcParams['axes.formatter.use_mathtext'] = True
plt.figure()
plt.plot(x,y)
plt.grid()
plt.show()