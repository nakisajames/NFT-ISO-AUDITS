from JailuApp.classes.base_structures import *
from JailuApp.models import Department


class TableDepartment(TableObjectBase):
    # table specific settings
    object_name = 'department'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})

        , "country": TableFieldBase(object_name, 'country', InputTypes.DROPDOWN.code,
                                                    ValidationTypes.NONE.code
                                                    , {Actions.Add.code: True, Actions.Edit.code: True,
                                                       Actions.List.code: True,
                                                       Actions.View.code: True}
                                                    , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                       Actions.Edit.code: True,
                                                       Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                    , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                       'value2': ''})
        , "department_type": TableFieldBase(object_name, 'department_type', InputTypes.DROPDOWN.code, ValidationTypes.NONE.code
                                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True,
                                    Actions.View.code: True}
                                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                 , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})

        , "link_supervisor": TableFieldBase(object_name, 'link_supervisor', InputTypes.TEXT.code,
                                             ValidationTypes.NONE.code
                                             , {Actions.Add.code: False, Actions.Edit.code: False,
                                                Actions.List.code: True,
                                                Actions.View.code: True}
                                             , {Actions.Add.code: False, Actions.SubmitAdd.code: False,
                                                Actions.Edit.code: False,
                                                Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                'value2': ''})
        , "link_employee": TableFieldBase(object_name, 'link_employee', InputTypes.TEXT.code,
                                            ValidationTypes.NONE.code
                                            , {Actions.Add.code: False, Actions.Edit.code: False,
                                               Actions.List.code: True,
                                               Actions.View.code: True}
                                            , {Actions.Add.code: False, Actions.SubmitAdd.code: False,
                                               Actions.Edit.code: False,
                                               Actions.SubmitEdit.code: False, Actions.Delete.code: False}
                                            , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                               'value2': ''})

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
        # collect parameters
        sql_parameter = []
        # put custom implementation for model
        sql = """select det.*, c.name as country_name, dt.name as department_type_name
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        , (select ifnull(count(ds.id),0) from department_supervisor ds where ds.department_id = det.id) as link_supervisor 
        , (select ifnull(count(ds.id),0) from department_employee ds where ds.department_id = det.id) as link_employee 
        from department det 
        join country c on det.country_id = c.id 
        join department_type dt on det.department_type_id = dt.id
        left join user_account eb on eb.id = det.entered_by_id
        left join user_account mb on mb.id = det.modified_by_id
        where 1=1 """

        # apply filters if available
        # apply sort
        sql += " order by det.entry_date DESC"
        # apply limit and offset
        return dict(list=self.apply_sql_limit(sql, sql_parameter), count=self.count_sql_result(sql, sql_parameter))

    # override for lookup information
    def get_list_data(self):
        data = self.select_all_records()
        data_list = list()
        for item in data["list"]:
            an_item = dict()
            an_item["id"] = TableFieldListItem("id", item.get("id"), item.get("id"))
            an_item["country"] = TableFieldListItem("country", item.get("country_id"), item.get("country_name"))
            an_item["department_type"] = TableFieldListItem("department_type", item.get("department_type_id"), item.get("department_type_name"))

            # dont show on export
            if self.current_action != Actions.ExcelExport.code:
                supervisor_link_options = """{
                                                        params:{
                                                            department_id:'""" + str(item.get("id")) + """',
                                                            }
                                                        }"""
                link_supervisor = """
                                        <button class="mb-2 mr-2 btn btn-pill btn-info" 
                                        onclick="ShowForm(this,'list','department_supervisor',null,1,""" + supervisor_link_options + """);">
                                        <span class="badge badge-pill badge-light">""" + str(
                    item.get("link_supervisor")) + """</span>
                                        Supervisors
                                        </button>
                                        """
                an_item["link_supervisor"] = TableFieldListItem("link_supervisor", item.get("link_supervisor"),
                                                                 link_supervisor)

                employee_link_options = """{
                                                                        params:{
                                                                            department_id:'""" + str(item.get("id")) + """',
                                                                            }
                                                                        }"""
                link_employee = """
                                                        <button class="mb-2 mr-2 btn btn-pill btn-info" 
                                                        onclick="ShowForm(this,'list','department_employee',null,1,""" + employee_link_options + """);">
                                                        <span class="badge badge-pill badge-light">""" + str(
                    item.get("link_employee")) + """</span>
                                                        Employees
                                                        </button>
                                                        """
                an_item["link_employee"] = TableFieldListItem("link_employee", item.get("link_employee"),
                                                                link_employee)



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
        sql = """select det.*, c.name as country_name, dt.name as department_type_name
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        , (select ifnull(count(ds.id),0) from department_supervisor ds where ds.department_id = det.id) as link_supervisor 
        , (select ifnull(count(ds.id),0) from department_employee ds where ds.department_id = det.id) as link_employee 
        from department det 
        join country c on det.country_id = c.id 
        join department_type dt on det.department_type_id = dt.id
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
            self.fields["country"].current_value = dict_obj.get("country_id")
            self.fields["country"].view_value = dict_obj.get("country_name")
            self.fields["department_type"].current_value = dict_obj.get("department_type_id")
            self.fields["department_type"].view_value = dict_obj.get("department_type_name")

            supervisor_link_options = """{
                                                                    params:{
                                                                        department_id:'""" + str(dict_obj.get("id")) + """',
                                                                        }
                                                                    }"""
            link_supervisor = """
                                                    <button class="mb-2 mr-2 btn btn-pill btn-info" 
                                                    onclick="ShowForm(this,'list','hr_bank_branch',null,1,""" + supervisor_link_options + """);">
                                                    <span class="badge badge-pill badge-light">""" + str(
                dict_obj.get("link_supervisor")) + """</span>
                                                    Supervisors
                                                    </button>
                                                    """
            self.fields["link_supervisor"].current_value = dict_obj.get("link_supervisor")
            self.fields["link_supervisor"].view_value = link_supervisor

            employee_link_options = """{
                                                                                params:{
                                                                                    department_id:'""" + str(
                dict_obj.get("id")) + """',
                                                                                    }
                                                                                }"""
            link_employee = """
                                                                <button class="mb-2 mr-2 btn btn-pill btn-info" 
                                                                onclick="ShowForm(this,'list','hr_bank_branch',null,1,""" + employee_link_options + """);">
                                                                <span class="badge badge-pill badge-light">""" + str(
                dict_obj.get("link_employee")) + """</span>
                                                                Employees
                                                                </button>
                                                                """
            self.fields["link_employee"].current_value = dict_obj.get("link_employee")
            self.fields["link_employee"].view_value = link_employee

    def insert_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        Department(id=new_guid()
                    , country_id=self.fields["country"].current_value
                    , department_type_id=self.fields["department_type"].current_value
                    , entry_date=current_datetime()
                    , entered_by_id=current_user_id()
                    , last_modified=current_datetime()
                    , modified_by_id=current_user_id()
                    ).save()
        return api_response

    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = Department.objects.get(id=self.fields["id"].current_value)
        # specify updates
        obj.country_id = self.fields["country"].current_value
        obj.department_type_id = self.fields["department_type"].current_value
        obj.last_modified = current_datetime()
        obj.modified_by_id = current_user_id()
        obj.save()
        return api_response

    def delete_row(self):
        api_response = {"error": False, "error_msg": "Delete completed successfully"}
        from django.db import IntegrityError
        try:
            # populate model and perform db operation
            obj = Department.objects.get(id=self.fields["id"].current_value)
            # specify updates
            obj.delete()
        except IntegrityError as e:
            api_response = {"error": True,
                            "error_msg": "Can not delete " + self.caption + " because its used elsewhere"}

        return api_response

    def html_add_form_page_load(self):
        self.fields["country"].lookup_data = Lookups.countrys()
        self.fields["department_type"].lookup_data = Lookups.department_types()

    def html_edit_form_page_load(self):
        self.fields["country"].lookup_data = Lookups.countrys()
        self.fields["department_type"].lookup_data = Lookups.department_types()





