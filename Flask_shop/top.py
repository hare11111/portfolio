from flask import Flask, render_template, request, redirect, session, url_for
import random, string
import hashlib
import db
import mail_pdf
from datetime import timedelta
import datetime

app = Flask(__name__)

app.secret_key = "".join(random.choices(string.ascii_letters, k=256))

#ログインページ
@app.route("/")
def login():
    error = request.args.get("error")
    return render_template("index.html", error=error)

#初期登録
@app.route("/syoki")
def syoki():
    list = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県",
            "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山形県","長野県",
            "岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
            "鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県",
            "佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
    return render_template("syoki.html",list=list)

#認証コード
@app.route("/ninsyou", methods=["post"])
def ninsyou():
    error = request.form.get("error")
    id = request.form.get("id")
    name = request.form.get("name")
    age = request.form.get("age")
    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    mail = request.form.get("mail")
    zip = request.form.get("zip")
    ken = request.form.get("ken")
    zyusyo = request.form.get("zyusyo")
    zyusyos = ken + zyusyo

    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    kodo = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    kodo = ''.join(kodo)
    mail_pdf.kodo_mail(name,mail,kodo)
    session["data"] = (id,name,age,birthday,gender,mail,zip,zyusyos,kodo)

    return render_template("ninsyou.html",error=None)

#パスワード設定
@app.route("/pw", methods=["post"])
def pw():
    error = request.form.get("error")
    nin_kodo = request.form.get("nin_kodo")
    data = session["data"]
    kodo = data[8]
    if kodo == nin_kodo:
        return render_template("pw.html", error=None)
    else:
        return render_template("ninsyou.html", error="認証失敗")

#登録内容確認
@app.route("/kakunin", methods=["post"])
def kakunin():
    pw = request.form.get("pw")
    pws = request.form.get("pws")
    if pw == pws:
        salt = [random.choice(string.ascii_letters + string.digits) for i in range(20)]
        salt = ''.join(salt)
        data = session["data"]
        return render_template("kakunin.html",data=data,pw=pw, salt=salt)
    else:
        return render_template("pw.html",error="同じパスワードを入力してください")

#ユーザ登録
@app.route("/toroku", methods=["post"])
def toroku():
    pw = request.form.get("pw")
    salt = request.form.get("salt")
    data = session["data"]
    id = data[0]
    name = data[1]
    age = data[2]
    birthday = data[3]
    gender = data[4]
    mail = data[5]
    zip = data[6]
    zyusyo = data[7]

    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 10).hex()

    result = db.insert_user(id,name,age,birthday,gender,mail,zip,zyusyo,hashed_pw,salt)
    if result == "ok":
        mail_pdf.toroku_mail(mail, name)
        session.pop("data",None)
        return render_template("toroku.html", name=name)
    else:
        return render_template("toroku_no.html")




#pw再設定
@app.route("/pw_sai", methods=["get"])
def pw_sai():
    return render_template("pw_sai.html")
    
@app.route("/mail_kodo", methods=["post"])
def mail_kodo():
    id = request.form.get("id")

    kodo = [random.choice(string.ascii_letters + string.digits) for i in range(20)]
    kodo = ''.join(kodo)

    db.reset_kodo_insert(id,kodo)

    result = db.mail_select(id)

    mail = db.mail_select(id)

    mail = str(mail[0])
    
    mail_pdf.reset_mail(mail,kodo)

    return render_template("mail_kodo.html")



@app.route("/reset", methods=["get"])
def reset():
    kodo = request.args.get("rand")
    
    result = db.select_reset_id(kodo)
    id = result[0]

    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    session["id"] = id
    error = request.form.get("error")
    return render_template("reset.html",error=None)

@app.route("/pw_reset", methods=["post"])
def pw_reset():
    pw = request.form.get("pw")
    pws = request.form.get("pws")
    if pw == pws:
        id = session["id"]
        salt = [random.choice(string.ascii_letters + string.digits) for i in range(20)]
        salt = ''.join(salt)

        b_pw = bytes(pw, "utf-8")
        b_salt = bytes(salt, "utf-8")
        hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 10).hex()

        mail = db.select_mail(id)
        mail = mail[0]
        result = db.pw_updata(hashed_pw,salt,id)
        
        mail_pdf.henkou_mail(mail)
        session.pop("id",None)


        return render_template("pw_reset.html", result=result)

    else:
        return render_template("reset.html",error="同じパスワードを入力してください")





