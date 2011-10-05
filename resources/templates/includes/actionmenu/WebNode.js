<% import karacos %>
<% import sys, traceback %>
% try:
<% request = karacos.serving.get_request() %>
<% session = karacos.serving.get_session() %>
<% response = karacos.serving.get_response() %>
<% instance = None %>
%try:
	<% instance = response.__instance__ %>
%except:
	
%endtry
% if 'instance_id' in request.str_params and 'base_id' in request.str_params:
<% instance = karacos.base.db[request.str_params['base_id']].db[request.str_params['instance_id']] %>
% endif

% if instance != None:
<% node_actions = instance._get_actions() %>
(function(submenu){
	var 
		item,
		actionwindow = KaraCos.actionMenu.actionWindow;
	if (auth.hasAction('reset_admin_ACL')){
		item = $('<li><button>Reinitialiser les droits</button></li>');
		item.find('button').button().click(actionsMenu.getActionButtonHandler("${instance._get_action_url()}",'reset_admin_ACL'));
		submenu.append(item);
	}
	if (auth.hasAction('add_attachment')){
		item = KaraCos('<li><button>Ajouter un ficher</button></li>');
		// add_attachment needs to use different handler, let it use default behavior for now
		// TODO: use html5 post as binary/base64 (see aloha DragnDrop plugin)
		item.find('button').button().click(function(){
			KaraCos.getForm({
				url: "${instance._get_action_url()}",
				form: "add_attachment",
				callback: function(data, form) {
					var add_attachment_template = jsontemplate.Template(form, KaraCos.jst_options);
					actionwindow.empty().append(add_attachment_template.expand(data));
//						actionwindow.find('.form_add_attachment_button').button()
//						.click(function() {
//							var params = {},
//								method = 'add_attachment';
//							// rought coding for upload
//							$(this).closest('form').submit();
////							$.each($(this).closest('form').serializeArray(), function(i, field) {
////								if (field.name === "method") {
////									method = field.value;
////								} else {
////									params[field.name] = field.value;
////								}
////							}); // each
////							KaraCos.action({ url: "${instance._get_action_url()}",
////								method: method,
////								async: false,
////								params: params,
////								callback: function(data) {
////									if (data.success) {
////										
////										actionwindow.dialog('close');
////										
////									}
////								},
////								error: function(data) {
////									actionwindow.empty().append(data.message);
////								}
////							}); // POST login form
//						});  // click
					actionwindow.dialog({width: '600px', modal:true}).show();
				}
			});
		});
		submenu.append(item);
	}
	if (auth.hasAction('create_child_node')) {
		item = $('<li><button>Créer un noeud</button></li>');
		item.find('button').button().click(actionsMenu.getActionFormButtonHandler("${instance._get_action_url()}",'create_child_node'));
		submenu.append(item);
	}
})(submenu);
% endif
% except:
	some errors :
	<pre>
		${sys.exc_info()}
		---
		%for line in traceback.format_exc().splitlines():
			${line}
		%endfor
	</pre>
% endtry