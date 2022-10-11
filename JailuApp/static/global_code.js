// get value and return value with commas
function val_add_commas(nStr){
	nStr = String(nStr).replace( /\,/g, "");
	var x = nStr.split( '.' );
	var x1 = x[0];
	var x2 = x.length > 1 ? '.' + x[1] : '';
	var rgx = /(\d+)(\d{3})/;
	while ( rgx.test(x1) ) {
		x1 = x1.replace( rgx, '$1' + ',' + '$2' );
	}
	return x1 + x2;
}

// get value and return value without commas
function val_remove_commas(nStr){
	return String(nStr).replace(/[,]/g,"");
}

// get value in element, add commas and save it back
function ele_add_commas(input){
	var nStr = input.value + '';
	input.value = val_add_commas(nStr);
}


// Check if same text
function sameText(o1, o2) {
    return (String(o1).toLowerCase() == String(o2).toLowerCase());
}

function is_empty(value, o2) {
	if(value === null)
		return true;
	else if(value === undefined)
		return true;
	else if(String(value).length === 0)
		return true;
	else
		return false;
}

function round(value,places = 2){
	//return Math.round((parseFloat(value) + Number.EPSILON) * 100) / 100;
	return parseFloat((parseFloat(value).toFixed(places)));
}

// Check if same string
function sameString(o1, o2) {
    return (String(o1) == String(o2));
}

function smoothScrollTo(selector) {
	$('html, body').animate({
                    scrollTop: $(selector).offset().top
                }, 1000);
}

var def_show_form_options = {
	destination_element: "#content_body",
	records_per_page: EW.records_per_page,
	params:{}
}




function ShowForm(element, action, object, object_id = null, current_page = 1, options = def_show_form_options)
{

	//cleanup options if needed
	options.destination_element = options.destination_element === undefined?def_show_form_options.destination_element:options.destination_element;
	//for records_per_page dont modify if custom was provided
	options.records_per_page = options.records_per_page === undefined?def_show_form_options.records_per_page:options.records_per_page;
	options.params = options.params === undefined?def_show_form_options.params:options.params;

	const ex_filter_form_values = CollectExFilterParameters(object);

	var pagination = "{}";
	if(action === EW.action.List || action === EW.action.ExcelExport)
	{

		pagination = JSON.stringify({'records_per_page': options.records_per_page, 'current_page': current_page});
	}

	//disable button
	var old_html = "";
	//check if called from click
	if(element !== undefined && element != null)
	{
		old_html = $(element).html();
		$(element).html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>Loading...");
		$(element).attr("disabled","true");
	}



    $.ajax({
		type: "POST",
		cache: false,
		url: "api",
		dataType :"json",
		data: { rand_time: new Date().getTime(), api_object: object, api_action: action
			, object_id: object_id, pagination: pagination
			, ex_filter_values: JSON.stringify(ex_filter_form_values)
			, params: JSON.stringify(options.params)
		} ,
		//url: "test_api.php",
		success: function(response){
			//enable button
			//check if called from click
			if(element !== undefined && element != null)
			{
				$(element).html(old_html);
				$(element).removeAttr("disabled");
			}

		  //console.log(response);
		  //read data out
		  if(response.error === false)
		  {
		  	//check if it an export and dont bother with content
			  if (response.download_file_name !== undefined)
			  {
			  	console.log(response);
			  	const win = window.open('download?file_name='+response.download_file_name, '_blank');
				if (win) {
					//Browser has allowed it to be opened
					win.focus();
				} else {
					//Browser has blocked it
					ShowFailureMessage('Please allow popups for this website, To download exported files');
				}
			  }
			  else // any other actions deal with showing content
			  {
			  	if(response.header_title !== undefined) //if mising dont action
				{
					$("#header_title").html(response.header_title);
					//smooth scroll to top of page
				  	smoothScrollTo(".app-header");
				}
			  	if(response.content_title !== undefined) //if mising dont action
				{
					$("#content_title").html(response.content_title);
				}
			  	$(options.destination_element).html(response.content_body)


			  }

		  }
		  else
		  {
		       //show error message
			  ShowFailureMessage(response.error_msg)
			  console.log('failed error:'+response.error_msg);
		  }
		},
		error: function(data){
		//enable button
		//check if called from click
		if(element !== undefined && element != null)
		{
			$(element).html(old_html);
			$(element).removeAttr("disabled");
		}
		console.log('failed to Load form:',data);
		//show error message
		ShowFailureMessage("Oops Server failed to complete this request");
		}
		});

}

