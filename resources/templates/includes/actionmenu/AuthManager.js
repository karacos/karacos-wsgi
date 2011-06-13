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
	% if 'create_user' in node_actions:
		
		item = KaraCos('<li id="create_user_action_button"><a href="#">Create user</a></li>');
		subsubmenu = KaraCos('<ul id="create_user_action_menu"></ul>');
		item.click(function(event){
			$.ajax({ url: "/fragment/create_user_form.jst",
				context: document.body,
				type: "GET",
				async: false,
				success: function(form) {
					var data = {
							"url": '${instance._get_action_url()}',
						},
						create_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
					actionwindow.empty().append(create_domain_template.expand(data));
					actionwindow.dialog({width: '600px', modal:true}).show();
					actionwindow.find('#add_username_to_group_field').autocomplete({
						appendTo: actionwindow.find('#add_username_to_group_field').parent(),
						source: function( request, response ) {
							KaraCos.action({ url: data.url,
								method: 'list_users',
								async: false,
								params: {},
								callback: function(data) {
									if (data.success) {
									response( $.map( data.data, function( item ) {
										return {
											label: item.name,
											value: item.name
										}
									}));
									actionwindow.find('#add_username_to_group_field')
									.parent().find(".ui-autocomplete").show();
									}
								},
								error: function(data) {
									
								}
							}); // POST login form
						},
//						'max-height': '100px',
//						'overflow-y': 'auto',
//						/* prevent horizontal scrollbar */
//						'overflow-x': 'hidden',
//						/* add padding to account for vertical scrollbar */
//						'padding-right': '20px',
//						minLength: 2,
//						select: function( event, ui ) {
//							console.log( ui.item ?
//								"Selected: " + ui.item.label :
//								"Nothing selected, input was " + this.value);
//						},
//						open: function() {
//							$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
//						},
//						close: function() {
//							$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
//						}
					});
					actionwindow.find('#add_user_to_groupname_field').autocomplete({
						appendTo: actionwindow.find('#add_user_to_groupname_field').parent(),
						source: function( request, response ) {
							KaraCos.action({ url: '${instance._get_action_url()}',
								method: 'list_groups',
								async: false,
								params: {},
								callback: function(data) {
									if (data.success) {
									response( $.map( data.data, function( item ) {
										return {
											label: item.name,
											value: item.name
										}
									}));
									actionwindow.find('#add_user_to_groupname_field')
										.parent().find(".ui-autocomplete").show();
									}
								},
								error: function(data) {
									
								}
							}); // POST login form
						},
//						'max-height': '100px',
//						'overflow-y': 'auto',
//						/* prevent horizontal scrollbar */
//						'overflow-x': 'hidden',
//						/* add padding to account for vertical scrollbar */
//						'padding-right': '20px',
//						minLength: 2,
//						select: function( event, ui ) {
//							console.log( ui.item ?
//								"Selected: " + ui.item.label :
//								"Nothing selected, input was " + this.value);
//						},
//						open: function() {
//							$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" ).show();
//						},
//						close: function() {
//							$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
//						}
					});
					actionwindow.find('.create_user_button').button()
					.click(function() {
						var params = {};
						$.each($(this).closest('form').serializeArray(), function(i, field) {
							if (field.name === "method") {
								method = field.value;
							} else {
								params[field.name] = field.value;
							}
						}); // each
						KaraCos.action({ url: data.url,
							method: 'create_user',
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
				}
			});
		});
		submenu.append(item);
	%endif
	% if 'list_users' in node_actions:
		item = KaraCos('<li id="create_group_action_button"><a href="#">List users</a></li>');
		item.click(function(event) {
			$.ajax({ url: "/fragment/list_users.jst",
				context: document.body,
				type: "GET",
				async: false,
				success: function(form) {
					var list_users_template = jsontemplate.Template(form, KaraCos.jst_options);
					KaraCos.action({ url: "${instance._get_action_url()}",
						method: 'list_users',
						async: false,
						params: {},
						callback: function(data) {
							if (data.success) {
								actionwindow.empty().append(list_users_template.expand(data));
								actionwindow.dialog({width: '600px', modal:true}).show();
								$.each(data.data, function(pos, user) {
									var $user = $('[about*="urn:uuid:' + user._id + '"]');
									$user.data(user);
									$user.find('a[href*="#view"]').click(function(event){
										event.stopPropagation();
										event.preventDefault();
										//TODO: do the show/modify user 
									})
								});
							}
						},
						error: function(data) {
							
						}
					});
				}
			});
		});
		submenu.append(item);
	% endif
% if 'create_group' in node_actions:
		
		item = KaraCos('<li id="create_group_action_button"><a href="#">Create group</a></li>');
		subsubmenu = KaraCos('<ul id="create_group_action_menu"></ul>');
		item.click(function(event){
			$.ajax({ url: "/fragment/create_group_form.jst",
				context: document.body,
				type: "GET",
				async: false,
				success: function(form) {
					var data = {
							"url": "${instance._get_action_url()}",
					};
					var create_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
					actionwindow.empty().append(create_domain_template.expand(data));
					actionwindow.find('.create_user_button').button()
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
							method: 'create_group',
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
	% if 'add_user_to_group' in node_actions:
		item = KaraCos('<li><a href="#">Add user to group</a></li>');
		item.click(function(event){
		$.ajax({ url: "/fragment/add_user_to_group_form.jst",
			context: document.body,
			type: "GET",
			async: false,
			success: function(form) {
				var data = {
						"url": "${instance._get_action_url()}",
				};
				var create_domain_template = jsontemplate.Template(form, KaraCos.jst_options);
				actionwindow.empty().append(create_domain_template.expand(data));
				actionwindow.find('.add_user_to_group_button').button()
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
						method: 'add_user_to_group',
						async: false,
						params: params,
						callback: function(data) {
							if (data.success) {
								actionwindow.dialog('close');
							}
						},
						error: function(data) {
							
						}
					});
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