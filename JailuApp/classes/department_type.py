from JailuApp.classes.base_structures import *
from JailuApp.models import DepartmentType


class TableDepartmentType(TableObjectBase):
    # table specific settings
    object_name = 'department_type'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "name": TableFieldBase(object_name, 'name', InputTypes.TEXT.code, ValidationTypes.NONE.code
                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''}
                                 ,{'is_unique': True})


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
        sql = """select det.*
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from department_type det 
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
            an_item["name"] = TableFieldListItem("name", item.get("name"), item.get("name"))

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
        sql = """select det.*
        , eb.full_name as entered_by_name 
        , mb.full_name as modified_by_name 
        from department_type det 
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

    def insert_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        DepartmentType(id=new_guid()
                    , name=self.fields["name"].current_value
                    , entry_date=current_datetime()
                    , entered_by_id=current_user_id()
                    , last_modified=current_datetime()
                    , modified_by_id=current_user_id()
                    ).save()
        return api_response

    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = DepartmentType.objects.get(id=self.fields["id"].current_value)
        # specify updates
        obj.name = self.fields["name"].current_value
        obj.last_modified = current_datetime()
        obj.modified_by_id = current_user_id()
        obj.save()
        return api_response

    def delete_row(self):
        api_response = {"error": False, "error_msg": "Delete completed successfully"}
        from django.db import IntegrityError
        try:
            # populate model and perform db operation
            obj = DepartmentType.objects.get(id=self.fields["id"].current_value)
            # specify updates
            obj.delete()
        except IntegrityError as e:
            api_response = {"error": True,
                            "error_msg": "Can not delete " + self.caption + " because its used elsewhere"}

        return api_response



