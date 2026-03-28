from flask import Flask, request, jsonify, render_template_string, render_template
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False


# 数据库连接
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        db="mall",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor
    )


# 1. 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()

        if not username or not password:
            return jsonify({"code": 1, "msg": "账号密码不能为空"})

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id,role FROM user WHERE username=%s AND password=%s",
                       (username, password))
        user = cursor.fetchone()
        if user:
            return jsonify({
                "code": 0,
                "msg": "登录成功",
                "userId": user["id"],
                "role": user["role"]
            })
        return jsonify({"code": 1, "msg": "账号或密码错误"})
    except Exception as e:
        return jsonify({"code": -1, "msg": str(e)})


# 2. 注册接口
@app.route("/api/register", methods=["POST"])
def api_register():
    try:
        username = request.json.get("username", "").strip()
        password = request.json.get("password", "").strip()

        if not username or len(username) < 2:
            return jsonify({"code": 1, "msg": "账号至少2位"})
        if not password or len(password) < 2:
            return jsonify({"code": 1, "msg": "密码至少2位"})

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO user(username,password,role) VALUES(%s,%s,'user')",
                       (username, password))
        db.commit()
        return jsonify({"code": 0, "msg": "注册成功"})
    except Exception as e:
        return jsonify({"code": -1, "msg": str(e)})


# 2. 首页获取所有商品
@app.route("/api/index/goods", methods=["GET"])
def index_goods():
    cursor = get_db().cursor()
    cursor.execute("SELECT id, name, price,stock FROM goods")
    data = cursor.fetchall()
    return jsonify({"code": 0, "data": data})


