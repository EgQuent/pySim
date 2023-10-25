import numpy as np
from solver import HeatSolver

class PostProcessor:

    def __init__(self, solver: HeatSolver, path = ".//"):
        self.solver = solver
        self.path = path

    def print_matrix(self, decimal = 2):
        print(self.solver.u[1:-1, 1:-1].round(decimal))

    def export_csv(self, name = "heat_export", ext=".csv", dec = 2):
        matrix = self.solver.u[1:-1, 1:-1].round(dec)
        np.savetxt(self.path + "/" + name + "_t" + str(round(self.solver.crt_time,2)) + ext, matrix, delimiter=",")