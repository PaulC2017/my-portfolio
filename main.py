# Web Casear

from flask import Flask, request, redirect 
from caesar import rotate_string

 

app = Flask(__name__ )
app.config['DEBUG'] = True

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

    <form action="/encrypt", method="POST" >
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

@app.route("/encrypt")
def index():
     return  form.format("")+ jeop
 

@app.route("/encrypt" , methods=["POST"])
def encrypt():

     
    the_text=(request.form['text'])
    the_rot = (request.form['rot'])

    if is_integer(the_rot):
     
        answer = rotate_string(the_text,int(the_rot))
         
        return  form.format(answer) + "<br>" + "<div>Success!! - Ok to deliver the message <br> <br>Please Feel free to encrypt another message </div>" + jeop
    else:
        return form.format("") + "<p>Invalid Rotate by Entry - It must be an integer</p>" + jeop



app.run()