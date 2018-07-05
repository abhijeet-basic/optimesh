# -*- coding: utf-8 -*-
#
import numpy

import meshio
import optimesh

from helpers import download_mesh


def test_simple_lloyd(max_num_steps=5):
    X = numpy.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.4, 0.5, 0.0],
        ]
    )
    cells = numpy.array([[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]])

    X, cells = optimesh.lloyd(X, cells, 1.0e-2, 100, fcc_type="boundary", verbosity=2)

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-12
    ref = 4.985355657854027
    assert abs(norm1 - ref) < tol * ref
    ref = 2.1179164560036154
    assert abs(norm2 - ref) < tol * ref
    ref = 1.0
    assert abs(normi - ref) < tol * ref

    return


def test_pacman_lloyd(max_num_steps=1000):
    filename = download_mesh(
        "pacman.vtk", "19a0c0466a4714b057b88e339ab5bd57020a04cdf1d564c86dc4add6"
    )
    mesh = meshio.read(filename)

    X, _ = optimesh.lloyd(
        mesh.points,
        mesh.cells["triangle"],
        1.0e-2,
        100,
        fcc_type="boundary",
        verbosity=1,
    )

    # Test if we're dealing with the mesh we expect.
    nc = X.flatten()
    norm1 = numpy.linalg.norm(nc, ord=1)
    norm2 = numpy.linalg.norm(nc, ord=2)
    normi = numpy.linalg.norm(nc, ord=numpy.inf)

    tol = 1.0e-12
    ref = 1939.1198108068188
    assert abs(norm1 - ref) < tol * ref
    ref = 75.94965207932323
    assert abs(norm2 - ref) < tol * ref
    ref = 5.0
    assert abs(normi - ref) < tol * ref

    return


if __name__ == "__main__":
    # test_simple_lloyd(
    test_pacman_lloyd(max_num_steps=100)
