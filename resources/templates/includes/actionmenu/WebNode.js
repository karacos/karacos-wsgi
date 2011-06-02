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
	% if 'reset_admin_ACL' in node_actions:
	item = KaraCos('<li><a href="#">Reinitialiser les droits</a></li>');
	item.click(function(){
		actionwindow.empty().dialog({width: '600px', modal:true}).show();
		KaraCos.action({ url: "${instance._get_action_url()}",
			method: 'reset_admin_ACL',
			async: true,
			params: {},
			callback: function(data) {
				if (data.success) {
					actionwindow.append(data.message);
				}
			},
			error: function(data) {
				actionwindow.append(data.message);
			}
		}); // POST login form
	});  // click
	submenu.append(item);
	% endif
	% if 'add_attachment' in node_actions:
		item = KaraCos('<li><a href="#">Ajouter un ficher</a></li>');
	item.click(function(){
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
	% endif
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