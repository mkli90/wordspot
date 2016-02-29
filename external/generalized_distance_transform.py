#!/usr/bin/python3
# coding=utf-8
__author__ = 'bbogacz'

# Batteries

# Numpy
import numpy
import numpy.random

from matplotlib import pyplot as plt


def of_column(D):
    assert len(D.shape) == 1

    M = 2 ** 31
    n = D.shape[0]
    f = D[:]

    k = 0
    v = numpy.arange(0, n)
    z = numpy.zeros((v.shape[0] + 1,))
    z[0] = -M
    z[1] = +M

    for q in range(1, n):
        while True:
            s = ((f[q] + q ** 2) - (f[v[k]] + v[k] ** 2)) / (2 * q - 2 * v[k])
            if s <= z[k]:
                k = k - 1
            else:
                k = k + 1
                v[k] = q
                z[k] = s
                z[k + 1] = +M
                break

    k = 0

    for q in range(0, n):
        while z[k + 1] < q:
            k = k + 1
        D[q] = (q - v[k]) ** 2 + f[v[k]]

    return D


def test_of_column():
    column = numpy.zeros((200,))
    column[100] = -100
    dt = of_column(column)

    assert dt[100] == -100


def of_image(I):
    D1 = numpy.zeros(I.shape)
    for i in range(0, I.shape[0]):
        D1[i, :] = of_column(I[i, :])

    D2 = numpy.zeros(I.shape)
    for i in range(0, I.shape[1]):
        D2[:, i] = of_column(D1[:, i])

    return D2


def test_of_image():
    image = numpy.zeros((200, 200))
    image[100, 100] = -100
    dt = of_image(image)

    assert dt[100, 100] == -100


def test_of_image_many_close_points():
    image = numpy.zeros((1000, 1000))
    image[:] = 1000
    image[numpy.array(numpy.random.uniform(100, 900, (1000,)), dtype=int),
          numpy.array(numpy.random.uniform(100, 900, (1000,)), dtype=int)] = \
        numpy.random.uniform(0, 100, (1000,))
    dt = of_image(image)

    plt.matshow(dt)
    plt.show()
