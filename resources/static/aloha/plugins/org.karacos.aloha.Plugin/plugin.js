/*
* Karacos plugin for aloha
*/
if(typeof KaraCos=="undefined"||!KaraCos)
    {
    var KaraCos={};
    }
KaraCos.Plugin=new GENTICS.Aloha.Plugin("org.karacos.aloha.Plugin");
KaraCos.Plugin.languages=["en","fr"];
KaraCos.Plugin.init=function(){
	this.pagedata = {}
    var that=this;
    var saveButton=new GENTICS.Aloha.ui.Button({label:this.i18n("save"),
                                                onclick:function(){that.save()}});
    url_href = this.settings['instance_url'] + "/" + this.settings['edit_content_action'];
    $.ajax({ url: url_href,
    	dataType: "json",
    	context: document.body,
        success: function(data) {
    	len = data.form.fields.length
    	for (var i=0 ; i<len; ++i) {
    		field = data.form.fields[i];
    		fieldvalue = "";
    		if (field.value) {
    			fieldvalue = field.value;
    		}
    		that.pagedata[field.name] = fieldvalue;
    	}
    	console.log(that);
    },
    });
    GENTICS.Aloha.Ribbon.addButton(saveButton);

   };
KaraCos.Plugin.save=function(){
	config = this.settings['idfieldsref'];
    var content="";
    var that = this;
	jQuery.each(GENTICS.Aloha.editables,
	            function(index,editable){
			that.pagedata[config[editable.getId()]] = editable.getContents();
	        content=content+"Editable ID: "+config[editable.getId()]+"\nHTML code: "+editable.getContents()+"\n\n";
	        });
	$.ajax({ url: this.settings['instance_url'],
    	dataType: "json",
    	contentType: 'application/json',
    	data: $.toJSON({
    		'method' : this.settings['edit_content_action'],
    		'id' : 1,
    		'params' : that.pagedata,
    	}),
    	context: document.body,
    	type: "POST",
        success: function(data) {
    		console.log(data);
    },});
	       console.log(this);
  };
