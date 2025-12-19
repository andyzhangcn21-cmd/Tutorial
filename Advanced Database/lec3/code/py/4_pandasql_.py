import pandas as pd
from pandasql import sqldf     # 核心接口就这一个函数

# 1. 造两个演示表
orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "user_id":  [101, 102, 101, 103, 102],
    "amount":   [128.5, 200, 75, 300, 150]
})

users = pd.DataFrame({
    "user_id": [101, 102, 103],
    "city":    ["BJ", "SH", "GZ"]
})

# 2. 写 SQL：统计每个城市下单次数与总金额，只保留总额>200 的城市
sql = """
SELECT u.city,
       COUNT(*)   AS order_cnt,
       SUM(o.amount) AS total_amt
FROM   orders o
JOIN   users  u ON o.user_id = u.user_id
GROUP  BY u.city
HAVING total_amt > 200
ORDER  BY total_amt DESC
"""

# 3. 执行 SQL（两种写法）
# 写法 A：手动把全局变量传进去
result = sqldf(sql, globals())
print(result)

# 写法 B：用匿名函数，让 sqldf 自动识别局部变量
# result = sqldf(sql)

######################################################################

sale = pd.DataFrame({
    "ym":     ["2025-08"]*6,
    "shop":   ["A", "A", "B", "B", "C", "C"],
    "product":["p1", "p2", "p1", "p2", "p1", "p2"],
    "qty":    [110, 95, 80, 120, 130, 70]
})

# 取出每个门店销量最高的产品（Top-1）
sql = """
SELECT ym, shop, product, qty
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY shop ORDER BY qty DESC) AS rn
    FROM sale
) t
WHERE rn = 1
"""

print(sqldf(sql))
