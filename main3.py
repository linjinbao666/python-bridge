# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 20:43:35 2024

@author: yuanmeng
"""

import pandas as pd
import numpy as np

# 读取Excel文件
data = pd.read_excel('/home/amrom/ppp/a.xlsx', header=1)
# 将DataFrame转换为二维数组
data1 = data.iloc[:, 1:]  # 1 表示第二列的索引，冒号表示选择所有行
data2 = data1.values.astype(np.float64)



# 计算各指标均值
mean_values = np.mean(data2, axis=0)

# 计算各指标标准差
std_values = np.std(data2, axis=0)

# 计算变异系数（标准差/均值）
cv = std_values / mean_values

# 避免除以零的错误
cv = np.where(mean_values == 0, 0, cv)

# 计算变异系数总和
cv_sum = cv.sum()

# 计算权重
weights = cv / cv_sum

print("均值：", mean_values)
print("标准差：", std_values)
print("变异系数：", cv)
print("权重：", weights)

def calculate_A_sqrt_for_rows(data, weights):  
      
    # 计算每个样本的加权平方和  
    A_squares = np.sum((data2 * weights) ** 2, axis=1)  
    # 对每个结果开平方  
    A_sqrts = np.sqrt(A_squares)  
      
    return A_sqrts  
  
# 调用函数  
A_sqrts = calculate_A_sqrt_for_rows(data, weights) 

print(f"每个样本的综合评分值A开平方后的结果为: {A_sqrts}")
