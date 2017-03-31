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
email_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return user_RE.match(username)

def valid_password(password):
    return password_RE.match(password)

def valid_email(email):
    return email_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site) """

    def get(self, uNameErr="", pWordErr="", vPWordErr="", eMailAddrErr=""):

        edit_header = "<h1>Signup</h1>"

        # a form for allowing user to signup for site
        signup_form_hdr = """
        <form action="/AddUser" method="post">
            <table style:width="100%">"""

        signup_form_field1 = """
                <tr>
                    <td><label>Username</td>
                    <td><input type="text" name="uName"/></label></td>
                    <td><div class=error>""" + self.request.get("uNameErr") + """</div><br></td>
                </tr>"""

        signup_form_field2 = """
                <tr>
                    <td><label>Password</td>
                    <td><input type="text" name="pWord"/></label></td>
                    <td><div class=error>""" + self.request.get("pWordErr") + """</div><br></td>
                </tr>"""

        signup_form_field3 = """
                <tr>
                    <td><label>Verify Password</td>
                    <td><input type="text" name="vPWord"/></label></td>
                    <td><div class=error>""" + self.request.get("vPWordErr") + """</div><br></td>
                </tr>"""

        signup_form_field4 = """
                <tr>
                    <td><label>Email (optional)</td>
                    <td><input type="text" name="eMailAddr"/></label></td>
                    <td><div class=error>""" + self.request.get("eMailAddrErr") + """</div><br></td>
                </tr>"""

        signup_form_ftr = """
            </table>
            <input type="submit" value="Submit"/>
            <br>
        </form>"""

        signup_form = signup_form_hdr + signup_form_field1 + signup_form_field2 + signup_form_field3 + signup_form_field4 + signup_form_ftr


        # combine all the pieces to build the content of our response
        content = page_header + edit_header + signup_form + page_footer
        self.response.write(content)


class AddUser(webapp2.RequestHandler):
    """ Handles requests coming in to /AddUser """
    def post(self):
    # look at input in signup_form to validate what user entered
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

        if not valid_email(esc_eMail_Addr):
            eMailAddrErr = "Please enter a valid Email address"
            errFlag = True
        else:
            eMailAddrErr = ""

        #if errors exist, redirect user to form & provide error messages
        if errFlag:
            self.redirect("/?uNameErr=" + uNameErr, "pWordErr=" + pWordErr, "vPWordErr=" + vPWordErr, "eMailAddrErr=" + eMailAddrErr)
        else:
            # build response content
            content = "<h2>Welcome, " + u_Name + "!</h2>"
            self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/AddUser', AddUser),
], debug=True)
