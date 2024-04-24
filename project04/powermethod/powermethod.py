import numpy as np


def powermethod(A, y, niter, tol, verbose=False):
    """
    Compute approximations of the largest absolute eigenvalue and eigenvector
    with the power method [1]_.

    Parameters
    ----------
    A : array_like, shape (n, n)
        Matrix to compute largest absolute eigenvalue and eigenvector.
    y : array_like
        Initial vector.
    niter : int
        Maximum number of iterations.
    tol : float
        Tolerance when to stop iterating.
    verbose : bool, optional
        Print iterations. Default False.

    Returns
    -------
    theta : float
        Largest absolute eigenvalue.
    v : array_like
        Corresponding eigenvector.

    References
    ----------
    .. [1] Bai et al., "Templates for the Solution of Linear Systems: Building
           Blocks for Iterative Methods", SIAM, 2000,
           https://doi.org/10.1137/1.9780898719581
    """
    for it in range(niter):
        # Normalize vector: v = y / || y ||_2
        v = y / np.linalg.norm(y)
        # Matrix-vector multiply: y = A v (local rows)
        y = np.dot(A, v)
        # Compute eigenvalue: theta = v^T y
        theta = np.dot(v, y)
        if verbose:
            print(f"{it = }, {theta = :25.15f}, {y = }")
        # Check convergence
        if np.linalg.norm(y -  theta*v) <= tol*np.abs(theta):
            v = y / np.linalg.norm(y)
            break
    if it < niter:
        return theta, v
    else:
        raise ValueError("Did not converge.")


if __name__ == "__main__":
    n = 5
    rng = np.random.default_rng(42)
    A = np.ones((n, n))
    # A = rng.random((n, n))
    y = rng.random(n)
    theta, y = powermethod(A, y, 10, 1.e-15, verbose=True)
    print(f"Power method: {theta = }, {y = }")
