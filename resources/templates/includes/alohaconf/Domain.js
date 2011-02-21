
	GENTICS.Aloha.settings = {
	##logLevels: {'error': true, 'warn': true, 'info': true, 'debug': false},
	   'i18n' : {
	     'current' : 'fr'
	   },
	   'base' : GENTICS_Aloha_base,
	   'ribbon' : true,
	   'plugins': {
	   				"com.gentics.aloha.plugins.DragAndDropFiles": {
	   					config : { 'drop' : {'max_file_size': '200000',
	   										 'upload': {'uploader_class':'GENTICS.Aloha.Uploader',
	   										 			'config': {
		   										 			'url': '/content/',
		   										 			'extra_headers':{'Accept':'application/json'},
		   										 			'additional_params': {"location":""},
					   										'www_encoded': false }}}},
					  	editables : {
							'#domain_title'	: {},
							'#domain_content': { 'drop' : {'max_file_size': '200000',
	   										 'upload': {'uploader_class':'GENTICS.Aloha.Uploader',
	   										 			'config': {
		   										 			'url': '/content/',
		   										 			'extra_headers':{'Accept':'application/json'},
		   										 			'additional_params': {"location":""},
					   										'www_encoded': false }}}}
					  	}
	   				},
	   				"com.gentics.aloha.plugins.Image": {
	   					config : { 'img': { 'max_width': '50px',
	   										'max_height': '50px' }},
					  	editables : {
							'#domain_title'	: {}
							
					  	}
	   				},
	   				"org.karacos.aloha.Plugin": { 
	   				instance_url : "",
	   				edit_content_action : "edit_content",
	   				idfieldsref : {
							domain_title	: "title",
							domain_content 	: "content"
					  	}},
					"com.gentics.aloha.plugins.Link": {
								config : [ 'a' ],
							  	editables : {
								'#domain_title'	: [  ]
							  	},
							  	targetregex : '^(?!.*${instance.__domain__['fqdn']}).*',
							  	target : '_blank'
							  	},
					"com.gentics.aloha.plugins.List": {
						editables : {
								'#domain_title'	: [  ]
							  	}
					},
					"com.gentics.aloha.plugins.Table": {
						editables : {
								'#domain_title'	: [  ],
								'#domain_content'	: [ 'table'  ]
							  	}
					},
		   			"com.gentics.aloha.plugins.Format": { 
						config : [ 'b', 'i','u','del','sub','sup', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat'],
					  	editables : {
							'#domain_title'	: [ ], // no formatting allowed
							'#domain_content' 	: [ 'b', 'i', 'u', 'del', 'sub', 'sup','h2', 'h3', 'h4', 'h5', 'h6', 'pre','removeFormat'  ] // just basic formattings, no headers, etc.
					  	}
					} // plugin
				} // plugins
				
		}; //Aloha.Settings
	$(function(){ 

		$("#domain_title").aloha();
		$("#domain_content").aloha();
});