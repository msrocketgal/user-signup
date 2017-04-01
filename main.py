import webapp2
import cgi
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>

<head>
    <style type="text/css">
        .error {
            color: red;
            }
        td {
            text-align: left;
            padding: 5px;
        }
    </style>
</head>
<body>

"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

#create functions to validate user input
def valid_username(username):
    user_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return user_RE.match(username)

def valid_password(password):
    password_RE = re.compile(r"^.{3,20}$")
    return password_RE.match(password)

def valid_email(email):
    email_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return email_RE.match(email)


def getErrMsgs(errCode):
    """ accept error code parameter that is 4 digits in length; any digit other than zero indicates a specific error
        build a list of error messages based on digits in error code"""
    errMsgs = []

    if int(errCode[0]) > 0:
        uNameErr = "Please enter a valid Username"
    else:
        uNameErr = ""

    if int(errCode[1]) > 0:
        pWordErr = "Please enter a valid Password"
    else:
        pWordErr = ""

    if int(errCode[2]) > 0:
        vPWordErr = "Your Passwords do not match"
    else:
        vPWordErr = ""

    if int(errCode[3]) > 0:
        eMailAddrErr = "Please enter a valid Email address"
    else:
        eMailAddrErr = ""

    errMsgs = [uNameErr,pWordErr,vPWordErr,eMailAddrErr]

    return(errMsgs)


def build_form(errCode='0000', uName='', eMail=''):
    """ build a form for allowing user to signup for site """

    #call getErrMsgs fucntion to break error code out into specific error messages for use in building form
    errMsgs = getErrMsgs(errCode)
    uNameErr = str(errMsgs[0])
    pWordErr = str(errMsgs[1])
    vPWordErr = str(errMsgs[2])
    eMailAddrErr = str(errMsgs[3])

    #create variables containing sections of a form that can be concatenated to build an entire form
    form_top = """
    <form action="/" method="post">
        <table style:width="100%">
        <h1>Signup</h1>"""

    form_field1 = """
            <tr>
                <td><label>Username</td></label>
                <td><input type='text' name='uName' required value='""" + uName + """' >
                <span class=error>{0}</span><br></td>
            </tr>""".format(uNameErr)

    form_field2 = """
            <tr>
                <td><label>Password</td></label>
                <td><input type="password" name="pWord" required value="" >
                <span class=error>{0}</span><br></td>
            </tr>""".format(pWordErr)

    form_field3 = """
            <tr>
                <td><label>Verify Password</td></label>
                <td><input type="password" name="vPWord" required value="" >
                <span class=error>{0}</span><br></td>
            </tr>""".format(vPWordErr)

    form_field4 = """
            <tr>
                <td><label>Email (optional)</td></label>
                <td><input type="email" name="eMailAddr" value='""" + eMail + """' >
                <span class=error>{0}</span><br></td>
            </tr>""".format(eMailAddrErr)

    form_bottom = """
        </table>
        <input type="submit" value="Submit"/>
        <br>
    </form>"""

    new_form = form_top + form_field1 + form_field2 + form_field3 + form_field4 + form_bottom
    return new_form


class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site) """

    def get(self):
        signup_form = build_form()
        content = page_header + signup_form + page_footer
        self.response.write(content)

    def post(self):
        u_Name = self.request.get("uName")
        p_Word = self.request.get("pWord")
        v_PWord = self.request.get("vPWord")
        eMail_Addr = self.request.get("eMailAddr")

        # 'escape' the user's input so that if they typed HTML, it doesn't hack our site
        esc_u_Name = cgi.escape(u_Name, quote=True)
        esc_p_Word = cgi.escape(p_Word, quote=True)
        esc_v_PWord = cgi.escape(v_PWord, quote=True)
        esc_eMail_Addr = cgi.escape(eMail_Addr, quote=True)

        # validate user input and build 4-digit error code
        errCode = ""

        if not valid_username(esc_u_Name):
            errCode = "1"
        else:
            errCode = "0"

        if not valid_password(esc_p_Word):
            errCode += "1"
        else:
            errCode += "0"

        if esc_v_PWord != esc_p_Word:
            errCode += "1"
        else:
            errCode += "0"

        if esc_eMail_Addr != "" and not valid_email(esc_eMail_Addr):
            errCode += "1"
        else:
            errCode += "0"

        #if errors exist, redirect user to form & provide error messages
        if errCode != "0000":
            error_form = build_form(errCode, esc_u_Name, esc_eMail_Addr)
            content = page_header + error_form + page_footer
            self.response.write(content)
        else:
            self.redirect('/Welcome?uName=' + esc_u_Name)


class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to /Welcome """
    def get(self):
        welcomeName = self.request.get("uName")
        content = "<h1>Welcome, " + welcomeName + "!</h1>"
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', Welcome),
], debug=True)
