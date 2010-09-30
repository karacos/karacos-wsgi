/*
* Karacos plugin for aloha
*/
if(typeof KaraCos=="undefined"||!KaraCos)
    {
    var KaraCos={};
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
	
	this.insertImgButton = new GENTICS.Aloha.ui.Button({
        'iconClass' : 'GENTICS_button GENTICS_button_img',
        'size' : 'small',
        'onclick' : function () { that.insertImg(); },
        'tooltip' : that.i18n('button.addimg.tooltip'),
        'toggle' : true
    });
	GENTICS.Aloha.FloatingMenu.addButton(
	        'GENTICS.Aloha.continuoustext',
	        this.insertImgButton,
	        GENTICS.Aloha.i18n(GENTICS.Aloha, 'floatingmenu.tab.insert'),
	        1
	    );
	GENTICS.Aloha.FloatingMenu.createScope(this.getUID('img'), 'GENTICS.Aloha.continuoustext');

    this.imgSrcField = new GENTICS.Aloha.ui.AttributeField();
    this.imgSrcField.setResourceObjectTypes(KaraCos.Plugin.resourceObjectTypes);
    // add the input field for links
    GENTICS.Aloha.FloatingMenu.addButton(
        this.getUID('img'),
        this.imgSrcField,
        this.i18n('floatingmenu.tab.img'),
        1
    );
    this.imgUploadButton = new GENTICS.Aloha.ui.Button({
    	'label' : that.i18n('button.uploadimg.label'),
    	'size' : 'small',
    	'onclick' : function () { 
    	// TODO: upload image window...
    	
    },
    	'tooltip' : that.i18n('button.uploadimg.tooltip'),
    	'toggle' : true
    });
    //this.imgUploadButton.setResourceObjectTypes(KaraCos.Plugin.resourceObjectTypes);
    GENTICS.Aloha.FloatingMenu.addButton(
    		this.getUID('img'),
    		this.imgUploadButton,
    		this.i18n('floatingmenu.tab.img'),
    		2
    );
    
    
}

KaraCos.Plugin.bindInteractions = function () {
    var that = this;

    // update link object when src changes
    this.imgSrcField.addListener('keyup', function(obj, event) {
    	
    	that.srcChange();
    });

    // on blur check if href is empty. If so remove the a tag
    this.imgSrcField.addListener('blur', function(obj, event) {
        if ( this.getValue() == '' ) {
            //that.removeLink();
        }
    });
     
}

KaraCos.Plugin.subscribeEvents = function () {
	var that = this;
	
    // add the event handler for selection change
    GENTICS.Aloha.EventRegistry.subscribe(GENTICS.Aloha, 'selectionChanged', function(event, rangeObject) {
    	var foundMarkup = that.findImgMarkup( rangeObject );
    	var config = that.getEditableConfig(GENTICS.Aloha.activeEditable.obj);
        if ( jQuery.inArray('img', config) != -1) {
        	that.insertImgButton.show();
        } else {
        	that.insertImgButton.hide();
            // leave if img is not allowed
            return;
        }
        if ( foundMarkup ) {
        	//img found
        	that.insertImgButton.hide();
        	GENTICS.Aloha.FloatingMenu.setScope(that.getUID('img'));
            that.imgSrcField.setTargetObject(foundMarkup, 'src');
            that.imgUploadButton.targetImg = foundMarkup;
        } else {
        	hat.imgUploadButton.setTargetObject(null);
        	that.imgSrcField.setTargetObject(null);
        }
    	// TODO this should not be necessary here!
    	GENTICS.Aloha.FloatingMenu.doLayout();
    });
    	
	
}
KaraCos.Plugin.findImgMarkup = function ( range ) {
	if ( typeof range == 'undefined' ) {
        var range = GENTICS.Aloha.Selection.getRangeObject();   
    }
	try {
	    if (range.startContainer.childNodes[range.startOffset].nodeName.toLowerCase() == 'img') {
			console.log(range);
			return range.startContainer.childNodes[range.startOffset];
		}
	} catch (e) {}
    return null;
    
};
KaraCos.Plugin.insertImg = function() {
	var range = GENTICS.Aloha.Selection.getRangeObject();
	
    // if selection is collapsed then extend to the word.
    if (range.isCollapsed()) {
        GENTICS.Utils.Dom.extendToWord(range);
    }
    if ( range.isCollapsed() ) {
    	var newImg = jQuery('<img src=""></img>');
        GENTICS.Utils.Dom.insertIntoDOM(newImg, range, jQuery(GENTICS.Aloha.activeEditable.obj));
    } else {
    	console.log(range.getSelectedSiblings());
    	alert('img cannot markup a selection');
    }
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