function CollectFormParameters(object)
{
	var field_identifier = '[table_object_name="'+object+'"]';
	var form_values = {};
	//get all fields
	$.each( $(field_identifier), function( key, value ) {
		//console.log(this);
		var field_name = $(this).attr('field_object_name');
		var field_value = $(this).val();

		//add to collection
		form_values[field_name] = field_value;
	});
	return form_values;
}


function CollectExFilterParameters(object)
{
	var field_identifier = '#list_ex_filter_content [table_object_name="'+object+'"]';
	var form_values = {};
	//get all fields
	$.each( $(field_identifier), function( key, value ) {
		//console.log(this);
		var field_name = $(this).attr('field_object_name');
		var field_value = $(this).val();

		//add to collection
		form_values[field_name] = field_value;
	});
	return form_values;
}

function ShowSuccessMessage(mesage)
{
	Swal.fire({
		toast: true,
		position: 'top-end',
		showConfirmButton: false,
		timer: 3000,
		type: 'success',
		title: mesage
      })
}


function ShowFailureMessage(mesage)
{
	Swal.fire({toast: false,
		position: 'center',
	    type: 'error',
	    title: 'Oops',
		html: mesage,
		showConfirmButton: true
})
}

function DialogShowSuccessMessage(mesage)
{

	Swal.fire({
		toast: false,
		position: 'center',
		showConfirmButton: true,
		type: 'success',
		title: mesage
	  })
}
function DialogShowInfoMessage(mesage)
{

	Swal.fire({
		toast: false,
		position: 'center',
		showConfirmButton: true,
		type: 'info',
		title: mesage
	  })
}

var def_delete_form_options = {
	return_action: EW.action.List,
	return_object_id: null,
	return_current_page: 1,
	params:{
		destination_element: "#content_body",
		records_per_page: EW.records_per_page,
		params:{},
	}
}

function ConfirmCustomAction(element,object,action,object_id,message, options = def_delete_form_options)
{
	//cleanup options
	options.return_object = options.return_object === undefined?object:options.return_object;
	options.return_action = options.return_action === undefined?def_delete_form_options.return_action:options.return_action;
	options.return_object_id = options.return_object_id === undefined?def_delete_form_options.return_object_id:options.return_object_id;
	options.return_current_page = options.return_current_page === undefined?def_delete_form_options.return_current_page:options.return_current_page;
	options.params = options.params === undefined?def_delete_form_options.params:options.params;
	options.params.destination_element = options.params.destination_element === undefined?def_delete_form_options.params.destination_element:options.params.destination_element;
	options.params.records_per_page = options.params.records_per_page === undefined?def_delete_form_options.params.records_per_page:options.params.records_per_page;
	options.params.params = options.params.params === undefined?def_delete_form_options.params.params:options.params.params;

	Swal.fire({
		position: 'center',
		title: 'Are you sure?',
		html: message,
		type: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Yes do it!',
}).then((result) => {
  if (result.value) {
    SubmitForm(element,action, object, object_id, options);
  }
})
}

function ConfirmDelete(element,object,object_id,message, options = def_delete_form_options)
{
	//cleanup options
	options.return_object = options.return_object === undefined?object:options.return_object;
	options.return_action = options.return_action === undefined?def_delete_form_options.return_action:options.return_action;
	options.return_object_id = options.return_object_id === undefined?def_delete_form_options.return_object_id:options.return_object_id;
	options.return_current_page = options.return_current_page === undefined?def_delete_form_options.return_current_page:options.return_current_page;
	options.params = options.params === undefined?def_delete_form_options.params:options.params;
	options.params.destination_element = options.params.destination_element === undefined?def_delete_form_options.params.destination_element:options.params.destination_element;
	options.params.records_per_page = options.params.records_per_page === undefined?def_delete_form_options.params.records_per_page:options.params.records_per_page;
	options.params.params = options.params.params === undefined?def_delete_form_options.params.params:options.params.params;

	Swal.fire({
		position: 'center',
		title: 'Are you sure?',
		html: message,
		type: 'warning',
		showCancelButton: true,
		confirmButtonColor: '#3085d6',
		cancelButtonColor: '#d33',
		confirmButtonText: 'Yes delete it!',
}).then((result) => {
  if (result.value) {
    SubmitForm(element,EW.action.Delete, object, object_id, options);
  }
})
}



var def_submit_form_options = {
	"return_action": EW.action.List,
	"return_object_id": null,
	"return_current_page": 1,
	"params":{
		"destination_element": "#content_body",
		"records_per_page": EW.records_per_page,
		"params":{},
	}
}


