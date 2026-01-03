import dashscope
from dashscope import Generation
import os
import json
import re
from typing import Dict, Any

class NLPService:
    """自然语言处理服务，使用DashScope API将自然语言转换为结构化查询"""
    
    def __init__(self):
        """初始化NLP服务"""
        api_key = os.getenv('DASHSCOPE_API_KEY')
        if api_key:
            dashscope.api_key = api_key
        else:
            print("警告: DASHSCOPE_API_KEY未设置，将使用简化的查询解析")
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """将自然语言查询转换为结构化查询参数
        
        Args:
            query: 自然语言查询字符串
        
        Returns:
            结构化查询参数字典
        """
        # 如果没有配置API Key，使用简化的规则匹配
        if not os.getenv('DASHSCOPE_API_KEY'):
            return self._simple_parse_query(query)
        
        try:
            # 使用DashScope API进行查询解析
            prompt = self._build_prompt(query)
            response = Generation.call(
                model='qwen-turbo',
                prompt=prompt,
                temperature=0.1
            )
            
            if response.status_code == 200:
                result_text = response.output.text
                # 尝试从返回文本中提取JSON
                parsed_query = self._extract_json_from_text(result_text)
                return parsed_query
            else:
                print(f"DashScope API调用失败: {response.status_code}")
                return self._simple_parse_query(query)
        except Exception as e:
            print(f"解析查询时出错: {str(e)}")
            return self._simple_parse_query(query)
    
    def _build_prompt(self, query: str) -> str:
        """构建提示词"""
        prompt = f"""你是一个银行客户数据查询助手。请将用户的自然语言查询转换为结构化的查询参数。

用户查询: {query}

请分析查询意图，并返回JSON格式的查询参数。可能的参数包括：
- name_contains: 客户名称包含的关键词（字符串）
- risk_preference: 风险偏好（可选值：稳健型、积极型、保守型等）
- asset_scale_min: 最小资产规模（数字）
- asset_scale_max: 最大资产规模（数字）
- trading_frequency: 交易频率（字符串）

示例：
查询："姓李的客户有谁" -> {{"name_contains": "李"}}
查询："稳健型客户有哪些" -> {{"risk_preference": "稳健型"}}
查询："资产规模大于100万的客户" -> {{"asset_scale_min": 1000000}}

请只返回JSON对象，不要包含其他说明文字。
"""
        return prompt
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """从文本中提取JSON对象"""
        # 尝试直接解析JSON
        try:
            return json.loads(text.strip())
        except:
            pass
        
        # 尝试提取JSON代码块
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # 如果都失败了，返回空字典
        return {}
    
    def _simple_parse_query(self, query: str) -> Dict[str, Any]:
        """简化的查询解析（不使用API，基于规则匹配）"""
        result = {}
        query_lower = query.lower()
        
        # 匹配"姓X的"或"名字包含X的"
        name_match = re.search(r'(?:姓|名字包含|名称包含|叫|是)(.{1,10})(?:的|客户|人)', query)
        if name_match:
            result['name_contains'] = name_match.group(1)
        
        # 匹配风险偏好
        if '稳健' in query or '稳健型' in query:
            result['risk_preference'] = '稳健型'
        elif '积极' in query or '积极型' in query:
            result['risk_preference'] = '积极型'
        elif '保守' in query or '保守型' in query:
            result['risk_preference'] = '保守型'
        
        # 匹配资产规模
        # 提取数字（单位：万、百万等）
        asset_match = re.search(r'资产[规模]*(?:大于|超过|高于|不少于)?(\d+)(?:万|百万|千万)?', query)
        if asset_match:
            value = int(asset_match.group(1))
            if '万' in query and '百万' not in query:
                value = value * 10000
            elif '百万' in query:
                value = value * 1000000
            result['asset_scale_min'] = value
        
        asset_match_max = re.search(r'资产[规模]*(?:小于|低于|不超过|少于)?(\d+)(?:万|百万|千万)?', query)
        if asset_match_max:
            value = int(asset_match_max.group(1))
            if '万' in query and '百万' not in query:
                value = value * 10000
            elif '百万' in query:
                value = value * 1000000
            result['asset_scale_max'] = value
        
        return result

