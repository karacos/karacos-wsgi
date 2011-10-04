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
		item, subsubmenu, subitem,
		actionwindow = KaraCos.actionMenu.actionWindow;
	if (auth.hasAction('edit_domain')) {
		item = $('<li id="edit_domain_action_button"><a href="#">Modifier un domaine</a></li>');
		subsubmenu = $('<ul id="edit_domain_action_menu"></ul>');
		// TODO: move block to full js with json data
		<% domains = instance._domain_list() %>
		% for domain in domains:
			subitem = $('<li><a href="#">${domains[domain]["name"]}</a></li>');
		subitem.click(function(event){
			$.ajax({ url: "/fragment/edit_domain_form.jst",
				context: document.body,
				type: "GET",
				async: false,
				success: function(form) {
					var domain = {
							"name": "${domains[domain]['name']}",
							"url": "${instance._get_action_url()}",
							"fqdn": "${domains[domain]['fqdn']}"
					};
					var edit_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
					actionwindow.empty().append(edit_domain_template.expand(domain));
					actionwindow.find('.edit_domain_button').button()
					.click(function() {
						var params = {};
						$.each($(this).closest('form').serializeArray(), function(i, field) {
							if (field.name === "method") {
								method = field.value;
							} else {
								params[field.name] = field.value;
							}
						}); // each
						KaraCos.action({ url: "${instance._get_action_url()}",
							method: 'edit_domain',
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
		subsubmenu.append(subitem);
		%endfor
		item.append(subsubmenu);
		submenu.append(item);
		
	}
	if (auth.hasAction('create_domain')){
		item = KaraCos('<li><a href="#">Create Domain</a></li>');
		item.click(actionsMenu.getActionFormButtonHandler("${instance._get_action_url()}",'create_domain'));
//		function(event){
//			$.ajax({ url: "/fragment/create_domain_form.jst",
//				context: document.body,
//				type: "GET",
//				async: false,
//				success: function(form) {
//					var data = {
//							"url": "${instance._get_action_url()}",
//					};
//					var create_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
//					actionwindow.empty().append(create_domain_template.expand(data));
//					actionwindow.find('.create_domain_button').button()
//					.click(function() {
//						var params = {};
//						$.each($(this).closest('form').serializeArray(), function(i, field) {
//							if (field.name === "method") {
//								method = field.value;
//							} else {
//								params[field.name] = field.value;
//							}
//						}); // each
//						KaraCos.action({ url: "${instance._get_action_url()}",
//							method: 'create_domain',
//							async: false,
//							params: params,
//							callback: function(data) {
//								if (data.success) {
//									actionwindow.dialog('close');
//								}
//							},
//							error: function(data) {
//								
//							}
//						}); // POST login form
//					});  // click
//					actionwindow.dialog({width: '600px', modal:true}).show();
//				}
//			});
//		});
		submenu.append(item);
	}
	item = $('<li><a href="#">WebNode Menu</a><li>');
	subsubmenu = $('<ul></ul>');
	submenu.append(item);
	(function(submenu) {
		<%include file="/includes/actionmenu/WebNode.js"/>
	})(subsubmenu);
	item.append(subsubmenu);
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