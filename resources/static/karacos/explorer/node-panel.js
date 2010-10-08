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
	
	this.items = [new KaraCos.Explorer.NodeContentPanel({
		store: this.contentElementsStore,
        autoHeight:true,
        title:'Node content',
        
	})];
	KaraCos.Explorer.ItemTabPanel.superclass.constructor.call(this);
	
};
Ext.extend(KaraCos.Explorer.ItemTabPanel, Ext.TabPanel, {
	
});