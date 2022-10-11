from JailuApp.classes.global_code import *


class TableFieldBase:
    table_object_name = 'unknown'
    object_name = 'unknown'
    caption = 'unknown'
    field_type = InputTypes.TEXT.code
    required = {Actions.Add.code: True, Actions.Edit.code: True
        , Actions.SubmitAdd.code: True, Actions.SubmitEdit.code: True}
    show_on = {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True , Actions.View.code: True}
    ex_search = {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''}
    settings = {'is_unique': False, "unique_table_name":table_object_name}
    validation_type = ValidationTypes.NONE.code
    default_add = None
    current_value = ''
    view_value = ''
    lookup_data = None

    def clear_value(self):  # clear data to avoid caching
        self.table_object_name = 'unknown'
        self.object_name = 'unknown'
        self.caption = 'unknown'
        self.field_type = InputTypes.TEXT.code
        self.required = {Actions.Add.code: True, Actions.Edit.code: True
            , Actions.SubmitAdd.code: True, Actions.SubmitEdit.code: True}
        self.show_on = {Actions.Add.code: True, Actions.Edit.code: True, Actions.List.code: True, Actions.View.code: True}
        self.ex_search = {'show': False, 'filter_type': FilterTypes.LIKE.code, 'value': '', 'value2': ''}
        self.settings = {'is_unique': False, "unique_table_name": self.table_object_name}
        self.validation_type = ValidationTypes.NONE.code
        self.default_add = None
        self.current_value = ''
        self.view_value = ''
        self.lookup_data = None

    def __init__(self, m_table_object_name, m_object_name, m_field_type, m_validation_type, m_show_on
                 , m_required, m_ex_search, m_settings=None):
        self.clear_value() #  ensure o cached values
        self.table_object_name = str(m_table_object_name)
        self.object_name = str(m_object_name)
        self.field_type = str(m_field_type)
        self.validation_type = str(m_validation_type)
        self.show_on = m_show_on
        self.required = m_required
        self.caption = Lang.fld_phrase(self.table_object_name,self.object_name)
        self.ex_search = m_ex_search
        if m_settings is not None: # use only if not empty
            #  set only provided ones
            self.settings["is_unique"] = m_settings.get("is_unique",False)
            self.settings["unique_table_name"] = m_settings.get("unique_table_name", self.table_object_name)

    def str_default_add(self):
        try:
            return '' if self.default_add is None else str(self.default_add)
        except:
            return ''

    def html_control(self, action):
        if self.show_on[action] is True:
            return str("""
            <div class='col-lg-12 row form-group' """ +
                       ("hidden='true'" if (self.object_name == "id" and action != Actions.View.code) else "") + """ 
            control_for='x_""" + self.object_name + """'>
                """ + self.html_caption(action) + """
                """ + self.html_input(action) + """
            </div>
            """)
        else:
            return ""

    def html_ex_search(self, action):
        if self.ex_search["show"] is True:
            return str("""
            <div class='text-center form-group' control_for='xf_""" + self.object_name + """'>
                """ + self.html_caption(action) + """
                """ + self.html_input(action) + """
            </div>
            """)
        else:
            return ""

    def html_input(self, action):
        submit_on_enter = ' submit_on_enter(event,"' + self.table_object_name + '_' + action + '")'
        if action == Actions.Add.code and self.field_type == InputTypes.TEXT.code:
            return str("""
                <div class='col-lg-8'>
                <input onkeypress='""" + submit_on_enter + """' 
                 class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                       + self.object_name + """' value='""" + self.str_default_add() + """'></input>
                </div>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.TEXT.code:
            return ("""
                <div class='col-lg-8'>
                <input onkeypress='""" + submit_on_enter + """'  """ + (
                "hidden='true' disabled='true'" if self.object_name == "id" else "")
                    + """ class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' value='"""
                    + ( "" if is_empty(self.current_value) else str(self.current_value) ) + """'></input>
                </div>
            """)
        elif action == Actions.List.code and self.field_type == InputTypes.TEXT.code:
            return str("""
                <div >
                <input class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='xf_""" + self.object_name + """' name='xf_"""
                       + self.object_name + """' value='""" + str(
                        self.ex_search["value"]) + """'></input>
                </div>
            """)
        elif action == Actions.Add.code and self.field_type == InputTypes.DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.str_default_add()) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>"""
            return html
        elif action == Actions.Edit.code and self.field_type == InputTypes.DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.current_value) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>"""
            return html
        elif action == Actions.List.code and self.field_type == InputTypes.DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.ex_search["value"]) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>"""
            return html
        elif action == Actions.Add.code and self.field_type == InputTypes.DATETIME.code:
            return str("""
                <div class='col-lg-8'>
                <input class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                       + self.object_name + """' value='""" + self.str_default_add() + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD H:mm:ss',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                </div>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.DATETIME.code:
            return ("""
                <div class='col-lg-8'>
                <input class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' value='""" + str(
                        self.current_value) + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD H:mm:ss',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                </div>
            """)
        elif action == Actions.List.code and self.field_type == InputTypes.DATETIME.code:
            html = """
                <div >
                <input class='form-control' table_object_name='""" + self.table_object_name + """' 
                 field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                  id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                  value='""" + str(self.ex_search["value"]) + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD H:mm:ss',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                """
            # if between draw a second one
            if self.ex_search["filter_type"] == FilterTypes.BETWEEN.code:
                html += """
                <span class="badge bg-info">AND</span>
                <input class='form-control' table_object_name='""" + self.table_object_name + """' 
                 field_object_name='y_""" + self.object_name + """' placeholder='""" + self.caption + """2' 
                  id='y_""" + self.object_name + """' name='y_""" + self.object_name + """' 
                  value='""" + str(self.ex_search["value2"]) + """'></input>
                <script>
                $('#y_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD H:mm:ss', icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                """

            html += """ </div>  """
            return html
        elif action == Actions.Add.code and self.field_type == InputTypes.DATE.code:
            return str("""
                <div class='col-lg-8'>
                <input class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                       + self.object_name + """' value='""" + self.str_default_add() + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                </div>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.DATE.code:
            return ("""
                <div class='col-lg-8'>
                <input class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' value='""" + str(
                        self.current_value) + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                </div>
            """)
        elif action == Actions.List.code and self.field_type == InputTypes.DATE.code:
            html = """
                <div >
                <input class='form-control' table_object_name='""" + self.table_object_name + """' 
                 field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                  id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                  value='""" + str(self.ex_search["value"]) + """'></input>
                <script>
                $('#x_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD',icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                """
            # if between draw a second one
            if self.ex_search["filter_type"] == FilterTypes.BETWEEN.code:
                html += """
                <span class="badge bg-info">AND</span>
                <input class='form-control' table_object_name='""" + self.table_object_name + """' 
                 field_object_name='y_""" + self.object_name + """' placeholder='""" + self.caption + """2' 
                  id='y_""" + self.object_name + """' name='y_""" + self.object_name + """' 
                  value='""" + str(self.ex_search["value2"]) + """'></input>
                <script>
                $('#y_""" + self.object_name + """').datetimepicker({format: 'YYYY-MM-DD', icons: {
                    time: "pe-7s-clock",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                }});
                </script>
                """

            html += """ </div>  """
            return html

        elif action == Actions.Add.code and self.field_type == InputTypes.FILE.code:
            return str("""
                <div class='col-lg-8 row'>
                <input hidden='true' disabled='true' class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' value='""" + str(
                        self.current_value) + """'></input>
                <form id='form_for_x_""" + self.object_name + """' action="upload_file" method="post" 
                enctype="multipart/form-data" target='iframe_for_x_""" + self.object_name + """'  >
                    <input onchange="start_tempUpload('x_""" + self.object_name + """');" class='form-control' type="file" fileuploaderfor='x_"""
                       + self.object_name + """' id='x_""" + self.object_name + """_uploader' name='x_"""
                       + self.object_name + """_uploader' size="30" />
                     
                     <iframe id='iframe_for_x_""" + self.object_name + """' 
                     name='iframe_for_x_""" + self.object_name + """' 
                     src="about:blank" style="width:0;height:0;border:0px solid #fff;"></iframe>
                 </form>
                 <div id='uploader_for_x_""" + self.object_name + """' class="spinner-border text-danger" role="status"
                  style='display: none;'>
                    <span class='sr-only'>Uploading...</span>
                 </div>
                </div>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.FILE.code:
            return str("""
                        <div class='col-lg-8'>
                        <input hidden='true' disabled='true' class='form-control' table_object_name='""" + self.table_object_name
                   + """' field_object_name='""" + self.object_name + """' placeholder='"""
                   + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                   + self.object_name + """' value='""" + (str(
            self.current_value) if is_empty(self.current_value) is False else "")  + """'></input>
                        <form id='form_for_x_""" + self.object_name + """' action="upload_file" method="post" 
                        enctype="multipart/form-data" target='iframe_for_x_""" + self.object_name + """'  >
                            <input onchange="start_tempUpload('x_""" + self.object_name + """');" class='form-control' type="file" fileuploaderfor='x_"""
                   + self.object_name + """' id='x_""" + self.object_name + """_uploader' name='x_"""
                   + self.object_name + """_uploader' value='""" + (str(
            self.current_value) if is_empty(self.current_value) is False else "") + """' size="30" />

                             <iframe  id='iframe_for_x_""" + self.object_name + """' 
                             name='iframe_for_x_""" + self.object_name + """' 
                             src="about:blank" style="width:0;height:0;border:0px solid #fff;"></iframe>
                         </form>
                         <div id='uploader_for_x_""" + self.object_name + """' class='spinner-border text-danger' role='status'
                          style='display: none;'>
                            <span class='sr-only'>Uploading...</span>
                         </div>
                        </div>
                    """)
        elif action == Actions.Add.code and self.field_type == InputTypes.TEXTAREA.code:
            return str("""
                <div class='col-lg-8'>
                <textarea class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                       + self.object_name + """' >""" + self.str_default_add() + """</textarea>
                </div>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.TEXTAREA.code:
            return ("""
                <div class='col-lg-8'>
                <textarea """ + (
                "hidden='true' disabled='true'" if self.object_name == "id" else "")
                    + """ class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' >""" + ( "" if is_empty(self.current_value) else str(self.current_value) )  + """</textarea>
                </div>
            """)
        elif action == Actions.Add.code and self.field_type == InputTypes.HTML_EDITOR_TINYMCE.code:
            return str("""
                <div class='col-lg-8'>
                <textarea class='form-control' table_object_name='""" + self.table_object_name
                       + """' field_object_name='""" + self.object_name + """' placeholder='"""
                       + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                       + self.object_name + """' >""" + self.str_default_add() + """</textarea>
                </div>
                <script>
                //remove previous editor if any
                //use only ID
                tinymce.EditorManager.execCommand('mceRemoveEditor',true, 'x_""" + self.object_name + """');
                //initialise editor
                //use jquery ID selector
                tinymce.init({
                    selector: '#x_""" + self.object_name + """',
                    //event handler to always update html content into primary field
                    setup: function (editor) {
                        editor.on('change', function () {
                            editor.save();
                        });
                    },
                    height: 300,
                    plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
                    menubar: 'file edit view insert format tools table help',
                    toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print',
                });
                </script>
            """)
        elif action == Actions.Edit.code and self.field_type == InputTypes.HTML_EDITOR_TINYMCE.code:
            return ("""
                <div class='col-lg-8'>
                <textarea """ + (
                "hidden='true' disabled='true'" if self.object_name == "id" else "")
                    + """ class='form-control' table_object_name='""" + self.table_object_name
                    + """' field_object_name='""" + self.object_name + """' placeholder='"""
                    + self.caption + """' id='x_""" + self.object_name + """' name='x_"""
                    + self.object_name + """' >""" + ( "" if is_empty(self.current_value) else str(self.current_value) )  + """</textarea>
                </div>
                <script>
                //remove previous editor if any
                //use only ID
                tinymce.EditorManager.execCommand('mceRemoveEditor',true, 'x_""" + self.object_name + """');
                //initialise editor
                //use jquery ID selector
                tinymce.init({
                    selector: '#x_""" + self.object_name + """',
                    //event handler to always update html content into primary field
                    setup: function (editor) {
                        editor.on('change', function () {
                            editor.save();
                        });
                    },
                    height: 300,
                    plugins: 'print preview paste importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap quickbars emoticons',
                    menubar: 'file edit view insert format tools table help',
                    toolbar: 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print',
                });
                </script>
            """)
        elif action == Actions.Add.code and self.field_type == InputTypes.RADIOBUTTON.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                   value='""" + self.str_default_add() + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='radio'  name='x_""" + self.object_name + """' 
                                    data-radiofor='x_""" + self.object_name + """'
                                  id='x_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(self.str_default_add()) == str(ele[0]) else '') + """
                                  onchange='capture_selection_radio_button(this)'>
                                  <label class='form-check-label' for='x_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.Edit.code and self.field_type == InputTypes.RADIOBUTTON.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                   value='""" + ( "" if is_empty(self.current_value) else str(self.current_value) ) + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='radio'  name='x_""" + self.object_name + """' 
                                    data-radiofor='x_""" + self.object_name + """'
                                  id='x_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(self.current_value) == str(ele[0]) else '') + """
                                  onchange='capture_selection_radio_button(this)'>
                                  <label class='form-check-label' for='x_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.List.code and self.field_type == InputTypes.RADIOBUTTON.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='xf_""" + self.object_name + """' name='xf_""" + self.object_name + """' 
                   value='""" + self.ex_search["value"] + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='radio'  name='xf_""" + self.object_name + """' 
                                    data-radiofor='xf_""" + self.object_name + """'
                                  id='xf_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(self.ex_search["value"]) == str(ele[0]) else '') + """
                                  onchange='capture_selection_radio_button(this)'>
                                  <label class='form-check-label' for='xf_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.Add.code and self.field_type == InputTypes.MULTISELECTION_CHECKBOX.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                   value='""" + self.str_default_add() + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                selected_values = str(self.str_default_add).split(",")
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='checkbox'  name='x_""" + self.object_name + """' 
                                    data-checkboxfor='x_""" + self.object_name + """'
                                  id='x_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(ele[0]) in str(self.default_add) else '') + """
                                  onchange='capture_selection_checkbox(this)'>
                                  <label class='form-check-label' for='x_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.Edit.code and self.field_type == InputTypes.MULTISELECTION_CHECKBOX.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='x_""" + self.object_name + """' name='x_""" + self.object_name + """' 
                   value='""" + ( "" if is_empty(self.current_value) else str(self.current_value) ) + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                # compile selected values in a string
                selected_values = str(self.current_value).split(",")
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='checkbox'  name='x_""" + self.object_name + """' 
                                    data-checkboxfor='x_""" + self.object_name + """'
                                  id='x_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(ele[0]) in selected_values else '') + """
                                  onchange='capture_selection_checkbox(this)'>
                                  <label class='form-check-label' for='x_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.List.code and self.field_type == InputTypes.MULTISELECTION_CHECKBOX.code:
            html = """
                <div class='col-lg-8'>
                <input hidden class='form-control' table_object_name='""" + self.table_object_name + """' 
                   field_object_name='""" + self.object_name + """' placeholder='""" + self.caption + """' 
                   id='xf_""" + self.object_name + """' name='xf_""" + self.object_name + """' 
                   value='""" + self.ex_search["value"] + """'></input>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                int_ind = 1 #  use for creating ids for radio buttons
                for ele in self.lookup_data:
                    html += """
                                <div class='form-check form-check-inline'>
                                  <input class='form-check-input' type='radio'  name='xf_""" + self.object_name + """' 
                                    data-checkboxfor='xf_""" + self.object_name + """'
                                  id='xf_""" + self.object_name + str(int_ind) + """' value='""" + str(ele[0]) + """'
                                  """ + ('checked' if str(self.ex_search["value"]) == str(ele[0]) else '') + """
                                  onchange='capture_selection_checkbox(this)'>
                                  <label class='form-check-label' for='xf_""" + self.object_name + str(int_ind) + """'>
                                  """ + str(ele[1]) + """
                                  </label>
                                </div>"""

                    int_ind += 1 # got to next

            html += """</div>"""
            return html
        elif action == Actions.View.code and self.field_type == InputTypes.MULTISELECTION_CHECKBOX.code:
            html = """"""
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                selected_values = str(self.current_value).split(",")
                for ele in self.lookup_data:
                    if str(ele[0]) in selected_values:
                        if html == """""":
                            html += str(ele[1])
                        else:
                            html += ","+ str(ele[1])
            return html
        elif action == Actions.Add.code and self.field_type == InputTypes.SELECT2DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.str_default_add()) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>
                <script>
                $('#x_""" + self.object_name + """').select2({dropdownAutoWidth: true, width: 'auto'});
                </script>
            """
            return html
        elif action == Actions.Add.code and self.field_type == InputTypes.SELECT2DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.str_default_add()) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>
                <script>
                $('#x_""" + self.object_name + """').select2({dropdownAutoWidth: true, width: 'auto'});
                </script>
            """
            return html
        elif action == Actions.Edit.code and self.field_type == InputTypes.SELECT2DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.current_value) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>
                <script>
                $('#x_""" + self.object_name + """').select2({dropdownAutoWidth: true, width: 'auto'});
                </script>
            """
            return html
        elif action == Actions.List.code and self.field_type == InputTypes.SELECT2DROPDOWN.code:
            html = """
                <div class='col-lg-8'>
                <select class='form-control' table_object_name='""" + self.table_object_name + """' field_object_name
                ='""" + self.object_name + """' placeholder='""" + self.caption + """' id='x_""" + self.object_name +\
                   """' name='x_""" + self.object_name + """' > 
                   <option value=''>""" + Lang.phrase('please_select') + """</option>
                """
            # fill with lookup data
            if self.lookup_data is not None:  # only loop when you have values
                for ele in self.lookup_data:
                    html += """<option """ + ('selected' if str(self.ex_search["value"]) == str(ele[0]) else '') +\
                            """ value='""" + str(ele[0]) + """'>""" + str(ele[1]) + """</option> """

            html += """</select></div>
                <script>
                $('#x_""" + self.object_name + """').select2({dropdownAutoWidth: true, width: 'auto'});
                </script>
            """
            return html
        elif action == Actions.View.code :
            html = """
                <div class='col-lg-8'>
                <label class='col-lg-12'>
                """ + str(self.view_value) + """
                </label>
                </div> 
                """
            return html
        else:
            return """<div class='alert alert-danger'>
              <h5><i class='icon fa fa-ban'></i> Unsupported Control!</h5>
              This input control is not yet supported.
            </div>"""

    def html_caption(self, action):
        if action == Actions.Add.code or action == Actions.Edit.code:
            return """
                <label label_for='x_""" + self.object_name + """' class='col-lg-4'>
                """ + self.caption + (
                "<i class='fa fa-asterisk ew-required' ></i>" if (self.required[action] is True) else "") + """
                </label>
                """
        elif action == Actions.List.code:
            return """ <label >""" + self.caption + """ <span class="badge bg-info">""" \
                   + self.ex_search["filter_type"] + """</span>
                </label>
                """
        elif action == Actions.View.code:
            return """
                <label label_for='x_""" + self.object_name + """' class='col-lg-4' style="word-break: break-all;">
                """ + self.caption + """
                </label>
                """
        else:
            return """
                    <label label_for='x_""" + self.object_name + """' class='col-lg-4' style="word-break: break-all;">
                    """ + self.caption + """
                    </label>
                    """

    def is_valid_type(self):
        if is_empty(self.current_value) is False:  # test only if it has a value
            if self.validation_type == ValidationTypes.NONE.code:
                return True
            elif self.validation_type == ValidationTypes.INT.code:
                return is_integer(self.current_value)
            elif self.validation_type == ValidationTypes.FLOAT.code:
                return is_float(self.current_value)
            elif self.validation_type == ValidationTypes.DATE.code:
                return is_date(self.current_value)
            elif self.validation_type == ValidationTypes.DATETIME.code:
                return is_datetime(self.current_value)
            elif self.validation_type == ValidationTypes.DATE.code:
                return is_date(self.current_value)
            elif self.validation_type == ValidationTypes.EMAIL.code:
                return is_email(self.current_value)
            elif self.validation_type == ValidationTypes.PHONE_NUMBER_10.code:
                return is_phone_number(self.current_value)
            elif self.validation_type == ValidationTypes.NON_NUMERIC.code:
                # negate condition
                return (contains_a_number(self.current_value) is False)
            else:
                return False
        else:
            return True


    def is_required_valid(self, action):
        return False if (self.required[action] is True and is_empty(self.current_value) is True) else True


class TableFieldListItem:
    object_name = 'unknown'
    current_value = None
    view_value = None

    def __init__(self, m_object_name, m_current_value=None, m_view_value=None):
        self.object_name = str(m_object_name)
        self.current_value = m_current_value
        self.view_value = str(m_view_value)


class TableObjectBase:
    object_name = 'unknown'
    caption = 'unknown'
    current_action = 'unknown'
    request_data = None
    fields = {}
    pagination = {"records_per_page": EW.records_per_page, 'current_page': 1,
                  'start_limit': 0, 'end_limit': EW.records_per_page}

    def __init__(self):
        self.caption = Lang.tbl_phrase(self.object_name)

    def select_all_records(self):
        # put custom implementation for model
        return {"list": list(), "count": 0}

    def apply_sql_limit(self,query, parameters = []):
        try:
            #if not exporting to excel then limit output
            if self.current_action != Actions.ExcelExport.code and self.current_action != Actions.PdfExport.code:
                from django.db.models import QuerySet
                if type(query) is str:
                    limited_sql = query + " LIMIT  " + str(self.pagination["start_limit"]) + ", " + str(self.pagination["records_per_page"])
                    return my_custom_sql(limited_sql,parameters)
                elif type(query) is QuerySet:
                    return query[self.pagination["start_limit"]:self.pagination["end_limit"]]
            else:
                from django.db.models import QuerySet
                if type(query) is str:
                    return my_custom_sql(query, parameters)
                elif type(query) is QuerySet:
                    return query
        except:
            return list()

    def count_sql_result(self,query, parameters = []):
        try:
            from django.db.models import QuerySet
            if type(query) is str:
                count_sql = """select ifnull(count(count_list.id),0) as value from ( """ + query + """ ) as count_list """
                return int(my_custom_sql(count_sql,parameters)[0]["value"])
            elif type(query) is QuerySet:
                return query.__len__()

        except:
            return 0

    # list data
    def get_list_data(self):
        data = self.select_all_records()
        data_list = list()
        for item in data["list"]:
            dict_obj = item.__dict__
            an_item = dict()
            for a_field in self.fields:
                an_item[a_field] = TableFieldListItem(a_field, dict_obj[a_field], dict_obj[a_field])
            data_list.append(an_item)
        return {"list": data_list, "count": data["count"]}

    def html_add_form_page_load(self):
        return None

    def html_add_form(self):
        # call page load
        self.html_add_form_page_load()

        api_response = {"header_title": self.caption + "s", "content_title": self.caption + " Add",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}
        html_text = """
        <div class="card card-info">
        <div class="card-body">
        <div class='col-lg-12'>
        """
        # add all add form fields
        for a_field in self.fields:
            html_text += self.fields[a_field].html_control(self.current_action)
        html_text += """
        </div>
        </div>
        <div class="card-footer" style="display: block;">
          """ + submit_add_link(self.object_name,self.get_submit_add_return_options()) + """
          """ + self.cancel_add_link() + """
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "Completed Successfully"
        api_response["content_body"] = html_text
        return api_response

    def html_edit_form_page_load(self):
        return None

    def html_edit_form(self):
        self.html_edit_form_page_load()
        api_response = {"header_title": self.caption + "s", "content_title": self.caption + " Edit",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}
        html_text = """
        <div class="card card-info">
        <div class="card-body">
        <div class='col-lg-12'>
        """
        # add all add form fields
        for a_field in self.fields:
            html_text += self.fields[a_field].html_control(self.current_action)
        html_text += """
        </div>
        </div>
        <div class="card-footer" style="display: block;">
          """ + submit_edit_link(self.object_name,self.get_submit_edit_return_options()) + """
          """ + self.cancel_edit_view_link() + """
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "Completed Successfully"
        api_response["content_body"] = html_text

        return api_response

    def html_view_form_page_load(self):
        # first log that action
        op_summary = Actions.View.name() + " " + self.caption + " record"
        op_description = op_summary
        record_system_log(self.object_name, self.fields["id"].current_value, Actions.View.code
                          , op_summary, op_description)

    def html_view_form(self):
        self.html_view_form_page_load()
        api_response = {"header_title": self.caption + "s", "content_title": self.caption + " View",
                        "content_body": "content_body", "content_footer": "content_footer",
                        "error": True, "error_msg": "Unknown API Error"}
        html_text = """
        <div class="card card-info">
        <div class="card-body">
        <div class='col-lg-12'>
        """
        # add all add form fields
        for a_field in self.fields:
            html_text += self.fields[a_field].html_control(self.current_action)
        html_text += """
        </div>
        </div>
        <div class="card-footer" style="display: block;">
          """ + self.cancel_edit_view_link() + """
        </div>
        </div>
        """

        api_response["error"] = False
        api_response["error_msg"] = "Completed Successfully"
        api_response["content_body"] = html_text

        return api_response

    def clear_field_data(self):
        for a_field in self.fields:
            # clear any cache
            self.fields[a_field].current_value = ""
            self.fields[a_field].view_value = ""
            self.fields[a_field].ex_search["value"] = ""
            self.fields[a_field].ex_search["value2"] = ""

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
        if is_empty(self.request_data.get("object_id", None)) is False and str(self.request_data.get("object_id", "")) != "null":  # if there is data from add / edit/ delete from
            self.get_record_data(self.request_data["object_id"])
        if self.request_data.get("pagination", "{}") != "{}":  # if there is pagination data
            self.extract_pagination_data(json.loads(self.request_data["pagination"]))

    def extract_form_data(self, data):

        for a_field in self.fields:
            if data.get(self.fields[a_field].object_name, None) is not None:
                self.fields[a_field].current_value = data.get(self.fields[a_field].object_name)
                self.fields[a_field].view_value = self.fields[a_field].current_value

    def extract_ex_filter(self, data):
        for a_field in self.fields:
            if self.fields[a_field].ex_search["show"] is True:
                # get value 1
                if data.get(self.fields[a_field].object_name, None) is not None:
                    self.fields[a_field].ex_search["value"] = data.get(self.fields[a_field].object_name)
                # get value 1
                if data.get(('y_' + self.fields[a_field].object_name), None) is not None:
                    self.fields[a_field].ex_search["value2"] = data.get(('y_' + self.fields[a_field].object_name))

    def extract_pagination_data(self, data):
        self.pagination["records_per_page"] = int(data.get("records_per_page", self.pagination["records_per_page"]))
        self.pagination["current_page"] = data.get("current_page", self.pagination["current_page"])
        self.pagination["start_limit"] = (self.pagination["current_page"] - 1) * self.pagination["records_per_page"]
        self.pagination["end_limit"] = self.pagination["current_page"] * self.pagination["records_per_page"]

    def select_a_record(self, object_id):
        # put custom implementation for model
        return list()

    def get_record_data(self, object_id):
        dict_obj = self.select_a_record(object_id)
        if dict_obj.__len__() != 0:
            for a_field in self.fields:
                if dict_obj.get(self.fields[a_field].object_name, None) is not None:
                    self.fields[a_field].current_value = dict_obj.get(self.fields[a_field].object_name)
                    self.fields[a_field].view_value = self.fields[a_field].current_value

    def is_field_value_unique(self,field_id):
        if self.current_action == Actions.SubmitAdd.code:
            check_unique_value = my_custom_sql(""" select ifnull(count(id),0) as value from 
            """ + str(self.fields[field_id].settings["unique_table_name"]) + """  
            where lower(""" + str(self.fields[field_id].object_name) + """) 
            = lower(%s)  """, [str(self.fields[field_id].current_value)])[0]
            if check_unique_value["value"] > 0:
                return False
        elif self.current_action == Actions.SubmitEdit.code:
            check_unique_value = my_custom_sql(""" select ifnull(count(id),0) as value from 
            """ + str(self.fields[field_id].settings["unique_table_name"]) + """  
            where lower(""" + str(self.fields[field_id].object_name) + """) 
            = lower(%s) and id != 
            '""" + str(self.fields["id"].current_value) + """'  """, [str(self.fields[field_id].current_value)])[0]
            if check_unique_value["value"] > 0:
                return False
        return  True

    def validate_form_data(self):
        api_response = {"error": False, "error_msg": "Validation Passed Successfully"}

        # perform required primary validations for form data
        for a_field in self.fields:
            if self.fields[a_field].is_required_valid(self.current_action) is False:  # validate required
                api_response["error"] = True
                api_response["error_msg"] = "Please Enter Required Field " + self.fields[a_field].caption
                break  # stop looping
            if self.fields[a_field].is_valid_type() is False:  # validate data type
                api_response["error"] = True
                api_response["error_msg"] = self.fields[a_field].caption + " must be a valid " + self.fields[
                    a_field].validation_type
                # customize message
                if self.fields[a_field].validation_type == ValidationTypes.PHONE_NUMBER_10.code:
                    api_response["error_msg"] = self.fields[a_field].caption + " must be a valid 10 digit phone number in format 07XXXXXXXX"
                elif self.fields[a_field].validation_type == ValidationTypes.NON_NUMERIC.code:
                    api_response["error_msg"] = self.fields[a_field].caption + " must not contain any numbers"
                break  # stop looping
            if self.fields[a_field].settings.get("is_unique",False) is True:  # validate unique if allowed
                if self.is_field_value_unique(a_field) is False:
                    api_response["error"] = True
                    api_response["error_msg"] = str(self.fields[a_field].caption) + """ must be unique and
                                 (""" + str(self.fields[a_field].current_value) + """) already exists"""
                    break  # stop looping
        return api_response

    def row_inserted(self):
        api_response = {"error": False, "error_msg": self.caption + " Added Successfully"}
        # other after effects
        # perform logging
        op_summary = Actions.Add.name() + " " + self.caption + " record"
        op_description = op_summary
        record_system_log(self.object_name, self.fields["id"].current_value, Actions.Add.code
                          , op_summary, op_description)
        return api_response

    def insert_row(self):
        api_response = {"error": True, "error_msg": "No Implimentation found"}
        return api_response

    def submit_add_form(self):
        api_response = self.validate_form_data()
        if api_response["error"] is True:  # check primary validations
            return api_response
        api_response = self.insert_row()  # run insert query
        if api_response["error"] is True:  # check insert worked
            return api_response
        api_response = self.row_inserted()

        return api_response

    def update_row(self):
        api_response = {"error": True, "error_msg": "No Implimentation found"}
        return api_response

    def row_updated(self):
        api_response = {"error": False, "error_msg": self.caption + " Updated Successfully"}
        # other after effects
        # perform logging
        op_summary = Actions.Edit.name() + " " + self.caption + " record"
        op_description = op_summary
        record_system_log(self.object_name, self.fields["id"].current_value, Actions.Edit.code
                          , op_summary, op_description)
        return api_response

    def submit_edit_form(self):
        api_response = self.validate_form_data()
        if api_response["error"] is True:  # check primary validations
            return api_response
        api_response = self.update_row()  # run insert query
        if api_response["error"] is True:  # check insert worked
            return api_response
        api_response = self.row_updated()

        return api_response

    def delete_row(self):
        api_response = {"error": True, "error_msg": "No Implimentation found"}
        return api_response

    def row_deleted(self):
        api_response = {"error": False, "error_msg": self.caption + " Deleted Successfully"}
        # other after effects
        # perform logging
        op_summary = Actions.Delete.name() + " " + self.caption + " record"
        op_description = op_summary
        record_system_log(self.object_name, self.fields["id"].current_value, Actions.Delete.code
                          , op_summary, op_description)
        return api_response

    def submit_delete_form(self):

        api_response = {"error": False, "error_msg": "Validation Passed Successfully"}
        #  only validate id value
        # perform required primary validations for form data
        if self.fields["id"].is_required_valid(self.current_action) is False:  # validate required
            api_response["error"] = True
            api_response["error_msg"] = "Please Enter Required Field " + self.fields["id"].caption
            return api_response
        elif self.fields["id"].is_valid_type() is False:  # validate data type
            api_response["error"] = True
            api_response["error_msg"] = self.fields["id"].caption + " must be a valid " + self.fields["id"].field_type
            return api_response
        else:
            api_response = self.delete_row()  # run insert query
            if api_response["error"] is True:  # check insert worked
                return api_response
            api_response = self.row_deleted()

        return api_response

    def draw_ex_search_panel(self):
        html = """"""
        # draw all fields that have extended search
        for a_field in self.fields:
            if self.fields[a_field].ex_search["show"] is True:
                html += self.fields[a_field].html_ex_search(Actions.List.code)
        # add button
        if html != """""":
            html = """
                        <div id='list_ex_filter_content' class='row text-center callout callout-info'>
                        """ + html

            html += """<div class="col-lg-12 text-left">
                    """ + ex_filter_link(self.object_name) + """
                    </div>
                    """
            html += """</div>"""
        return html

    def html_list_export(self):
        api_response = {"download_url": "export_url", "error": True, "error_msg": "Failed to export"}

        # draw the rows
        list_data = self.get_list_data()["list"]
        # organise for export
        # add the captions
        export_dict = list()
        # reformat all the data
        # COMPILE DATA AS 2 DIMENSIONAL ARRAY
        an_item = list()
        for a_field in self.fields:
            #  ignore fields not passed
            if list_data[0].get(self.fields[a_field].object_name, None) is not None:
                an_item.append(self.fields[a_field].caption)
        export_dict.append(an_item)

        for ele in list_data:
            an_item = list()
            for a_field in self.fields:
                #  ignore fields not passed
                if ele.get(self.fields[a_field].object_name, None) is not None:
                    an_item.append(ele[self.fields[a_field].object_name].view_value)
            export_dict.append(an_item)
        try:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            output_file_name = excel_export(export_dict, self.caption + " export.xls")
            import json
            params_passed = json.loads(self.request_data.get("params", "{}"))
            if params_passed.get("email_export",False) is True:
                email_file_url = os.path.join(MEDIA_ROOT, 'temp',output_file_name)
                email_ret = email_a_file(output_file_name,email_file_url)
                if email_ret["error"] is False:
                    api_response["error"] = False
                    api_response["error_msg"] = "File Emailed successfully"
                    api_response["email_export"] = True
                else:
                    api_response["error"] = True
                    api_response["error_msg"] = "Failed to email the file, error:" + email_ret["error_msg"]
            else:
                api_response["download_file_name"] = output_file_name
                api_response["download_file_path"] = os.path.join("media", 'temp', api_response["download_file_name"])
                api_response["error"] = False
                api_response["error_msg"] = "Exported successfully"
        except Exception as x:
            api_response["error"] = True
            api_response["error_msg"] = "Error while exporting, error:" + str(x)
        return api_response

    def html_list_pdf_export(self):
        api_response = {"download_url": "export_url", "error": True, "error_msg": "Failed to export"}

        # draw the rows
        list_data = self.get_list_data()["list"]

        pdf_text = """
        <html>
          <head>
            <meta name="pdfkit-page-size" content="Legal"/>
            <!--
            <meta name="pdfkit-orientation" content="Landscapet"/>
            -->
            <meta name="pdfkit-orientation" content="Portrait"/>
          </head>
          <body style='width:auto;'>
          <table style="width:100%;height:auto;border:1px solid #2851B7;">
          <tr >
          """
        # draw header
        for a_field in self.fields:
            #  ignore fields not passed
            if list_data[0].get(self.fields[a_field].object_name, None) is not None:
                pdf_text += """<td style='border:1px solid #2851B7;'> """ + str(self.fields[a_field].caption) + """"</td>"""

        pdf_text += """
          </tr>
        """

        # draw data
        for ele in list_data:
            pdf_text += """<tr>"""
            for a_field in self.fields:
                #  ignore fields not passed
                if ele.get(self.fields[a_field].object_name, None) is not None:
                    pdf_text += """<td style='border:1px solid #2851B7;'> """ + str(ele[self.fields[a_field].object_name].view_value) + """</td>"""
            pdf_text += """</tr>"""

        pdf_text += """
        
          </table>
          </body>
          </html>
        """


        try:
            from django_jailuapp.settings import MEDIA_ROOT
            import os
            output_file_name = self.caption + " export.pdf"
            file_path = os.path.join(MEDIA_ROOT, 'temp', output_file_name)
            ret = generate_pdf(pdf_text, file_path)
            if ret["error"] is False:
                import json
                params_passed = json.loads(self.request_data.get("params", "{}"))
                if params_passed.get("email_export", False) is True:
                    email_file_url = os.path.join(MEDIA_ROOT, 'temp', output_file_name)
                    email_ret = email_a_file(output_file_name, email_file_url)
                    if email_ret["error"] is False:
                        api_response["error"] = False
                        api_response["error_msg"] = "File Emailed successfully"
                        api_response["email_export"] = True
                    else:
                        api_response["error"] = True
                        api_response["error_msg"] = "Failed to email the file, error:" + email_ret["error_msg"]
                else:
                    api_response["download_file_name"] = output_file_name
                    api_response["download_file_path"] = os.path.join("media", 'temp',
                                                                      api_response["download_file_name"])
                    api_response["error"] = False
                    api_response["error_msg"] = "Exported successfully"
            else:
                api_response["error"] = True
                api_response["error_msg"] = "Error generating pdf, error:" + ret["error_msg"]
        except Exception as x:
            api_response["error"] = True
            api_response["error_msg"] = "Error while exporting, error:" + str(x)
        return api_response

    def html_list_form_page_load(self):
        # first log that action
        op_summary = Actions.List.name() + " " + self.caption + " records"
        op_description = op_summary
        record_system_log(self.object_name, None, Actions.List.code
                          , op_summary, op_description)
        return None

    def get_show_add_return_options(self):
        return """{
                params:{
                    return_object:'""" + str(self.object_name) + """',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:""" + str(self.pagination['current_page']) + """,
                    return_records_per_page:""" + str(self.pagination['records_per_page']) + """
                    }
                }"""

    def get_submit_add_return_options(self):
        import json
        #  get the return actions from calling API
        #  FORCE TO ALWAYS GOT TO PAGE 1
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                    return_object:'""" + str(params_passed.get("return_object", "undefined")) + """',
                    return_action:'""" + str(params_passed.get("return_action", "undefined")) + """',
                    return_current_page:1,
                    params:{
                        records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """}
                    }"""

    def get_show_edit_return_options(self):
        return """{
                params:{
                    return_object:'""" + str(self.object_name) + """',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:""" + str(self.pagination['current_page']) + """,
                    return_records_per_page:""" + str(self.pagination['records_per_page']) + """
                    }
                }"""

    def get_submit_edit_return_options(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        return """{
                    return_object:'""" + str(params_passed.get("return_object", "undefined")) + """',
                    return_action:'""" + str(params_passed.get("return_action", "undefined")) + """',
                    return_current_page:""" + str(params_passed.get("return_current_page", "undefined")) + """,
                    params:{
                        records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """}
                    }"""

    def get_show_view_return_options(self):
        return """{
                params:{
                    return_object:'""" + str(self.object_name) + """',
                    return_action:'""" + str(Actions.List.code) + """',
                    return_current_page:""" + str(self.pagination['current_page']) + """,
                    return_records_per_page:""" + str(self.pagination['records_per_page']) + """
                    }
                }"""

    def cancel_edit_view_link(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        inner_param =  """{
                            records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """
                            }"""
        return """
        <button onclick="ShowForm(this,'""" + str(params_passed.get("return_action", "undefined")) + """'
        ,'""" + str(params_passed.get("return_object", "undefined")) + """'
        ,null
        ,""" + str(params_passed.get("return_current_page", "undefined")) + """
        ,""" + inner_param + """)" 
        class="btn btn-secondary float-right">""" + Lang.phrase("btn_close") + """</button>
        """

    def cancel_add_link(self):
        import json
        #  get the return actions from calling API
        params_passed = json.loads(self.request_data.get("params", "{}"))
        inner_param =  """{
                            records_per_page:""" + str(params_passed.get("return_records_per_page", "undefined")) + """
                            }"""
        return """
        <button onclick="ShowForm(this,'""" + str(params_passed.get("return_action", "undefined")) + """'
        ,'""" + str(params_passed.get("return_object", "undefined")) + """'
        ,null
        ,""" + str(params_passed.get("return_current_page", "undefined")) + """
        ,""" + inner_param + """)" 
        class="btn btn-secondary float-right">""" + Lang.phrase("btn_cancel") + """</button>
        """

    def get_submit_delete_return_options(self):
        return """{
                return_object:'"""+str(self.object_name)+"""',
                return_action:'"""+str(Actions.List.code)+"""',
                return_current_page:"""+str(self.pagination['current_page'])+""",
                params:{records_per_page:"""+str(self.pagination['records_per_page'])+"""}
                }"""

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
        <div id='list_data_content' style="max-width: 100%;width: 100%;">
        <div class='row text-center'>
        <div class="col-xs-6 col-sm-4 col-md-3">
        """ + export_excel_link(self.object_name) + """
        """ + export_pdf_link(self.object_name) + """
        </div>
        <div class="col-xs-6 col-sm-4 col-md-3">
        """ + add_link(self.object_name,self.get_show_add_return_options()) + """
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
                        html_text += """<td style="word-break: break-word;">
                        """ + str(item[a_field].view_value) + """
                        </td>"""
                # add list options
                html_text += """<td >
                          """ + view_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_show_view_return_options()) + """
                          """ + edit_link(self.object_name, item[self.fields["id"].object_name].current_value, self.get_show_edit_return_options()) + """
                          """ + delete_link(self.object_name, item[self.fields["id"].object_name].current_value,self.get_submit_delete_return_options()) + """
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

        return api_response
