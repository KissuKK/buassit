from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from data_service import DataService
from nlp_service import NLPService

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化服务
data_service = DataService()
nlp_service = NLPService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': '服务运行正常'})

@app.route('/api/query/nlp', methods=['POST'])
def natural_language_query():
    """自然语言查询接口"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': '查询内容不能为空'}), 400
        
        # 使用NLP服务解析查询
        parsed_query = nlp_service.parse_query(query)
        
        # 执行查询
        results = data_service.query_customers(parsed_query)
        
        return jsonify({
            'success': True,
            'query': query,
            'parsed_query': parsed_query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query/single', methods=['POST'])
def single_customer_query():
    """单客户查询接口"""
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        customer_name = data.get('customer_name')
        
        if not customer_id and not customer_name:
            return jsonify({'error': '请提供客户ID或客户名称'}), 400
        
        # 查询客户信息
        customer = data_service.get_customer_by_id_or_name(customer_id, customer_name)
        
        if customer is None:
            return jsonify({
                'success': False,
                'message': '未找到该客户'
            }), 404
        
        return jsonify({
            'success': True,
            'customer': customer
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query/batch', methods=['POST'])
def batch_customer_query():
    """批量客户查询接口"""
    try:
        data = request.get_json()
        customer_ids = data.get('customer_ids', [])
        customer_names = data.get('customer_names', [])
        
        if not customer_ids and not customer_names:
            return jsonify({'error': '请提供客户ID列表或客户名称列表'}), 400
        
        # 批量查询客户信息
        results = data_service.get_customers_by_ids_or_names(customer_ids, customer_names)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/all', methods=['GET'])
def get_all_customers():
    """获取所有客户列表（分页）"""
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        all_customers = data_service.get_all_customers()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        paginated_customers = all_customers[start:end]
        
        return jsonify({
            'success': True,
            'customers': paginated_customers,
            'total': len(all_customers),
            'page': page,
            'page_size': page_size
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 默认使用5001端口，避免与macOS AirPlay Receiver冲突
    port = int(os.environ.get('PORT', 5001))
    print(f'后端服务启动在 http://localhost:{port}')
    app.run(debug=True, host='0.0.0.0', port=port)

