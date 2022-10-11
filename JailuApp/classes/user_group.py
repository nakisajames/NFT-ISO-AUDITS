from JailuApp.classes.base_structures import *
from JailuApp.models import UserGroup, GroupPermission, UserAccount


class TableUserGroup(TableObjectBase):
    # table specific settings
    object_name = 'user_group'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.INT.code
                             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: True
                                 , Actions.View.code: True}
                             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
                             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "name": TableFieldBase(object_name, 'name', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True
                                     , Actions.View.code: True}
                                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                             , {'show': True, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''}
                                 ,{'is_unique': True})
    }

    def select_all_records(self):
        # put custom implementation for model
        data = UserGroup.objects
        # apply filters if available
        if is_empty(self.fields["name"].ex_search["value"]) is False:
            data = data.filter(name__icontains=str(self.fields["name"].ex_search["value"]))
        # apply sort
        data = data.order_by('id')

        #apply limit and offset
        return dict(list=self.apply_sql_limit(data), count=self.count_sql_result(data))

    def extract_data(self):
        #clear all cached data
        self.clear_field_data()

        import json
        if self.request_data.get("api_action", None) is not None:  # if there is data from add / edit/ delete from
            self.current_action = str(self.request_data["api_action"])
        if self.request_data.get("form_values", "{}") != "{}":  # if there is data from add / edit/ delete from
            self.extract_form_data(json.loads(self.request_data["form_values"]))
        if self.request_data.get("ex_filter_values", "{}") != "{}":  # if there is data from add / edit/ delete from
            self.extract_ex_filter(json.loads(self.request_data["ex_filter_values"]))
        if is_empty(self.request_data.get("object_id", None)) is False and self.request_data.get("object_id", "") != "null":  # if there is data from add / edit/ delete from
            self.get_record_data(self.request_data["object_id"])
        if self.request_data.get("pagination", "{}") != "{}":  # if there is pagination data
            self.extract_pagination_data(json.loads(self.request_data["pagination"]))

    def select_a_record(self, object_id):
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.*
        from user_group det 
        where 1=1 """
        # apply filter
        sql += """ and det.id = %s  limit 1"""
        sql_parameter.append(str(object_id))

        return my_custom_sql(sql, sql_parameter)[0]  # get record to be edited

    def insert_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        UserGroup(name=self.fields["name"].current_value).save()
        return api_response

    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = UserGroup.objects.get(id=self.fields["id"].current_value)
        # specify updates
        obj.name = self.fields["name"].current_value
        obj.save()
        return api_response


    def delete_row(self):
        api_response = {"error": False, "error_msg": "Delete completed successfully"}
        from django.db import IntegrityError
        try:
            if str(self.fields["id"].current_value) == str(Security.super_admin_group_id):
                api_response["error"] = True
                api_response["error_msg"] = "You can not delete Super Administrators group"
            elif str(self.fields["id"].current_value) == str(Security.anonymous_group_id):
                api_response["error"] = True
                api_response["error_msg"] = "You can not delete Anonymous group"
            elif UserAccount.objects.all().filter(user_group_id=self.fields["id"].current_value).count() > 0:
                api_response["error"] = True
                api_response["error_msg"] = "This User Group still has UserAccount records attached to it"
            else:
                # remove all permissions first
                GroupPermission.objects.all().filter(user_group_id=self.fields["id"].current_value).delete()
                UserGroup.objects.get(id=self.fields["id"].current_value).delete()
        except IntegrityError as e:
            api_response = {"error": True,
                            "error_msg": "Can not delete " + self.caption + " because its used elsewhere"}

        return api_response


    def html_list_form(self):
        self.html_list_form_page_load()
        api_response = {"header_title": self.caption + "s", "content_title": self.caption + " List",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}

        # draw the rows
        list_data = self.get_list_data()

        # draw search panel
        html_text = self.draw_ex_search_panel()

        # draw list content
        html_text += """
        <div id='list_data_content'>
        <div class='row text-center'>
        <div class="col-xs-6 col-sm-4 col-md-3">
        """ + export_excel_link(self.object_name) + """
        """ + export_pdf_link(self.object_name) + """
        </div>
        <div class="col-xs-6 col-sm-4 col-md-3">
        """ + add_link(self.object_name, self.get_show_add_return_options()) + """
        </div>
        <div class="col-xs-12 col-sm-4 col-md-6">
        """ + pagination(self.object_name, list_data["count"], self.pagination["current_page"], self.pagination["records_per_page"]) + """
        </div>
        </div>
        <div class='card table-responsive col-lg-12' style='padding:10px;width:96%;margin-left: 2%;margin-right: 2%;'>
        <table class='table-bordered table-hover table-striped text-center' style='width: 100%;'>
        <thead>
        <tr>
        """

        # draw all fields
        for a_field in self.fields:
            if self.fields[a_field].show_on[Actions.List.code] is True:
                html_text += """<td>""" + self.fields[a_field].caption + """</td>"""
        # draw options area
        html_text += """<td>&nbsp</td>
        </tr>
        </thead>
        <tbody>
        """

        if list_data["count"] == 0:
            html_text += """<tr><td colspan='30'>
            <div class='alert alert-danger'>
              <h5><i class='icon fa fa-ban'></i> No Data!</h5>
              No """ + self.caption + """ records found.
            </div>
            </td></tr>
            """
        else:
            # select while limiting according to pagination
            for item in list_data["list"]:
                html_text += """<tr>"""
                for a_field in self.fields:
                    if self.fields[a_field].show_on[Actions.List.code] is True:
                        html_text += """<td>""" + str(item[a_field].view_value) + """</td>"""
                # add list options
                html_text += """<td >
                          """ + view_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_show_view_return_options()) + """
                          """ + edit_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_show_edit_return_options()) + """
                          """ + """<a class="btn btn-info btn-sm" href="javascript:void(0);"
                            onclick="ShowForm(this,'permission_list','""" + str(
                            self.object_name) + """','""" + str(
                            item["id"].current_value) + """')">
                              <i class='fas fa-user'></i>""" + Lang.phrase("link_edit_permissions") + """
                          </a>
                            """ + """
                          """ + delete_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_submit_delete_return_options()) + """
                                </td>
                                """

                html_text += """</tr>"""

        html_text += """
        </tbody>
        </table>
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "Completed Successfully"
        api_response["content_body"] = html_text

        return api_response

    def update_missing_permission(self):
        # get existing permissions
        existing = GroupPermission.objects.filter(user_group_id=self.fields["id"].current_value)
        all_existing_table_name = [ ele.table_name for ele in existing ]
        missing_table_name = [ ele for ele in Security.table_objects if ele not in  all_existing_table_name ]
        for tbl_name in missing_table_name:
            GroupPermission(user_group_id=self.fields["id"].current_value
                                , table_name=tbl_name).save()


    # list data
    def get_permissions_list_data(self):
        self.update_missing_permission()
        data = GroupPermission.objects.filter(user_group_id=self.fields["id"].current_value)
        data_list = list()
        for item in data:
            an_item = dict()
            an_item["table_name"] = item.table_name
            an_item["table_caption"] = Lang.tbl_phrase(item.table_name)
            an_item[Actions.Add.code] = item.add
            an_item[Actions.Delete.code] = item.delete
            an_item[Actions.Edit.code] = item.edit
            an_item[Actions.List.code] = item.list
            an_item[Actions.View.code] = item.view
            data_list.append(an_item)
        return data_list

    def html_permission_list_form(self):
        api_response = {"header_title": self.caption + "s", "content_title": self.caption + " List",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}

        # draw the rows
        list_data = self.get_permissions_list_data()


        # draw list content
        html_text = """
        <div id='list_data_content'>
        <div class="card-header">
            <h3 class="card-title">User Group: """ + self.fields["name"].view_value + """ (""" + str(self.fields["id"].current_value) + """)</h3>
        </div>
        <div class='card table-responsive col-lg-12' style='padding:10px;width:96%;margin-left: 2%;margin-right: 2%;'>
        <table class='table-bordered table-hover table-striped text-center' style='width: 100%;'>
        <thead>
        <tr>
        <td>Object</td>
        <td>""" + Actions.Add.name() + """
        <td>""" + Actions.Delete.name() + """
        <td>""" + Actions.Edit.name() + """
        <td>""" + Actions.List.name() + """
        <td>""" + Actions.View.name() + """
        </tr>
        </thead>
        <tbody>
        """

        if list_data.__len__() == 0:
            html_text += """<tr><td colspan='30'>
            <div class='alert alert-danger'>
              <h5><i class='icon fa fa-ban'></i> No Data!</h5>
              No """ + self.caption + """ records found.
            </div>
            </td></tr>
            """
        else:
            # select while limiting according to pagination
            for item in list_data:
                html_text += """<tr item_type='permission_row' table_name='""" + item["table_name"] + """'>
                        <td item_type='table_name' data_value='""" + item["table_name"] + """'>""" + item["table_caption"] + """</td>
                        <td>
                        <div class="">
                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                          <input """ + ('checked' if item[Actions.Add.code] is True else '') + """ type="checkbox" item_type='add' table_value='""" + item["table_name"] + """' class="custom-control-input" id='""" + item["table_name"] + "_" + Actions.Add.code + """'>
                        <label class="custom-control-label" for='""" + item["table_name"] + "_" + Actions.Add.code + """'>&nbsp</label></div>
                        </div>
                        </td>
                        <td>
                        <div class="">
                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                          <input """ + ('checked' if item[Actions.Delete.code] is True else '') + """ type="checkbox" item_type='delete' table_value='""" + item["table_name"] + """' class="custom-control-input" id='""" + item["table_name"] + "_" + Actions.Delete.code + """'>
                        <label class="custom-control-label" for='""" + item["table_name"] + "_" + Actions.Delete.code + """'>&nbsp</label></div>
                        </div>
                        </td>
                        <td>
                        <div class="">
                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                          <input """ + ('checked' if item[Actions.Edit.code] is True else '') + """ type="checkbox" item_type='edit' table_value='""" + item["table_name"] + """' class="custom-control-input" id='""" + item["table_name"] + "_" + Actions.Edit.code + """'>
                        <label class="custom-control-label" for='""" + item["table_name"] + "_" + Actions.Edit.code + """'>&nbsp</label></div>
                        </div>
                        </td>
                        <td>
                        <div class="">
                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                          <input """ + ('checked' if item[Actions.List.code] is True else '') + """ type="checkbox" item_type='list' table_value='""" + item["table_name"] + """' class="custom-control-input" id='""" + item["table_name"] + "_" + Actions.List.code + """'>
                        <label class="custom-control-label" for='""" + item["table_name"] + "_" + Actions.List.code + """'>&nbsp</label></div>
                        </div>
                        </td>
                        <td>
                        <div class="">
                        <div class="custom-control custom-switch custom-switch-off-danger custom-switch-on-success">
                          <input """ + ('checked' if item[Actions.View.code] is True else '') + """ type="checkbox" item_type='view' table_value='""" + item["table_name"] + """' class="custom-control-input" id='""" + item["table_name"] + "_" + Actions.View.code + """'>
                        <label class="custom-control-label" for='""" + item["table_name"] + "_" + Actions.View.code + """'>&nbsp</label></div>
                        </div>
                        </td>
                        
                        </tr>"""

        html_text += """
        </tbody>
        </table>
        </div>
        </div>
        <div class="card-footer">
          <button onclick="SubmitPermissionsForm('""" + str(self.fields["id"].current_value) \
                     + """')" class="btn btn-info">""" + Lang.phrase("btn_save") + """</button>
          <button onclick="ShowForm(this,'""" + Actions.List.code + """','""" + self.object_name \
                     + """')" class="btn btn-default float-right">""" + Lang.phrase("btn_cancel") + """</button>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "Completed Successfully"
        api_response["content_body"] = html_text

        return api_response

    def update_permissions(self):
        api_response = {"error": False, "error_msg": "Validation Failed"}
        permission_list = self.request_data.get("permission_list", "[]")
        if is_empty(self.fields["id"].current_value) is True:
            api_response["error"] = True
            api_response["error_msg"] = "Please Enter Required Field Group ID"
        elif str(self.fields["id"].current_value) == str(Security.super_admin_group_id):
            api_response["error"] = True
            api_response["error_msg"] = "You can not set Permissions for Super Administrators"
        elif str(self.fields["id"].current_value) == str(Security.anonymous_group_id):
            api_response["error"] = True
            api_response["error_msg"] = "You can not set Permissions for Anonymous"
        elif UserGroup.objects.filter(id=self.fields["id"].current_value).count() == 0:
            api_response["error"] = True
            api_response["error_msg"] = "Unknown User Group (" + str(self.fields["id"].current_value) + ")"
        elif permission_list == "[]":
            api_response["error"] = True
            api_response["error_msg"] = "Please Enter Required Permission List"
        else:
            import json
            permission_list = json.loads("{\"data\":"+permission_list+"}").get("data")
            for item in permission_list:
                obj = GroupPermission.objects.get(user_group_id=self.fields["id"].current_value,
                                                  table_name=item["table_name"])
                obj.add = bool(item["add"])
                obj.edit = bool(item["edit"])
                obj.delete = bool(item["delete"])
                obj.list = bool(item["list"])
                obj.view = bool(item["view"])
                obj.save()
            api_response["error"] = False
            api_response["error_msg"] = "Saved successfully"
        return api_response

    def permission_updated(self):
        api_response = {"error": False, "error_msg": self.caption + "Permissions Updated Successfully"}
        # other after effects
        # perform logging
        record_system_log(self.object_name, None, "update_group_permission", "Group Permissions Updated"
                          , "Group Permissions Updated")
        return api_response


    def submit_permissions(self):
        api_response = self.update_permissions()
        if api_response["error"] is True:  # check insert worked
            return api_response
        api_response = self.permission_updated()

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
        if Security.check_permission(self.object_name, self.request_data["api_action"]) is False:
            api_response["error"] = True
            api_response["error_msg"] = Lang.phrase("permission_denied")
        elif self.request_data["api_action"] == Actions.List.code:
            api_response = self.html_list_form()
        elif self.request_data["api_action"] == Actions.Add.code:
            api_response = self.html_add_form()
        elif self.request_data["api_action"] == Actions.SubmitAdd.code:
            api_response = self.submit_add_form()
        elif self.request_data["api_action"] == Actions.Edit.code:
            api_response = self.html_edit_form()
        elif self.request_data["api_action"] == Actions.SubmitEdit.code:
            api_response = self.submit_edit_form()
        elif self.request_data["api_action"] == Actions.Delete.code:
            api_response = self.submit_delete_form()
        elif self.request_data["api_action"] == Actions.ExcelExport.code:
            api_response = self.html_list_export()
        elif self.request_data["api_action"] == Actions.PdfExport.code:
            api_response = self.html_list_pdf_export()
        elif self.request_data["api_action"] == Actions.View.code:
            api_response = self.html_view_form()
        elif self.request_data["api_action"] == "permission_list" and Security.is_admin() is False:
            api_response["error"] = True
            api_response["error_msg"] = Lang.phrase("permission_admin_only")
        elif self.request_data["api_action"] == "submit_permissions" and Security.is_admin() is False:
            api_response["error"] = True
            api_response["error_msg"] = Lang.phrase("permission_admin_only")
        elif self.request_data["api_action"] == "permission_list":
            api_response = self.html_permission_list_form()
        elif data["api_action"] == "submit_permissions":
            api_response = self.submit_permissions()

        return api_response



