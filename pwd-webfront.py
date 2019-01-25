from flask import Flask, render_template, request
import random
import execnet

#allow python3.6 to call pythhon2.7 as ldap3 is not python3 compatible...yet...
def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()

app=Flask(__name__)

with open("nouns.txt") as noun_file:
    nouns=noun_file.read().split()
with open("adjectives.txt") as adj_file:
    adjs=adj_file.read().split()

##for user late:
#        password=random.choice(adjs)+random.choice(nouns)

@app.route("/",methods=['GET'])
def index():
    if request.method=='GET':
        return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    if request.method=='POST':
        username=request.headers.get('REMOTE_USER')
#        username='tempuser'
        newpassword=request.form["newPassword"]
        renewpassword=request.form["reEnterNewPassword"]
        if newpassword==renewpassword:
            result=call_python_version("2.7","pwdmgr","passwordChange",[username,newpassword])
            return render_template("submit.html",result=result)
        else:
            return render_template("error.html")


@app.route("/admin", methods=['GET'])
def admin():
    if request.method=='GET':
        return render_template("admin.html")

@app.route("/adminsubmit", methods=['POST'])
def adminsubmit():
    if request.method=='POST':
#        requester=request.headers.get('REMOTE_USER')
        username=request.form["aduser"]
        result=call_python_version("2.7","pwdmgr","passwordReset",[username])
        return render_template("adminsubmit.html",result=result)

if __name__ == '__main__':
    app.debug=True
    app.run()
