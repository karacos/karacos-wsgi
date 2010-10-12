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
