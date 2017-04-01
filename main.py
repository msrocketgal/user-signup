#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
user_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_RE = re.compile(r"^.{3,20}$")
email_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return user_RE.match(username)

def valid_password(password):
    return password_RE.match(password)

def valid_email(email):
    return email_RE.match(email)

def build_form(uNameErr="",pWordErr="",vPWordErr="",eMailAddrErr="", uName="", pWord="", vPWord="", eMail=""):
    # a form for allowing user to signup for site
    form_hdr = """
    <form action="/" method="post">
        <table style:width="100%">
        <h1>Signup</h1>"""

    form_field1 = """
            <tr>
                <td><label>Username</td>
                <td><input type='text' name='uName' value=""" + uName + """ ></label></td>
                <td><div class=error>{0}</div><br></td>
            </tr>""".format(uNameErr)

    form_field2 = """
            <tr>
                <td><label>Password</td>
                <td><input type="text" name="pWord" value=""" + pWord + """ ></label></td>
                <td><div class=error>{0}</div><br></td>
            </tr>""".format(pWordErr)

    form_field3 = """
            <tr>
                <td><label>Verify Password</td>
                <td><input type="text" name="vPWord" value=""" + vPWord + """ ></label></td>
                <td><div class=error>{0}</div><br></td>
            </tr>""".format(vPWordErr)

    form_field4 = """
            <tr>
                <td><label>Email (optional)</td>
                <td><input type="text" name="eMailAddr" value=""" + eMail + """ ></label></td>
                <td><div class=error>{0}</div><br></td>
            </tr>""".format(eMailAddrErr)

    form_ftr = """
        </table>
        <input type="submit" value="Submit"/>
        <br>
    </form>"""

    new_form = form_hdr + form_field1 + form_field2 + form_field3 + form_field4 + form_ftr
    return new_form

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site) """

    def get(self, uNameErr="", pWordErr="", vPWordErr="", eMailAddrErr=""):

        #edit_header = "<h1>Signup</h1>"

        signup_form = build_form()

        # combine all the pieces to build the content of our response
        content = page_header + signup_form + page_footer
        self.response.write(content)


    def post(self):
        u_Name = self.request.get("uName")
        p_Word = self.request.get("pWord")
        v_PWord = self.request.get("vPWord")
        eMail_Addr = self.request.get("eMailAddr")

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        esc_u_Name = cgi.escape(u_Name, quote=True)
        esc_p_Word = cgi.escape(p_Word, quote=True)
        esc_v_PWord = cgi.escape(v_PWord, quote=True)
        esc_eMail_Addr = cgi.escape(eMail_Addr, quote=True)

        # validate user input and build error message as needed
        errFlag = False

        if not valid_username(esc_u_Name):
            uNameErr = "Please enter a valid Username"
            errFlag = True
        else:
            uNameErr = ""

        if not valid_password(esc_p_Word):
            pWordErr = "Please enter a valid Password"
            errFlag = True
        else:
            pWordErr = ""

        if esc_v_PWord != esc_p_Word:
            vPWordErr = "Your Passwords do not match"
            errFlag = True
        else:
            vPWordErr = ""

        if esc_eMail_Addr != "" and not valid_email(esc_eMail_Addr):
            eMailAddrErr = "Please enter a valid Email address"
            errFlag = True
        else:
            eMailAddrErr = ""

        #if errors exist, redirect user to form & provide error messages
        if errFlag:
            #edit_header = "<h1>Signup</h1>"
            error_form = build_form(uNameErr, pWordErr, vPWordErr, eMailAddrErr, esc_u_Name, esc_p_Word, esc_v_PWord, esc_eMail_Addr)
            content = page_header + error_form + page_footer
            self.response.write(content)
        else:
            welcomeForm = """
            <form action="/Welcome" method="post">"""
            content = page_header + welcomeForm + "<h2>Welcome, " + u_Name + "!</h2>" + page_footer
            self.response.write(content)


class WelcomeUser(webapp2.RequestHandler):
    """ Handles requests coming in to /WelcomeUser """
    def get(self):
        #u_Name = self.request.get("uName")
        welcomeForm = """
        <form action="/Welcome" method="post">"""
        content = page_header + welcomeForm + "<h2>Welcome, " + u_Name + "!</h2>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Welcome', WelcomeUser),
], debug=True)