function SubmitForm(element,action, object, object_id = null, options = def_submit_form_options)
{
	//cleanup options
	options.return_object = options.return_object === undefined?object:options.return_object;
	options.return_action = options.return_action === undefined?def_delete_form_options.return_action:options.return_action;
	options.return_object_id = options.return_object_id === undefined?def_delete_form_options.return_object_id:options.return_object_id;
	options.return_current_page = options.return_current_page === undefined?def_delete_form_options.return_current_page:options.return_current_page;
	options.params = options.params === undefined?def_delete_form_options.params:options.params;
	options.params.destination_element = options.params.destination_element === undefined?def_delete_form_options.params.destination_element:options.params.destination_element;
	options.params.records_per_page = options.params.records_per_page === undefined?def_delete_form_options.params.records_per_page:options.params.records_per_page;
	options.params.params = options.params.params === undefined?def_delete_form_options.params.params:options.params.params;

	//disable button
	var old_html = $(element).html();
	$(element).html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>Working...");
	$(element).attr("disabled","true");

	const active_form_values = CollectFormParameters(object);
	//console.log(active_form_values);
    $.ajax({
		type: "POST",
		cache: false,
		url: "api",
		dataType :"json",
		data: { rand_time:new Date().getTime(), api_object: object, api_action: action, object_id: object_id
			, form_values: JSON.stringify(active_form_values), params: JSON.stringify(options.params)} ,
		//url: "test_api.php",
		success: function(response){

			//enable button
			$(element).html(old_html);
			$(element).removeAttr("disabled");

		  //console.log(response);
		  //read data out
		  if(response.error === false)
		  {
			//in case its a file download
			if (response.download_file_path !== undefined)
			  {
			  	console.log(response);
			  	const win = window.open(response.download_file_path, '_blank');
				if (win) {
					//Browser has allowed it to be opened
					win.focus();
				} else {
					//Browser has blocked it
					ShowFailureMessage('Please allow popups for this website, To download exported files');
				}
			  }
			//in case it was to send an email
			else if (response.email_export !== undefined)
				{
					ShowSuccessMessage(response.error_msg);
				}
				else
				{
					//show success message
				   ShowSuccessMessage(response.error_msg);
				  //got to next page
				  ShowForm(element,options.return_action, options.return_object, options.return_object_id
					  , options.return_current_page, options.params)
				}

		  }
		  else
		  {
		      //show error message
			  ShowFailureMessage(response.error_msg)
		  }
		},
		error: function(data){
			//enable button
			$(element).html(old_html);
			$(element).removeAttr("disabled");
			console.log('failed to Load form:',data);
			//show error message
			ShowFailureMessage("Oops Server failed to complete this request");
		}
		});

}



function SubmitPermissionsForm(object_id = null)
{
	const action = "submit_permissions";
	const object = "user_group";
	const next_action = EW.action.List;
	var field_identifier = '[item_type="permission_row"]';
	var permission_list = [];
	//get all fields
	$.each( $(field_identifier), function( key, value ) {
		const permission_row = {};
		//console.log(this);
		const table_name = $(this).attr('table_name');
		permission_row["table_name"] = table_name;
		permission_row["add"] = $('[item_type="add"][table_value="'+table_name+'"]input').prop("checked");
		permission_row["edit"] = $('[item_type="edit"][table_value="'+table_name+'"]input').prop("checked");
		permission_row["delete"] = $('[item_type="delete"][table_value="'+table_name+'"]input').prop("checked");
		permission_row["list"] = $('[item_type="list"][table_value="'+table_name+'"]input').prop("checked");
		permission_row["view"] = $('[item_type="view"][table_value="'+table_name+'"]input').prop("checked");
		permission_list.push(permission_row);

	});

	//console.log(active_form_values);
    $.ajax({
		type: "POST",
		cache: false,
		url: "api",
		dataType :"json",
		data: { rand_time: new Date().getTime(), api_object: object, api_action: action, object_id: object_id, permission_list: JSON.stringify(permission_list)} ,
		//url: "test_api.php",
		success: function(response){
		  //console.log(response);
		  //read data out
		  if(response.error === false)
		  {
		  	   //show success message
		  	   ShowSuccessMessage(response.error_msg);
			  //got to next page
			  ShowForm(null,next_action,object);
		  }
		  else
		  {
		      //show error message
			  ShowFailureMessage(response.error_msg)
		  }
		},
		error: function(data){
		console.log('failed to Load form:',data);
		//show error message
		ShowFailureMessage("Oops Server failed to complete this request");
		}
		});

}



