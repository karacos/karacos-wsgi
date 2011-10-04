<%def name="activate_editor(instance)">
	// default aloha.ns.js#activate_editor
	##<%include file="${instance.get_aloha_template_uri()}"/>
	Aloha.bind('aloha-ready',function(){
		console.log("activating editor for semantic entity");
		Aloha.jQuery('[typeof][about]').find("[property]").aloha();
	});
</%def>
<%def name="save_instance(instance)">
// default aloha.ns.js#save_instance
	var objects = $('[typeof][about=*"urn:uuid:${instance.id}"]'), model;
	model = VIE.ContainerManager.getInstanceForContainer(objects);
	//Backbone.sync('_update',model);
	model.save();
	Aloha.jQuery('[typeof][about]').find("[property]").mahalo();

</%def>