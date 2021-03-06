

from helpers import *
from caesar import rotate_string

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

import cgi
 

app = Flask(__name__ )
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
 
app.secret_key = "y337kGcys&zP3B"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10))
    password = db.Column(db.String(20))    
    blogs = db.relationship("Blog", backref="owner")
    
    def __init__(self, user_name, password):
        self.user_name=user_name  
        self.password=password
         
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    removed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, removed, owner):
        self.title = title
        self.body = body
        self.removed = removed
        self.owner = owner










# Web Casear

form = """<!DOCTYPE html>
<html>
    <head>
        <style>
            form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }}
            textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;   
            }}
              
            .error {{color: red; }}

            p {{
                color:red;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
         }}

            div {{
                color:green;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
         }}

           span {{
                color:green;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
         }}
        </style>
          
    </head>
    <body>  

    <form action="/encrypt_post", method="POST" >
        <a href='/'>Return to Home Page</a> <br> <br>
        <label>
            
            Rotate by
            <input type="text" value="0" name="rot"/>
         </label>
         <p class="error"> </p>
         <textarea placeholder="Enter text here" name="text"   >{0}</textarea>
          
         <input type="submit" value="Submit Query">
         
    
    </form>

"""

jeop = """<!DOCTYPE html>
<html>
    <head>
    <style>
        .msg {
    
                color:blue;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
                
                }
          
         
    
    </style>
        
    </head>
    
    <body>

    <form action="/encrypt" methopd="POST">
        
        <span class="msg"> We're waiting for your input &#9786 </span>
        <br>
        <span class="msg">Press the pause button when you're tired of hearing the music</span>
        <div class="msg">
            <iframe width="420" height="315"
                   src="https://www.youtube.com/embed/anmdGj2v2WI?autoplay=1&loop=1&playlist=anmdGj2v2WI">
            </iframe>
                  
        </div>
        
        
    </form>
    </body>
 
</html>
 """