function SubmitLoginForm()
{
	const object_id = null
	const active_form_values = {};
	active_form_values["user_name"] = $("#user_name").val();
	active_form_values["password"] = $("#password").val();

	//console.log(active_form_values);
    $.ajax({
		type: "POST",
		cache: false,
		url: "api",
		dataType :"json",
		data: { rand_time: new Date().getTime(), api_object: "security_action", api_action: "submit_login", object_id: object_id, form_values: JSON.stringify(active_form_values)} ,
		//url: "test_api.php",
		success: function(response){
		  //console.log(response);
		  //read data out
		  if(response.error === false)
		  {
		  	   //show success message
		  	   ShowSuccessMessage(response.error_msg);
			  //reload empty page
			  window.location.reload();
		  }
		  else
		  {
		      //show error message
			  ShowFailureMessage(response.error_msg)
		  }
		},
		error: function(data){
		console.log('failed to Load form:',data);
		//show error message
		ShowFailureMessage("Oops Server failed to complete this request");
		}
		});

}


function SubmitLogOutForm()
{
	const object_id = null
	const active_form_values = {};

	//console.log(active_form_values);
    $.ajax({
		type: "POST",
		cache: false,
		url: "api",
		dataType :"json",
		data: { rand_time: new Date().getTime(), api_object: "security_action", api_action: "submit_logout", object_id: object_id, form_values: JSON.stringify(active_form_values)} ,
		//url: "test_api.php",
		success: function(response){
		  //console.log(response);
		  //read data out
		  if(response.error === false)
		  {
		  	   //show success message
		  	   ShowSuccessMessage(response.error_msg);
			  //got to next page
			  window.location.reload();
		  }
		  else
		  {
		      //show error message
			  ShowFailureMessage(response.error_msg)
		  }
		},
		error: function(data){
		console.log('failed to Load form:',data);
		//show error message
		ShowFailureMessage("Oops Server failed to complete this request");
		}
		});

}

function send_browser_notification(title, options)
{

	// Let's check if the browser supports notifications
  if (!("Notification" in window)) {
    console.log("This browser does not support desktop notification");
  }

  // Let's check whether notification permissions have already been granted
  else if (Notification.permission === "granted") {
    // If it's okay let's create a notification
    var notification = new Notification(title, options);
      //notification.renotify = true;
	  notification.onclick = function() {
	   window.open(EW.notification_click_url);
	  };
  }

  // Otherwise, we need to ask the user for permission
  else if (Notification.permission !== "denied") {
    console.log("Please enable notifications");
  }


}

function request_notification_permission()
{
	// request permission on page load
	 if (!Notification) {
	  ShowFailureMessage('Desktop notifications not available in your browser. Try Chrome.');
	  return;
	 }

	 if (Notification.permission !== 'granted')
	  Notification.requestPermission().then(function (permission) {
      // If the user accepts, let's create a notification
      if (permission === "granted") {
        send_browser_notification('Hey There',{
		requireInteraction: false,
		vibrate: [200, 100, 200],
		icon: EW.notification_icon,
		body: 'You will receive notification from now on',
	  })
      }
    });

}

function start_tempUpload(control_id){
	  $('#uploader_for_'+control_id).show(); // show loader
	  $('#form_for_'+control_id).submit(); // Submit the form
}

function capture_selection_radio_button(control_id){
      parent_control_id = $(control_id).attr("data-radiofor");
      var my_value = $(control_id).val();
	  $('#'+parent_control_id).val(my_value); // save value
}

function capture_selection_checkbox(control_id){
      parent_control_id = $(control_id).attr("data-checkboxfor");
      var my_value = "";
      // go through all checked checkboxes getting values for those ticked
      $.each( $('[data-checkboxfor="'+parent_control_id+'"]:checkbox:checked'), function( key, value ) {
		//console.log(this);
		var field_value = $(this).val();
		if (my_value == "")
		{
			my_value += field_value;
		}
		else
		{
			my_value += ","+field_value;
		}
	});
	  $('#'+parent_control_id).val(my_value); // save value
}


