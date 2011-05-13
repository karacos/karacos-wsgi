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
		item, subsubmenu, subitem,
		actionwindow = KaraCos.actionMenu.actionWindow;
	% if 'edit_domain' in node_actions:
		
		item = KaraCos('<li id="edit_domain_action_button"><a href="#">Modifier un domaine</a></li>');
		subsubmenu = KaraCos('<ul id="edit_domain_action_menu"></ul>');
		<% domains = instance._domain_list() %>
		% for domain in domains:
			subitem = KaraCos('<li><a href="#">${domains[domain]["name"]}</a></li>');
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
	%endif
	% if 'create_domain' in node_actions:
		item = KaraCos('<li><a href="#">Create Domain</a></li>');
		item.click(function(event){
		$.ajax({ url: "/fragment/create_domain_form.jst",
			context: document.body,
			type: "GET",
			async: false,
			success: function(form) {
				var data = {
						"url": "${instance._get_action_url()}",
				};
				var create_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
				actionwindow.empty().append(create_domain_template.expand(data));
				actionwindow.find('.create_domain_button').button()
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
						method: 'create_domain',
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
	% endif
	item = KaraCos('<li><a href="#">WebNode</a><li>');
	subsubmenu = KaraCos('<ul></ul>');
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