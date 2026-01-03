import React from 'react';
import { Layout, Typography, Tabs, ConfigProvider } from 'antd';
import NLPQuery from './components/NLPQuery';
import SingleCustomerQuery from './components/SingleCustomerQuery';
import BatchCustomerQuery from './components/BatchCustomerQuery';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  const tabItems = [
    {
      key: 'nlp',
      label: '自然语言查询',
      children: <NLPQuery />,
    },
    {
      key: 'single',
      label: '单客户查询',
      children: <SingleCustomerQuery />,
    },
    {
      key: 'batch',
      label: '批量客户查询',
      children: <BatchCustomerQuery />,
    },
  ];

  return (
    <ConfigProvider>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ background: '#001529', padding: '0 24px' }}>
          <Title level={3} style={{ color: '#fff', margin: '16px 0' }}>
            银行客户咨询助手
          </Title>
        </Header>
        <Content style={{ padding: '24px', background: '#f0f2f5' }}>
          <div style={{ background: '#fff', padding: '24px', borderRadius: '8px' }}>
            <Tabs defaultActiveKey="nlp" items={tabItems} size="large" />
          </div>
        </Content>
      </Layout>
    </ConfigProvider>
  );
}

export default App;

