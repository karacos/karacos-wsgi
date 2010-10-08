Ext.namespace('KaraCos.Explorer');
/**
 * Node Content panel with dropZone
 * 
 */
KaraCos.Explorer.NodeContentPanel = function(config) {
	
	Ext.apply(this, config);
			
	// unique store for all tabs
	var tpl = new Ext.XTemplate(
		    '<tpl for=".">',
		        '<div class="karacos-explorer-thumb-wrap">',
		        '<div class="karacos-explorer-thumb"><img src="{imgsrc}" style="width: 64px;height: 64px;" title="{text}"/></div>',
		        '<span class="x-editable">{text}</span></div>',
		    '</tpl>',
		    '<div class="x-clear"></div>'
		);
	this.tpl = tpl;
	this.ContentGrid = new Ext.DataView({
        store: config.store,
        tpl: tpl,
        autoHeight:true,
        multiSelect: true,
        overClass:'karacos-content',
        itemSelector:'div.thumb-wrap',
        title:'Node content',
        emptyText: 'Nothing to display'
    });
	that = this;
	this.items = [this.ContentGrid]
	
	KaraCos.Explorer.NodeContentPanel.superclass.constructor.call(this);
	// Initialize panel
	this.on('render',function(e){
					e.initDnDUploader();								
				});
	
	
};
Ext.extend(KaraCos.Explorer.NodeContentPanel, Ext.Panel, {
	initDnDUploader:function(){
	
			//==================
			// Attach drag and drop listeners to document body
			// this prevents incorrect drops, reloading the page with the dropped item
			// This may or may not be helpful
			if(!document.body.BodyDragSinker){
				document.body.BodyDragSinker = true;
				
				var body = Ext.fly(document.body);
				body.on({
					dragenter:function(event){
						return true;
					}
					,dragleave:function(event){
						return true;
					}
					,dragover:function(event){
						event.stopEvent();
						return true;
					}
					,drop:function(event){
						//console.log(event);
						event.stopEvent();
						return true;
					}
				});
			}
			// end body events
			//==================
			
			this.el.on({
				dragenter:function(event){
					event.browserEvent.dataTransfer.dropEffect = 'move';
					return true;
				}
				,dragover:function(event){
					event.browserEvent.dataTransfer.dropEffect = 'move';
					event.stopEvent();
					return true;
				}
				,drop:{
					scope:this
					,fn:function(event){
					console.log(event);
						event.stopEvent();
						var files = event.browserEvent.dataTransfer.files;
		
						if(files === undefined){
							return true;
						}
						var len = files.length;
						while(--len >= 0){
							//this.processDnDFileUpload(files[len]);
						}
					}
				}
			});
			
		}, // initDnd
		
});