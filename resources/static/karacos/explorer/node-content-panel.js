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
	this.items = [this.ContentGrid];
	
	KaraCos.Explorer.NodeContentPanel.superclass.constructor.call(this);
	// Initialize panel
	this.addEvents('fileupload','fileselectionerror' );
	this.on('render', function(e){
					e.initDnDUploader(e);								
				});
	this.on('fileupload', function(e){
		console.log(e);								
	});
};

Ext.extend(KaraCos.Explorer.NodeContentPanel, Ext.Panel, {
	initDnDUploader:function(panel){
			var that = panel;
			KaraCos.Explorer.sinkBodyEvents();
			// define listeners for upload action
			listeners = {
				scope:panel
				,uploadloadstart:function(event){
					//this.updateFile(fileRec, 'status', 'Sending');
				}
				,uploadprogress:function(event){
					//this.updateFile(fileRec, 'progress', Math.round((event.loaded / event.total)*100));
				}
				// XHR Events
				,loadstart:function(event){
					//this.updateFile(fileRec, 'status', 'Sending');
				}
				,progress:function(event){
					//fileRec.set('progress', Math.round((event.loaded / event.total)*100) );
					//fileRec.commit();
				}
				,abort:function(event){
					//this.updateFile(fileRec, 'status', 'Aborted');
					panel.fireEvent('fileupload', panel, false, {error:'XHR upload aborted'});
				}
				,error:function(event){
					//this.updateFile(fileRec, 'status', 'Error');
					panel.fireEvent('fileupload', panel, false, {error:'XHR upload error'});
				}
				,load:function(event){
					
					try{
						var result = Ext.util.JSON.decode(upload.xhr.responseText);//throws a SyntaxError.
					} catch(e) {
						Ext.MessageBox.show({
							buttons: Ext.MessageBox.OK
							,icon: Ext.MessageBox.ERROR
							,modal:false
							,title:'Upload Error!'
							,msg:'Invalid JSON Data Returned!<BR><BR>Please refresh the page to try again.'
						});
						//this.updateFile(fileRec, 'status', 'Error');
						panel.fireEvent('fileupload', panel, false, {error:'Invalid JSON returned'});
						return true;
					} // catch
					if ( result.success ) {
						var record = panel.store.recordType( {
							id:'',
							text:result.data,
							imgsrc:result.data,
							imgstyle:'width:64px;height:64px'
						});
						panel.fireEvent('fileupload', panel, true, result);
					}else{
						//this.fileAlert('<BR>'+file.name+'<BR><b>'+result.error+'</b><BR>');
						//this.updateFile(fileRec, 'status', 'Error');
						panel.fireEvent('fileupload', panel, false, result);
					}
				} // load
			}; // listener
			
			KaraCos.Explorer.bindUploadDropFile(panel,this.getNodeUrl,listeners);
		}, // initDnd
		getNodeUrl: function(panel) {
			url = panel.linkedNode.id;
			return url;
		}
			
});