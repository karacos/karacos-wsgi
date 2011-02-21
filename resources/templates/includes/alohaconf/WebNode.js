	GENTICS.Aloha.settings = {
			logLevels: {'error': true, 'warn': false, 'info': false, 'debug': false},
	   'i18n' : {
	     'current' : 'fr'
	   },
	   'base' : GENTICS_Aloha_base,
	   'ribbon' : true,
	   'plugins': {
				   "com.gentics.aloha.plugins.DragAndDropFiles": {
	   					config : { 'drop' : {'max_file_size': '2000000',
	   										 'max_file_count': 2,
	   										 'upload': {'url': "${instance._get_action_url()}",
	   										 			'extra_headers':{'Accept':'application/json'},
				   										'www_encoded': false }}},
					  	editables : {
							'#resource_title'	: {},
							'#resource_content': { 'drop' : {'max_file_size': '2000000',
	   										 'upload': {
	   										 			'config': {
		   										 			'url': '${instance._get_action_url()}',
		   										 			'extra_headers':{'Accept':'application/json'},
					   										'www_encoded': false }}}}
				   							
					  	}
	   				},
	   				"com.gentics.aloha.plugins.Image": {
	   					config : { 'img': { 'max_width': '50px',
	   										'max_height': '50px' }},
					  	editables : {
							'#resource_title'	: {}
					  	},
	   				},
	   				"org.karacos.aloha.Plugin": { 
	   				instance_url : "${instance._get_action_url()}",
	   				edit_content_action : "edit_content",
	   				idfieldsref : {
							resource_title	: "title",
							resource_content 	: "content"
					  	}},
					"com.gentics.aloha.plugins.Link": {
								config : [ 'a' ],
							  	editables : {
								'#resource_title'	: [  ]
							  	},
							  	targetregex : '^(?!.*${instance.__domain__['fqdn']}).*',
							  	target : '_blank',
							  	},
					"com.gentics.aloha.plugins.List": {
						editables : {
								'#resource_title'	: [  ]
							  	}
					},
					"com.gentics.aloha.plugins.Table": {
						editables : {
								'#resource_title'	: [  ],
								'#resource_content'	: [ 'table'  ]
							  	}
					},
		   			"com.gentics.aloha.plugins.Format": { 
						config : [ 'b', 'i','u','del','sub','sup', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat'],
					  	editables : {
							'#resource_title'	: [ ], // no formatting allowed
							'#resource_content' 	: [ 'b', 'i', 'u', 'del', 'sub', 'sup','h2', 'h3', 'h4', 'h5', 'h6', 'pre','removeFormat'  ] // just basic formattings, no headers, etc.
					  	}
					} // plugin
				} // plugins
				
		}; //Aloha.Settings
	$(function(){ 
			$("#resource_title").aloha();
			$("#resource_content").aloha();

});