#トップページ
@app.route("/top", methods=["post"])
def top():
    id = request.form.get("id")
    pw = request.form.get("pw")

    result = db.login(id, pw)

    if result != None:

        session["user"] = True
        session["data"] = result

        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=365)

        count = 0
        session["count"] = count

        result = db.product()

        clas = db.product_class()

        return render_template("top.html",product=result, clas=clas)
    else:
        return redirect(url_for("login", error="ログイン失敗"))

#学生トップページ(画面遷移)
@app.route("/top", methods=["get"])
def tops():
    if "user" in session:
        result = db.product()

        clas = db.product_class()
        return render_template("top.html",product=result, clas=clas)
    else:
        return redirect("/")

#学生トップページ(検索結果)
@app.route("/top2", methods=["get"])
def top2():
    if "user" in session:
        name = request.args.get("name")
        clas = request.args.get("clas")

        if clas == "":
            if name == "":
                result = db.product()
            else:
                result = db.name_product(name)

        else:
            if name == "":
                result = db.clas_product(clas)
            else:
                result = db.name_clas_product(name,clas)


        clas = db.product_class()

        return render_template("top2.html",product=result, clas=clas)
    else:
        return redirect("/")

@app.route("/syousai", methods=["get"])
def syousai():
    if "user" in session:
        name = request.args.get("name")

        result = db.select_product(name)
        data = result[3]
        data = data.replace("\n", "<br>")

        return render_template("syousai.html",product=result,data=data)
    else:
        return redirect("/")

@app.route("/add", methods=["get"])
def add():
    if "user" in session:
        no = request.args.get("no")
        name = request.args.get("name")
        price = request.args.get("price")
        cla = request.args.get("cla")
        cnt = request.args.get("cnt")


        if not "cart" in session:
            product_list = []
            point = int(price) * int(cnt) //100
            
            count = session["count"]

            product_list.append([no,name,cla,int(price),int(cnt),point,count])
            count += 1
            session["count"] =count
            session["cart"] = product_list
        else :
            product_list = session.pop("cart", None)
            point = int(price) * int(cnt) //100
            count = session["count"]
            product_list.append([no,name,cla,int(price),int(cnt),point,count])
            count += 1
            session["count"] =count
            session["cart"] = product_list

        
        result = db.select_product(name)
        data = result[3]
        data = data.replace("\n", "<br>")
        return render_template("syousai.html",product=result,data=data)
    else:
        return redirect("/")


#おすすめ商品
@app.route("/osusume")
def osusume():
    if "user" in session:
        result = db.select_osusume()

        data = session["data"]
        id =data[0]
        u_osusume = db.select_user_osusume(id)

        u_osusume = list(u_osusume)
        random.shuffle(u_osusume)
        u_osusume_list = []
        for i in range(5):
            u_osusume_list.append(u_osusume[i])

        return render_template("osusume.html",osusume=result,u_osusume=u_osusume_list)
    else:
        return redirect("/")

#おすすめ商品詳細
@app.route("/syousai1", methods=["get"])
def syousai1():
    if "user" in session:
        name = request.args.get("name")

        result = db.select_product(name)
        data = result[3]
        data = data.replace("\n", "<br>")

        return render_template("syousai1.html",product=result,data=data)
    else:
        return redirect("/")

@app.route("/cart")
def cart():
    if "user" in session:
        if "cart" in session:
            product_list = session["cart"]

            return render_template("cart.html",product_list=product_list)
        else:
            return render_template("cart2.html")
    else:
        return redirect("/")

@app.route("/pop")
def pop():
    if "user" in session:
        if "cart" in session:
            count = request.args.get("count")
            count = int(count)
            product_list = session["cart"]

            l = list(product_list)

            l.pop(count)

            count = 0
            product_list = []

            for i in l:
                i[6] = count
                product_list.append(i)
                count += 1

            if product_list == []:
                session.pop("cart",None)
                session["count"] = count
                return redirect(url_for("cart"))
            else:
                session["cart"] = product_list
                session["count"] = count
                return render_template("cart.html",product_list=product_list)
        else:
            return render_template("cart2.html")
    else:
        return redirect("/")


@app.route("/syousai2", methods=["get"])
def syousai2():
    if "user" in session:
        name = request.args.get("name")
        cnt = request.args.get("cnt")

        result = db.select_product(name)
        data = result[3]
        data = data.replace("\n", "<br>")

        return render_template("syousai2.html",product=result,data=data,cnt=cnt)
    else:
        return redirect("/")


