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

(function domainSubMenu(submenu){
	var 
		item,
		actionwindow = KaraCos.actionWindow;
	if (auth.hasAction('create_child_node')) {
		item = KaraCos('<li><button>Créer un noeud</button></li>');
		item.find('button').button().click(actionsMenu.getActionFormButtonHandler("${instance.__domain__._get_action_url()}",'create_child_node'));
		submenu.append(item);
	}
	if (auth.hasAction('add_fqdn_alias')) {
		item = KaraCos('<li><button>Ajouter un alias</button></li>');
		item.find('button').button().click(actionsMenu.getActionFormButtonHandler("${instance.__domain__._get_action_url()}",'add_fqdn_alias'));
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