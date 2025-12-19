from flask import Flask, request, render_template
from flask_caching import Cache
from models import db, UserInput

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/lec5d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db.init_app(app)

# Configure the cache
app.config['CACHE_TYPE'] = 'SimpleCache' # Use a simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Cache timeout in seconds

cache = Cache(app)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/')
@cache.cached(timeout=60)
def index():
    # 查询数据库中的所有用户输入
    user_inputs = UserInput.query.all()
    return render_template('17.html', user_inputs=user_inputs)

@app.route('/submit', methods=['POST'])
def submit():
    # 获取表单提交的数据
    user_input = request.form.get('user_input')
    # 创建一个新的 UserInput 对象并保存到数据库
    new_input = UserInput(content=user_input)
    db.session.add(new_input)
    db.session.commit()
    # 重定向到主页
    return index()

if __name__ == '__main__':
    app.run(debug=True)
