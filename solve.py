import argparse
import os
import time

import pygame
from PIL import Image

from factory import SolverFactory
from maze import Maze

max_iter = 300


def solve(factory, method, input_file, output_file):
    print("Loading Image")
    im = Image.open(input_file)

    print("Creating Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Node Count:", maze.count)
    total = t1 - t0
    print("Time elapsed:", total, "\n")

    [title, solver] = factory.createsolver(method)
    print("Starting Solve:", title)

    t0 = time.time()
    [result, stats] = solver(maze)
    t1 = time.time()

    total = t1 - t0

    print("Nodes explored: ", stats[0])
    if (stats[2]):
        print("Path found, length", stats[1])
    else:
        print("No Path Found")
    print("Time elapsed: ", total)

    print("Saving Image and generating simulation")

    im = im.convert('RGB')
    im_pixels = im.load()

    result_path = [n.Position for n in result]

    length = len(result_path)

    im_pixels[tuple(reversed(maze.end.Position))] = (255, 0, 0)

    n = length / max_iter
    if n == 0:
        n = 1

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 24)
    pygame.init()
    info_object = pygame.display.Info()
    size = (info_object.current_h, info_object.current_h)
    screen = pygame.display.set_mode(size)

    pygame.event.get()

    for i in range(0, length - 1):
        a = result_path[i]
        b = result_path[i + 1]

        # Blue - red
        r = int((i * 1. / length) * 255)
        # px = (r, 0, 255 - r)

        if r < (255 / 2):
            px = (0, 255 - r * 2, 255)
        else:
            px = ((r - (255 / 2)) * 2, 0, 255 - ((r - (255 / 2)) * 2))

        if a[0] == b[0]:
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                im_pixels[x, a[0]] = px
        elif a[1] == b[1]:
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                im_pixels[a[1], y] = px

        if i % n == 0:
            im.save(output_file)
            img = pygame.image.load(output_file)
            img = pygame.transform.scale(img, size)
            rect = img.get_rect()
            screen.blit(img, rect)

            pygame.display.flip()
            pygame.event.get()

    im.save(output_file)


def main():
    sf = SolverFactory()
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--method", nargs='?', const=sf.Default, default=sf.Default,
                        choices=sf.Choices)
    parser.add_argument("output_file")
    input_file = "examples\\normal.png"
    args = parser.parse_args()

    solve(sf, args.method, input_file, args.output_file)


if __name__ == "__main__":
    main()
