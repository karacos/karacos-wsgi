<%def name="activate_editor(instance)">
	<%include file="${instance.get_aloha_template_uri()}"/>
	KaraCos('body').bind('aloha',function(){
		KaraCos('[about="urn:uuid:${instance.id}"]').each(function(){
			KaraCos.$(this).vieSemanticAloha();
		});
	});
</%def>
<%def name="save_instance(instance)">
	var objects = KaraCos('[about="urn:uuid:${instance.id}"]'), model;
	model = VIE.ContainerManager.getInstanceForContainer(objects);
	//Backbone.sync('_update',model);
	model.save();
</%def>