function draw_fusion_chart(chart_type,renderAt,api_object,api_action,parameters = {})
{
	$.ajax({
			type: "GET",
			cache: false,
			url: "api?api_object="+api_object+"&api_action="+api_action+"&rand_time="+new Date().getTime(),
			dataType :"json",
			data: parameters ,
			success: function(response){
			  //console.log(response);
			  //read data out
			  if(response.error === false)
			  {
				  var categories = response.chart_data.categories === undefined?[]:response.chart_data.categories;
				  var dataset = response.chart_data.dataset === undefined?[]:response.chart_data.dataset;
				  var data = response.chart_data.data === undefined?[]:response.chart_data.data;
				  if(categories != null && dataset != null){
					FusionCharts.ready(function() {
					  var revenueChart = new FusionCharts({
						type: chart_type,
						renderAt: renderAt,
						width: "100%",
						height: "100%",
						dataFormat: "json",
						dataSource: {
						  "chart": {
							"caption": response.chart_data.chart_options.caption,
							"subcaption": response.chart_data.chart_options.subcaption,
							"xaxisname": response.chart_data.chart_options.xaxisname,
							"yaxisname": response.chart_data.chart_options.yaxisname,
							"formatnumberscale": response.chart_data.chart_options.formatnumberscale,
							"plottooltext": response.chart_data.chart_options.plottooltext,
							"drawcrossline": response.chart_data.chart_options.drawcrossline,
							"exportEnabled": response.chart_data.chart_options.exportEnabled
						  },
						  "categories": categories,
						  "dataset": dataset,
						  "data": data
						}
					  }).render();

					});


				  }
			  }
			  else
			  {
				   //show error message
				  ShowFailureMessage(response.error_msg)
				  console.log('failed to pick '+api_action+' error:'+response.error_msg);
			  }
			},
			error: function(data){
				console.log('failed to Load form:',data);
				//show error message
				ShowFailureMessage("Oops Server failed to complete this request, Check your Internet Connection");
			}


	});

}


function get_draw_html(renderAt,api_object,api_action,parameters = {})
{
	$.ajax({
			type: "GET",
			cache: false,
			url: "api?api_object="+api_object+"&api_action="+api_action+"&rand_time="+new Date().getTime(),
			dataType :"json",
			data: parameters ,
			success: function(response){
			  //console.log(response);
			  //read data out
			  if(response.error === false)
			  {
				  var html = response.html;
				  $(renderAt).html(html);
			  }
			  else
			  {
				   //show error message
				  ShowFailureMessage(response.error_msg)
				  console.log('failed to pick '+api_action+' error:'+response.error_msg);
			  }
			},
			error: function(data){
				console.log('failed to Load form:',data);
				//show error message
				ShowFailureMessage("Oops Server failed to complete this request, Check your Internet Connection");
			}


	});

}


function get_concatenate_html(renderAt,api_object,api_action,parameters = {})
{
	$.ajax({
			type: "GET",
			cache: false,
			url: "api?api_object="+api_object+"&api_action="+api_action+"&rand_time="+new Date().getTime(),
			dataType :"json",
			data: parameters ,
			success: function(response){
			  //console.log(response);
			  //read data out
			  if(response.error === false)
			  {
				  var html = response.html;
				  $(renderAt).append(html);
			  }
			  else
			  {
				   //show error message
				  ShowFailureMessage(response.error_msg)
				  console.log('failed to pick '+api_action+' error:'+response.error_msg);
			  }
			},
			error: function(data){
				console.log('failed to Load form:',data);
				//show error message
				ShowFailureMessage("Oops Server failed to complete this request, Check your Internet Connection");
			}


	});

}

function submit_on_enter(event,identifier){
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if(keycode == '13'){
		$("#submit_form_"+identifier).click()
	}
}

function SubmitChangePassword(element)
  {
        const object_id = null
        const active_form_values = {};
        var old_password = $("#old_password").val();
        var new_password = $("#new_password").val();
        var new_password_2 = $("#new_password_2").val();

        //disable button
        var old_html = $(element).html();
        $(element).html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span>Working...");
        $(element).attr("disabled","true");

        //console.log(active_form_values);
        $.ajax({
            type: "POST",
            cache: false,
            url: "api",
            dataType :"json",
            data: { rand_time: new Date().getTime(), api_object: 'security_action'
                , api_action: "confirm_change_password", object_id: object_id
                , old_password: old_password, new_password: new_password, new_password_2: new_password_2
                , status: $("#status").val()
                , comment: $("#comment").val()
            } ,
            success: function(response){
              //console.log(response);
              //read data out

              //enable button
              $(element).html(old_html);
              $(element).removeAttr("disabled");

              if(response.error === false)
              {
                   //show success message
                   DialogShowSuccessMessage(response.error_msg);
                   window.location.reload();

              }
              else
              {
                  //show error message
                  ShowFailureMessage(response.error_msg)
              }
            },
            error: function(data){
            //enable button
            $(element).html(old_html);
            $(element).removeAttr("disabled");
            console.log('failed to Load form:',data);
            //show error message
            ShowFailureMessage("Oops Server failed to complete this request");
            }
            });

  }

//event for those triggered on blur to also be triggered one enter
function trigger_blur_event_on_enter(event,identifier){
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if(keycode == '13'){
		//get the vent set for on blur and tell it to run
		$(identifier)[0].onblur();

	}
}

//placeholder event handler for google maps
function initMap() {
	
}

