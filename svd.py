import matplotlib.pyplot as plt
import numpy as np
import os


class RGBSVD:
    def __init__(self, image_tensor):
        self.nrows = image_tensor.shape[0]
        self.ncols = image_tensor.shape[1]
        self.R_SVD = SVD(image_tensor[:, :, 0])
        self.G_SVD = SVD(image_tensor[:, :, 1])
        self.B_SVD = SVD(image_tensor[:, :, 2])

    def get_rank_k_approximation(self, k):
        self.R_SVD.update_approx(k)
        self.G_SVD.update_approx(k)
        self.B_SVD.update_approx(k)
        approx = np.dstack([self.R_SVD.approx, self.G_SVD.approx, self.B_SVD.approx])
        return np.around(approx).astype(np.uint8)


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


def rsvd_image_approximation(img, k, n_iter = 1, p = 5):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    Ur, Sr, Vhr = randomized_SVD(R, k, n_iter, p)
    Ug, Sg, Vhg = randomized_SVD(G, k, n_iter, p)
    Ub, Sb, Vhb = randomized_SVD(B, k, n_iter, p)
    new_R = rank_approximation(Ur, Sr, Vhr, k)
    new_G = rank_approximation(Ug, Sg, Vhg, k)
    new_B = rank_approximation(Ub, Sb, Vhb, k)
    return np.dstack([new_R, new_G, new_B])


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


if __name__ == "__main__":
    img = plt.imread(os.path.join('resources', 'jupiter.jpg'))  # returns (M,N,3) numpy array in [0,1] if .png, else int
    # array in [0,255]
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    k = 150
    Ur, Sr, Vhr = randomized_SVD(R, k, 1, 5)
    Ug, Sg, Vhg = randomized_SVD(G, k, 1, 5)
    Ub, Sb, Vhb = randomized_SVD(B, k, 1, 5)

    new_R = Ur[:, :k] @ np.diag(Sr[:k]) @ Vhr[:k, :]
    new_G = Ug[:, : k] @ np.diag(Sg[:k]) @ Vhg[:k, :]
    new_B = Ub[:, : k] @ np.diag(Sb[:k]) @ Vhb[:k, :]
    # SVDR = SVD(R)
    # SVDG = SVD(G)
    # SVDB = SVD(B)
    # new_image = np.dstack([SVDR.rank_approx(k), SVDG.rank_approx(k), SVDB.rank_approx(k)])
    # print(SVDR.approx - R)
    new_image_r = np.dstack([new_R, new_G, new_B])
    plt.imshow(np.around(new_image_r).astype(int))  # be sure to put it in [0,255] range
    plt.show()
