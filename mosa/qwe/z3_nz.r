# Matrix:
# 22 20 16 18 25
# 23 22 25 24 28
# 20 15 22 25 24
# 19 20 20 23 24
# 22 22 20 20 24

library(lpSolve)
costs <- matrix(
        c(
            22, 23, 20, 19, 22,
            20, 22, 15, 20, 22,
            16, 25, 22, 20, 20,
            18, 24, 25, 23, 20,
            25, 28, 24, 24, 24),
        nrow=5)

row_rhs     <- rep(1, 5)
row_signs   <- rep("==", 5)

col_rhs     <- rep(1, 5)
col_signs   <- rep("==", 5)

result <- lp.transport(costs, "min", row_signs, row_rhs, col_signs, col_rhs)

print("Оптимальное значение целевой функции:")
print(result$objval)

print("Матрица назначений:")
print(result$solution)