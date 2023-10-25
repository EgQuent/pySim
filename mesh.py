import numpy as np
import matplotlib.pyplot as plt

class Node:

    _counter = 0

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.id = Node._counter
        Node._counter += 1
        self.values = {}

    def __str__(self) -> str:
        return str(self.id)


class Mesh:
    def __init__(self, lx, ly, dx, dy):
        self.lx, self.ly = lx, ly
        self.dx, self.dy = dx, dy
        self.nx, self.ny = int(lx/dx), int(ly/dy)
        self.mesh = []

    def create(self):
        for j in range (0, self.ny):
            line = []
            for i in range (0, self.nx):
                node = Node(i*self.dx, j*self.dy)
                line.append(node)
            self.mesh.append(line)


    def __str__(self) -> str:
        if self.mesh is [] :
            return str("[]")
        else:
            table = ""
            for line in self.mesh:
                for node in line:
                    table = table + str(node) + " "
                table = table + "\n"
            return table
    
    def show(self):
        x, y = [], []
        for line in self.mesh:
            for node in line:
                x.append(node.x)
                y.append(node.y)
        plt.scatter(x, y)
        plt.show()


if __name__ == "__main__":
    test_mesh = Mesh(10, 10, 1, 1)
    test_mesh.create()
    print(test_mesh)
    test_mesh.show()
