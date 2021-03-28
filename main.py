import sys
import random
import pygame
import os

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
bsize = 10
width = int(1300/bsize)*bsize
height = int(650/bsize)*bsize
screen = pygame.display.set_mode((width, height))
grid = [[False] * int(width/bsize) for i in range(int(height/bsize))]
click = 0
clock = pygame.time.Clock()
player = None
path = []
food = None
visited = []


def BFS():
    global visited
    path.clear()
    queue = [(player[1], player[0])]
    visited = [[None] * int(width/bsize) for i in range(int(height/bsize))]
    while len(queue) > 0:
        curr = queue[0]
        if curr[0] == food[1] and curr[1] == food[0]:
            while not(curr[0] == player[1] and curr[1] == player[0]):
                curr = visited[curr[0]][curr[1]]
                path.append(curr)
            break
        try:
            if curr[0]+1 < len(grid) and grid[curr[0]+1][curr[1]] == False and visited[curr[0]+1][curr[1]] is None:
                queue.append((curr[0]+1, curr[1]))
                visited[curr[0]+1][curr[1]] = curr
            if curr[0]-1 >= 0 and grid[curr[0]-1][curr[1]] == False and visited[curr[0]-1][curr[1]] is None:
                queue.append((curr[0]-1, curr[1]))
                visited[curr[0]-1][curr[1]] = curr
            if curr[1]+1 < len(grid[0]) and grid[curr[0]][curr[1]+1] == False and visited[curr[0]][curr[1]+1] is None:
                queue.append((curr[0], curr[1]+1))
                visited[curr[0]][curr[1]+1] = curr
            if curr[1]-1 >= 0 and grid[curr[0]][curr[1]-1] == False and visited[curr[0]][curr[1]-1] is None:
                queue.append((curr[0], curr[1]-1))
                visited[curr[0]][curr[1]-1] = curr
        except:
            pass
        queue.remove(curr)



def changeObs(x, y, mode):
    if int(x/bsize) == player[0] and int(y/bsize) == player[1] or int(x/bsize) == food[0] and int(y/bsize) == food[1]:
        return
    grid[int(y/bsize)][int(x/bsize)] = mode
    BFS()

while True:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if grid[int(mousePos[1]/bsize)][int(mousePos[0]/bsize)]:
                click = 1
            else:
                click = 2
        if event.type == pygame.MOUSEBUTTONUP:
            click = 0
        if click > 0:
            changeObs(mousePos[0], mousePos[1], True if click == 2 else False)
    while food is None or player is None or food[0] == player[0] and food[1] == player[1] or len(path) == 0:
        player = (random.randint(0, int(width / bsize)), random.randint(0, int(height / bsize)))
        food = (random.randint(0, int(width / bsize)), random.randint(0, int(height / bsize)))
        BFS()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == False:
                pygame.draw.rect(screen, (255, 255, 255), (j*bsize, i*bsize, bsize, bsize))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (j*bsize, i*bsize, bsize, bsize))
    # for i in range(len(visited)):
    #     for j in range(len(visited[i])):
    #         if visited[i][j] is not None:
    #             pygame.draw.rect(screen, (0, 100, 0), (j * bsize, i * bsize, bsize, bsize))
    for curr in path:
        pygame.draw.rect(screen, (0, 0, 255), (curr[1] * bsize, curr[0] * bsize, bsize, bsize))
    if not click:
        player = (path[len(path)-1][1], path[len(path)-1][0])
        path.remove(path[len(path)-1])
    pygame.draw.rect(screen, (255, 0, 0), (player[0]*bsize, player[1]*bsize, bsize, bsize))
    pygame.draw.rect(screen, (0, 255, 0), (food[0]*bsize, food[1]*bsize, bsize, bsize))
    pygame.display.update()
    clock.tick(60)






