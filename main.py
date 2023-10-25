from mesh import Mesh
from solver import HeatSolver
from postprocessor import PostProcessor


class Simulator:

    def __init__(self):
        self.mesh = None
        self.solver = None
        self.post_processor = None

    def set_mesh(self, lx, ly, dx, dy):
        self.mesh = Mesh(lx, ly, dx, dy)
        self.mesh.create()

    def set_solver(self):
        self.solver = HeatSolver(self.mesh)

    def set_temperature(self, value, restriction=None):
        self.solver.set_value('temperature', value, restriction)
        self.solver.update_temperature_matrix()

    def set_thermal_diffusivity(self, value, restriction=None):
        self.solver.set_value('diffusivity', value, restriction)
        self.solver.update_diffusity_matrix()

    def set_post_processor(self, path = ".//", export_type = ["csv"]):
        self.post_processor = PostProcessor(self.solver, path, export_type)

    def run(self, time_step=10, time=None, export=True, export_step=0):
        if time is not None :
            time_step = int(time / self.solver.dt) +1
        count_step = 0
        self.solver.update_border_temperature_matrix()
        print(f"INIT t= 0s & dt= {round(self.solver.dt,2)}s")
        self.post_processor.print_matrix()
        for _ in range (0,time_step):
            count_step += 1
            self.solver.do_timestep()
            if export == True and export_step != 0 and count_step % export_step == 0:
                print(f"RUN : t= {round(self.solver.crt_time,2)}s")
                self.post_processor.print_matrix()
        final_time = round(time_step*self.solver.dt,2)
        print(f"RUN : t= {final_time}s")
        self.post_processor.print_matrix()
        if export :
            self.post_processor.export()
        return final_time





if __name__ == "__main__":

    sim = Simulator()
    sim.set_mesh(100, 100, 1, 1)
    sim.set_solver()
    sim.set_temperature(60, ((0,50),(101,101)))
    # sim.set_thermal_diffusivity(HeatSolver.D_WATER, ((0,50),(101,101)))
    sim.set_post_processor(export_type=["img"])
    sim.run(time=3600, export = True, export_step=0)