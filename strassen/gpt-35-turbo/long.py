import numpy as np

def check_matrices(A, B):
    if not isinstance(A, (list, np.ndarray)) or not isinstance(B, (list, np.ndarray)):
        raise TypeError("Inputs should be lists, numpy arrays, or pandas dataframes")

    if len(A) == 0 or len(B) == 0:
        raise ValueError("Input matrices should not be empty")

    if len(A) != len(A[0]) or len(B) != len(B[0]):
        raise ValueError("Matrices should be square matrices")

    if len(A) != len(B):
        raise ValueError("Matrices should have the same dimensions for multiplication")

    n = len(A)
    if (n & (n - 1)) != 0:
        raise ValueError("Matrix dimensions should be powers of 2")


def strassen_matrix_multiply(A, B):
    check_matrices(A, B)

    n = len(A)

    if n <= 2:
        return np.dot(A, B)

    # Divide matrices into submatrices
    k = n // 2
    A11 = A[:k, :k]
    A12 = A[:k, k:]
    A21 = A[k:, :k]
    A22 = A[k:, k:]

    B11 = B[:k, :k]
    B12 = B[:k, k:]
    B21 = B[k:, :k]
    B22 = B[k:, k:]

    # Calculate Strassen algorithm matrices
    M1 = strassen_matrix_multiply(A11 + A22, B11 + B22)
    M2 = strassen_matrix_multiply(A21 + A22, B11)
    M3 = strassen_matrix_multiply(A11, B12 - B22)
    M4 = strassen_matrix_multiply(A22, B21 - B11)
    M5 = strassen_matrix_multiply(A11 + A12, B22)
    M6 = strassen_matrix_multiply(A21 - A11, B11 + B12)
    M7 = strassen_matrix_multiply(A12 - A22, B21 + B22)

    # Calculate result submatrices
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combine submatrices to get result
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

    return C
