import React, { useState } from 'react';
import { Input, Button, Card, Descriptions, message, Space, Typography, Tag } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { singleCustomerQuery } from '../services/api';

const { Title, Text } = Typography;

const SingleCustomerQuery = () => {
  const [customerId, setCustomerId] = useState('');
  const [customerName, setCustomerName] = useState('');
  const [loading, setLoading] = useState(false);
  const [customer, setCustomer] = useState(null);

  const handleSearch = async () => {
    if (!customerId.trim() && !customerName.trim()) {
      message.warning('请输入客户ID或客户名称');
      return;
    }

    setLoading(true);
    try {
      const response = await singleCustomerQuery(
        customerId.trim() || undefined,
        customerName.trim() || undefined
      );
      if (response.success) {
        setCustomer(response.customer);
        message.success('查询成功');
      } else {
        message.error(response.message || '未找到该客户');
        setCustomer(null);
      }
    } catch (error) {
      message.error('查询失败：' + (error.response?.data?.error || error.message));
      setCustomer(null);
    } finally {
      setLoading(false);
    }
  };

  const getRiskPreferenceColor = (value) => {
    const colorMap = {
      '稳健型': 'green',
      '积极型': 'orange',
      '保守型': 'blue',
    };
    return colorMap[value] || 'default';
  };

  return (
    <div>
      <Card style={{ marginBottom: '24px' }}>
        <Title level={4}>单客户查询</Title>
        <Text type="secondary">
          根据客户ID或客户名称查询单个客户的详细信息
        </Text>
        <Space direction="vertical" style={{ width: '100%', marginTop: '16px' }} size="large">
          <Input
            placeholder="请输入客户ID"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
            onPressEnter={handleSearch}
            allowClear
          />
          <Input
            placeholder="或输入客户名称"
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
            onPressEnter={handleSearch}
            allowClear
          />
          <Button
            type="primary"
            icon={<SearchOutlined />}
            loading={loading}
            onClick={handleSearch}
            size="large"
            block
          >
            查询
          </Button>
        </Space>
      </Card>

      {customer && (
        <Card>
          <Title level={5}>客户详细信息</Title>
          <Descriptions bordered column={1}>
            <Descriptions.Item label="客户ID">
              {customer.user_id}
            </Descriptions.Item>
            <Descriptions.Item label="客户名称">
              {customer.user_name}
            </Descriptions.Item>
            <Descriptions.Item label="资产规模">
              {customer.asset_scale ? customer.asset_scale.toLocaleString() : '-'}
            </Descriptions.Item>
            <Descriptions.Item label="交易频率">
              {customer.trading_frequency || '-'}
            </Descriptions.Item>
            <Descriptions.Item label="风险偏好">
              {customer.risk_preference ? (
                <Tag color={getRiskPreferenceColor(customer.risk_preference)}>
                  {customer.risk_preference}
                </Tag>
              ) : '-'}
            </Descriptions.Item>
          </Descriptions>
        </Card>
      )}
    </div>
  );
};

export default SingleCustomerQuery;

