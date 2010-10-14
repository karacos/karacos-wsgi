/**
 * Main explorer Panel for admin
 * 
 * 
 */
/*Ext.override(Ext.dd.DDProxy, {
    startDrag: function(x, y) {
        var dragEl = Ext.get(this.getDragEl());
        var el = Ext.get(this.getEl());
 
        dragEl.applyStyles({border:'','z-index':2000});
        dragEl.update(el.dom.innerHTML);
        dragEl.addClass(el.dom.className + ' dd-proxy');
    },
    

}); */

Ext.namespace('KaraCos.Explorer');
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
	
	this.tabPanel = new KaraCos.Explorer.ItemTabPanel({
		title: 'Content',
		region: 'center',
		margins:'3 3 3 0', 
		activeTab: 0,
		defaults:{autoScroll:true},
	});
	this.items = [this.treePanel,this.tabPanel];	 
	KaraCos.Explorer.DomainExplorer.superclass.constructor.call(this);
	this.treePanel.on('nodeselected',this.onTreeSelection, this);
};

Ext.extend(KaraCos.Explorer.DomainExplorer, Ext.Window, {
	onTreeSelection: function(node) {
		//this.contentElementsStore
		this.tabPanel.nodeSelected(node);
		//this.tabPanel.contentElementsStore.loadData(items);
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