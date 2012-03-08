(function(window,undefined){
			var
				$ = window.jQuery,
				Aloha = window.Aloha,
				$body = $('body');

			Aloha.settings = {
					logLevels: {'error': true, 'warn': true, 'info': true, 'debug': true},
					errorhandling : false,
					ribbon: false,

					"placeholder": {
						'*': '<img src="http://aloha-editor.org/logo/Aloha%20Editor%20HTML5%20technology%20class%2016.png" alt="logo"/>&nbsp;Placeholder All',
						'#typo3span': 'Placeholder for span'
					},
					"i18n": {
						// you can either let the system detect the users language (set acceptLanguage on server)
						// In PHP this would would be '<?=$_SERVER['HTTP_ACCEPT_LANGUAGE']?>' resulting in
						// "acceptLanguage": 'de-de,de;q=0.8,it;q=0.6,en-us;q=0.7,en;q=0.2'
						// or set current on server side to be in sync with your backend system
						"current": "en"
					},
					"repositories": {
						"com.gentics.aloha.repositories.LinkList": {
							data: [
										{ name: 'Aloha Developers Wiki', url:'http://www.aloha-editor.com/wiki', type:'website', weight: 0.50 },
										{ name: 'Aloha Editor - The HTML5 Editor', url:'http://aloha-editor.com', type:'website', weight: 0.90  },
										{ name: 'Aloha Demo', url:'http://www.aloha-editor.com/demos.html', type:'website', weight: 0.75  },
										{ name: 'Aloha Wordpress Demo', url:'http://www.aloha-editor.com/demos/wordpress-demo/index.html', type:'website', weight: 0.75  },
										{ name: 'Aloha Logo', url:'http://www.aloha-editor.com/images/aloha-editor-logo.png', type:'image', weight: 0.10  }
							]
						}
					},
					"plugins": {
						"format": {
							// all elements with no specific configuration get this configuration
							config : [ 'b', 'i','sub','sup'],
								editables : {
								// no formatting allowed for title
								'[property*="title"]'	: [ ],
								// formatting for all editable DIVs
								'div'		: [ 'b', 'i', 'del', 'sub', 'sup'  ],
								// content is a DIV and has class .article so it gets both buttons
								'.article'	: [ 'b', 'i', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat']
								}
						},
						"link": {
							// all elements with no specific configuration may insert links
							config : [ 'a' ],
								editables : {
								// No links in the title.
								'[property*="title"]'	: [  ]
								},
								// all links that match the targetregex will get set the target
							// e.g. ^(?!.*aloha-editor.com).* matches all href except aloha-editor.com
								targetregex : '^(?!.*aloha-editor.com).*',
								// this target is set when either targetregex matches or not set
								// e.g. _blank opens all links in new window
								target : '_blank',
								// the same for css class as for target
								cssclassregex : '^(?!.*aloha-editor.com).*',
								cssclass : 'aloha',
								// use all resources of type website for autosuggest
								objectTypeFilter: ['website'],
								// handle change of href
								onHrefChange: function( obj, href, item ) {
									if ( item ) {
									jQuery(obj).attr('data-name', item.name);
									} else {
									jQuery(obj).removeAttr('data-name');
									}
								}
						},
						"image": {
					   					config : { 'img': { 'max_width': '50px',
												'max_height': '50px' }},
						  	editables : {
								'[property*="title"]'	: {},
								'[property*="number"]'	: {},
								'[property*="price"]'	: {}
								
						  	}
						},
						"draganddropfiles":  { 
							config: {'drop' : {    'max_file_size': 300000,
								'max_file_count': 2,
								'upload': {
				                    'uploader_instance':'Aloha.Repositories.Uploader',
				                    'config': {
										'callback': function(resp) { 
											var json_res = jQuery.parseJSON(resp);
											if (json_res.success) {
												return json_res.data;
											} else {
												throw 'File upload error';
											}
										},
										'image': {
											'max_width': 800,
											'max_height': 800
										},
				                        'method':'POST',
				                        'url': "/content",
				                        'file_name_param':"filename",
				                        'file_name_header':'X-File-Name',
				                        'extra_headers':{}, //Extra parameters
				                        'extra_post_data': {}, //Extra parameters
				                        'send_multipart_form': false, //true for html4 TODO: make browser check
				                        //'additional_params': {"location":""},
				                        'www_encoded': false }
				                    }
				            	}
							}
				        }
					}
				};


		})(window);