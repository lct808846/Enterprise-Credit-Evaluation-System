from myadmin.models import ScoreWeight

def calculate_company_score(company):

    default_weights = ScoreWeight.get_default_weights()

    weight = default_weights

    # 定义各维度的最大值（假设值，你需要根据实际情况调整）
    max_execute = 100  # 执行情况的最大值
    max_case = 100     # 案件数量的最大值
    max_money = 1000000  # 总金额的最大值（单位：元）
    max_judge = 100    # 判决情况的最大值

    # 初始化评分项
    scores = {
        'execute': 0,
        'case': 0,
        'money': 0,
        'judge': 0,
    }

    # 计算各维度评分
    def calculate_dimension_score(value, max_value,weight_name):
        if value is None or value == '':
            return 0
        try:
            value_float = float(value.replace(',', ''))  # 处理可能存在的逗号
        except ValueError:
            return 0

        # 如果值为0，则该维度得分为满分25分
        if value_float == 0:
            return weight[weight_name]*100

        # 否则，计算比例并转换为分数
        proportion = min(value_float / max_value, 1)  # 确保比例不超过1
        return weight[weight_name]*100 * (1 - proportion)

    # 计算执行情况得分
    execute_scores = [
        calculate_dimension_score(company.execute_one_year, max_execute,'execute'),
        calculate_dimension_score(company.execute_two_year, max_execute,'execute'),
        calculate_dimension_score(company.execute_three_year, max_execute,'execute'),
    ]
    scores['execute'] = sum(execute_scores) / 3

    # 计算案件数量得分
    case_scores = [
        calculate_dimension_score(company.case_one_year, max_case,'case'),
        calculate_dimension_score(company.case_two_year, max_case,'case'),
        calculate_dimension_score(company.case_three_year, max_case,'case'),
    ]
    scores['case'] = sum(case_scores) / 3

    # 计算总金额得分
    money_scores = [
        calculate_dimension_score(company.one_all_money, max_money,'money'),
        calculate_dimension_score(company.two_all_money, max_money,'money'),
        calculate_dimension_score(company.three_all_money, max_money,'money'),
    ]
    scores['money'] = sum(money_scores) / 3

    # 计算判决情况得分
    judge_scores = [
        calculate_dimension_score(company.judge_one_year, max_judge,'judge'),
        calculate_dimension_score(company.judge_two_year, max_judge,'judge'),
        calculate_dimension_score(company.judge_three_year, max_judge,'judge'),
    ]
    scores['judge'] = sum(judge_scores) / 3

    # 计算总评分
    total_score = sum(scores.values())

    return round(total_score, 2)