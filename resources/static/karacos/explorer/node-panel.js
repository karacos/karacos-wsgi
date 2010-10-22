/**
 * Node tabbed panel
 * 
 */
Ext.namespace('KaraCos.Explorer');
KaraCos.Explorer.ItemTabPanel = function(config) {
	Ext.apply(this, config);
	// unique store for all tabs
	this.contentElementsStore = new Ext.data.JsonStore({
        fields: ['id','text','imgsrc','imgstyle']

	});
	that = this;
	this.nodeContentPanel = new KaraCos.Explorer.NodeContentPanel({
		store: this.contentElementsStore,
        autoHeight:true,
        title:'Node content'
        });
	this.items = [this.nodeContentPanel];
	KaraCos.Explorer.ItemTabPanel.superclass.constructor.call(this);
	this.nodeContentPanel.getNode = function() {
		console.log("getNode");
		console.log(that.linkedNode);
		return that.linkedNode;
	};
	this.nodeContentPanel.on('fileupload',this.refresh, this);
};
Ext.extend(KaraCos.Explorer.ItemTabPanel, Ext.TabPanel, {
	nodeSelected: function(node) {
		items = KaraCos.Explorer.getNodeItems(node.id);
		this.linkedNode = node;
		this.contentElementsStore.loadData(items);
		this.nodeContentPanel.linkedNode = node;
	},
	refresh: function(file, result) {
		console.log(file);
		items = KaraCos.Explorer.refreshNodeItems(this.linkedNode.id);
		this.contentElementsStore.loadData(items);
	}
});