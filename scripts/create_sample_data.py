"""
创建示例Excel数据文件
"""
import pandas as pd
import os

# 确保data目录存在
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)

# 创建示例客户数据
customers_data = {
    'user_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010'],
    'user_name': ['李小明', '张三', '王五', '李华', '赵六', '刘七', '陈八', '杨九', '黄十', '周十一'],
    'asset_scale': [500000, 1200000, 800000, 2000000, 350000, 1500000, 950000, 600000, 1800000, 750000],
    'trading_frequency': ['高频', '中频', '低频', '高频', '中频', '高频', '中频', '低频', '高频', '中频'],
    'risk_preference': ['稳健型', '积极型', '保守型', '积极型', '稳健型', '积极型', '稳健型', '保守型', '积极型', '稳健型']
}

# 创建示例行为事件数据
events_data = {
    'event_time': [
        '2024-01-15 10:30:00', '2024-01-16 14:20:00', '2024-01-17 09:15:00',
        '2024-01-18 16:45:00', '2024-01-19 11:30:00', '2024-01-20 13:20:00',
        '2024-01-21 15:10:00', '2024-01-22 10:00:00', '2024-01-23 14:30:00',
        '2024-01-24 09:45:00'
    ],
    'event_type': ['登录', '交易', '咨询', '交易', '登录', '交易', '咨询', '登录', '交易', '咨询'],
    'event_detail': [
        '用户登录系统', '购买理财产品', '咨询贷款利率', '赎回基金',
        '用户登录系统', '购买股票基金', '咨询定期存款', '用户登录系统',
        '购买债券', '咨询外汇业务'
    ],
    'user_id': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010'],
    'user_name': ['李小明', '张三', '王五', '李华', '赵六', '刘七', '陈八', '杨九', '黄十', '周十一']
}

# 创建DataFrame
customers_df = pd.DataFrame(customers_data)
events_df = pd.DataFrame(events_data)

# 保存到Excel文件
excel_file_path = os.path.join(data_dir, 'customers.xlsx')
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    customers_df.to_excel(writer, sheet_name='customers', index=False)
    events_df.to_excel(writer, sheet_name='events', index=False)

print(f'示例数据文件已创建: {excel_file_path}')
print(f'客户数据: {len(customers_df)} 条')
print(f'行为事件数据: {len(events_df)} 条')

