/**
 * Upload handling window
 */

Ext.namespace('KaraCos.Explorer');
KaraCos.Explorer.Uploader = function(config) {
	this.initialConfig = config;
	Ext.apply(this, config);
	var fields = ['id', 'name', 'size', 'status', 'progress'];
	this.fileRecord = Ext.data.Record.create(fields);
	this.fileGrid = new Ext.grid.GridPanel({
				/*
				x:0
				,y:30
				,width:this.initialConfig.gridWidth || 420
				,height:this.initialConfig.gridHeight || 200
				,enableHdMenu:false
				 * 
				 */
				region: 'center',
				store:new Ext.data.ArrayStore({
					fields: fields,
					reader: new Ext.data.ArrayReader({idIndex: 0}, this.fileRecord)
				}),
				columns:[
					{header:'File Name',dataIndex:'name', width:150}
					,{header:'Size',dataIndex:'size', width:60}//, renderer:Ext.util.Format.fileSize}
					,{header:'&nbsp;',dataIndex:'status', width:30}//, scope:this, renderer:this.statusIconRenderer}
					,{header:'Status',dataIndex:'status', width:60}
					,{header:'Progress',dataIndex:'progress'}//,scope:this, renderer:this.progressBarColumnRenderer}
				]
				/*,listeners:{
					render:{
						scope:this
						,fn:function(){
							this.fileGrid = this.items.items[1];							
						}	
					}
				} // listeners */
			});
	this.items = [this.fileGrid];
	KaraCos.Explorer.Uploader.superclass.constructor.call(this);
}; // Constructor function

/**
 * Class description
 */
Ext.extend(KaraCos.Explorer.Uploader, Ext.Window, {
	/*
	uploadListeners:{
		scope:this
		,uploadloadstart:function(event){
			this.updateFile(fileRec, 'status', 'Sending');
		}
		,uploadprogress:function(event){
			this.updateFile(fileRec, 'progress', Math.round((event.loaded / event.total)*100));
		}
		// XHR Events
		,loadstart:function(event){
			this.updateFile(fileRec, 'status', 'Sending');
		}
		,progress:function(event){
			fileRec.set('progress', Math.round((event.loaded / event.total)*100) );
			fileRec.commit();
		}
		,abort:function(event){
			this.updateFile(fileRec, 'status', 'Aborted');
			this.fireEvent('fileupload', this, false, {error:'XHR upload aborted'});
		}
		,error:function(event){
			this.updateFile(fileRec, 'status', 'Error');
			this.fireEvent('fileupload', this, false, {error:'XHR upload error'});
		}
		,load:function(event){
			
			try{
				var result = Ext.util.JSON.decode(upload.xhr.responseText);//throws a SyntaxError.
			}catch(e){
				Ext.MessageBox.show({
					buttons: Ext.MessageBox.OK
					,icon: Ext.MessageBox.ERROR
					,modal:false
					,title:'Upload Error!'
					,msg:'Invalid JSON Data Returned!<BR><BR>Please refresh the page to try again.'
				});
				this.updateFile(fileRec, 'status', 'Error');
				this.fireEvent('fileupload', this, false, {error:'Invalid JSON returned'});
				return true;
			}
			if( result.success ){
				fileRec.set('progress', 100 );
				fileRec.set('status', 'Done');
				fileRec.commit();						
				this.fireEvent('fileupload', this, true, result);
			}else{
				this.fileAlert('<BR>'+file.name+'<BR><b>'+result.error+'</b><BR>');
				this.updateFile(fileRec, 'status', 'Error');
				this.fireEvent('fileupload', this, false, result);
			}
		} // on load
	}, // listeners
	
	 * 
	 */
	/**
	 * 
	 */
	updateFile:function(fileRec, key, value){
		fileRec.set(key, value);
		fileRec.commit();
	},
	/**
	 * Add a file to upload in the grid
	 */
	addFileUpload: function(file,path) {
		Ext.apply(file,{
			id: ++this.fileId
			,status: 'Pending'
			,progress: '0'
			,complete: '0'
		});
		var fileRec = new this.fileRecord(file);
		this.fileGrid.store.add(fileRec);
		/*
		upload = new Ext.ux.XHRUpload({
			url: t_url
			,filePostName:'att_file'
			,fileNameHeader:'X-File-Name'
			,extraPostData:{'return_json':'','base64':''}
			,extraHeaders:{'Accept':'application/json'}
			,sendMultiPartFormData:false
			,file:files[len]
			,listeners:this.uploadListeners
		}); //XHRUpload
		 * 
		 */
	}
	
});