# 添加商品【权限】
@app.route("/api/goods/add", methods=["POST"])
def goods_add():
    user_id = request.json.get("user_id")
    if not is_admin(user_id):
        return jsonify({"code": -1, "msg": "无权限，只有管理员可以添加"})
    try:
        name = request.json["name"].strip()
        price = request.json["price"]
        stock = request.json.get("stock", 100)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO goods(name,price,stock) VALUES(%s,%s,%s)",
                       (name, price, stock))
        db.commit()
        return jsonify({"code": 0, "msg": "添加成功"})
    except Exception as e:
        print("添加错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# 修改商品【权限】(管理员)（动态sql）
@app.route("/api/goods/update", methods=["POST"])
def goods_update():
    user_id = request.json.get("user_id")
    if not is_admin(user_id):
        return jsonify({"code": -1, "msg": "无权限，只有管理员可以修改"})
    try:
        goods_id = request.json["id"]
        name = request.json.get("name")
        price = request.json.get("price")
        stock = request.json.get("stock")

        sql = "UPDATE goods SET "
        args = []
        if name is not None:
            sql += "name=%s,"
            args.append(name.strip())
        if price is not None:
            sql += "price=%s,"
            args.append(price)
        if stock is not None:
            sql += "stock=%s,"
            args.append(stock)

        if not args:
            return jsonify({"code": 1, "msg": "请填写要修改的字段"})
        sql = sql.strip(",") + " WHERE id=%s"
        args.append(goods_id)

        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql, args)
        db.commit()
        return jsonify({"code": 0, "msg": "修改成功"})
    except Exception as e:
        print("修改错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# 删除商品【权限】
@app.route("/api/goods/delete", methods=["POST"])
def goods_delete():
    user_id = request.json.get("user_id")
    if not is_admin(user_id):
        return jsonify({"code": -1, "msg": "无权限，只有管理员可以删除"})
    try:
        goods_id = request.json["id"]
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM goods WHERE id=%s", (goods_id,))
        db.commit()
        return jsonify({"code": 0, "msg": "删除成功"})
    except Exception as e:
        print("删除错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# 判断是否为管理员
def is_admin(user_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT role FROM user WHERE id=%s", (user_id,))
    role = cursor.fetchone()
    return role and role["role"] == "admin"


# 3. 搜索商品
@app.route('/api/search', methods=['POST'])
def search():
    keyword = request.json.get('keyword', '')
    c = get_db().cursor()
    sql = "SELECT id,name,price,stock FROM goods WHERE name LIKE %s"
    c.execute(sql, (f"%{keyword}%",))
    data = c.fetchall()
    return jsonify({"code": 0, "data": data})


# 4. 加入购物车
@app.route('/api/cart/add', methods=['POST'])
def add_cart():
    try:
        data = request.get_json()
        user_id = int(data["user_id"])
        goods_id = int(data["goods_id"])

        db = get_db()
        cursor = db.cursor()

        # 查询是否存在
        cursor.execute("SELECT id, num FROM cart WHERE user_id=%s AND goods_id=%s", (user_id, goods_id))
        row = cursor.fetchone()

        if row:
            new_num = row["num"] + 1
            cursor.execute("UPDATE cart SET num=%s WHERE id=%s", (new_num, row["id"]))
        else:
            cursor.execute("INSERT INTO cart(user_id, goods_id, num) VALUES (%s,%s,1)", (user_id, goods_id))

        db.commit()
        cursor.close()
        db.close()

        return jsonify({"code": 0, "msg": "加入成功"})

    except Exception as e:
        print("加入购物车错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# 5. 查看购物车
@app.route('/api/cart/list', methods=['POST'])
def cart_list():
    user_id = request.json['user_id']
    c = get_db().cursor()
    sql = """
    SELECT g.id as goods_id, g.name,g.price,c.num 
    FROM cart c 
    JOIN goods g ON c.goods_id=g.id 
    WHERE c.user_id=%s
    """
    c.execute(sql, (user_id,))
    data = c.fetchall()
    return jsonify({"code": 0, "data": data})


# ==========================
# ✅ 购物车数量增减（最终无错版）
# ==========================
@app.route("/api/cart/update_num", methods=["POST"])
def api_cart_update_num():
    try:
        data = request.get_json()  # 必须用这个！
        user_id = int(data["user_id"])
        goods_id = int(data["goods_id"])
        change = int(data["change"])

        db = get_db()
        cursor = db.cursor()

        # 获取当前数量
        cursor.execute("SELECT num FROM cart WHERE user_id=%s AND goods_id=%s", (user_id, goods_id))
        row = cursor.fetchone()
        if not row:
            return jsonify({"code": 1, "msg": "商品不存在"})

        new_num = row["num"] + change

        # 最少为1
        if new_num < 1:
            return jsonify({"code": 1, "msg": "数量不能小于1"})

        cursor.execute("UPDATE cart SET num=%s WHERE user_id=%s AND goods_id=%s",
                       (new_num, user_id, goods_id))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({"code": 0, "msg": "更新成功"})

    except Exception as e:
        print("更新数量错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# ==========================
# 🔥 1. 结算下单（核心）
# ==========================
@app.route("/api/order/checkout", methods=["POST"])
def api_order_checkout():
    try:
        user_id = request.json["user_id"]
        db = get_db()
        cursor = db.cursor()

        # 1. 查询购物车
        cursor.execute("""
            SELECT c.goods_id, c.num, g.price 
            FROM cart c
            JOIN goods g ON c.goods_id = g.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()

        if not cart_items:
            return jsonify({"code": 1, "msg": "购物车为空"})

        # 2. 计算总价
        total_price = 0
        for item in cart_items:
            total_price += float(item["price"]) * item["num"]

        # 3. 生成订单
        cursor.execute("""
            INSERT INTO orders(user_id, total_price, status)
            VALUES (%s, %s, 1)
        """, (user_id, total_price))
        order_id = cursor.lastrowid

        # 4. 写入订单商品
        for item in cart_items:
            cursor.execute("""
                INSERT INTO order_items(order_id, goods_id, num, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, item["goods_id"], item["num"], item["price"]))

            # 5. 扣减库存
            cursor.execute("""
                UPDATE goods 
                SET stock = stock - %s 
                WHERE id = %s AND stock >= %s
            """, (item["num"], item["goods_id"], item["num"]))

        # 6. 清空购物车
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

        db.commit()
        return jsonify({"code": 0, "msg": "结算成功", "order_id": order_id})

    except Exception as e:
        print("结算错误：", e)
        return jsonify({"code": -1, "msg": str(e)})


# ==========================
# 2. 获取订单列表
# ==========================
@app.route("/api/order/list", methods=["POST"])
def api_order_list():
    user_id = request.json["user_id"]
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, total_price, create_time 
        FROM orders 
        WHERE user_id = %s 
        ORDER BY id DESC
    """, (user_id,))
    orders = cursor.fetchall()

    return jsonify({"code": 0, "data": orders})


# ==========================
# 3. 获取订单详情
# ==========================
@app.route("/api/order/detail", methods=["POST"])
def api_order_detail():
    order_id = request.json["order_id"]
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT g.name, oi.num, oi.price 
        FROM order_items oi
        JOIN goods g ON oi.goods_id = g.id
        WHERE oi.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()

    return jsonify({"code": 0, "data": items})


@app.route('/login.html')
def login_page():
    return render_template('login.html')


@app.route('/index.html')
def index_page():
    return render_template('index.html')


@app.route('/search.html')
def search_page():
    return render_template('search.html')


@app.route('/cart.html')
def cart_page():
    return render_template('cart.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
