
Ext.namespace('KaraCos.Explorer');

KaraCos.Explorer.sinkBodyEvents = 

/**
 * Upload dropped file to dest using XRH HTML5 file POST
 * 
 * @param id : id of element where drop is done
 * @param url : destination url for POST request
 */
KaraCos.Explorer.bindUploadDropFile = function(panel,url,listeners) {
	console.log("binding panel");
	console.log(panel);
	try {
		KaraCos.Explorer.sinkBodyEvents();
		if (!listeners || listeners == undefined) {
			listeners = {};
		}
		jQuery('#'+panel.el.id).get(0).addEventListener('drop', function(event){
			try {
				//alert('event drop in panel');
				event.sink = true;
			//console.log(event);
				 var files = event.dataTransfer.files;
				 var count = files.length;
		        // if no files where dropped, use default handler
		        if (count < 1) {
					event.sink = false;
					return true;
				}
				var len = files.length;
				Ext.MessageBox.show({
					buttons: Ext.MessageBox.OK
					,icon: Ext.MessageBox.ERROR
					,modal:false
					,title:'Upload requested!'
					,msg:"You've dropped "+count+" files !<BR><BR>These files will be uploaded."
				});
				var t_url = "";
				if (typeof url == 'function') {
					t_url = url(panel);
				} else {
					t_url = url;
				}
				while(--len >= 0){
					upload = new Ext.ux.XHRUpload({
						url: t_url
						,filePostName:'att_file'
						,fileNameHeader:'X-File-Name'
						,extraPostData:{'return_json':'','base64':''}
						,extraHeaders:{'Accept':'application/json'}
						,sendMultiPartFormData:false
						,file:files[len]
						,listeners:listeners
					}); //XHRUpload
					upload.send();
				} // while
			} catch (e) {
				console.log(e);
			}
			return false;
		}, false);
	} catch (e) {
		console.log(e);
	}
};