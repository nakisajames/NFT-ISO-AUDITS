from JailuApp.classes.base_structures import *
from JailuApp.models import UserAccount, UserSetting


class TableUserAccount(TableObjectBase):
    # table specific settings
    object_name = 'user_account'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "user_photo": TableFieldBase(object_name, 'user_photo', InputTypes.FILE.code,
                                            ValidationTypes.NONE.code
                                            , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                               Actions.View.code: True}
                                            , {Actions.Add.code: False, Actions.SubmitAdd.code: False,
                                               Actions.Edit.code: False,
                                               Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                            , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                               'value2': ''})
        , "full_name": TableFieldBase(object_name, 'full_name', InputTypes.TEXT.code, ValidationTypes.NON_NUMERIC.code
                                       , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                          Actions.View.code: True}
                                       , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                          Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                       ,
                                       {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "primary_email": TableFieldBase(object_name, 'primary_email', InputTypes.TEXT.code, ValidationTypes.EMAIL.code
                                      , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                         Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "primary_phone": TableFieldBase(object_name, 'primary_phone', InputTypes.TEXT.code,
                                          ValidationTypes.PHONE_NUMBER_10.code
                                          , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                             Actions.View.code: True}
                                          , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                             Actions.Edit.code: True,
                                             Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                          , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                             'value2': ''})
        , "secondary_email": TableFieldBase(object_name, 'secondary_email', InputTypes.TEXT.code, ValidationTypes.EMAIL.code
                                      , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: False,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                                         Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "secondary_phone": TableFieldBase(object_name, 'secondary_phone', InputTypes.TEXT.code, ValidationTypes.PHONE_NUMBER_10.code
                                      , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: False,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                                         Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})


        , "user_group": TableFieldBase(object_name, 'user_group', InputTypes.DROPDOWN.code, ValidationTypes.INT.code
                                       , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                          Actions.View.code: True}
                                       , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                          Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                       ,
                                       {'show': True, 'filter_type': FilterTypes.EQUAL.code, 'value': '', 'value2': ''})
        , "user_name": TableFieldBase(object_name, 'user_name', InputTypes.TEXT.code, ValidationTypes.NONE.code
               , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
               , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                  Actions.SubmitEdit.code: True, Actions.Delete.code: False}
               , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''}, {'is_unique': True})
        , "password": TableFieldBase(object_name, 'password', InputTypes.TEXT.code, ValidationTypes.NONE.code
               , {Actions.Add.code: True, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: False}
               , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: False,
                  Actions.SubmitEdit.code: False, Actions.Delete.code: False}
               , {'show': False, 'filter_type': FilterTypes.BETWEEN.code, 'value': '', 'value2': ''})
        , "status": TableFieldBase(object_name, 'status', InputTypes.RADIOBUTTON.code, ValidationTypes.NONE.code
             , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
             ,  {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True, Actions.SubmitEdit.code: True, Actions.Delete.code: False}
             , {'show': True, 'filter_type': FilterTypes.BETWEEN.code, 'value': '', 'value2': ''})

        , "entry_date": TableFieldBase(object_name, 'entry_date', InputTypes.TEXT.code, ValidationTypes.NONE.code
           , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: True}
           , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False
           , Actions.SubmitEdit.code: False, Actions.Delete.code: False}
           , {'show': False, 'filter_type': FilterTypes.BETWEEN.code, 'value': '','value2': ''})
        , "entered_by": TableFieldBase(object_name, 'entered_by', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: True}
             , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                Actions.SubmitEdit.code: False, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "last_modified": TableFieldBase(object_name, 'last_modified', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: True}
             , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                Actions.SubmitEdit.code: False, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.BETWEEN.code, 'value': '', 'value2': ''})
        , "modified_by": TableFieldBase(object_name, 'modified_by', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: True}
             , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                Actions.SubmitEdit.code: False, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})

    }

    def select_all_records(self):
        #collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.*, ug.name as group_name
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from user_account det join user_group ug on ug.id = det.user_group_id 
        left join user_account eb on eb.id = det.entered_by
        left join user_account mb on mb.id = det.modified_by
        where 1=1 """

        # apply filters if available
        if is_empty(self.fields["user_group"].ex_search["value"]) is False:
            sql += " and det.user_group_id = %s "
            sql_parameter.append(str(self.fields["user_group"].ex_search["value"]))
        if is_empty(self.fields["status"].ex_search["value"]) is False:
            sql += " and det.status = %s "
            sql_parameter.append(str(self.fields["status"].ex_search["value"]))
        # apply sort
        sql += " order by det.entry_date DESC"
        # apply limit and offset
        return dict(list=self.apply_sql_limit(sql,sql_parameter), count=self.count_sql_result(sql,sql_parameter))

    # override for lookup information
    def get_list_data(self):
        data = self.select_all_records()
        data_list = list()
        for item in data["list"]:
            an_item = dict()
            an_item["id"] = TableFieldListItem("id", item.get("id"), item.get("id"))

            import os
            file_url = os.path.join("media", 'user_account_user_photo', str(item.get("user_photo", "")))
            file_view = """
                        <a target='_blank' href='""" + file_url + """' class="avatar-icon-wrapper avatar-icon-xl">
                          <div class="avatar-icon rounded"><img src='""" + file_url + """' alt=""></div>
                        </a>
                        """
            if self.current_action == Actions.PdfExport.code:
                file_url = EW.notification_click_url + "/media/user_account_user_photo/" + str(item.get("user_photo", ""))
                file_view = """
                            <a target='_blank' href='""" + file_url + """'>
                              <div><img src='""" + file_url + """' style='height:100px;width:auto;'></div>
                            </a>
                            """
            # for those that have no photos
            if is_empty(item.get("user_photo", None)) or self.current_action == Actions.ExcelExport.code:
                file_view = ""

            an_item["user_photo"] = TableFieldListItem("user_photo", item.get("user_photo"), file_view)

            an_item["full_name"] = TableFieldListItem("full_name", item.get("full_name"), item.get("full_name"))
            an_item["primary_email"] = TableFieldListItem("primary_email", item.get("primary_email"), item.get("primary_email"))
            an_item["secondary_email"] = TableFieldListItem("secondary_email", item.get("secondary_email"), item.get("secondary_email"))
            an_item["primary_phone"] = TableFieldListItem("primary_phone", item.get("primary_phone"), item.get("primary_phone"))
            an_item["secondary_phone"] = TableFieldListItem("secondary_phone", item.get("secondary_phone"), item.get("secondary_phone"))

            an_item["user_group"] = TableFieldListItem("user_group", item.get("user_group_id"), item.get("group_name"))
            an_item["user_name"] = TableFieldListItem("user_name", item.get("user_name"), item.get("user_name"))
            an_item["status"] = TableFieldListItem("status", item.get("status"), item.get("status"))


            an_item["entry_date"] = TableFieldListItem("entry_date", item.get("entry_date"), item.get("entry_date"))
            an_item["entered_by"] = TableFieldListItem("entered_by", item.get("entered_by"), item.get("entered_by_name"))
            an_item["last_modified"] = TableFieldListItem("last_modified", item.get("last_modified"), item.get("last_modified"))
            an_item["modified_by"] = TableFieldListItem("modified_by", item.get("modified_by"), item.get("modified_by_name"))
            data_list.append(an_item)
        return {"list": data_list, "count": data["count"]}

    def select_a_record(self, object_id):
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """ select det.*, ug.name as group_name
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from user_account det join user_group ug on ug.id = det.user_group_id 
        left join user_account eb on eb.id = det.entered_by
        left join user_account mb on mb.id = det.modified_by
        where 1=1 """
        # apply filter
        sql += """ and det.id = %s  limit 1"""
        sql_parameter.append(str(object_id))

        return my_custom_sql(sql,sql_parameter)[0]  # get record to be edited


    def get_record_data(self, object_id):
        dict_obj = self.select_a_record(object_id)
        # if its not empty
        if dict_obj.__len__() != 0:
            for a_field in self.fields:
                if dict_obj.get(self.fields[a_field].object_name, None) is not None:
                    self.fields[a_field].current_value = dict_obj.get(self.fields[a_field].object_name)
                    self.fields[a_field].view_value = self.fields[a_field].current_value
            #  cater for foreign keys
            self.fields["user_group"].current_value = dict_obj.get("user_group_id")
            self.fields["user_group"].view_value = dict_obj.get("group_name")
            self.fields["entered_by"].current_value = dict_obj.get("entered_by_id")
            self.fields["entered_by"].view_value = dict_obj.get("entered_by_name")
            self.fields["modified_by"].current_value = dict_obj.get("modified_by_id")
            self.fields["modified_by"].view_value = dict_obj.get("modified_by_name")

            from django_jailuapp.settings import MEDIA_ROOT
            import os
            file_url = os.path.join("media", 'user_account_user_photo', str(dict_obj.get("user_photo")))
            file_view = """
                                    <a target='_blank' href='""" + file_url + """' class="avatar-icon-wrapper avatar-icon-xl">
                                      <div class="avatar-icon rounded"><img src='""" + file_url + """' alt=""></div>
                                    </a>
                                    """
            self.fields["user_photo"].current_value = dict_obj.get("user_photo")
            self.fields["user_photo"].view_value = file_view


    def insert_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # do more checks
        check_unique_username = my_custom_sql(""" select ifnull(count(id),0) as value from user_account 
                where user_name = %s  """, [str(self.fields["user_name"].current_value)])[0]
        if check_unique_username["value"] > 0:
            api_response["error"] = True
            api_response["error_msg"] = """The username (""" + str(self.fields["user_name"].current_value) + """) 
                    is already taken please specify a different one:"""
            return api_response

        # handle media upload
        if is_empty(self.fields["user_photo"].current_value) is False:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            source_file = os.path.join(MEDIA_ROOT, 'temp', self.fields["user_photo"].current_value)
            destination_file = os.path.join(MEDIA_ROOT, 'user_account_user_photo',
                                            self.fields["user_photo"].current_value)
            #  save the temp file to destination
            ret = copy_file(source_file, destination_file)

            if ret["error"] is True:
                api_response["error"] = True
                api_response["error_msg"] = "Failed to save user_photo file error:" + ret["error_msg"]
                return api_response
            else:
                # remove temp file
                delete_file(source_file)
                # get actual saved file_name
                self.fields["user_photo"].current_value = ret["uploaded_file_name"]


        # populate model and perform db operation
        user_id = new_guid()
        UserAccount(id=user_id
                    , user_photo=self.fields["user_photo"].current_value
                    , full_name=self.fields["full_name"].current_value
                    , primary_email=self.fields["primary_email"].current_value
                    , secondary_email=self.fields["secondary_email"].current_value
                    , primary_phone=self.fields["primary_phone"].current_value
                    , secondary_phone=self.fields["secondary_phone"].current_value
                    , user_group_id=self.fields["user_group"].current_value
                    , user_name=self.fields["user_name"].current_value
                    , password=enrypt_passwordMd5(self.fields["password"].current_value)
                    , status='Active'
                    , entry_date=current_datetime()
                    , entered_by=current_user_id()
                    , last_modified=current_datetime()
                    , modified_by=current_user_id()
                    ).save()

        #  save extra settings
        bulk_objects = list()
        bulk_objects.append(UserSetting(id=new_guid()
                                        , user_id=user_id, name="tour_status", value="Pending"
                                        , entry_date=current_datetime(), entered_by_id=current_user_id()
                                        , last_modified=current_datetime(), modified_by_id=current_user_id()
                                        ))

        #  bulk import that shit
        UserSetting.objects.bulk_create(bulk_objects)

        # send email notification
        email_subject = "Welcome to " + Lang.phrase("site_title")
        email_link_to_follow = EW.notification_click_url + ""
        email_full_names = self.fields["full_name"].current_value
        email_to_address = [self.fields["primary_email"].current_value]
        email_body_content = """
                Your """ + Lang.phrase("site_title") + """ Account is ready, please use  the credentials below. 
                 <br/>Link:<a href='""" + str(email_link_to_follow) + """'><strong>""" + str(email_link_to_follow) + """</strong></a>
                 <br/>Username:<strong>""" + str(self.fields["user_name"].current_value) + """</strong>
                 <br/>Password:<strong>""" + str(self.fields["password"].current_value) + """</strong>
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
        email_body_html = email_body_html.replace("[[email_subject]]",email_subject)
        email_body_html = email_body_html.replace("[[email_full_names]]", email_full_names)
        email_body_html = email_body_html.replace("[[email_body_content]]", email_body_content)

        smtp_send_email(email_to_address, email_subject, email_body_plain_text, email_body_html)



        return api_response

    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = UserAccount.objects.get(id=self.fields["id"].current_value)

        #  delete old file
        if is_empty(obj.user_photo) is False:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            delete_file(os.path.join(MEDIA_ROOT, 'user_account_user_photo', obj.user_photo))

        if is_empty(self.fields["user_photo"].current_value) is False:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            source_file = os.path.join(MEDIA_ROOT, 'temp', self.fields["user_photo"].current_value)
            destination_file = os.path.join(MEDIA_ROOT, 'user_account_user_photo',
                                            self.fields["user_photo"].current_value)
            #  save the temp file to destination
            ret = copy_file(source_file, destination_file)

            if ret["error"] is True:
                api_response["error"] = True
                api_response["error_msg"] = "Failed to save front_page file error:" + ret["error_msg"]
                return api_response
            else:
                # remove temp file
                delete_file(source_file)
                # get actual saved file_name
                self.fields["user_photo"].current_value = ret["uploaded_file_name"]
                # populate model and perform db operation


        # specify updates
        obj.user_photo = self.fields["user_photo"].current_value
        obj.full_name = self.fields["full_name"].current_value
        obj.primary_email = self.fields["primary_email"].current_value
        obj.secondary_email = self.fields["secondary_email"].current_value
        obj.primary_phone = self.fields["primary_phone"].current_value
        obj.secondary_phone = self.fields["secondary_phone"].current_value
        obj.user_group_id = self.fields["user_group"].current_value
        obj.user_name = self.fields["user_name"].current_value
        obj.status = self.fields["status"].current_value
        obj.last_modified = current_datetime()
        obj.modified_by = current_user_id()
        obj.save()
        return api_response

    def delete_row(self):
        api_response = {"error": False, "error_msg": "Delete completed successfully"}
        from django.db import IntegrityError
        try:

            # populate model and perform db operation
            obj = UserAccount.objects.get(id=self.fields["id"].current_value)

            # delete dependencies
            UserSetting.objects.filter(user_id=str(self.fields["id"].current_value)).delete()

            #  delete old file
            if is_empty(obj.user_photo) is False:
                from django_jailuapp.settings import MEDIA_ROOT
                import os
                delete_file(os.path.join(MEDIA_ROOT, 'user_account_user_photo', obj.user_photo))

            # specify updates
            obj.delete()
        except IntegrityError as e:
            api_response = {"error": True,
                            "error_msg": "Can not delete " + self.caption + " because its used elsewhere"}

        return api_response

    def html_add_form_page_load(self):
        self.fields["user_group"].lookup_data = Lookups.user_groups()
        self.fields["status"].lookup_data = Lookups.active_disabled_status()
        self.fields["status"].default_add = 'Active'

    def html_edit_form_page_load(self):

        # copy actual file into temp folder
        if is_empty(self.fields["user_photo"].current_value) is False:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            temp_file = os.path.join(MEDIA_ROOT, 'temp', self.fields["user_photo"].current_value)
            actual_file = os.path.join(MEDIA_ROOT, 'user_account_user_photo',
                                       self.fields["user_photo"].current_value)
            # remove existing temp file
            delete_file(temp_file)
            #  save the temp file to destination
            ret = copy_file(actual_file, temp_file)
            if ret["error"] is False:
                # get actual temp file_name
                self.fields["user_photo"].current_value = ret["uploaded_file_name"]
            # populate model and perform db operation

        self.fields["user_group"].lookup_data = Lookups.user_groups()
        self.fields["status"].lookup_data = Lookups.active_disabled_status()
        self.fields["status"].current_value = 'Active'

    def html_list_form_page_load(self):
        # first log that action
        op_summary = Actions.List.name() + " " + self.caption + " records"
        op_description = op_summary
        record_system_log(self.object_name, None, Actions.List.code
                          , op_summary, op_description)

        self.fields["user_group"].lookup_data = Lookups.user_groups()
        self.fields["status"].lookup_data = Lookups.active_disabled_status()

    def extract_data(self):
        #clear all cached data
        self.clear_field_data()

        import json
        if self.request_data.get("api_action", None) is not None:  # if there is data from add / edit/ delete from
            self.current_action = str(self.request_data["api_action"])
        if is_empty(self.request_data.get("object_id", None)) is False and str(self.request_data.get("object_id", None)) != "null":  # if there is data from add / edit/ delete from
            self.get_record_data(self.request_data["object_id"])
        if self.request_data.get("form_values", "{}") != "{}":  # if there is data from add / edit/ delete from
            self.extract_form_data(json.loads(self.request_data["form_values"]))
        if self.request_data.get("ex_filter_values", "{}") != "{}":  # if there is data from add / edit/ delete from
            self.extract_ex_filter(json.loads(self.request_data["ex_filter_values"]))
        if self.request_data.get("pagination", "{}") != "{}":  # if there is pagination data
            self.extract_pagination_data(json.loads(self.request_data["pagination"]))




