/*
* Karacos plugin for aloha
*/
if(typeof KaraCos=="undefined"||!KaraCos)
    {
    var KaraCos={};
    }
KaraCos.Plugin=new GENTICS.Aloha.Plugin("org.karacos.aloha.Plugin");
KaraCos.Plugin.languages=["en","fr"];

/*
 * Init plugin
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
						if (this.actiondata.form) {
							$.kc_write_kc_action(this.actiondata,$('#dialog_window'));
							$('#dialog_window').dialog('open');	
						}
					}}); // actionbutton
					actionButton.actiondata = that.rsdata.actions[i];
					GENTICS.Aloha.Log.info(that,"processing action button creation " + that.rsdata.actions[i].label );
					GENTICS.Aloha.Ribbon.addButton(actionButton);
					// actionButton.show();
				}
			}
			// GENTICS.Aloha.Ribbon.toolbar.render();
			// GENTICS.Aloha.Ribbon.toolbar.show();
		} // for
		if (that.edit_page) {
				console.log(that.edit_page_action);
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
   }; // END INIT

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
