from JailuApp.classes.base_structures import *


class TableSystemLog(TableObjectBase):
    # table specific settings
    object_name = 'system_log'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "entry_date": TableFieldBase(object_name, 'entry_date', InputTypes.DATETIME.code, ValidationTypes.DATETIME.code
                 , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True, Actions.View.code: True}
                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
             , {'show': True, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "user_id": TableFieldBase(object_name, 'user_id', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                       , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True,
                                          Actions.View.code: True}
                                       , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                          Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                       ,
                                       {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "table_name": TableFieldBase(object_name, 'table_name', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                       , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True,
                                          Actions.View.code: True}
                                       , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                          Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                       ,
                                       {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "record_id": TableFieldBase(object_name, 'record_id', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                      , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                         Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "operation_type": TableFieldBase(object_name, 'operation_type', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                      , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                                         Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "operation_summary": TableFieldBase(object_name, 'operation_summary', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                      , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: True,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                         Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "full_description": TableFieldBase(object_name, 'full_description', InputTypes.TEXT.code, ValidationTypes.NONE.code
                                      , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False,
                                         Actions.View.code: True}
                                      , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False,
                                         Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                      ,
                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})


    }

    def select_all_records(self):
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.* 
        , concat_ws(' ',u.full_name) user_full_name 
        from system_log det left join user_account u on u.id = det.user_id 
        where 1=1 """;

        # apply filters if available

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
            an_item["entry_date"] = TableFieldListItem("entry_date", item.get("entry_date"), item.get("entry_date"))
            an_item["table_name"] = TableFieldListItem("table_name", item.get("table_name"), item.get("table_name"))
            an_item["record_id"] = TableFieldListItem("record_id", item.get("record_id"), item.get("record_id"))
            an_item["operation_type"] = TableFieldListItem("operation_type", item.get("operation_type"), item.get("operation_type"))
            an_item["operation_summary"] = TableFieldListItem("operation_summary", item.get("operation_summary"), item.get("operation_summary"))
            an_item["full_description"] = TableFieldListItem("full_description", item.get("full_description"), item.get("full_description"))
            an_item["user_id"] = TableFieldListItem("user_id", item.get("user_id"), item.get("user_full_name"))

            data_list.append(an_item)
        return {"list": data_list, "count": data["count"]}

    def select_a_record(self, object_id):
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.* 
                , concat_ws(' ',u.full_name) user_full_name 
                from system_log det left join user_account u on u.id = det.user_id 
                where 1=1 """
        # apply filter
        sql += """ and det.id = %s  limit 1"""
        sql_parameter.append(str(object_id))

        return my_custom_sql(sql, sql_parameter)[0]  # get record to be edited


    def get_record_data(self, object_id):
        dict_obj = self.select_a_record(object_id)
        # if its not empty
        if dict_obj.__len__() != 0:
            for a_field in self.fields:
                if dict_obj.get(self.fields[a_field].object_name, None) is not None:
                    self.fields[a_field].current_value = dict_obj.get(self.fields[a_field].object_name)
                    self.fields[a_field].view_value = self.fields[a_field].current_value
            #  cater for foreign keys
            self.fields["user_id"].current_value = dict_obj.get("user_id")
            self.fields["user_id"].view_value = dict_obj.get("user_full_name")


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
            # select full list
            for item in list_data["list"]:
                html_text += """<tr>"""
                for a_field in self.fields:
                    if self.fields[a_field].show_on[Actions.List.code] is True:
                        html_text += """<td>""" + str(item[a_field].view_value) + """</td>"""
                # add list options
                html_text += """<td >
                          """ + view_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_show_view_return_options()) + """
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



