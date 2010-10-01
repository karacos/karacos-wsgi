/*
* Karacos plugin for aloha
*/
if(typeof KaraCos=="undefined"||!KaraCos)
    {
	alert('org.karacos.aloha.Img plugin is required');
    }
KaraCos.Plugin=new GENTICS.Aloha.Plugin("org.karacos.aloha.Plugin");
KaraCos.Plugin.languages=["en","fr"];
KaraCos.Plugin.config = ['img'];
/*
 * Initalize plugin
 */
KaraCos.Plugin.init=function(){
	
	this.pagedata = {}
    var that=this;
	that.add_attachment = null;
	// get user action forms and initialize actions for user
	if (that.settings['instance_url'] == undefined) {
		that.settings['instance_url'] = '';
	}
	url_href = that.settings['instance_url'] + "/get_user_actions_forms";
	$.ajax({ url: url_href,
    	dataType: "json",
    	context: document.body,
    	async: false, // plugin init should wait for success b4 continuing
        success: function(data) {
			GENTICS.Aloha.Log.info(that,data);
			that.user_actions = [];
			that.edit_page = false;
			if (data['status'] == "success") {
				GENTICS.Aloha.Log.info(that,"successful result");
				that.rsdata = data['data'];
				}
			},// success on get_user_actions_forms
	}); // $.ajax for get_user_actions_forms
	if (that.rsdata) {
		len = that.rsdata.actions.length;
		for (var i=0 ; i<len; ++i) {
			that.user_actions[i] = that.rsdata.actions[i].action;
			if (that.rsdata.actions[i].action == that.settings['edit_content_action']) {
				that.edit_page = true;
				that.edit_page_action = that.rsdata.actions[i];
			} else {
				if (that.rsdata.actions[i].action == "add_attachment") {
					that.add_attachment = that.rsdata.actions[i];
				}
				if (that.rsdata.actions[i].label) {
					var actionButton=new GENTICS.Aloha.ui.Button({label:that.rsdata.actions[i].label,
						onclick:function(){ // When a button is clicked :
						if (this.actiondata.form && this.actiondata.action != 'register') {
							$.kc_write_kc_action(this.actiondata,$('#dialog_window'));
							$('#dialog_window').dialog('open');	
						} else {
							document.location = this.instance_url + '/' + this.actiondata.action;
						}
					}}); // actionbutton
					actionButton.actiondata = that.rsdata.actions[i];
					actionButton.instance_url = that.settings['instance_url'];
					GENTICS.Aloha.Log.info(that,"processing action button creation " + that.rsdata.actions[i].label );
					GENTICS.Aloha.Ribbon.addButton(actionButton);
					// actionButton.show();
				}
			}
			// GENTICS.Aloha.Ribbon.toolbar.render();
			// GENTICS.Aloha.Ribbon.toolbar.show();
		} // for
		if (that.edit_page) {
			GENTICS.Aloha.Log.info(that,that.edit_page_action);
				len = that.edit_page_action.form.fields.length;
				for (var i=0 ; i<len; ++i) {
					field = that.edit_page_action.form.fields[i];
					fieldvalue = "";
					if (field.value) {
						fieldvalue = field.value;
					}
					that.pagedata[field.name] = fieldvalue;
				}
				var editMore=new GENTICS.Aloha.ui.Button({label:that.i18n("editMore"),
					onclick:function(){that.editMore()}});
				GENTICS.Aloha.Ribbon.addButton(editMore);
				// editMore.show();
				// GENTICS.Aloha.Ribbon.toolbar.render();
				// GENTICS.Aloha.Ribbon.toolbar.show();
				var saveButton=new GENTICS.Aloha.ui.Button({label:that.i18n("save"),
					onclick:function(){that.save()}});
				GENTICS.Aloha.Ribbon.addButton(saveButton);
				// saveButton.show();
				// GENTICS.Aloha.Ribbon.toolbar.render();
				// GENTICS.Aloha.Ribbon.toolbar.show();
			} // if edit_page 
		} // if data.status == "success"
	GENTICS.Aloha.Log.info(that,that);
	//console.log(that);
	// $.ajax
	that.initImage();
	that.bindInteractions();
	that.subscribeEvents();
   }; // END INIT

