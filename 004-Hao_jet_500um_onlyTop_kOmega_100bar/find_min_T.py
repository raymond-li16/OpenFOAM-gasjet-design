import pandas as pd
import numpy as np

df = pd.read_csv("2024-12-19-002-openfoam.csv")
x = df['Points:0'].to_numpy()
y = df['Points:1'].to_numpy()
z = df['Points:2'].to_numpy()
T = df['T'].to_numpy()
Ux = df['U:0'].to_numpy()
Uy = df['U:1'].to_numpy()
Uz = df['U:2'].to_numpy()
U = np.sqrt(Ux**2 + Uy**2 + Uz**2)

index = np.argmin(T)
print(f"min T: {T[index]}, U = {U[index]}, at (x,y,z) = ({x[index]},{y[index]},{z[index]})")

index_umax = np.argmax(U)
print(f"max U: {U[index_umax]}, T = {T[index_umax]} at (x,y,z) = ({x[index_umax]},{y[index_umax]},{z[index_umax]})")