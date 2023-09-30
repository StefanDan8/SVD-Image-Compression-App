from itertools import repeat
from multiprocessing import Pool
import numpy as np


class RGBSVD:
    def __init__(self, image_tensor):
        self.nrows = image_tensor.shape[0]
        self.ncols = image_tensor.shape[1]
        self.R_SVD = SVD(image_tensor[:, :, 0])
        self.G_SVD = SVD(image_tensor[:, :, 1])
        self.B_SVD = SVD(image_tensor[:, :, 2])

    def get_rank_k_approximation(self, k, png):
        self.R_SVD.update_approx(k)
        self.G_SVD.update_approx(k)
        self.B_SVD.update_approx(k)
        approx = np.dstack([self.R_SVD.approx, self.G_SVD.approx, self.B_SVD.approx])
        if png:
            return np.clip(approx, a_min = 0, a_max = 1)  # it's already float
        else:
            return np.clip(approx, a_min = 0, a_max = 255).astype(int)


class SVD:
    def __init__(self, matrix):
        self.U, self.S, self.Vh = np.linalg.svd(matrix)
        self.current_rank = 50
        self.approx = self.rank_approx(self.current_rank)

    def rank_approx(self, rank):
        return rank_approximation(self.U, self.S, self.Vh, rank)

    def update_approx(self, target):
        if self.current_rank < target:
            self.approx += self.U[:, self.current_rank:target] @ \
                           np.diag(self.S[self.current_rank:target]) @ \
                           self.Vh[self.current_rank:target, :]
            self.current_rank = target
        else:
            if target <= 0:
                raise Exception("The rank must be positive.")
            self.approx -= self.U[:, target:self.current_rank] @ \
                           np.diag(self.S[target:self.current_rank]) @ \
                           self.Vh[target:self.current_rank, :]
            self.current_rank = target


def rank_approximation(U, S, Vh, k):
    return U[:, :k] @ np.diag(S[:k]) @ Vh[:k, :]


def rsvd_image_approximation(img, k, png, n_iter = 1, p = 5):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    new_R = rank_approximation(*randomized_SVD(R, k, n_iter, p), k)
    new_G = rank_approximation(*randomized_SVD(G, k, n_iter, p), k)
    new_B = rank_approximation(*randomized_SVD(B, k, n_iter, p), k)
    if png:
        return np.clip(np.dstack([new_R, new_G, new_B]), a_min = 0, a_max = 1)  # it's already float
    else:
        return np.clip(np.dstack([new_R, new_G, new_B]), a_min = 0, a_max = 255).astype(int)


def approx(X, k, n_iter, p):
    return rank_approximation(*randomized_SVD(X, k, n_iter, p), k)


def rsvd_image_approx_parallel(img, k, n_iter = 1, p = 5):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    with Pool() as pool:
        result = pool.starmap(approx, zip([R, G, B], repeat(k), repeat(n_iter), repeat(p)))

    return np.dstack(result)


def randomized_SVD(X, rank, n_iter, p):
    """
        Computes the randomized SVD of a matrix X .

                Parameters:
                        X (…, M, N) array_like: matrix to be factorized
                        rank (int): target rank
                        n_iter (int): number of power iterations
                        p (int): oversampling factor

                Returns:
                        U, S, Vh
        """
    # Step 1 : Sample column space of X with P matrix
    n_col = X.shape[1]
    P = np.random.randn(n_col, rank + p)  # projection matrix
    Z = X @ P

    # power iteration n_iter steps
    for k in range(n_iter):
        Z = X @ (X.T @ Z)

    Q, R = np.linalg.qr(Z, mode = 'reduced')
    # Step 2: Compute the SVD on projected Y = Q.T @ Y
    Y = Q.T @ X
    UY, S, Vh = np.linalg.svd(Y, full_matrices = False)
    U = Q @ UY
    return U, S, Vh