KaraCos.Plugin.resourceObjectTypes = [];

KaraCos.Plugin.initImage = function() {
	var that = this;
	
	if (that.add_attachment != null) {
	    that.imgUploadButton = new GENTICS.Aloha.ui.Button({
	    	'label' : that.i18n('button.uploadimg.label'),
	    	'size' : 'small',
	    	'onclick' : function () { 
	    		$.kc_write_kc_action(this.add_attachment,$('#dialog_window'));
	    		$('#dialog_window input.field').fileUploader({
	    			imageLoader: '',
	    			buttonUpload: '#dialog_window input.button',
	    			buttonClear: '#pxClear',
	    			successOutput: 'File Uploaded',
	    			errorOutput: 'Failed',
	    			inputName: 'att_file',
	    			inputSize: 30,
	    			allowedExtension: 'jpg|jpeg|png|gif',
	    			callback: function(data) {
	    			$('#dialog_window').dialog('close');
	    			console.log(that.imgUploadButton.targetImg);
	    			console.log(data);
	    			that.imgUploadButton.targetImg.src = data.data;
	    		}
	    			});
	    		$('#dialog_window').dialog('open');
	    		
	    },
	    	'tooltip' : that.i18n('button.uploadimg.tooltip'),
	    	'toggle' : true
	    });
	    this.imgUploadButton.add_attachment = that.add_attachment;
	    //this.imgUploadButton.setResourceObjectTypes(KaraCos.Plugin.resourceObjectTypes);
	    GENTICS.Aloha.FloatingMenu.addButton(
	    		KaraCos.Img.getUID('img'),
	    		this.imgUploadButton,
	    		this.i18n('floatingmenu.tab.img'),
	    		2
	    );
	}
};

KaraCos.Plugin.bindInteractions = function () {
    var that = this;

}

KaraCos.Plugin.subscribeEvents = function () {
	var that = this;
	
    // add the event handler for selection change
    GENTICS.Aloha.EventRegistry.subscribe(GENTICS.Aloha, 'selectionChanged', function(event, rangeObject) {
    	if (that.add_attachment != null) {
	    	var foundImgMarkup = KaraCos.Img.findImgMarkup( rangeObject );
	        if ( foundImgMarkup != null ) {
	        	//img found
	            that.imgUploadButton.targetImg = foundImgMarkup;
	        } else {
	        	that.imgUploadButton.targetImg = null;
	        }
	    	// TODO this should not be necessary here!
	    	GENTICS.Aloha.FloatingMenu.doLayout();
    	}
    });
    	
	
}




KaraCos.Plugin.srcChange = function () {
	// For now hard coded attribute handling with regex.
	//this.imgField.setAttribute('target', this.target, this.targetregex, this.hrefField.getQueryValue());
	//this.imgField.setAttribute('class', this.cssclass, this.cssclassregex, this.hrefField.getQueryValue());
}

/**
 * Edit more (window with additional info (which cannont be edited on page)
 */
KaraCos.Plugin.editMore=function(){
	   
   }; // END EDIT MORE

/**
 * save page content
 */
KaraCos.Plugin.save=function(){
	config = this.settings['idfieldsref'];
    var content="";
    var that = this;
	jQuery.each(GENTICS.Aloha.editables,
	            function(index,editable){
			that.pagedata[config[editable.getId()]] = editable.getContents();
	        content=content+"Editable ID: "+config[editable.getId()]+"\nHTML code: "+editable.getContents()+"\n\n";
	        });
	$.ajax({ url: that.settings['instance_url'],
    	dataType: "json",
    	contentType: 'application/json',
    	data: $.toJSON({
    		'method' : that.settings['edit_content_action'],
    		'id' : 1,
    		'params' : that.pagedata,
    	}),
    	context: document.body,
    	type: "POST",
        success: function(data) {
		GENTICS.Aloha.Log.info(that,data);
    },});
	GENTICS.Aloha.Log.info(that,that);
  };
