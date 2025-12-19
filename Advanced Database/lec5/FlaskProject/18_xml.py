from flask import Flask, request, Response
from models import db, UserInput
import xml.etree.ElementTree as ET

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/lec5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
    # 解析 XML 请求
    xml_data = request.get_data()
    root = ET.fromstring(xml_data)
    user_input = root.find('content').text

    # 创建一个新的 UserInput 对象并保存到数据库
    new_input = UserInput(content=user_input)
    db.session.add(new_input)
    db.session.commit()

    # 构建 XML 响应
    response_root = ET.Element('response')
    ET.SubElement(response_root, 'status').text = 'success'
    ET.SubElement(response_root, 'message').text = 'Input saved successfully'
    response_xml = ET.tostring(response_root, encoding='unicode')

    return Response(response_xml, mimetype='text/xml')

@app.route('/inputs', methods=['GET'])
def get_inputs():
    # 查询数据库中的所有用户输入
    user_inputs = UserInput.query.all()

    # 构建 XML 响应
    response_root = ET.Element('inputs')
    for input in user_inputs:
        input_element = ET.SubElement(response_root, 'input')
        ET.SubElement(input_element, 'id').text = str(input.id)
        ET.SubElement(input_element, 'content').text = input.content
    response_xml = ET.tostring(response_root, encoding='unicode')

    return Response(response_xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(debug=True)

# $xmlData = @"
# <request>
#     <content>Hello, Flask!</content>
# </request>
# "@
#
# Invoke-WebRequest -Uri http://127.0.0.1:5000/submit -Method Post -ContentType "text/xml" -Body $xmlData


# Invoke-WebRequest -Uri http://127.0.0.1:5000/inputs -Method Get
