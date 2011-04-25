<% import karacos %>
<% import sys, traceback %>
% try:
<% request = karacos.serving.get_request() %>
<% session = karacos.serving.get_session() %>
% if 'instance_id' in request.str_params and 'base_id' in request.str_params:
<% instance = karacos.base.db[request.str_params['base_id']].db[request.str_params['instance_id']] %>
<% node_actions = instance._get_actions() %>
(function(submenu){
	var 
		item,
		actionwindow = KaraCos.actionMenu.actionWindow;
	% if 'create_child_node' in node_actions:
		item = KaraCos('<li><a href="#">Créer un noeud</a></li>');
		item.click(function(){
					KaraCos.getForm({
						url: "${instance._get_action_url()}",
						form: "create_child_node",
						callback: function(data, form) {
							var create_child_node_template = jsontemplate.Template(form, KaraCos.jst_options);
							actionwindow.empty().append(create_child_node_template.expand(data));
							actionwindow.find('.form_create_child_node_button').button()
							.click(function() {
								var params = {},
									method = 'create_child_node';
								$.each($(this).closest('form').serializeArray(), function(i, field) {
									if (field.name === "method") {
										method = field.value;
									} else {
										params[field.name] = field.value;
									}
								}); // each
								KaraCos.action({ url: "${instance._get_action_url()}",
									method: method,
									async: false,
									params: params,
									callback: function(data) {
										if (data.success) {
											
											actionwindow.dialog('close');
											
										}
									},
									error: function(data) {
										
									}
								}); // POST login form
							});  // click
							actionwindow.dialog({width: '600px', modal:true}).show();
						}
					});
				});
		submenu.append(item);
	%endif
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