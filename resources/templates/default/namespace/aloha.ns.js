<%def name="activate_editor(instance)">
	<%include file="${instance.get_aloha_template_uri()}"/>
	KaraCos('body').bind('aloha',function(){
		KaraCos('[about="urn:uuid:${instance.id}"]').each(function(){
			var semantic_entity = this;
//			Aloha.bind('alohaI18nPluginsLoaded',
//				function(){
				KaraCos.$(semantic_entity).vieSemanticAloha();
//				});
		});
	});
</%def>
<%def name="save_instance(instance)">
	var objects = KaraCos('[about="urn:uuid:${instance.id}"]'), model;
	model = VIE.ContainerManager.getInstanceForContainer(objects);
	//Backbone.sync('_update',model);
	model.save();
</%def>