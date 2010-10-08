/**
 * KaraCos integrated plugin for Aloha
 * Copyright 2010 Nicolas Karageuzian
 * Domain explorer
 * 
 *
 */
Ext.namespace('KaraCos.Explorer');

/**
 * KaraCos async tree node
 */
KaraCos.Explorer.TreeNode = function(config) {
	Ext.apply(this, config);
	KaraCos.Explorer.TreeNode.superclass.constructor.call(this);
};

Ext.extend( KaraCos.Explorer.TreeNode, Ext.tree.AsyncTreeNode, {
	
});

/**
 * 
 */
KaraCos.Explorer.nodeItems = {};
KaraCos.Explorer.getNodeItems = function(url) {
	try {
		return KaraCos.Explorer.nodeItems[url].items;
	} catch(e) {
		var items = [];
		var url_href = "/w_browse_types";
		if (url != '/') {
			url_href = url + "/w_browse_types";
		}
		jQuery.ajax({ url: url_href,
			dataType: "json",
			context: document.body,
			async: false, // plugin init should wait for success b4 continuing
		    success: function(data) {
				jQuery.each(data,function(k,v){
					t_url = "/";
					if (url != '/') {
						t_url = url + '/' + k;
					} else {
						t_url = '/' + k;
					}
					item = {text: k,
							id: t_url,
							cls : 'karacos_explorer_' + v.webType,
							parent_url:url,
							imgsrc: '/_browser/karacos/explorer/images/type_' + v.webType + '.png',
							imgstyle: 'width:16px;height:16px',
							kc_link_href: t_url,
					};
					items.push(item);
				});
			},
		}); // $.ajax for browse_childrens
		if (url != '/') {
			url_href = url + "/_att";
			jQuery.ajax({ url: url_href,
		    	dataType: "json",
		    	context: document.body,
		    	async: false, // plugin init should wait for success b4 continuing
		        success: function(data) {
					jQuery.each(data.form.fields[0].values, function(id,value) {
						t_url = "/";
						if (url != '/') {
							t_url = url + '/' + value.value;
						} else {
							t_url = '/' + value.value;
						}
						item = {id: t_url,
								text: value.label,
								leaf:true,
								parent_url:url};
						var imgreg = /.*(\.jpg)|(\.gif)|(\.jpeg)|(\.png)$/;
						var match = value.value.toLowerCase().match(imgreg);
						if ( match != null) {
							item.cls = 'karacos_file_image';
							item.imgsrc = value.value;
							item.imgstyle = 'width:64px;height:64px';
						}
						var sndreg = /.*(\.mp3)|(\.ogg)|(\.m4a)|(\.aac)$/;
						var match = value.value.toLowerCase().match(sndreg);
						if ( match != null) {
							item.cls = 'karacos_file_sound';
							item.imgsrc = '/_browser/karacos/explorer/images/type_AudioTrack.png';
							item.imgstyle = 'width:16px;height:16px';
							item.kc_link_href = value.value;
						}
						if (!item.imgsrc) {
							item.imgsrc = '/_browser/karacos/explorer/images/page_package.gif';
							item.imgstyle = 'width:16px;height:16px';
							item.kc_link_href = value.value;
						}
						items.push(item);
					});
				}, //success
				failure: function(data) {}, // do nothing
			
			}); //ajax
		} //
		KaraCos.Explorer.nodeItems[url] = {items : items};
		return KaraCos.Explorer.nodeItems[url].items;
	} //catch
}

/**
 * Tree Loader
 */
KaraCos.Explorer.TreeLoader = function(config) {
	Ext.apply(this, config);
	KaraCos.Explorer.TreeLoader.superclass.constructor.call(this);
};

Ext.extend( KaraCos.Explorer.TreeLoader, Ext.tree.TreeLoader, {
	directFn : function(url, callback, scope) {
			var response = {
					status: true,
					argument: {callback: callback, node: url}
			};
			items = KaraCos.Explorer.getNodeItems(url);
			
			callback(items,response);
		}, // directFn
}); // TreeLoader
