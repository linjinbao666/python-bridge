from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    # 获取 POST 请求中的 JSON 数据
    data_dict = request.get_json()

    # 将 JSON 数据加载为 Pandas DataFrame
    data = pd.DataFrame(data_dict)

    # 移除第一列（地区），仅保留数值列
    data2 = data.iloc[:, 1:].values.astype(np.float64)

    # 计算统计量和权重
    mean_values = np.mean(data2, axis=0)
    std_values = np.std(data2, axis=0)
    cv = std_values / mean_values
    cv = np.where(mean_values == 0, 0, cv)
    cv_sum = cv.sum()
    weights = cv / cv_sum

    # 定义结果
    result = {
        "均值": mean_values.tolist(),
        "标准差": std_values.tolist(),
        "变异系数": cv.tolist(),
        "权重": weights.tolist()
    }

    # 计算每个样本的综合评分值A开平方后的结果
    def calculate_A_sqrt_for_rows(data, weights):
        A_squares = np.sum((data * weights) ** 2, axis=1)
        A_sqrts = np.sqrt(A_squares)
        return A_sqrts

    # 调用函数
    A_sqrts = calculate_A_sqrt_for_rows(data2, weights)
    result["每个样本的综合评分值A开平方后的结果"] = A_sqrts.tolist()

    # 返回 JSON 格式的结果
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

