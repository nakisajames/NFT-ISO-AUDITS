from JailuApp.classes.base_structures import *
from JailuApp.models import UserAccount, UserSetting


class TableSecurityActions(TableObjectBase):
    # table specific settings
    object_name = 'security_action'

    # field settings
    fields = {
        "user_name": TableFieldBase(object_name, 'user_name', InputTypes.TEXT.code, ValidationTypes.INT.code
                             , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: False}
                             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
                             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "password": TableFieldBase(object_name, 'password', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True}
                                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})

    }

    def check_login(self):
        api_response = {"error": False, "error_msg": "Validation Failed"}

        if is_empty(self.fields["user_name"].current_value) is True:
            api_response["error"] = True
            api_response["error_msg"] = "Please Enter Required Field " + self.fields["user_name"].caption
        elif is_empty(self.fields["password"].current_value) is True:
            api_response["error"] = True
            api_response["error_msg"] = "Please Enter Required Field " + self.fields["password"].caption
        else:

            user = UserAccount.objects.filter(user_name=self.fields["user_name"].current_value
                                              , password= enrypt_passwordMd5(self.fields["password"].current_value)).first()
            if user is not None:  # if db login was successful
                Security.save_user_session(user.id)
                api_response["error"] = False
                api_response["error_msg"] = "Logged In successfully"
            else:
                api_response["error"] = True
                api_response["error_msg"] = "Invalid Username or Password "
        return api_response

    def user_logged_in(self):
        api_response = {"error": False, "error_msg": "Logged In successfully"}
        # other after effects
        # perform logging
        record_system_log(self.object_name, None, "login", "User Logged In", "User Logged In")
        return api_response

    def submit_login(self):
        api_response = self.check_login()
        if api_response["error"] is True:
            # perform logging
            record_system_log(self.object_name, None, "login", "User Logged In Failed", api_response["error_msg"])
            return api_response
        api_response = self.user_logged_in()

        return api_response

    def log_out(self):
        api_response = {"error": False, "error_msg": "Logged Out successfully"}
        # perform logging
        record_system_log(self.object_name, None, "logout", "User Logged Out", "User Logged Out")
        # delete user from session
        Security.clear_user_session()
        # other after effects


        return api_response

    def user_logged_out(self):
        api_response = {"error": False, "error_msg": "Logged Out successfully"}
        # other after effects
        # perform logging
        return api_response

    def submit_logout(self):
        api_response = self.log_out()
        if api_response["error"] is True:  # check insert worked
            return api_response
        api_response = self.user_logged_out()

        return api_response

    def update_user_setting(self):
        api_response = {"error": False, "error_msg": "Operation Completed successfull"}
        # populate model and perform db operation
        obj = UserSetting.objects.get(user_id=str(current_user_id()), name= self.request_data.get("setting_name", ""))
        # specify updates
        obj.value = self.request_data.get("setting_value", "")
        obj.last_modified = current_datetime()
        obj.modified_by_id = current_user_id()
        obj.save()

        return api_response

    def show_forgot_password_form(self):
        api_response = {"error": True, "error_msg": "Unknown API error", "html": ""}

        html = """
        <div class="card border-info" style="margin-bottom: 0px !important;">
        <div class="card-body">
        <div class=''>

        <div class='row'>
        <div class='col-lg-12'>
        <input class="form-control" size="30" id='user_name_email' type='text' value='' placeholder='Enter Username / Email'/>
        </div>
        </div>

        </div>

        </div>
        </div>
         <div class="card-footer" style="display: block;padding: .25rem 0.5rem;">
            <button class="mb-2 mr-2 btn-icon btn btn-success" onclick="SubmitForgotPasswordRequest(this)">
                <i class="fas fa-paper-plane btn-icon-wrapper"> </i>Submit
            </button>
            <button class="mb-2 mr-2 btn-icon btn btn btn-secondary float-right" onclick="CloseForgotPasswordForm()">
                <i class="fa fa-times btn-icon-wrapper"> </i>Cancel
            </button>
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "completed successfully"
        api_response["html"] = html

        return api_response


    def show_forgot_password_confirm_form(self):
        api_response = {"error": True, "error_msg": "Unknown API error", "html": ""}
        html = """"""
        find_by_username = UserAccount.objects.filter(user_name=str(self.request_data.get("user_name_email","")))
        find_by_email = UserAccount.objects.filter(primary_email=str(self.request_data.get("user_name_email","")))
        if is_empty(self.request_data.get("user_name_email",None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "PLease Enter your Username / Email Address"
        elif find_by_username.count() == 0 and find_by_email.count() == 0 :
            api_response["error"] = True
            api_response["error_msg"] = "No Account found with that username or email address"
        elif find_by_email.count() > 1:
            api_response["error"] = True
            api_response["error_msg"] = "This email belongs to more than one account, please provide your username instead"
        else:
            obj = None
            if find_by_username.count() > 0:
                obj = find_by_username[0]
            elif find_by_email.count() > 0:
                obj = find_by_email[0]
            else:
                api_response["error"] = True
                api_response["error_msg"] = "Error: Could not identify account to use"
            new_otp = generate_otp()
            verification_code = enrypt_passwordMd5(str(new_otp + obj.id))
            html = """
            <div class="card border-info" style="margin-bottom: 0px !important;">
            <div class="card-body">
            <div class=''>
    
            <div class='row'>
            <input hidden id='user_name_email' type='text' value='""" + str(self.request_data.get("user_name_email","")) + """' />
            <input hidden id='fp_code_hash' type='text' value='""" + str(verification_code) + """' />
            <div class='col-lg-12'>
            <input class="form-control" size="30" id='fp_verify_code' type='text' value='' placeholder='Enter Verification Code'/>
            </div>
            </div>
    
            </div>
    
            </div>
            </div>
             <div class="card-footer" style="display: block;padding: .25rem 0.5rem;">
                <button class="mb-2 mr-2 btn-icon btn btn-success" onclick="ConfirmForgotPasswordCRequest(this)">
                    <i class="fas fa-paper-plane btn-icon-wrapper"> </i>Confirm
                </button>
                <button class="mb-2 mr-2 btn-icon btn btn btn-secondary float-right" onclick="CloseForgotPasswordForm()">
                    <i class="fa fa-times btn-icon-wrapper"> </i>Cancel
                </button>
            </div>
            </div>
            """

            # send email notification
            email_subject = "Requesting Password Reset"
            email_link_to_follow = EW.notification_click_url + ""
            email_full_names = obj.full_name
            email_to_address = [obj.primary_email]
            email_body_content = """
                                            You have requested a <strong>password reset</strong> for your """ + Lang.phrase("site_title") + """ Account , please use the verification code below. 
                                             <br/>Verification code:<strong>""" + str(new_otp) + """</strong>
                                             <br/>
                                            """
            email_body_plain_text = """
                                            <div style="margin-bottom:14pt; margin-top:14pt">
                                            Dear """ + email_full_names + """,</div>
                                            <div style="margin-bottom:14pt; margin-top:14pt">
                                            """ + email_body_content + """
                                            <br />
                                            Best regards!<br />
                                            """ + Lang.phrase("site_title") + """ Team</div>
                                            </div>
                                            """

            email_body_html = template_email()
            # fill in blanks
            email_body_html = email_body_html.replace("[[email_subject]]", email_subject)
            email_body_html = email_body_html.replace("[[email_full_names]]", email_full_names)
            email_body_html = email_body_html.replace("[[email_body_content]]", email_body_content)

            smtp_send_email(email_to_address, email_subject, email_body_plain_text, email_body_html)

            api_response["error"] = False
            api_response["error_msg"] = "A verification code was sent to your email.<br>Please enter it here to confirm"
            api_response["html"] = html

        return api_response

    def confirm_forgot_password_reset(self):
        api_response = {"error": True, "error_msg": "Unknown API error"}

        find_by_username = UserAccount.objects.filter(user_name=str(self.request_data.get("user_name_email", "")))
        find_by_email = UserAccount.objects.filter(primary_email=str(self.request_data.get("user_name_email", "")))
        if is_empty(self.request_data.get("user_name_email", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "PLease Enter your Username / Email Address"
        elif find_by_username.count() == 0 and find_by_email.count() == 0:
            api_response["error"] = True
            api_response["error_msg"] = "No Account found with that username or email address"
        elif find_by_email.count() > 1:
            api_response["error"] = True
            api_response[
                "error_msg"] = "This email belongs to more than one account, please provide your username instead"
        elif is_empty(self.request_data.get("fp_code_hash", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "Confirmation hash is missing"
        elif is_empty(self.request_data.get("fp_verify_code", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "PLease Enter verification code"
        else:
            obj = None
            if find_by_username.count() > 0:
                obj = find_by_username[0]
            elif find_by_email.count() > 0:
                obj = find_by_email[0]
            else:
                api_response["error"] = True
                api_response["error_msg"] = "Error: Could not identify account to use"
            verification_otp = str(self.request_data.get("fp_verify_code", None))

            if self.request_data.get("fp_code_hash", None) != enrypt_passwordMd5(str(verification_otp + obj.id)):
                api_response["error"] = True
                api_response["error_msg"] = "Wrong Confirmation code"
            else:
                #generate and save new password
                new_password = generate_password()
                obj.password = enrypt_passwordMd5(new_password)
                obj.save()

                # send email notification
                email_subject = "Password Reset"
                email_link_to_follow = EW.notification_click_url + ""
                email_full_names = obj.full_name
                email_to_address = [obj.primary_email]
                email_body_content = """
                                Your """ + Lang.phrase("site_title") + """ Account <strong>password</strong> has been reset, please use the credentials below. 
                                 <br/>Link:<a href='""" + str(email_link_to_follow) + """'><strong>""" + str(
                    email_link_to_follow) + """</strong></a>
                                 <br/>Username:<strong>""" + str(obj.user_name) + """</strong>
                                 <br/>Password:<strong>""" + str(new_password) + """</strong>
                                 <br/>
                                """
                email_body_plain_text = """
                                <div style="margin-bottom:14pt; margin-top:14pt">
                                Dear """ + email_full_names + """,</div>
                                <div style="margin-bottom:14pt; margin-top:14pt">
                                """ + email_body_content + """
                                <br />
                                Best regards!<br />
                                """ + Lang.phrase("site_title") + """ Team</div>
                                </div>
                                """

                email_body_html = template_email()
                # fill in blanks
                email_body_html = email_body_html.replace("[[email_subject]]", email_subject)
                email_body_html = email_body_html.replace("[[email_full_names]]", email_full_names)
                email_body_html = email_body_html.replace("[[email_body_content]]", email_body_content)

                smtp_send_email(email_to_address, email_subject, email_body_plain_text, email_body_html)

                api_response["error"] = False
                api_response["error_msg"] = "Password reset successfully, A new password has been send to your email"

        return api_response

    def show_change_password_form(self):
        api_response = {"header_title": self.caption + "s", "content_title": " Change Password",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}

        html = """
        <div class="card border-info" style="margin-bottom: 0px !important;">
        <div class="card-body">
        <div class=''>

        <div class='col-lg-12 row form-group'>
        <div class='col-lg-4'>
        Old Password
        </div>
        <div class='col-lg-8'>
        <input class="form-control" size="30" id='old_password' type='password' value='' placeholder='Enter Old Password'/>
        </div>
        </div>
        
        <div class='col-lg-12 row form-group'>
        <div class='col-lg-4'>
        New Password
        </div>
        <div class='col-lg-8'>
        <input class="form-control" size="30" id='new_password' type='password' value='' placeholder='Enter New Password'/>
        </div>
        </div>
        
        <div class='col-lg-12 row form-group'>
        <div class='col-lg-4'>
        Re-Enter Password
        </div>
        <div class='col-lg-8'>
        <input class="form-control" size="30" id='new_password_2' type='password' value='' placeholder='Re-Enter New Password'/>
        </div>
        </div>

        </div>

        </div>
        </div>
         <div class="card-footer" style="display: block;padding: .25rem 0.5rem;">
            <button class="mb-2 mr-2 btn-icon btn btn-success" onclick="SubmitChangePassword(this)">
                <i class="fas fa-paper-plane btn-icon-wrapper"> </i>Change Password
            </button>
            <button class="mb-2 mr-2 btn-icon btn btn btn-secondary float-right" onclick="window.location.reload();">
                <i class="fa fa-times btn-icon-wrapper"> </i>Cancel
            </button>
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "completed successfully"
        api_response["content_body"] = html

        return api_response


    def confirm_change_password(self):
        api_response = {"error": True, "error_msg": "Unknown API error"}

        find_by_id = UserAccount.objects.filter(id=str(current_user_id()))
        if find_by_id.count() == 0:
            api_response["error"] = True
            api_response["error_msg"] = "You must be logged in to perform this action"
        elif is_empty(self.request_data.get("old_password", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "Please enter old password"
        elif is_empty(self.request_data.get("new_password", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "PLease Enter new password"
        elif is_empty(self.request_data.get("new_password_2", None)) is True:
            api_response["error"] = True
            api_response["error_msg"] = "PLease Re-Enter new password"
        else:
            obj = None
            if find_by_id.count() > 0:
                obj = find_by_id[0]
            else:
                api_response["error"] = True
                api_response["error_msg"] = "Error: Could not identify account to use"

            if obj.password != enrypt_passwordMd5(str(self.request_data.get("old_password", None))):
                api_response["error"] = True
                api_response["error_msg"] = "Incorrect Old password"
            elif str(self.request_data.get("new_password", None)) != str(self.request_data.get("new_password_2", None)):
                api_response["error"] = True
                api_response["error_msg"] = "New password and Re-Entered password do not match"
            else:
                #generate and save new password
                new_password = str(self.request_data.get("new_password", None))
                obj.password = enrypt_passwordMd5(new_password)
                obj.save()

                # send email notification
                email_subject = "Password Changed"
                email_link_to_follow = EW.notification_click_url + ""
                email_full_names = obj.full_name
                email_to_address = [obj.primary_email]
                email_body_content = """
                                Your """ + Lang.phrase("site_title") + """ Account <strong>password</strong> has been changed, please use the credentials below. 
                                 <br/>Link:<a href='""" + str(email_link_to_follow) + """'><strong>""" + str(
                    email_link_to_follow) + """</strong></a>
                                 <br/>Username:<strong>""" + str(obj.user_name) + """</strong>
                                 <br/>Password:<strong>""" + str(new_password) + """</strong>
                                 <br/>
                                """
                email_body_plain_text = """
                                <div style="margin-bottom:14pt; margin-top:14pt">
                                Dear """ + email_full_names + """,</div>
                                <div style="margin-bottom:14pt; margin-top:14pt">
                                """ + email_body_content + """
                                <br />
                                Best regards!<br />
                                """ + Lang.phrase("site_title") + """ Team</div>
                                </div>
                                """

                email_body_html = template_email()
                # fill in blanks
                email_body_html = email_body_html.replace("[[email_subject]]", email_subject)
                email_body_html = email_body_html.replace("[[email_full_names]]", email_full_names)
                email_body_html = email_body_html.replace("[[email_body_content]]", email_body_content)

                smtp_send_email(email_to_address, email_subject, email_body_plain_text, email_body_html)

                api_response["error"] = False
                api_response["error_msg"] = "Password Changed successfully,the new password has been send to your email"

        return api_response

    def perform_action(self, data=None):
        # save request data
        self.request_data = data
        # in case data was passed from a form
        if self.request_data is None:
            self.request_data = dict()
        self.extract_data()

        # perform desired action
        api_response = {"error": True, "error_msg": "Unsupported Operation"}
        if self.request_data["api_action"] == "submit_login":
            api_response = self.submit_login()
        elif self.request_data["api_action"] == "submit_logout":
            api_response = self.submit_logout()
        elif data["api_action"] == "update_user_setting":
            api_response = self.update_user_setting()
        elif data["api_action"] == "show_forgot_password_form":
            api_response = self.show_forgot_password_form()
        elif data["api_action"] == "show_forgot_password_confirm_form":
            api_response = self.show_forgot_password_confirm_form()
        elif data["api_action"] == "confirm_forgot_password_reset":
            api_response = self.confirm_forgot_password_reset()
        elif data["api_action"] == "show_change_password_form":
            api_response = self.show_change_password_form()
        elif data["api_action"] == "confirm_change_password":
            api_response = self.confirm_change_password()

        return api_response
