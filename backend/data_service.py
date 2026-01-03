import pandas as pd
import os
from typing import Dict, List, Optional, Any

class DataService:
    """数据服务类，负责读取和查询Excel数据"""
    
    def __init__(self, data_file_path: str = None):
        """初始化数据服务
        
        Args:
            data_file_path: Excel文件路径，默认为../data/customers.xlsx
        """
        if data_file_path is None:
            # 获取当前文件的目录，然后找到data目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_file_path = os.path.join(current_dir, '..', 'data', 'customers.xlsx')
        
        self.data_file_path = data_file_path
        self.customers_df = None
        self.events_df = None
        self._load_data()
    
    def _load_data(self):
        """加载Excel数据"""
        try:
            if os.path.exists(self.data_file_path):
                # 读取Excel文件，假设有两个sheet：customers和events
                excel_file = pd.ExcelFile(self.data_file_path)
                
                # 读取客户信息表
                if 'customers' in excel_file.sheet_names:
                    self.customers_df = pd.read_excel(self.data_file_path, sheet_name='customers')
                elif '客户信息' in excel_file.sheet_names:
                    self.customers_df = pd.read_excel(self.data_file_path, sheet_name='客户信息')
                else:
                    # 如果只有一张表，默认读取第一张
                    self.customers_df = pd.read_excel(self.data_file_path, sheet_name=0)
                
                # 读取行为事件表（如果存在）
                if 'events' in excel_file.sheet_names:
                    self.events_df = pd.read_excel(self.data_file_path, sheet_name='events')
                elif '行为事件' in excel_file.sheet_names:
                    self.events_df = pd.read_excel(self.data_file_path, sheet_name='行为事件')
                
                # 标准化列名（支持中英文）
                self._normalize_column_names()
                
            else:
                # 如果文件不存在，创建空的DataFrame
                self.customers_df = pd.DataFrame(columns=[
                    'user_id', 'user_name', 'asset_scale', 'trading_frequency', 'risk_preference'
                ])
                self.events_df = pd.DataFrame(columns=[
                    'event_time', 'event_type', 'event_detail', 'user_id', 'user_name'
                ])
                print(f"警告: 数据文件 {self.data_file_path} 不存在，使用空数据")
        except Exception as e:
            print(f"加载数据时出错: {str(e)}")
            # 创建空的DataFrame作为备用
            self.customers_df = pd.DataFrame(columns=[
                'user_id', 'user_name', 'asset_scale', 'trading_frequency', 'risk_preference'
            ])
            self.events_df = pd.DataFrame(columns=[
                'event_time', 'event_type', 'event_detail', 'user_id', 'user_name'
            ])
    
    def _normalize_column_names(self):
        """标准化列名为英文"""
        if self.customers_df is not None and not self.customers_df.empty:
            column_mapping = {
                '用户ID': 'user_id',
                '用户名': 'user_name',
                '用户名称': 'user_name',
                '资产规模': 'asset_scale',
                '交易频率': 'trading_frequency',
                '风险偏好': 'risk_preference',
            }
            self.customers_df.rename(columns=column_mapping, inplace=True)
    
    def get_all_customers(self) -> List[Dict]:
        """获取所有客户信息"""
        if self.customers_df is None or self.customers_df.empty:
            return []
        
        return self.customers_df.to_dict('records')
    
    def get_customer_by_id_or_name(self, customer_id: Optional[str] = None, 
                                   customer_name: Optional[str] = None) -> Optional[Dict]:
        """根据ID或名称查询单个客户
        
        Args:
            customer_id: 客户ID
            customer_name: 客户名称
        
        Returns:
            客户信息字典，如果未找到返回None
        """
        if self.customers_df is None or self.customers_df.empty:
            return None
        
        if customer_id:
            result = self.customers_df[self.customers_df['user_id'] == customer_id]
            if not result.empty:
                return result.iloc[0].to_dict()
        
        if customer_name:
            result = self.customers_df[self.customers_df['user_name'] == customer_name]
            if not result.empty:
                return result.iloc[0].to_dict()
        
        return None
    
    def get_customers_by_ids_or_names(self, customer_ids: List[str] = None, 
                                      customer_names: List[str] = None) -> List[Dict]:
        """根据ID列表或名称列表批量查询客户
        
        Args:
            customer_ids: 客户ID列表
            customer_names: 客户名称列表
        
        Returns:
            客户信息列表
        """
        if self.customers_df is None or self.customers_df.empty:
            return []
        
        results = []
        
        if customer_ids:
            for customer_id in customer_ids:
                customer = self.get_customer_by_id_or_name(customer_id=customer_id)
                if customer:
                    results.append(customer)
        
        if customer_names:
            for customer_name in customer_names:
                customer = self.get_customer_by_id_or_name(customer_name=customer_name)
                if customer:
                    # 避免重复添加
                    if not any(c.get('user_id') == customer.get('user_id') for c in results):
                        results.append(customer)
        
        return results
    
    def query_customers(self, query_params: Dict[str, Any]) -> List[Dict]:
        """根据查询参数查询客户
        
        Args:
            query_params: 查询参数字典，包含以下可能的键：
                - name_contains: 名称包含（支持模糊匹配）
                - risk_preference: 风险偏好
                - asset_scale_min: 最小资产规模
                - asset_scale_max: 最大资产规模
                - trading_frequency: 交易频率
        
        Returns:
            符合条件的客户列表
        """
        if self.customers_df is None or self.customers_df.empty:
            return []
        
        df = self.customers_df.copy()
        
        # 名称包含查询（模糊匹配）
        if 'name_contains' in query_params and query_params['name_contains']:
            name_filter = df['user_name'].str.contains(
                query_params['name_contains'], 
                case=False, 
                na=False
            )
            df = df[name_filter]
        
        # 风险偏好查询
        if 'risk_preference' in query_params and query_params['risk_preference']:
            df = df[df['risk_preference'] == query_params['risk_preference']]
        
        # 资产规模范围查询
        if 'asset_scale_min' in query_params and query_params['asset_scale_min'] is not None:
            df = df[df['asset_scale'] >= query_params['asset_scale_min']]
        
        if 'asset_scale_max' in query_params and query_params['asset_scale_max'] is not None:
            df = df[df['asset_scale'] <= query_params['asset_scale_max']]
        
        # 交易频率查询
        if 'trading_frequency' in query_params and query_params['trading_frequency']:
            df = df[df['trading_frequency'] == query_params['trading_frequency']]
        
        return df.to_dict('records')

