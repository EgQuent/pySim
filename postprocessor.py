import numpy as np
import matplotlib.pyplot as plt
from solver import HeatSolver

class PostProcessor:

    def __init__(self, solver: HeatSolver, path = ".//", export_type=["csv"]):
        self.solver = solver
        self.path = path
        self.export_type = export_type

    def print_matrix(self, decimal = 2):
        print(self.solver.u[1:-1, 1:-1].round(decimal))

    def export(self):
        if "csv" in self.export_type:
            self.export_csv()

        if "img" in self.export_type:
            self.export_img()

    def export_csv(self, name = "heat_export", ext=".csv", dec = 2):
        matrix = self.solver.u[1:-1, 1:-1].round(dec)
        np.savetxt(self.path + "/" + name + "_t" + str(round(self.solver.crt_time,2)) + ext, matrix, delimiter=",")


    def export_img(self, name="heat_export", ext=".png", dec=2):
        matrix = self.solver.u[1:-1, 1:-1].round(dec).copy()
        fig = plt.figure()
        img = plt.imshow(matrix, cmap=plt.get_cmap('bwr'), vmin=matrix.min(), vmax=matrix.max())
        plt.axis('off')
        plt.title('Result at t={:.1f} s'.format(round(self.solver.crt_time, 2)))
        color_bar = plt.colorbar(img)
        color_bar.set_label('Thermal Scale')
        plt.show()