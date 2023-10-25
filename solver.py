import numpy as np
import matplotlib.pyplot as plt
from mesh import Mesh
from tools import is_in_rectangle, is_rectangle

class BasicSolver:

    def __init__(self, mesh):
        if isinstance(mesh, Mesh):
            self.mesh = mesh
        else:
            TypeError
        self.dx2, self.dy2 = self.mesh.dx**2, self.mesh.dy**2

    def set_value(self, key, value, restriction=None):
        """Restriction is a rectangle defined by a couple of coordinates [[x1,y1],[x2,y2]]"""
        for line in self.mesh.mesh:
            for node in line:
                if restriction is None:
                    node.values[str(key)]=value
                elif is_rectangle(restriction) :
                    if is_in_rectangle((node.x, node.y), restriction[0], restriction[1]) :
                        node.values[str(key)]=value

class HeatSolver(BasicSolver):

    D_WATER = 0.282
    D_AIR = 0.176
    INIT_TEMP = 20.

    def __init__(self, mesh):
        super().__init__(mesh)
        self.d = HeatSolver.D_AIR * np.ones((self.mesh.nx+2, self.mesh.ny+2))
        self.u = HeatSolver.INIT_TEMP * np.ones((self.mesh.nx+2, self.mesh.ny+2))
        self.set_thermal_diffusivity(HeatSolver.D_AIR)
        self.set_temperature(HeatSolver.INIT_TEMP)
        self.dt = self.dx2 * self.dy2 / (2 * self.d.max() * (self.dx2 + self.dy2))

    def set_temperature(self, value, restriction=None):
        self.set_value('temperature', value, restriction)

    def update_temperature_matrix(self):
        for i in range(0, self.mesh.nx):
            for j in range(0, self.mesh.ny):
                self.u[i+1,j+1] = self.mesh.mesh[i][j].values['temperature']

    def update_border_temperature_matrix(self):
        self.u[0] = self.u[1]
        self.u[-1] = self.u[-2]
        self.u[:,0] = self.u[:,1]
        self.u[:,-1] = self.u[:,-2]

    def set_thermal_diffusivity(self, value, restriction=None):
        self.set_value('diffusivity', value, restriction)

    def update_diffusity_matrix(self):
        for i in range(0, self.mesh.nx):
            for j in range(0, self.mesh.ny):
                self.d[i+1,j+1] = self.mesh.mesh[i][j].values['diffusivity']

    def do_timestep(self):
        # Propagate with forward-difference in time, central-difference in space
        u0 = self.u.copy()
        self.u[1:-1, 1:-1] = u0[1:-1, 1:-1] + self.d[1:-1, 1:-1] * self.dt * (
            (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/self.dx2
            + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/self.dy2 )
        self.update_border_temperature_matrix()
        return u0
    
    def run(self, time_step=10, time=None):
        if time is not None :
            time_step = int(time / self.dt) +1
        self.update_border_temperature_matrix()
        print("INIT t= 0s")
        print(self.u)
        for _ in range (0,time_step):
            self.do_timestep()
        final_time = round(time_step*self.dt,2)
        print(f"RUN : t= {final_time}s")
        print(self.u)
        return final_time



if __name__ == "__main__":
    test_mesh = Mesh(10, 10, 1, 1)
    test_mesh.create()
    test_solver = HeatSolver(test_mesh)
    #test_solver.set_temperature(60, ((0,5),(11,11)))
    #test_solver.update_temperature_matrix()
    #test_solver.set_thermal_diffusivity(test_solver.D_WATER, ((0,5),(11,11)))
    #test_solver.update_diffusity_matrix()
    test_solver.run(time=180)




""" 
    # plate size, mm
    w = h = 10.
    # intervals in x-, y- directions, mm
    dx = dy = 0.1
    # Thermal diffusivity of steel, mm2.s-1
    D = 4.

    Tcool, Thot = 300, 700

    nx, ny = int(w/dx), int(h/dy)

    dx2, dy2 = dx*dx, dy*dy
    dt = dx2 * dy2 / (2 * D * (dx2 + dy2))

    u0 = Tcool * np.ones((nx, ny))
    u = u0.copy()

    # Initial conditions - circle of radius r centred at (cx,cy) (mm)
    r, cx, cy = 2, 5, 5
    r2 = r**2
    for i in range(nx):
        for j in range(ny):
            p2 = (i*dx-cx)**2 + (j*dy-cy)**2
            if p2 < r2:
                u0[i,j] = Thot

    def do_timestep(u0, u):
        # Propagate with forward-difference in time, central-difference in space
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
            (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
            + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

        u0 = u.copy()
        return u0, u

    # Number of timesteps
    nsteps = 101
    # Output 4 figures at these timesteps
    mfig = [0, 10, 50, 100]
    fignum = 0
    fig = plt.figure()
    for m in range(nsteps):
        u0, u = do_timestep(u0, u)
        if m in mfig:
            fignum += 1
            print(m, fignum)
            ax = fig.add_subplot(220 + fignum)
            im = ax.imshow(u.copy(), cmap=plt.get_cmap('hot'), vmin=Tcool,vmax=Thot)
            ax.set_axis_off()
            ax.set_title('{:.1f} ms'.format(m*dt*1000))
    fig.subplots_adjust(right=0.85)
    cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
    cbar_ax.set_xlabel('$T$ / K', labelpad=20)
    fig.colorbar(im, cax=cbar_ax)
    plt.show() """