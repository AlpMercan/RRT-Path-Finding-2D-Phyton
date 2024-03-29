import pygame
from RRTbasePy import RRTGraph
from RRTbasePy import RRTMap
import time

def main():
    dimensions = (512, 512)
    start = (50, 50)
    goal = (300, 300)
    obsdim = 30
    obsnum = 50
    iteration = 0
    t1 = 0

    pygame.init()
    map = RRTMap(start, goal, dimensions, obsdim, obsnum)
    graph = RRTGraph(start, goal, dimensions, obsdim, obsnum)

    obstacles = graph.makeobs()
    map.drawMap(obstacles)

    t1 = time.time()
    running = True  # Variable to control the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop if the user closes the window

        if (not graph.path_to_goal()):
            time.sleep(0.005)
            elapsed = time.time() - t1
            t1 = time.time()
            # Raise an exception if timeout
            if elapsed > 10:
                print('Timeout - re-initiating the calculations')
                break

            if iteration % 10 == 0:
                X, Y, Parent = graph.bias(goal)
                pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
                pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                                 map.edgeThickness)

            else:
                X, Y, Parent = graph.expand()
                pygame.draw.circle(map.map, map.grey, (X[-1], Y[-1]), map.nodeRad * 2, 0)
                pygame.draw.line(map.map, map.Blue, (X[-1], Y[-1]), (X[Parent[-1]], Y[Parent[-1]]),
                                 map.edgeThickness)

            if iteration % 5 == 0:
                pygame.display.update()
            iteration += 1
        else:
            map.drawPath(graph.getPathCoords())
            pygame.display.update()

        pygame.time.delay(100)

    pygame.quit()

if __name__ == '__main__':
    main()
