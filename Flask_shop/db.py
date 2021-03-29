import MySQLdb
import hashlib

def insert_user(id,name,age,birthday,gender,mail,zip,zyusyo,pw,salt):
    conn = get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO user(id,name,age,birthday,gender,mail,zip,zyusyo,pw,salt) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    try:
        cur.execute(sql, (id,name,age,birthday,gender,mail,zip,zyusyo,pw,salt))
        result = "ok"
    except Exception as s:
        print("SQL実行に失敗 :", s)
        result = "no"
    cur.close()
    conn.commit()
    conn.close()
    return result


def reset_kodo_insert(id,kodo):
    conn = get_connection()
    cur = conn.cursor()

    sql = "INSERT INTO reset VALUES(%s, %s)"

    try:
        cur.execute(sql, (id,kodo))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    cur.close()
    conn.commit()
    conn.close()

def mail_select(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT user.mail FROM reset INNER JOIN user ON reset.id = user.id WHERE reset.id = %s"

    try:
        cur.execute(sql, (id,))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def select_reset_id(kodo):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT id FROM reset WHERE kodo = %s"

    try:
        cur.execute(sql, (kodo,))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def select_mail(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT mail FROM user WHERE id = %s"

    try:
        cur.execute(sql, (id,))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

def pw_updata(pw,salt,id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "UPDATE user SET pw = %s, salt = %s where id = %s"

    try:
        cur.execute(sql, (pw,salt,id))
        result = "ok"
    except Exception as s:
        print("SQL実行に失敗 :", s)
        result = "no"

    cur.close()
    conn.commit()
    conn.close()

    return result



def login(id, pw):
    salt = search_salt(id)

    if salt == None:
        return None

    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 10).hex()

    result = select_user(id, hashed_pw)

    return result

def search_salt(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT salt FROM user WHERE id = %s"

    try:
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()
    if result:
        return result[0]

    return None


def select_user(id, pw):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT id, name, mail, zip, zyusyo, point FROM user WHERE id = %s AND pw = %s"

    try:
        cur.execute(sql, (id,pw))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()
    cur.close()
    conn.close()

    return result


def product():
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM product"

    try:
        cur.execute(sql)
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def name_product(name):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM product WHERE product_name like %s"

    try:
        cur.execute(sql,('%'+name+'%',))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    if result == ():
        return None
    else:
        return result

        

def clas_product(clas):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM product WHERE class = %s"

    try:
        cur.execute(sql,(clas,))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    if result == ():
        return None
    else:
        return result


def name_clas_product(name,clas):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM product WHERE product_name like %s AND class = %s"

    try:
        cur.execute(sql,('%'+name+'%',clas))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    if result == ():
        return None
    else:
        return result

def product_class():
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT DISTINCT class FROM product"

    try:
        cur.execute(sql)
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    return result


def select_osusume():
    conn = get_connection()
    cur = conn.cursor()

    sql = "select product.product_name,product.pasu, sum(kazu) as cnt from history INNER JOIN product ON history.no = product.no group by product.product_name,product.pasu ORDER BY cnt desc limit 5"

    try:
        cur.execute(sql)
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

def select_user_osusume(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "select product.class, count(product.class) from history INNER JOIN product ON history.no = product.no WHERE id = %s group by product.class ORDER BY count(product.class) desc"

    try:
        cur.execute(sql,(id,))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchone()
    result = user_osusume(result[0])
    cur.close()
    conn.close()

    return result


def user_osusume(clas):
    conn = get_connection()
    cur = conn.cursor()

    sql = "select product_name,pasu from product WHERE class = %s"

    try:
        cur.execute(sql,(clas,))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()

    
    cur.close()
    conn.close()

    return result


def select_product(name):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM product WHERE product_name = %s"

    try:
        cur.execute(sql, (name,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()


    cur.close()
    conn.close()

    return result

def updata_point(point,id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "UPDATE user SET point = %s where id = %s"

    try:
        cur.execute(sql, (point,id))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    cur.close()
    conn.commit()
    conn.close()


def insert_history(id,product_list):
    conn = get_connection()
    cur = conn.cursor()

    sql = "INSERT INTO history VALUES(%s, %s, %s, CURRENT_TIMESTAMP)"

    try:
        for i in product_list:
            cur.execute(sql, (id,i[0],i[4]))
    except Exception as s:
        print("SQL実行に失敗 :", s)

    cur.close()
    conn.commit()
    conn.close()


def update_account(mail,zip,zyusyos,id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "UPDATE user SET mail = %s, zip = %s, zyusyo = %s WHERE id = %s"

    try:
        cur.execute(sql, (mail,zip,zyusyos,id))
    except Exception as e:
        print("SQL実行に失敗：" , e)


    cur.close()
    conn.commit()
    conn.close()


def select_history(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT product.product_name, product.class, kazu, entry FROM history INNER JOIN product ON history.no = product.no where id = %s ORDER BY entry desc limit 20"

    try:
        cur.execute(sql,(id,))
    except Exception as e:
        print("SQL実行に失敗 :", e)

    result = cur.fetchall()
    cur.close()
    conn.close()


    return result


def get_connection():
    return MySQLdb.connect(user='root',passwd='*****',host='localhost',db='Flask_shop',charset="utf8")