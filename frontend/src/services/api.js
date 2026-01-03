import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 自然语言查询
export const nlpQuery = async (query) => {
  const response = await api.post('/query/nlp', { query });
  return response.data;
};

// 单客户查询
export const singleCustomerQuery = async (customerId, customerName) => {
  const response = await api.post('/query/single', {
    customer_id: customerId,
    customer_name: customerName,
  });
  return response.data;
};

// 批量客户查询
export const batchCustomerQuery = async (customerIds = [], customerNames = []) => {
  const response = await api.post('/query/batch', {
    customer_ids: customerIds,
    customer_names: customerNames,
  });
  return response.data;
};

// 获取所有客户（分页）
export const getAllCustomers = async (page = 1, pageSize = 20) => {
  const response = await api.get('/customers/all', {
    params: { page, page_size: pageSize },
  });
  return response.data;
};

export default api;

