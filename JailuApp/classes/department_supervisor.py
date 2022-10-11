from JailuApp.classes.base_structures import *
from JailuApp.models import DepartmentSupervisor


class TableDepartmentSupervisor(TableObjectBase):
    # table specific settings
    object_name = 'department_supervisor'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "department": TableFieldBase(object_name, 'department', InputTypes.DROPDOWN.code, ValidationTypes.NONE.code
                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "user": TableFieldBase(object_name, 'user', InputTypes.SELECT2DROPDOWN.code, ValidationTypes.NONE.code
                                       , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                          Actions.View.code: True}
                                       , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                          Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                       ,
                                       {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})


        , "entry_date": TableFieldBase(object_name, 'entry_date', InputTypes.TEXT.code, ValidationTypes.NONE.code
           , {Actions.Add.code: False, Actions.Edit.code: False, Actions.List.code: False, Actions.View.code: True}
           , {Actions.Add.code: False, Actions.SubmitAdd.code: False, Actions.Edit.code: False
           , Actions.SubmitEdit.code: False, Actions.Delete.code: False}
           , {'show': False, 'filter_type': FilterTypes.BETWEEN.code, 'value': '', 'value2': ''})
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
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.*, concat_ws('-',c.name,dt.name) as department_name
        , ua.full_name as user_name , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from department_supervisor det 
        join user_account ua on det.user_id = ua.id 
        join department d on det.department_id = d.id 
        join country c on d.country_id = c.id 
        join department_type dt on d.department_type_id = dt.id 
        left join user_account eb on eb.id = det.entered_by_id
        left join user_account mb on mb.id = det.modified_by_id
        where 1=1 """

        # apply filters if available
        # default filter for the employee
        import json
        params_passed = json.loads(self.request_data.get("params", "{}"))
        sql += " and det.department_id = %s "
        sql_parameter.append(str(params_passed.get("department_id", "")))
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
            an_item["department"] = TableFieldListItem("department", item.get("department_id"), item.get("department_name"))
            an_item["user"] = TableFieldListItem("user", item.get("user_id"), item.get("user_name"))

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
        sql = """select det.*, concat_ws('-',c.name,dt.name) as department_name
        , ua.full_name as user_name , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from department_supervisor det 
        join user_account ua on det.user_id = ua.id 
        join department d on det.department_id = d.id 
        join country c on d.country_id = c.id 
        join department_type dt on d.department_type_id = dt.id 
        left join user_account eb on eb.id = det.entered_by_id
        left join user_account mb on mb.id = det.modified_by_id
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
            self.fields["entered_by"].current_value = dict_obj.get("entered_by_id")
            self.fields["entered_by"].view_value = dict_obj.get("entered_by_name")
            self.fields["modified_by"].current_value = dict_obj.get("modified_by_id")
            self.fields["modified_by"].view_value = dict_obj.get("modified_by_name")
            self.fields["department"].current_value = dict_obj.get("department_id")
            self.fields["department"].view_value = dict_obj.get("department_name")
            self.fields["user"].current_value = dict_obj.get("user_id")
            self.fields["user"].view_value = dict_obj.get("user_name")

    def insert_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        DepartmentSupervisor(id=new_guid()
                    , department_id=self.fields["department"].current_value
                    , user_id=self.fields["user"].current_value
                    , entry_date=current_datetime()
                    , entered_by_id=current_user_id()
                    , last_modified=current_datetime()
                    , modified_by_id=current_user_id()
                    ).save()
        return api_response

    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = DepartmentSupervisor.objects.get(id=self.fields["id"].current_value)
        # specify updates
        obj.user_id = self.fields["user"].current_value
        obj.last_modified = current_datetime()
        obj.modified_by_id = current_user_id()
        obj.save()
        return api_response

    def delete_row(self):
        api_response = {"error": False, "error_msg": "Delete completed successfully"}
        from django.db import IntegrityError
        try:
            # populate model and perform db operation
            obj = DepartmentSupervisor.objects.get(id=self.fields["id"].current_value)
            # specify updates
            obj.delete()
        except IntegrityError as e:
            api_response = {"error": True,
                            "error_msg": "Can not delete " + self.caption + " because its used elsewhere"}

        return api_response


    def html_add_form_page_load(self):
        import json
        params_passed = json.loads(self.request_data.get("params", "{}"))
        self.fields["department"].lookup_data = Lookups.extract_lookup('id', 'name', my_custom_sql("""select d.id
        , concat_ws('-',c.name,dt.name) as name from department d join department_type dt on d.department_type_id = dt.id 
        join country c on d.country_id = c.id where d.id = %s 
        order by c.entry_date, dt.name """,[str(params_passed.get("department_id", None))]))
        self.fields["department"].default_add = params_passed.get("department_id", None)
        self.fields["user"].lookup_data = Lookups.non_developer_users()

    def html_edit_form_page_load(self):
        # limit banks shown
        self.fields["department"].lookup_data = Lookups.extract_lookup('id', 'name', my_custom_sql("""select d.id
        , concat_ws('-',c.name,dt.name) as name from department d join department_type dt on d.department_type_id = dt.id 
        join country c on d.country_id = c.id where d.id = %s 
        order by c.entry_date, dt.name """, [str(self.fields["department"].current_value)]))
        self.fields["user"].lookup_data = Lookups.non_developer_users()


    def get_show_add_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                params:{
                    return_object:'department_supervisor',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:""" + str(self.pagination['current_page']) + """,
                    return_records_per_page:""" + str(self.pagination['records_per_page']) + """,
                    department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                    }
                }"""

    def get_submit_add_return_options(self):
        import json
        #  get the return actions from calling API
        #  FORCE TO ALWAYS GOT TO PAGE 1
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                    return_object:'department_supervisor',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:1,
                    params:{
                        params:{
                            department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                            records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """,
                            }
                        }
                    }"""

    def cancel_add_link(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        inner_param = """{
                            params:{
                                department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                                records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """
                                }
                            }"""
        return """
        <button onclick="ShowForm(this,'""" + str(params_passed.get("return_action", "undefined")) + """'
        ,'""" + str(params_passed.get("return_object", "undefined")) + """'
        ,null
        ,""" + str(params_passed.get("return_current_page", "undefined")) + """
        ,""" + inner_param + """)" 
        class="btn btn-secondary float-right">""" + Lang.phrase("btn_cancel") + """</button>
        """

    def cancel_edit_view_link(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        inner_param = """{
                                    params:{
                                        department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                                        records_per_page:""" + str(
            params_passed.get("return_records_per_page", "undefined")) + """
                                        }
                                    }"""
        return """
        <button onclick="ShowForm(this,'""" + str(params_passed.get("return_action", "undefined")) + """'
        ,'""" + str(params_passed.get("return_object", "undefined")) + """'
        ,null
        ,""" + str(params_passed.get("return_current_page", "undefined")) + """
        ,""" + inner_param + """)" 
        class="btn btn-secondary float-right">""" + Lang.phrase("btn_close") + """</button>
        """

    def get_submit_edit_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                    return_object:'department_supervisor',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:1,
                    params:{
                        params:{
                            department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                            records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """,
                            }
                        }
                    }"""

    def get_show_edit_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                params:{
                    return_object:'department_supervisor',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:""" + str(self.pagination['current_page']) + """,
                    return_records_per_page:""" + str(self.pagination['records_per_page']) + """,
                    department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                    }
                }"""

    def get_submit_delete_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                return_object:'department_supervisor',
                return_action:'""" + str(Actions.List.code) + """',
                return_current_page:""" + str(self.pagination['current_page']) + """,
                params:{
                        params:{
                            department_id:'""" + str(params_passed.get("department_id", "null")) + """',
                            records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """,
                            }
                        }
                }"""

