import numpy as np
from numba import jit
import time

np.random.seed(42)

@jit
def energy_consumption(x):
    return np.sin(x) + 0.5 * np.cos(2 * x)

@jit
def monte_carlo_energy_integral(n_samples, a, b):
    x_samples = np.random.uniform(a, b, n_samples)
    y_samples = energy_consumption(x_samples)
    integral = (b - a) * np.mean(y_samples)
    return integral

a, b = 0, 24
n_iterations = [1000, 5000, 10000, 50000, 100000, 500000, 100000000]
results = {}

start_time = time.time()

for n in n_iterations:
    integral_value = monte_carlo_energy_integral(n, a, b)
    results[n] = integral_value
    print(f"Ітерації: {n}, Оцінка інтегралу: {integral_value}")

execution_time = time.time() - start_time
print(execution_time)
