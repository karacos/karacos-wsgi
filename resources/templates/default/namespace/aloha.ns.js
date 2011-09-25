<%def name="activate_editor(instance)">
	##<%include file="${instance.get_aloha_template_uri()}"/>
	require(['order!karacos/conf/aloha-default','order!aloha'], function() {
		$('body').bind('aloha',function(){
			console.log("activating editor for semantic entity");
			$('[typeof][about]').find("[property]").aloha();
		});
	});
</%def>
<%def name="save_instance(instance)">
(function($,undefined) {
	var objects = $('[typeof][about="urn:uuid:${instance.id}"]'), model;
	model = VIE.ContainerManager.getInstanceForContainer(objects);
	//Backbone.sync('_update',model);
	model.save();
})(window.alohaQuery);
</%def>