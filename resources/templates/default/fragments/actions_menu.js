<%inherit file="/default/parent/actions_menu" />
<% import karacos %>
<% import sys, traceback %>
% try:
<% request = karacos.serving.get_request() %>
<% session = karacos.serving.get_session() %>
% if 'instance_id' in request.str_params and 'base_id' in request.str_params:
<% instance = karacos.base.db[request.str_params['base_id']].db[request.str_params['instance_id']] %>
<% node_actions = instance._get_actions() %>
<% domain_actions = instance.__domain__._get_actions() %>
<% isdomain = False %>
% if instance == instance.__domain__ :
	<% isdomain = True %>
% endif
define(['jquery'], function($) {
	
	return {
		/**
		 * Handles click for action requiring no parameters in menu
		 * --> handles send action invocation
		 * --> display result
		 * 
		 * @param url: node url
		 * @param action: action to request
		 */
		getActionButtonHandler: function (url, action) {
			return function(event) {
				actionwindow.empty().dialog({width: '600px', modal:true}).show();
				KaraCos.action({ url: url,
					method: action,
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
			}
		},
		/**
		 * Handles click for action requiring parameters in menu :
		 * --> Display action form
		 * --> handles send data
		 * --> display result
		 * 
		 * @param url: node url
		 * @param action: action to request
		 */
		getActionFormButtonHandler: function (url, action) {
			return function(event) {
				KaraCos.getForm({
					url: url,
					form: action,
					callback: function(data, form) {
						var create_child_node_template = jsontemplate.Template(form, KaraCos.jst_options),
							actionWindow = KaraCos.actionWindow;
						actionWindow.empty().append(create_child_node_template.expand(data));
						actionWindow.find('.form_' + action + '_button').button()
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
							KaraCos.action({ url: url,
								method: method,
								async: false,
								params: params,
								callback: function(data) {
									if (data.success) {
										if (data.message !== undefined) {
											actionWindow.empty().append(data.message);	
										} else {
											actionWindow.dialog('destroy');
										}
										} else {
											if (data.message !== undefined) {
												actionWindow.empty().append(data.message);	
										} else {
											actionWindow.dialog('destroy');
										}
									}
								},
								error: function(data) {
									actionWindow.empty().append("error");
								}
							}); // POST login form
						});  // click
						actionWindow.dialog({width: '600px', modal:true}).show();
					}
				});			
			}
		},
		drawMenu: function(container) 
		{	
			var 
				actionsMenu = this,
				KaraCos = window.KaraCos,
				$ = window.kcQuery,
				auth = KaraCos.authManager,
				username = auth.user_actions_forms.user;
			$('body').bind('kcready', function(){
				var login = $('<button class="kc_button" id="kc_tb_login">Se connecter</button>'),fblogin,
					logout = $('<button class="kc_button" id="kc_tb_logout">Se déconnecter</button>'),
					domainMenuButton = $('<button class="kc_button" id="kc_domain_menu_button" >Domain menu</button>'),
					domainMenu = $('<ul class="kc_button kc_menu" id="kc_domain_menu" style="display:none"></ul>'),
					nodeMenuButton = $('<button class="kc_button" id="kc_node_menu_button" style="display:none" >${instance._get_type()} menu</button>'),
					nodeMenu = $('<ul class="kc_button kc_menu" id="kc_node_menu" style="display:none"></ul>'),
					userNameButton = $('<button class="kc_button" id="kc_user_name_menu">' + username + '</button>');
				if (!auth.isUserConnected()) {
					// User is not connected
					container.append(login);
					if (typeof FB !== 'undefined') {
						// Facebook button
						fblogin = $('<button>Se connecter avec facebook</button>');
						fblogin.button().click(function(){
							FB.login(function(response) {
								  if (response.authResponse) {
								    // user successfully logged in
								  } else {
								    // user cancelled login
								  }
								});
							}, {scope:'email'});
						container.append(fblogin);
					
					}
					// standard site registration login
					login.button().click(function(){
						auth.provideLoginUI(function(){
							auth.authenticationHeader(elem);
						});
					});
					//TODO : Google+ Login
					
					// break method...
					return;
				}
				
				// User is connected...
				
				container
					.append(nodeMenuButton)
					.append(userNameButton)
					.append(logout)
					.append(domainMenuButton)
					.append(domainMenu)
					.append(nodeMenu);
				logout.button().click(function(){
					auth.logout();
				});
				toolbar = $('#karacos_actions_toolbar');
				$(document).click(function hideMenuAtDocumentClickHandler(event){
					container.find('ul.kc_menu').hide();
				});
				if (typeof KaraCos.actionMenu === "undefined") {
					KaraCos.actionMenu = {};
					KaraCos.actionWindow = KaraCos('<div id="kc_action_menu"/>');
					$('body').append(KaraCos.actionWindow);
				}
				(function includeDomainMenu(submenu){
					<%include file="${instance.__domain__.get_menu_template_uri()}"/>
				})(domainMenu);
				domainMenu.menu().hide();
				domainMenuButton.addClass('menu').button({
					icon: 'ui-icon-triangle-1-s',
					orientation: 'r',
					checkButtonset: true
				}).click(function menuClickHandler(event) { 
					$('ul.kc_menu').hide();
					event.stopImmediatePropagation();
					event.preventDefault();
					domainMenu.css('position','absolute');
					domainMenu.css('left',domainMenuButton.offset().left + Number(domainMenuButton.css("width").match(/([0-9]*).*/)[1]));
					domainMenu.css('top',domainMenuButton.offset().top);
					domainMenu.animate({"width": "toggle"});
				});
				
				% if not isdomain:
					$(nodeMenuButton).show();
				(function includeInstanceMenu(submenu){
					<%include file="${instance.get_menu_template_uri()}"/>
				})(nodeMenu);
				nodeMenu.menu().hide();
				nodeMenuButton.addClass('menu').button({
					icon: 'ui-icon-triangle-1-s',
					orientation: 'r',
					checkButtonset: true
				}).click(function() { 
					$('ul.kc_menu').hide();
					event.stopImmediatePropagation();
					event.preventDefault();
					nodeMenu.css('position','absolute');
					nodeMenu.css('left',nodeMenuButton.offset().left + Number(nodeMenuButton.css("width").match(/([0-9]*).*/)[1]));
					nodeMenu.css('top',nodeMenuButton.offset().top);
					nodeMenu.animate({"width": "toggle"});
				});
				% endif
				
				
				if (auth.hasAction('_update')) {
					var editbutton = $('<button class="kc_button">Editer</button>').button(),
						savebutton = $('<button class="kc_button">Sauvegarder</button>').button();
					toolbar.prepend(editbutton);
					toolbar.prepend(savebutton);
					savebutton.hide();
					editbutton.click(
							function(event) {
								event.stopImmediatePropagation();
								event.preventDefault();
								KaraCos.activate_aloha(
									function() {
										savebutton.show();
										editbutton.hide();
										${self.aloha.activate_editor(instance)}
									}
								);
								//var button = KaraCos.$(this),
							});
					savebutton.click(
							function(event) {
								event.stopImmediatePropagation();
								event.preventDefault();
								savebutton.hide();
								editbutton.show();
								${self.aloha.save_instance(instance)}
							}).hide();
					
				}
				// user_menu
				userNameButton.button().click(function(event){
					var
					$this = $(this),
					$win = $('#kc_user_profile_win');
					if ($win.length === 0) {
						$win = $('<div id="kc_user_profile_win" title="User profile"/>');
						$('body').append($win);
						
					}
					event.stopImmediatePropagation();
					event.preventDefault();
					$.ajax({url:'/fragment/user_profile.html',
						context: document.body,
						type: "GET",
						async: false,
						success: function(form) {
							$win.empty().append(form);
							$win.dialog({width: '500px',modal: true,
								buttons: { "Ok": function() {
									var
									method = "modify_person_data",
									params = {};
									$.each($win.find('form').serializeArray(), function(i, field) {
										if (field.name === "method") {
											method = field.value;
										} else {
											params[field.name] = field.value;
										}
									}); // each
									KaraCos.action({ url: "/",
										method: method,
										async: false,
										params: params,
										callback: function(data) {
											if (data.success) {
												$win.dialog('close');
											}
										},
										error: function(data) {
											
										}
									}); // POST profile form
								} // button OK
							
								} // buttons
							}); // $win.dialog()
							$win.dialog('show');
						}
					});
				});
			});
		} // function drawmenu
	} // returned object
}); // define
%endif
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