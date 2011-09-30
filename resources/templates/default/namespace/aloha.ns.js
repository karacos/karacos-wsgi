<%def name="activate_editor(instance)">
	// aloha.ns.js#activate_editor
	##<%include file="${instance.get_aloha_template_uri()}"/>
	require(['vendor/ext-3.2.1/adapter/jquery/ext-jquery-adapter-debug'],
			function() {
		require(['vendor/ext-3.2.1/ext-all'], function() {
			require(['aloha-bootstrap'], function() {
				Aloha.bind('aloha-ready',function(){
					console.log("activating editor for semantic entity");
					Aloha.jQuery('[typeof][about]').find("[property]").aloha();
				});
			});
		});
	});
</%def>
<%def name="save_instance(instance)">
//aloha.ns.js#save_instance
	var objects = $('[typeof][about=*"urn:uuid:${instance.id}"]'), model;
	model = VIE.ContainerManager.getInstanceForContainer(objects);
	//Backbone.sync('_update',model);
	model.save();

</%def>