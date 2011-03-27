	GENTICS.Aloha.settings = {
			logLevels: {'error': true, 'warn': false, 'info': false, 'debug': false},
	   'i18n' : {
	     'current' : 'fr'
	   },
	   'errorhandling': false,
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
							'[property*="title"]'	: {},
							'[property*="content"]': { 'drop' : {'max_file_size': '2000000',
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
							'[property*="title"]'	: {},
							'[property*="number"]'	: {},
							'[property*="price"]'	: {}
							
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
								'[property*="title"]'	: [  ],
								'[property*="number"]'	: [  ],
								'[property*="price"]'	: [  ]
							  	},
							  	targetregex : '^(?!.*${instance.__domain__['fqdn']}).*',
							  	target : '_blank'
							  	},
					"com.gentics.aloha.plugins.List": {
						editables : {
								'[property*="title"]'	: [  ],
								'[property*="price"]'	: [  ],
							  	'[property*="number"]'	: [  ]
							  	}
					},
					"com.gentics.aloha.plugins.Table": {
						editables : {
								'[property*="title"]'	: [  ],
								'[property*="number"]'	: [  ],
								'[property*="price"]'	: [  ],
								'[property*="content"]'	: [ 'table'  ]
							  	}
					},
		   			"com.gentics.aloha.plugins.Format": { 
						config : [ 'b', 'i','u','del','sub','sup', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat'],
					  	editables : {
							'[property*="title"]'	: [ ], // no formatting allowed
							'[property*="number"]'	: [  ],
							'[property*="price"]'	: [  ],
							'[property*="content"]' 	: [ 'b', 'i', 'u', 'del', 'sub', 'sup','h2', 'h3', 'h4', 'h5', 'h6', 'pre','removeFormat'  ] // just basic formattings, no headers, etc.
					  	}
					} // plugin
				} // plugins
				
		}; //Aloha.Settings