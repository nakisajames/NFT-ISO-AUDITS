from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

@xframe_options_exempt #disable Xframe limit error
def index(request):
    parameters = None
    if request.method == "POST":
        parameters = request.POST.dict()
    elif request.method == "GET":
        parameters = request.GET.dict()
    from JailuApp.classes.base_structures import Actions, Lang, Menu, EW, Security, current_user_id, my_custom_sql, generate_tour_data
    Security.initialise(request)  # setup security
    title = Lang.phrase("site_title")
    site_sidebar_text = Lang.phrase("site_sidebar_text")
    from _datetime import datetime
    footer = str(datetime.now().year) + Lang.phrase("site_footer")

    user_full_names = Security.user_full_names()
    user_group_names = Security.user_group_names()
    menu = Menu().draw_menu()

    staring_page_object = "my_activity"
    staring_page_action = Actions.List.code
    staring_object_id = ""
    sidebar_logo = "/static/images/app_logo.png"


    # incase one has set destination already
    if parameters.get("starting_object",None) != None and parameters.get("starting_action",None) != None:
        staring_page_object = parameters.get("starting_object")
        staring_page_action = parameters.get("starting_action")
        staring_object_id = parameters.get("staring_object_id","")
    # check for other allowable actions
        staring_page_action = Actions.List.code
    elif Security.check_permission("user_account", Actions.List.code) is True:
        staring_page_object = "user_account"
        staring_page_action = Actions.List.code

    #  determine tour settings
    tour_data = my_custom_sql(
        "select name, value from user_setting where user_id = '" + str(current_user_id()) + "'")
    tour_setting = dict()
    for x in tour_data:
        tour_setting[str(x["name"])] = str(x["value"])

    # get tour data
    tour_setting["steps"] = generate_tour_data()["steps"]


    # set some values
    EW.notification_click_url = request.get_host()
    if Security.is_logged_in:
        return render(request, 'index2.html', {'title': title, 'menu': menu, 'footer': footer, 'actions': Actions
            , 'EW': EW, "user_full_names": user_full_names, "user_group_names": user_group_names
            , "staring_page_object": staring_page_object, "staring_page_action": staring_page_action
            , "staring_object_id": staring_object_id, "tour_setting": tour_setting
            , "site_sidebar_text": site_sidebar_text, "sidebar_logo": sidebar_logo})
    else:
        return render(request, 'login.html', {'title': title, 'menu': menu, 'footer': footer, 'actions': Actions, 'EW': EW})


@xframe_options_exempt #disable Xframe limit error
def download(request):
    parameters = None
    if request.method == "POST":
        parameters = request.POST.dict()
    elif request.method == "GET":
        parameters = request.GET.dict()
    from django_jailuapp.settings import MEDIA_ROOT
    import os
    filename = os.path.join(MEDIA_ROOT, 'temp', parameters["file_name"])
    pdf = open(filename, 'rb')
    # response = HttpResponse(pdf.read())
    response = HttpResponse(pdf, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + parameters["file_name"] + '"'
    return response


@xframe_options_exempt #disable Xframe limit error
@csrf_exempt  # disable token for now
def api(request):
    from JailuApp.classes.global_code import Security
    Security.initialise(request)  # setup security
    parameters = None
    if request.method == "POST":
        parameters = request.POST.dict()
    elif request.method == "GET":
        parameters = request.GET.dict()
    api_response = {"error": True, "error_msg": "Unsupported Operation"}

    from JailuApp.classes.global_code import EW
    EW.notification_click_url = "http://"+request.get_host()  # save hostname for reuse

    if parameters.get("api_object",None) is not None and parameters.get("api_action",None) is not None:
        if parameters["api_object"] == "user_group":
            from JailuApp.classes.user_group import TableUserGroup
            api_response = TableUserGroup().perform_action(parameters)
        elif parameters["api_object"] == "user_account":
            from JailuApp.classes.user_account import TableUserAccount
            api_response = TableUserAccount().perform_action(parameters)
        elif parameters["api_object"] == "security_action":
            from JailuApp.classes.security_action import TableSecurityActions
            api_response = TableSecurityActions().perform_action(parameters)
        elif parameters["api_object"] == "system_log":
            from JailuApp.classes.system_log import TableSystemLog
            api_response = TableSystemLog().perform_action(parameters)
        elif parameters["api_object"] == "country":
            from JailuApp.classes.country import TableCountry
            api_response = TableCountry().perform_action(parameters)
        elif parameters["api_object"] == "department":
            from JailuApp.classes.department import TableDepartment
            api_response = TableDepartment().perform_action(parameters)
        elif parameters["api_object"] == "department_type":
            from JailuApp.classes.department_type import TableDepartmentType
            api_response = TableDepartmentType().perform_action(parameters)
        elif parameters["api_object"] == "department_supervisor":
            from JailuApp.classes.department_supervisor import TableDepartmentSupervisor
            api_response = TableDepartmentSupervisor().perform_action(parameters)
        elif parameters["api_object"] == "department_employee":
            from JailuApp.classes.department_employee import TableDepartmentEmployee
            api_response = TableDepartmentEmployee().perform_action(parameters)

    else:
        api_response["error"] = True
        api_response["error_msg"] = "No Action / Object Specified"

    json_response = JsonResponse(api_response)
    return HttpResponse(json_response, content_type="application/json")


@csrf_exempt  # disable token for now
@xframe_options_exempt #disable Xframe limit error
def upload_file(request):
    from JailuApp.classes.global_code import Security
    Security.initialise(request)  # setup security
    control_id = 'unknown'
    file_name = ''
    if request.method == 'POST' and request.FILES.__sizeof__() > 0:
        for file in request.FILES:
            control_id = str(file).replace("_uploader","")
            myfile = request.FILES[file]
            from JailuApp.classes.global_code import upload_temp_file
            # use random file name everytime to avoid errors in spaces in filename
            from datetime import datetime
            ticks = datetime.now().timestamp()
            ret = upload_temp_file(myfile, myfile.name)
            if ret["error"] is False:
                file_name = ret["uploaded_file_name"]  # save actual file_name
    #  tell iframe to do the needfull
    html = """
    <script>
    //set filename
    console.log('temp_file_saved','""" + control_id + """','""" + file_name + """');
    parent.document.getElementById('""" + control_id + """').value = '""" + file_name + """'; 
    //disable loader
    parent.document.getElementById('uploader_for_""" + control_id + """').style.display = "none"; 
    </script>
    """
    return HttpResponse(html)




