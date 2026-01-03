import React, { useState } from 'react';
import { Input, Button, Card, Table, message, Space, Typography, Upload, Tabs, Tag } from 'antd';
import { SearchOutlined, UploadOutlined } from '@ant-design/icons';
import { batchCustomerQuery } from '../services/api';
import * as XLSX from 'xlsx';

const { TextArea } = Input;
const { Title, Text } = Typography;

const BatchCustomerQuery = () => {
  const [customerIds, setCustomerIds] = useState('');
  const [customerNames, setCustomerNames] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [resultCount, setResultCount] = useState(0);
  const [activeTab, setActiveTab] = useState('manual');

  const handleSearch = async () => {
    const ids = customerIds.split('\n').map(id => id.trim()).filter(id => id);
    const names = customerNames.split('\n').map(name => name.trim()).filter(name => name);

    if (ids.length === 0 && names.length === 0) {
      message.warning('请输入客户ID或客户名称');
      return;
    }

    setLoading(true);
    try {
      const response = await batchCustomerQuery(ids, names);
      if (response.success) {
        setResults(response.results || []);
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

  const handleFileUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);

        // 尝试提取客户ID或名称
        const ids = [];
        const names = [];
        
        jsonData.forEach(row => {
          if (row['客户ID'] || row['user_id'] || row['客户id']) {
            ids.push(String(row['客户ID'] || row['user_id'] || row['客户id']));
          }
          if (row['客户名称'] || row['user_name'] || row['客户名称'] || row['姓名']) {
            names.push(String(row['客户名称'] || row['user_name'] || row['姓名']));
          }
        });

        if (ids.length > 0) {
          setCustomerIds(ids.join('\n'));
          setActiveTab('manual');
          message.success(`成功读取 ${ids.length} 个客户ID`);
        } else if (names.length > 0) {
          setCustomerNames(names.join('\n'));
          setActiveTab('manual');
          message.success(`成功读取 ${names.length} 个客户名称`);
        } else {
          message.warning('文件中未找到客户ID或客户名称列');
        }
      } catch (error) {
        message.error('文件读取失败：' + error.message);
      }
    };
    reader.readAsArrayBuffer(file);
    return false; // 阻止自动上传
  };

  const handleTextFileUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target.result;
        const lines = text.split('\n').map(line => line.trim()).filter(line => line);
        
        // 尝试判断是ID还是名称（简单判断：如果是纯数字可能是ID）
        const isNumeric = lines.length > 0 && /^\d+$/.test(lines[0]);
        
        if (isNumeric) {
          setCustomerIds(lines.join('\n'));
        } else {
          setCustomerNames(lines.join('\n'));
        }
        
        setActiveTab('manual');
        message.success(`成功读取 ${lines.length} 条记录`);
      } catch (error) {
        message.error('文件读取失败：' + error.message);
      }
    };
    reader.readAsText(file);
    return false;
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

  const tabItems = [
    {
      key: 'manual',
      label: '手动输入',
      children: (
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <Text strong>客户ID列表（每行一个）：</Text>
            <TextArea
              rows={6}
              placeholder="请输入客户ID，每行一个"
              value={customerIds}
              onChange={(e) => setCustomerIds(e.target.value)}
              style={{ marginTop: '8px' }}
            />
          </div>
          <div>
            <Text strong>客户名称列表（每行一个）：</Text>
            <TextArea
              rows={6}
              placeholder="请输入客户名称，每行一个"
              value={customerNames}
              onChange={(e) => setCustomerNames(e.target.value)}
              style={{ marginTop: '8px' }}
            />
          </div>
          <Button
            type="primary"
            icon={<SearchOutlined />}
            loading={loading}
            onClick={handleSearch}
            size="large"
            block
          >
            批量查询
          </Button>
        </Space>
      ),
    },
    {
      key: 'file',
      label: '文件上传',
      children: (
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <Card>
            <Title level={5}>Excel文件上传</Title>
            <Text type="secondary">支持.xlsx或.xls格式，文件应包含"客户ID"或"客户名称"列</Text>
            <Upload
              beforeUpload={handleFileUpload}
              accept=".xlsx,.xls"
              showUploadList={false}
              style={{ marginTop: '16px' }}
            >
              <Button icon={<UploadOutlined />}>选择Excel文件</Button>
            </Upload>
          </Card>
          <Card>
            <Title level={5}>文本文件上传</Title>
            <Text type="secondary">支持.txt格式，每行一个客户ID或客户名称</Text>
            <Upload
              beforeUpload={handleTextFileUpload}
              accept=".txt"
              showUploadList={false}
              style={{ marginTop: '16px' }}
            >
              <Button icon={<UploadOutlined />}>选择文本文件</Button>
            </Upload>
          </Card>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card style={{ marginBottom: '24px' }}>
        <Title level={4}>批量客户查询</Title>
        <Text type="secondary">
          支持手动输入多个客户ID/名称，或上传包含客户信息的文件进行批量查询
        </Text>
        <div style={{ marginTop: '16px' }}>
          <Tabs activeKey={activeTab} items={tabItems} onChange={setActiveTab} />
        </div>
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

export default BatchCustomerQuery;

