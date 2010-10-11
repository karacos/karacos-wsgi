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
			console.log(panel);
			//==================
			// Attach drag and drop listeners to document body
			// this prevents incorrect drops, reloading the page with the dropped item
			// This may or may not be helpful
			
			 if(!document.body.BodyDragSinker){
				 console.log("Processing body event sink");
				document.body.BodyDragSinker = true;
				
				var body = Ext.fly(document.body);
				//$('body').get(0).addEventListener('drop', function(event){
				//	console.log(event);
				//	event.stopEvent();
				//	return true;
				//});
				body.on({
					dragenter:function(event){
						return true;
					}
					,dragleave:function(event){
						return true;
					}
					,dragover:function(event){
						event.stopEvent();
						//console.log(event);
						
						return true;
					}
					,drop:function(event){
						console.log(event);
						event.stopEvent();
						
						return true;
					}
				});
			}
			// end body events
			//==================
			console.log(panel);
			jQuery('#'+panel.el.id).get(0).addEventListener('drop', function(event){
				//event.sink = true;
				console.log(event);
				 var files = event.dataTransfer.files;
				 var count = files.length;
	            // if no files where dropped, use default handler
	            if (count < 1) {
					//event.sink = false;
					return true;
				}
				var len = files.length;
				node = that.linkedNode;
				while(--len >= 0){
					panel.processFileUpload(files[len], node);
				}
				return false;
			}, false);
			
		}, // initDnd
		processFileUpload: function(file, node) {
			console.log(file);
			var url_href = "/";
			if (node.id != '/') {
				url_href = node.id + "/";
			}
			upload = new Ext.ux.XHRUpload({
				url: url_href
				,filePostName:'att_file'
				,fileNameHeader:'X-File-Name'
				,extraPostData:{'return_json':'','base64':''}
				,extraHeaders:{'Accept':'application/json'}
				,sendMultiPartFormData:false
				,file:file
				,listeners:{
					scope:this
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
						that.fireEvent('fileupload', this, false, {error:'XHR upload aborted'});
					}
					,error:function(event){
						//this.updateFile(fileRec, 'status', 'Error');
						that.fireEvent('fileupload', this, false, {error:'XHR upload error'});
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
							this.fireEvent('fileupload', this, false, {error:'Invalid JSON returned'});
							return true;
						} // catch
						if ( result.success ) {
							var record = this.store.recordType( {
								id:'',
								text:file.name,
								imgsrc:result.data,
								imgstyle:'width:64px;height:64px'
							});
							this.fireEvent('fileupload', this, true, result);
							that.fireEvent('fileupload', this, true, result);
						}else{
							//this.fileAlert('<BR>'+file.name+'<BR><b>'+result.error+'</b><BR>');
							//this.updateFile(fileRec, 'status', 'Error');
							this.fireEvent('fileupload', this, false, result);
						}
					} // load
					} // listener
			}); //XHRUpload
			upload.send();
		} // ProcessFileUpload
});