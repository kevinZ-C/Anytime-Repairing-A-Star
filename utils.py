import math
from random import randint

import numpy as np
import pygame


def drawRect(color, x, y, screen, MARGIN, GRID_SIZE):
    pygame.draw.rect(screen,
                     color,
                     [(MARGIN + GRID_SIZE) * x + MARGIN,
                      (MARGIN + GRID_SIZE) * y + MARGIN,
                      GRID_SIZE,
                      GRID_SIZE])


def north(grid, x, y, GRID_Y):
    if y > 0 and not grid[x][y - 1].isObstacle:
        return grid[x][y - 1]


def south(grid, x, y, GRID_Y):
    if y < GRID_Y - 1 and not grid[x][y + 1].isObstacle:
        return grid[x][y + 1]


def west(grid, x, y, GRID_X):
    if x > 0 and not grid[x - 1][y].isObstacle:
        return grid[x - 1][y]


def east(grid, x, y, GRID_X):
    if x < GRID_X - 1 and not grid[x + 1][y].isObstacle:
        return grid[x + 1][y]


def northEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y > 0 and not grid[x + 1][y - 1].isObstacle:
        return grid[x + 1][y - 1]


def southEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y < GRID_Y - 1 and not grid[x + 1][y + 1].isObstacle:
        return grid[x + 1][y + 1]


def northWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y > 0 and not grid[x - 1][y - 1].isObstacle:
        return grid[x - 1][y - 1]


def southWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y < GRID_Y - 1 and not grid[x - 1][y + 1].isObstacle:
        return grid[x - 1][y + 1]


def drawPath(path, color, start, goal, screen, MARGIN, GRID_SIZE):
    for p in path:
        if not p == start and not p == goal:
            drawRect(color, p.x, p.y, screen, MARGIN, GRID_SIZE)
            pygame.display.update()


def drawGrid(GRID_X, GRID_Y, grid, screen, MARGIN, GRID_SIZE, BLACK, GRAY, GREEN, RED):
    for y in range(GRID_X):
        for x in range(GRID_Y):
            if grid[x][y].isObstacle:
                drawRect(BLACK, x, y, screen, MARGIN, GRID_SIZE)
            else:
                drawRect(GRAY, x, y, screen, MARGIN, GRID_SIZE)
            # if x == 0 and y == GRID_Y - 1:
            #     drawRect(GREEN, x, y, screen, MARGIN, GRID_SIZE)
            # if x == GRID_X - 1 and y == 0:
            #     drawRect(RED, x, y, screen, MARGIN, GRID_SIZE)


def randomColor():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def ED(current, goal):
    if not current == goal:
        return math.sqrt(((goal.x - current.x) ** 2) + ((goal.y - current.y) ** 2))
    else:
        return 0


def setChildren(GRID_X, GRID_Y, grid, percentChanceForWall, actualPercentOfWalls, start, goal):
    obstaclePositions = []
    numObstacles = 36
    obstacleSize = 2
    # obstacleGap = 2

    # Calculate number of obstacles per row/column
    obstaclesPerRow = int(np.sqrt(numObstacles))
    obstaclesPerColumn = numObstacles // obstaclesPerRow

    # Calculate the gap between obstacles based on the grid size and number of obstacles
    gapSize_X = (GRID_X - obstaclesPerRow * obstacleSize) // (obstaclesPerRow + 1)
    gapSize_Y = (GRID_Y - obstaclesPerColumn * obstacleSize) // (obstaclesPerColumn + 1)

    # Verify if it is possible to place the obstacles
    if gapSize_X <= 0 or gapSize_Y <= 0:
        raise ValueError('It is not possible to place the obstacles evenly with the current parameters')

    # Generate obstacle positions
    for i in range(obstaclesPerRow):
        for j in range(obstaclesPerColumn):
            x = (i + 1) * gapSize_X + i * obstacleSize
            y = (j + 1) * gapSize_Y + j * obstacleSize

            # Check if obstacle would intersect with start or goal
            if (x <= start.x <= x + obstacleSize and y <= start.y <= y + obstacleSize) or \
                    (x <= goal.x <= x + obstacleSize and y <= goal.y <= y + obstacleSize):
                continue

            obstaclePositions.append((x, y))

    # Create obstacles
    for x, y in obstaclePositions:
        for dx in range(obstacleSize):
            for dy in range(obstacleSize):
                grid[x + dx][y + dy].setObstacle()
                # actualPercentOfWalls += 1

    for y in range(GRID_X):
        for x in range(GRID_Y):
            if grid[x][y] != start and grid[x][y] != goal:
                if grid[x][y].isObstacle:
                    actualPercentOfWalls += 1
            if north(grid, x, y, GRID_Y):
                grid[x][y].children.append(north(grid, x, y, GRID_Y))
            if south(grid, x, y, GRID_Y):
                grid[x][y].children.append(south(grid, x, y, GRID_Y))
            if west(grid, x, y, GRID_X):
                grid[x][y].children.append(west(grid, x, y, GRID_X))
            if east(grid, x, y, GRID_X):
                grid[x][y].children.append(east(grid, x, y, GRID_X))
            # 基于机器人只有四自由度时的修改
            # if northEast(grid, x, y, GRID_X, GRID_Y):
            #     grid[x][y].children.append(northEast(grid, x, y, GRID_X, GRID_Y))
            # if northWest(grid, x, y, GRID_X, GRID_Y):
            #     grid[x][y].children.append(northWest(grid, x, y, GRID_X, GRID_Y))
            # if southEast(grid, x, y, GRID_X, GRID_Y):
            #     grid[x][y].children.append(southEast(grid, x, y, GRID_X, GRID_Y))
            # if southWest(grid, x, y, GRID_X, GRID_Y):
            #     grid[x][y].children.append(southWest(grid, x, y, GRID_X, GRID_Y))
    return grid
