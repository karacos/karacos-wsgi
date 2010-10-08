/**
 * Node tabbed panel
 * 
 */
KaraCos.Explorer.ItemTabPanel = function(config) {
	Ext.apply(this, config);
	// unique store for all tabs
	this.contentElementsStore = new Ext.data.JsonStore({
        fields: ['id','text','imgsrc','imgstyle']

	});
	var tpl = new Ext.XTemplate(
		    '<tpl for=".">',
		        '<div class="karacos-explorer-thumb-wrap">',
		        '<div class="karacos-explorer-thumb"><img src="{imgsrc}" style="width: 64px;height: 64px;" title="{text}"/></div>',
		        '<span class="x-editable">{text}</span></div>',
		    '</tpl>',
		    '<div class="x-clear"></div>'
		);

	this.ContentGrid = new Ext.DataView({
        store: this.contentElementsStore,
        tpl: tpl,
        autoHeight:true,
        multiSelect: true,
        overClass:'x-view-over',
        itemSelector:'div.thumb-wrap',
        title:'Node content',
        emptyText: 'No images to display'
    });
	
	this.items = [this.ContentGrid];
	KaraCos.Explorer.ItemTabPanel.superclass.constructor.call(this);
	
};
Ext.extend(KaraCos.Explorer.ItemTabPanel, Ext.TabPanel, {
});