@app.route("/kounyu", methods=["get"])
def kounyu():
    if "user" in session:
        product_list=session["cart"]
        prices = 0
        cnts = 0
        points = 0
        for i in product_list:

            prices += i[3] * i[4]
            cnts += i[4]
            points += i[5]

        return render_template("kounyu.html",product_list=session["cart"],prices=prices,cnts=cnts,points=points)
    else:
        return redirect("/")

@app.route("/point", methods=["post"])
def point():
    if "user" in session:
        prices = request.form.get("prices")
        cnts = request.form.get("cnts")
        points = request.form.get("points")
        data = session["data"]
        point = data[5]

        return render_template("point.html",point=point,prices=prices,cnts=cnts,points=points)
    else:
        return redirect("/")
        
@app.route("/last", methods=["post"])
def last():
    if "user" in session:
        prices = request.form.get("prices")
        prices = int(prices)
        cnts = request.form.get("cnts")
        points = request.form.get("points")
        u_point = request.form.get("u_point")
        data = session["data"]
        product_list = session["cart"]
        point = data[5]

        if u_point == "1":
            if prices < point:
                pointer = prices
            else:
                pointer = point
                pointer = int(pointer)

        else:
            pointer = request.form.get("pointer")
            pointer = int(pointer)
            if prices < pointer:
                pointer = prices
            else:
                pass

        price = prices - pointer

        return render_template("last.html",prices=prices,cnts=cnts,points=points,pointer=pointer,data=data,product_list=product_list,price=price)
    else:
        return redirect("/")

@app.route("/last2", methods=["post"])
def last2():
    if "user" in session:
        prices = request.form.get("prices")
        cnts = request.form.get("cnts")
        points = request.form.get("points")
        pointer = request.form.get("pointer")
        price = request.form.get("price")
        
        data = session["data"]
        product_list = session["cart"]

        mail_pdf.send_mail(data,price,product_list)

        id = data[0]
        point = data[5]

        point = point - int(pointer)

        db.updata_point(point,id)

        points = int(points) + point

        db.updata_point(points,id)
        session["data"] = (id,data[1],data[2],data[3],data[4],points)
        db.insert_history(id,product_list)
        
        product_list = session.pop("cart",None)
        session.pop("count",None)
        count = 0
        session["count"] = count
        return render_template("last2.html")
    else:
        return redirect("/")



@app.route("/user")
def user():
    if "user" in session:
        data = session["data"]
        return render_template("user.html",data=data)
    else:
        return redirect("/")

@app.route("/account")
def account():
    if "user" in session:
        data = session["data"]

        zyusyos = data[4]
        if "県" in zyusyos:
            s = zyusyos.split('県')
            ken = s[0] + "県"
            zyusyo = s[1]
        elif "道" in zyusyos:
            s = zyusyos.split('道')
            ken = s[0] + "道"
            zyusyo = s[1]
        elif "府" in zyusyos:
            s = zyusyos.split('府')
            ken = s[0] + "府"
            zyusyo = s[1]
        elif "東京" in zyusyos:
            s = zyusyos.split('都')
            ken = s[0] + "都"
            zyusyo = s[1]
        

        list = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県",
                "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山形県","長野県",
                "岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
                "鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県",
                "佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
        return render_template("account.html",data=data,list=list,ken=ken,zyusyo=zyusyo)
    else:
        return redirect("/")

@app.route("/account2", methods=["post"])
def account2():
    if "user" in session:
        data = session["data"]

        id = request.form.get("id")
        name = request.form.get("name")
        mail = request.form.get("mail")
        point = data[5]
        zip = request.form.get("zip")
        ken = request.form.get("ken")
        zyusyo = request.form.get("zyusyo")
        zyusyos = ken + zyusyo
        
        mail_pdf.account_mail(mail,name)
        db.update_account(mail,zip,zyusyos,id)
        session.pop("data", None)
        session["data"] = (id,name,mail,zip,zyusyos,point)
        data = session["data"]

        return render_template("user.html",data=data)
    else:
        return redirect("/")

#購入履歴
@app.route("/history")
def history():
    if "user" in session:
        data = session["data"]
        id = data[0]
        result = db.select_history(id)
        return render_template("history.html",history=result)
    else:
        return redirect("/")

#ログアウト
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)