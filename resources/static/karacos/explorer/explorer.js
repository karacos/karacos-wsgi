/**
 * Main explorer Panel for admin
 * 
 * 
 */
KaraCos.Explorer.DomainExplorer = function(config) {
	Ext.apply(this, config);
	this.treePanel = new KaraCos.Explorer.DomainTree({
		title: 'Navigation',
	    region: 'west',
	    animate:true, 
	    autoScroll:true,
	    loader: new KaraCos.Explorer.TreeLoader({dataUrl:'/'}),//KaraCos.Explorer.TreeLoader({dataUrl:'/'}),
	    enableDD:true,
	    containerScroll: true,
	    border: false,
	    width: 250,
	    height: 300,
	    dropConfig: {appendOnly:true}
	});
	console.log(this);
	
	this.treePanel.on('nodeselected',this.onTreeSelection, this);
	 
	this.tabPanel = new KaraCos.Explorer.ItemTabPanel({
		region: 'center',
		margins:'3 3 3 0', 
		activeTab: 0,
		defaults:{autoScroll:true},
	});
	this.items = [this.treePanel,this.tabPanel];
	KaraCos.Explorer.DomainExplorer.superclass.constructor.call(this);
};

Ext.extend(KaraCos.Explorer.DomainExplorer, Ext.Window, {
	onTreeSelection: function(node) {
		items = KaraCos.Explorer.getNodeItems(node.id);
		//this.contentElementsStore
		this.tabPanel.contentElementsStore.loadData(items);
	},
});
KaraCos.Explorer.domainExplorer = new KaraCos.Explorer.DomainExplorer({
    title: 'Explorer',
    width:600,
    height:350,
    //border:false,
    plain:true,
    layout: 'border',
    closeAction: 'hide',
});