import numpy as np

P = np.array([[0.7, 0.3],
              [0.4, 0.6]])
steady_state = np.linalg.matrix_power(P, 50)[0]
print("Expected user retention (steady state):", steady_state)
