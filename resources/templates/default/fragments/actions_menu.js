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
define([], function() {
	
	return {
		drawMenu: function(container) 
		{	
			var 
				KaraCos = window.KaraCos,
				$ = window.kcQuery,
				auth = KaraCos.authManager;
			$('body').bind('kcready', function(){
				var logout = $('<button id="kc_tb_logout">Se déconnecter</button>'),
					domainMenuButton = $('<button id="kc_domain_menu_button" >Domain menu</button>'),
					domainMenu = $('<ul class="kc_menu" id="kc_domain_menu" style="display:none"></ul>'),
					nodeMenuButton = $('<button id="kc_node_menu_button" style="display:none" >${instance._get_type()} menu</button>'),
					nodeMenu = $('<ul class="kc_menu" id="kc_node_menu" style="display:none"></ul>'),
					userNameButton = $('<button id="kc_user_name_menu">${session['username']}</button>');
				
				container
					.append(nodeMenuButton)
					.append(userNameButton)
					.append(logout)
					.append(domainMenuButton)
					.append(domainMenu)
					.append(nodeMenu);
			
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
					domainMenu.css('left',domainMenuButton.offset().left);
					domainMenu.animate({"height": "toggle"});
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
					nodeMenu.css('left',nodeMenuButton.offset().left);
					nodeMenu.animate({"height": "toggle"});
				});
				% endif
				
				
				% if '_update' in node_actions:
					var editbutton = $('<button>Editer</button>').button(),
					savebutton = $('<button>Sauvegarder</button>').button();
				toolbar.prepend(editbutton);
				toolbar.prepend(savebutton);
				savebutton.hide();
				editbutton.click(
						function(event) {
							event.stopImmediatePropagation();
							event.preventDefault();
							KaraCos.activate_aloha();
							//var button = KaraCos.$(this),
							savebutton.show();
							editbutton.hide();
							${self.aloha.activate_editor(instance)}
						});
				savebutton.click(
						function(event) {
							event.stopImmediatePropagation();
							event.preventDefault();
							savebutton.hide();
							editbutton.show();
							${self.aloha.save_instance(instance)}
						}).hide();
				% endif
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