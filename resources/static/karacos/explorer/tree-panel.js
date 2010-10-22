/////////////////// Domain Tree Class
Ext.namespace('KaraCos.Explorer');
/**
 * KaraCos Domain Tree constructor
 */
KaraCos.Explorer.DomainTree = function(config) {
	Ext.apply(this, config);
	KaraCos.Explorer.DomainTree.superclass.constructor.call(this);
//	domainRoot = new KaraCos.Explorer.TreeNode({
	domainRoot = new Ext.tree.AsyncTreeNode({
	    text: '/', 
	    draggable:true, // disable root node dragging
	    cls: 'karacos_file_domain',
	    id: '\/'
	});
//	domainRoot.url = '/';
	this.setRootNode(domainRoot);
	this.getSelectionModel().on('selectionchange', this.onSelectionChange, this);
	this.addEvents({nodeselected:true});

	this.on('contextmenu', this.onContextMenu, this);
	
};
/**
 * KaraCos domain Tree class
 * 
 */
Ext.extend(KaraCos.Explorer.DomainTree, Ext.tree.TreePanel, {
	onContextMenu : function(node, e){
			var that = this;
			if(this.ctxNode){
		        this.ctxNode.ui.removeClass('x-node-ctx');
		        this.ctxNode = null;
		    }
		    if(!node.isLeaf()){
		        this.ctxNode = node;
		        this.ctxNode.ui.addClass('x-node-ctx');
		        this.getNodeMenu(node).showAt(e.getXY());
		        
		    }
		},
	onSelectionChange: function(sm, node){
			console.log(sm);
			console.log(node);
	        if(node){
	            this.fireEvent('nodeselected', node.attributes);
	        }
    },
	onContextHide : function(){
	    if(this.ctxNode){
		        this.ctxNode.ui.removeClass('x-node-ctx');
		        this.ctxNode = null;
		    }
		},
	
	getNodeMenu: function(node,focus){
			var that = this;
			if(!node.menu){ // create context menu on first right click
				items = [];
			    var url_href = "/get_user_actions_forms";
				if (node.id != '/') {
					url_href = node.id + "/get_user_actions_forms";
				}
				jQuery.ajax({ url: url_href,
			    	dataType: "json",
			    	context: document.body,
			    	async: false, // plugin init should wait for success b4 continuing
			        success: function(data) {
			    		jQuery.each(data.data.actions, function(k,v) {
			    			// Iterate over actions
			    			menuItem = {
			    					id: node.id + '\/' + v.action,
			    					iconCls:'karacos_action_'+ v.action,
			    					scope: this
			    					//  handler: this.showWindow,
			    			};
			    			if (v.label) {
			    				menuItem.text = v.label;
			    			} else {
			    				menuItem.text = v.action;
			    			}
			    			item = new Ext.menu.Item(menuItem);
			    			items.push(item);
			    			item.form = v.form;
						
			    		}); // end iterate
					
					}
				});// ajax get_user_actions_forms
				this.menu = new Ext.menu.Menu({
					id:'feeds-ctx',
					items: items
				});
				this.menu.on('hide', this.onContextHide, this);
			} // if not node menu
		return this.menu;
		}

});