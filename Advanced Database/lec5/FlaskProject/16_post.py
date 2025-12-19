from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 渲染模板文件 16.html
    return render_template('16.html', user_input=None)

@app.route('/submit', methods=['POST'])
def submit():
    # 获取表单提交的数据
    user_input = request.form.get('user_input')
    # 渲染模板文件 index.html，并传递用户输入的数据
    return render_template('16.html', user_input=user_input)

if __name__ == '__main__':
    app.run(debug=True)
