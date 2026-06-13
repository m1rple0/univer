# Matrix:
# 6 7 3 2
# 5 1 4 3
# 3 2 6 2

# Right part:
# 180
# 90
# 170

# Demand:
# 90 90 100 160

library(lpSolve)
costs <- matrix(
        c(
            7, 1, 6,
            12, 8, 13,
            4, 6, 8,
            6, 5, 7,
            5, 3, 4),
        nrow=3)

row_rhs     <- c(180, 350, 20)
row_signs   <- rep("<=", 3)

col_rhs     <- c(110, 90, 120, 80, 150)
col_signs   <- rep(">=", 5)

result <- lp.transport(costs, "min", row_signs, row_rhs, col_signs, col_rhs, 11)

print("Значение целевой функции:")
print(result$objval)

print("Решение:")
print(result$solution)