def is_integer(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

@app.before_request
def require_login():  #for blogz
     
    allowed_routes = ["login","static", 'show_a_users_posts', 'post','reqs' , "signup","encrypt_post", "encrypt_get", "index","all_users", "blog"]
     
    if request.endpoint not in allowed_routes and "user_name" not in session:
        return redirect("/login" )

@app.route("/")
def index():
     return  render_template("base.html")


@app.route("/encrypt_get")
def encrypt_get():
     return  form.format("")+ jeop
 
@app.route("/encrypt_post" , methods=["POST"])
def encrypt_post():

     
    the_text=(request.form['text'])
    the_rot = (request.form['rot'])

    if is_integer(the_rot) and int(the_rot) > 0:
     
        answer = rotate_string(the_text,int(the_rot))
         
        return  form.format(answer) + "<br>" + "<div>Success!! - Ok to deliver the message <br> <br>Please Feel free to encrypt another message </div>" + jeop
    else:
        return form.format("") + "<p>Invalid Rotate by Entry - It must be an integer greater than zero</p>" + jeop


#Blogz



@app.route('/all_users', methods=['POST', 'GET'])
def all_users():
    # render list of all blog user ids
    post = User.query.all()
    return  render_template("index.html", post=post, page_title="blog users!", title="Blogz R Us")

@app.route("/Reqs", methods = ["GET", "POST"])
def reqs():
  return render_template("input_req.html", title="Blogz Signup Requirements")


@app.route('/signup', methods=['POST', 'GET'])
def signup():

     if request.method == "POST":
         input_error = False
         un_message = ""
         pw_message = ""
         vp_message = ""
          
     
         user_Name = cgi.escape(request.form["user_name"], quote = True)
         p_Word = cgi.escape(request.form["p_word"], quote = True)
         ver_P_Word = cgi.escape(request.form["ver_password"],quote = True)
     
         if check_user_name(user_Name) == False:
            un_message =  "That is not a valid username"
            input_error = True

         if check_pass_word(p_Word ) == False:
            pw_message =     "That is not a valid password"
            input_error = True
     
         if verify_pass_word(p_Word, ver_P_Word) == False:
            vp_message =   "The passwords do not match"
            input_error = True

         if input_error:
            
            return render_template("signup.html" , title="Sign up for Blogz", un_error = un_message, pw_error = pw_message, vp_error = vp_message, uName = user_Name )
         else:

            existing_user=User.query.filter_by(user_name=user_Name).first()
            
            if not existing_user:
                 new_user=User(user_Name,p_Word)
                 db.session.add(new_user)
                 db.session.commit()
                 user_id=new_user.id  # capture id for rendering of users very first post
                 session["user_name"] = user_Name
                 session["user_id"] = user_id
                 
                 print("")
                 print("THE ID OF THE NEW USER IS = ", user_id)
                 print("")
                 return redirect("/newpost")
            else:
                 flash("User ID already exists", "error")  
     
     return  render_template("signup.html", title="Sign up for Blogz" )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form["user_name"]
        password = request.form["password"]
        users = User.query.filter_by(user_name=user_name)
        user=users.first()
        if users.count() != 1:
            flash('User name does not exist', "error")
            return redirect("/login")
        elif password != user.password:
            flash('Incorrect password', "error")
            return redirect("/login")
        else:
            
            session['user_name'] = user.user_name
            session['user_id'] = user.id
            flash('welcome back,  ' + user.user_name)
            return redirect("/newpost")
             
    return  render_template("login.html",title="Log in to Blogz R Us")


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user_name']
    return  redirect("/Blog")

@app.route('/Blog', methods=['POST', 'GET'])
def blog():

   
    page_title = "blog posts!"
    post = Blog.query.filter_by(removed = False).order_by(Blog.id.desc()).all()
    
    return render_template('blog.html',title="Blogs R Us!", 
        post=post, page_title = page_title)  


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
     
    owner = User.query.filter_by(user_name = session["user_name"]).first()
    if request.method == 'POST':
         
        add_body = request.form['body']
        add_title = request.form['title']
        add_removed = False

        owner = User.query.filter_by(user_name = session["user_name"]).first()
        user_name = session["user_name"]
        user_id = session["user_id"]
        new_post = Blog(add_title,add_body, add_removed,owner)
        db.session.add(new_post)
        db.session.commit()
        
        return render_template("show_post.html", title="Add post to Blogz R Us!", post_title = add_title, post_body = add_body, user_name = user_name,user_id = user_id, page_title = "")
    
   
    
    add_body="post"
    add_title="title"    
    add_removed = False
    return render_template("add_new_post.html", title="Add post to Blogz R Us!", page_title = "new post",post_title=add_title,body=add_body)
    



@app.route('/show_post', methods=['POST', 'GET'])
def post():
    # show the post of a registered user just entered or a visitor clicked on
    post_title = request.args.get("post_title")
    post_body = request.args.get("post_body")
    user_name = request.args.get("user_name")
    post_id = request.args.get("user_id")
    print("POST ID = ", post_id)
    print("USER NAME ID = ", user_name)
    return render_template('show_post.html',title="Blogz R Us", post_title= post_title, post_body=post_body,user_name=user_name,user_id=post_id )
    

@app.route('/show_a_users_posts', methods=['POST', 'GET'])
def show_a_users_posts():
    # show all the posts from a specific user
    user_name = request.args.get("user_name")
    user_id = request.args.get("user_id")
     
    
    # posts=Blog.query.filter_by(owner_id=user_id).all()
    posts = Blog.query.filter_by(removed = False,owner_id=user_id).order_by(Blog.id.desc()).all()
    return render_template('show_a_users_posts.html',title="The posts you wanted to see",  posts=posts   ) #user_name=user_name, 




@app.route('/remove_post', methods=['POST'])
def remove_post(): 
    # user remove a specific post
    post_id = int(request.form['post_id'])
    post = Blog.query.get(post_id)
    post.removed = True
    db.session.add(post)
    db.session.commit()

    removed_post = Blog.query.get(post_id)
    removed_post_title = removed_post.title
    removed_post_body = removed_post.body
    return render_template('/remove_post.html', removed_post_title=removed_post_title,removed_post_body=removed_post_body, page_title = "Archived Post" )

@app.route('/archives', methods=['POST', 'GET'])
def archives():
    # show all the archived posts
    
    archived_post = Blog.query.filter_by(removed = True).order_by(Blog.id.desc()).all()
    return render_template('archived_posts.html',title="Blogs R Us!", 
        archived_post=archived_post, page_title = "Archived Posts")



if __name__ == '__main__':
    app.run()

 