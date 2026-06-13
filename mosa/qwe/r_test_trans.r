# Matrix:
# 6 5 2
# 3 7 4
# 7 8 1
# 2 2 3

library(lpSolve)
costs <- matrix(
        c(
            6, 3, 7, 2,
            5, 7, 8, 2,
            2, 4, 1, 3
            ),
        nrow=4)

row_rhs     <- c(250, 100, 80, 120)
row_signs   <- rep("<=", 4)

col_rhs     <- c(150, 150, 250)
col_signs   <- rep(">=", 3)

result <- lp.transport(costs, "min", row_signs, row_rhs, col_signs, col_rhs)

print("Оптимальное значение целевой функции:")
print(result$objval)

print("Матрица назначений:")
print(result$solution)