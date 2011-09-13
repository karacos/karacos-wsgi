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
<% node_actions = instance.__domain__._get_actions() %>
function getActionButtonHandler(action) {
	return function(event) {
		KaraCos.getForm({
			url: "${instance.__domain__._get_action_url()}",
			form: action,
			callback: function(data, form) {
				var create_child_node_template = jsontemplate.Template(form, KaraCos.jst_options);
				actionwindow.empty().append(create_child_node_template.expand(data));
				actionwindow.find('.form_' + action + '_button').button()
				.click(function() {
					var params = {},
						method = action;
					$.each($(this).closest('form').serializeArray(), function(i, field) {
						if (field.name === "method") {
							method = field.value;
						} else {
							params[field.name] = field.value;
						}
					}); // each
					KaraCos.action({ url: "${instance.__domain__._get_action_url()}",
						method: method,
						async: false,
						params: params,
						callback: function(data) {
							if (data.success) {
								if (data.message !== undefined) {
									actionwindow.empty().append(data.message);	
								} else {
									actionwindow.dialog('destroy');
								}
								} else {
									if (data.message !== undefined) {
									actionwindow.empty().append(data.message);	
								} else {
									actionwindow.dialog('destroy');
								}
							}
						},
						error: function(data) {
							actionwindow.empty().append("error");
						}
					}); // POST login form
				});  // click
				actionwindow.dialog({width: '600px', modal:true}).show();
			}
		});			
	}
}
(function(submenu){
	var 
		item,
		actionwindow = KaraCos.actionMenu.actionWindow;
	% if 'create_child_node' in node_actions:
		item = KaraCos('<li><a href="#">Créer un noeud</a></li>');
		item.click(getActionButtonHandler('create_child_node'));
		submenu.append(item);
	%endif
	% if 'add_fqdn_alias' in node_actions:
		item = KaraCos('<li><a href="#">Ajouter un alias</a></li>');
		item.click(getActionButtonHandler('add_fqdn_alias'));
		submenu.append(item);
	% endif
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