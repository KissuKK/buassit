import React, { useState } from 'react';
import { Input, Button, Card, Table, message, Space, Tag, Typography } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { nlpQuery } from '../services/api';

const { TextArea } = Input;
const { Title, Text } = Typography;

const NLPQuery = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [parsedQuery, setParsedQuery] = useState(null);
  const [resultCount, setResultCount] = useState(0);

  const handleSearch = async () => {
    if (!query.trim()) {
      message.warning('请输入查询内容');
      return;
    }

    setLoading(true);
    try {
      const response = await nlpQuery(query);
      if (response.success) {
        setResults(response.results || []);
        setParsedQuery(response.parsed_query);
        setResultCount(response.count || 0);
        message.success(`查询成功，找到 ${response.count || 0} 条结果`);
      } else {
        message.error(response.error || '查询失败');
      }
    } catch (error) {
      message.error('查询失败：' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '客户ID',
      dataIndex: 'user_id',
      key: 'user_id',
    },
    {
      title: '客户名称',
      dataIndex: 'user_name',
      key: 'user_name',
    },
    {
      title: '资产规模',
      dataIndex: 'asset_scale',
      key: 'asset_scale',
      render: (value) => value ? value.toLocaleString() : '-',
    },
    {
      title: '交易频率',
      dataIndex: 'trading_frequency',
      key: 'trading_frequency',
    },
    {
      title: '风险偏好',
      dataIndex: 'risk_preference',
      key: 'risk_preference',
      render: (value) => {
        const colorMap = {
          '稳健型': 'green',
          '积极型': 'orange',
          '保守型': 'blue',
        };
        return <Tag color={colorMap[value] || 'default'}>{value || '-'}</Tag>;
      },
    },
  ];

  return (
    <div>
      <Card style={{ marginBottom: '24px' }}>
        <Title level={4}>自然语言查询</Title>
        <Text type="secondary">
          支持自然语言查询，例如："姓李的客户有谁"、"稳健型客户有哪些"等
        </Text>
        <Space direction="vertical" style={{ width: '100%', marginTop: '16px' }} size="large">
          <TextArea
            rows={4}
            placeholder="请输入您的查询问题，例如：姓李的客户有谁"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onPressEnter={(e) => {
              if (e.ctrlKey || e.metaKey) {
                handleSearch();
              }
            }}
          />
          <Button
            type="primary"
            icon={<SearchOutlined />}
            loading={loading}
            onClick={handleSearch}
            size="large"
          >
            查询
          </Button>
        </Space>
        {parsedQuery && Object.keys(parsedQuery).length > 0 && (
          <div style={{ marginTop: '16px' }}>
            <Text type="secondary">解析后的查询条件：</Text>
            <pre style={{ 
              background: '#f5f5f5', 
              padding: '12px', 
              borderRadius: '4px',
              marginTop: '8px'
            }}>
              {JSON.stringify(parsedQuery, null, 2)}
            </pre>
          </div>
        )}
      </Card>

      {results.length > 0 && (
        <Card>
          <Title level={5}>查询结果（共 {resultCount} 条）</Title>
          <Table
            columns={columns}
            dataSource={results}
            rowKey="user_id"
            pagination={{ pageSize: 10 }}
          />
        </Card>
      )}
    </div>
  );
};

export default NLPQuery;

