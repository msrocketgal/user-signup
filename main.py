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
            text-align:right
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


class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site) """

    def get(self, uNameErr="", pWordErr="", vPWordErr="", eMailAddrErr=""):

        edit_header = "<h3>Signup</h3>"

        # a form for allowing user to signup for site
        signup_form = """
        <form action="/welcome" method="post">
            <table style:width="100%">
                <tr>
                    <td><label>Username</td>
                    <td><input type="text" name="uName"/></label></td>
                    <td><div class=error>{0}</div><br></td>
                </tr>

                <tr>
                    <td><label>Password</td>
                    <td><input type="text" name="pWord"/></label></td>
                    <td><div class=error>{1}</div><br></td>
                </tr>

                <tr>
                    <td><label>Verify Password</td>
                    <td><input type="text" name="vPWord"/></label></td>
                    <td><div class=error>{2}</div><br></td>
                </tr>

                <tr>
                    <td><label>Email (optional)</td>
                    <td><input type="text" name="eMailAddr"/></label></td>
                    <td><div class=error>{3}</div><br></td>
                </tr>
            </table>
            <input type="submit" value="Submit"/>
            <br>
        </form>
        """.format(uNameErr, pWordErr, vPWordErr, eMailAddrErr)

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''

        # combine all the pieces to build the content of our response
        content = page_header + edit_header + signup_form + error_element + page_footer
        self.response.write(content)


class AddUser(webapp2.RequestHandler):
    """ Validate User Info and take User to Welcome page after successfully signing up for site """

    def post(self):
        # look at input in signup_form to validate what user entered
        u_Name = self.request.get("uName")
        p_Word = self.request.get("pWord")
        v_PWord = self.request.get("vPWord")
        eMail_Addr = self.request.get("eMailAddr")


        #uNameErr = "Please enter a valid Username"
        #pWordErr = "Please enter a valid Password"
        #vPWordErr = "Your Passwords do not match"
        #eMailAddrErr = "Please enter a valid Email address"

        # TODO 1
        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site



        # TODO 2
        # if the user typed nothing at all, redirect and yell at them



        # TODO 3
        # if the user wants to add a terrible movie, redirect and yell at them




        # build response content
        content = "<h2>Welcome, " + u_Name + "!</h2>"
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', AddUser),
], debug=True)
