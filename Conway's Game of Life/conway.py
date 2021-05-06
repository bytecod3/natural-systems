
#imports
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """Returns a grid of N*N random values"""
    return np.random.choice(vals, N*N, p=[0.2,0.8]).reshape(N, N) # 20% probability of having OFF and 80% of having OFF

def addGlider(i, j, grid):
    """Adds a glider with top left corner cell at (i,j)"""
    glider = np.array(
        [[0,0,255],
        [255,0,255],
        [0,255,255]]
    )

    grid[i:i+3, j:j+3] = glider # copy glider pattern into the 2D grid

def update(frameNum, img, grid, N):
    """Copy grid since we require 8 neighbours for calculation
        and we go line by line
    """
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # compute -neighbour sum using toroidal boundary conditions
            # x and y wrap around so that the simulation takes place on a toroidal surface
            # formula: add all the surrounding cells and divide by 255 to know what number of cells are ON
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N]+
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                         ) / 255)

            # apply Conway's rules
            if grid[i, j] == ON:
                if(total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

        # update data
        img.set_data(newGrid)
        grid[:] = newGrid[:]  # overlay the new grid onto the old one
        return img,


def main():
    # command line arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movFile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--slider', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declare grid
    grid = np.array([])

    # check if "glider" demo is specified
    if args.glider:
        grid = np.zeroes(N*N).reshape(N*N)
        addGlider(1,1, grid)
    else:
        # populate grid with random on/off - playing with probability here (range = 20% -> 80%)
        grid = randomGrid(N)

    # setting up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N),
                                  frames =10,
                                  interval =updateInterval,
                                  save_count = 50)

    # set the output file
    if args.movFile:
        ani.save(args.movFile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()