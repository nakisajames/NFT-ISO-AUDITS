from JailuApp.classes.base_structures import *
from JailuApp.models import SystemSetting


class TableSystemSetting(TableObjectBase):
    # table specific settings
    object_name = 'system_setting'

    # field settings
    fields = {
        "id": TableFieldBase(object_name, 'id', InputTypes.TEXT.code, ValidationTypes.NONE.code
             , {Actions.Add.code: False, Actions.Edit.code: True, Actions.List.code: False, Actions.View.code: True}
             , {Actions.SubmitAdd.code: False, Actions.Edit.code: True,
                Actions.SubmitEdit.code: True, Actions.Delete.code: True}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "labour_cost_percentage": TableFieldBase(object_name, 'labour_cost_percentage', InputTypes.TEXT.code, ValidationTypes.FLOAT.code
                 , {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
                 , {Actions.Add.code: True, Actions.SubmitAdd.code: True, Actions.Edit.code: True,
                    Actions.SubmitEdit.code: True, Actions.Delete.code: False}
             , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''})
        , "transport_cost_percentage": TableFieldBase(object_name, 'transport_cost_percentage', InputTypes.TEXT.code,
                                                  ValidationTypes.FLOAT.code
                                                  , {Actions.Add.code: True, Actions.Edit.code: True,
                                                     Actions.List.code: True, Actions.View.code: True}
                                                  , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                     Actions.Edit.code: True,
                                                     Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                  , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                     'value2': ''})
        , "anodize_cost_percentage": TableFieldBase(object_name, 'anodize_cost_percentage', InputTypes.TEXT.code,
                                                  ValidationTypes.FLOAT.code
                                                  , {Actions.Add.code: True, Actions.Edit.code: True,
                                                     Actions.List.code: True, Actions.View.code: True}
                                                  , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                     Actions.Edit.code: True,
                                                     Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                  , {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                     'value2': ''})
        , "overhead_cost_percentage": TableFieldBase(object_name, 'overhead_cost_percentage', InputTypes.TEXT.code,
                                                      ValidationTypes.FLOAT.code
                                                      , {Actions.Add.code: True, Actions.Edit.code: True,
                                                         Actions.List.code: True, Actions.View.code: True}
                                                      , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                         Actions.Edit.code: True,
                                                         Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                      ,
                                                      {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                       'value2': ''})
        , "profit_cost_percentage": TableFieldBase(object_name, 'profit_cost_percentage', InputTypes.TEXT.code,
                                                     ValidationTypes.FLOAT.code
                                                     , {Actions.Add.code: True, Actions.Edit.code: True,
                                                        Actions.List.code: True, Actions.View.code: True}
                                                     , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                        Actions.Edit.code: True,
                                                        Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                     ,
                                                     {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
                                                      'value2': ''})
        , "wastage_cost_percentage": TableFieldBase(object_name, 'wastage_cost_percentage', InputTypes.TEXT.code,
                                                     ValidationTypes.FLOAT.code
                                                     , {Actions.Add.code: True, Actions.Edit.code: True,
                                                        Actions.List.code: True, Actions.View.code: True}
                                                     , {Actions.Add.code: True, Actions.SubmitAdd.code: True,
                                                        Actions.Edit.code: True,
                                                        Actions.SubmitEdit.code: True, Actions.Delete.code: False}
                                                     ,
                                                     {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '',
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
        sql = """select det.*
        , concat_ws(' ',eb.first_name, eb.sur_name, eb.middle_name) as entered_by_name 
        , concat_ws(' ',mb.first_name, mb.sur_name, mb.middle_name) as modified_by_name 
        from system_setting det 
        left join user_account eb on eb.id = det.entered_by_id
        left join user_account mb on mb.id = det.modified_by_id
        where 1=1 """

        # apply filters if available
        # apply sort
        sql += " order by det.entry_date DESC"
        # apply limit and offset
        return dict(list=self.apply_sql_limit(sql,sql_parameter), count=self.count_sql_result(sql, sql_parameter))

    # override for lookup information
    def get_list_data(self):
        data = self.select_all_records()
        data_list = list()
        for item in data["list"]:
            an_item = dict()
            an_item["id"] = TableFieldListItem("id", item.get("id"), item.get("id"))
            an_item["labour_cost_percentage"] = TableFieldListItem("labour_cost_percentage", item.get("labour_cost_percentage"), item.get("labour_cost_percentage"))
            an_item["transport_cost_percentage"] = TableFieldListItem("transport_cost_percentage", item.get("transport_cost_percentage"), item.get("transport_cost_percentage"))
            an_item["anodize_cost_percentage"] = TableFieldListItem("anodize_cost_percentage",
                                                                  item.get("anodize_cost_percentage"),
                                                                  item.get("anodize_cost_percentage"))
            an_item["overhead_cost_percentage"] = TableFieldListItem("overhead_cost_percentage",
                                                                  item.get("overhead_cost_percentage"),
                                                                  item.get("overhead_cost_percentage"))
            an_item["profit_cost_percentage"] = TableFieldListItem("profit_cost_percentage",
                                                                     item.get("profit_cost_percentage"),
                                                                     item.get("profit_cost_percentage"))
            an_item["wastage_cost_percentage"] = TableFieldListItem("wastage_cost_percentage",
                                                                     item.get("wastage_cost_percentage"),
                                                                     item.get("wastage_cost_percentage"))

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
        , concat_ws(' ',eb.first_name, eb.sur_name, eb.middle_name) as entered_by_name 
        , concat_ws(' ',mb.first_name, mb.sur_name, mb.middle_name) as modified_by_name 
        from system_setting det 
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


    def update_row(self):
        api_response = {"error": False, "error_msg": "Insert completed successfully"}
        # populate model and perform db operation
        obj = SystemSetting.objects.get(id=self.fields["id"].current_value)
        # specify updates
        obj.labour_cost_percentage = self.fields["labour_cost_percentage"].current_value
        obj.transport_cost_percentage = self.fields["transport_cost_percentage"].current_value
        obj.anodize_cost_percentage = self.fields["anodize_cost_percentage"].current_value
        obj.overhead_cost_percentage = self.fields["overhead_cost_percentage"].current_value
        obj.profit_cost_percentage = self.fields["profit_cost_percentage"].current_value
        obj.wastage_cost_percentage = self.fields["wastage_cost_percentage"].current_value
        obj.last_modified = current_datetime()
        obj.modified_by_id = current_user_id()
        obj.save()
        return api_response

    def get_submit_edit_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                    return_object:'""" + str(self.object_name) + """',
                    return_action:'""" + str(Actions.Edit.code) + """',
                    return_object_id:'1',
                    return_current_page:1,
                    params:{
                        records_per_page:""" + str(EW.records_per_page) + """}
                    }"""




