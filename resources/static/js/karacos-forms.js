//Always start with comments (concat et tcet)
/**
 * 
 */

(function($) {
	/**
	 * Return true type of (differences between array an object
	 */
	$.kc_type_of = function(v) {
	  if (typeof(v) == "object") {
		if (v === null) return "null";
		if (v.constructor == (new Array).constructor) return "array";
		if (v.constructor == (new Date).constructor) return "date";
		if (v.constructor == (new RegExp).constructor) return "regex";
		return "object";
	  }
	  return typeof(v);
	}
	
	
	/**
	 * Write a KaraCos field
	 */
	$.kc_write_kc_field = function(field,parent){
		try {
			field_value = "";
			if (field.value) {
				field_value = field.value;
			}
			if (field.formType) {
				if (field.formType == 'TEXTAREA') {
					parent.append("<div class='form_field_holder'></div>");
					field_div = parent.children(':last');
					if (field.title) {
						field_div.append("<label for='' class='left'/>");
						//"${field['name']}" class="left">${field['title']}</label>
						field_div.children(':last').attr('for',field.name);
						field_div.children(':last').append(field.title);
					}

					field_div.append("<textarea name=''/>");
					field_div.children(':last').attr('name',field.name);
					field_div.children(':last').attr('value',field_value);
				}
				if (field.formType == 'WYSIWYM') {
					parent.append("<div class='form_field_holder'></div>");
					field_div = parent.children(':last');
					field_div.append("<p></p>");
					label_p = field_div.children(':last');
					if (field.title) {
						label_p.children(':last').append(field.title);
					}
					field_div.append("<textarea name=''></textarea>");
					area = field_div.children(':last');
					area.attr('name',field.name);
					area.attr('value',field_value);
					//if (!(field.name in CKEDITOR.instances)) {
						area.wymeditor({
					        stylesheet: 'styles.css',
					       // skin: 'twopanels',
					        lang: 'fr'
					 	   });
					//} else
						//TOTO quelque chose
						//CKEDITOR.instances[field.name];
				}
				if (field.formType == 'DATE') {
					parent.append("<div class='form_field_holder'></div>");
					field_div = parent.children(':last');
					if (field.title) {
						field_div.append("<label for='' class='left'/>");
						//"${field['name']}" class="left">${field['title']}</label>
						field_div.children(':last').attr('for',field.name);
						field_div.children(':last').append(field.title);
					}
					field_div.append("<input class='datepicker' type='text'/>");
					input_el = field_div.children(':last');
					input_el.attr('id',"field_"+field.name);
					input_el.attr('name',field.name);
					input_el.attr('value',field_value);
					input_el.AnyTime_picker(
								{ format: "%Y-%m-%e", firstDOW: 1 } );
				}
					
				if (field.formType == 'WYSIWYG') {
					parent.append("<div class='form_field_holder'></div>");
					field_div = parent.children(':last');
					field_div.append("<p></p>");
					label_p = field_div.children(':last');
					if (field.title) {
						label_p.children(':last').append(field.title);
					}
					field_div.append("<textarea name=''></textarea>");
					area = field_div.children(':last');
					area.attr('name',field.name);
					area.attr('value',field_value);
					if (!(field.name in CKEDITOR.instances)) {
						area.ckeditor();
					} else
						//TOTO quelque chose
						CKEDITOR.instances[field.name];
				}
			}
			else {
				parent.append("<div class='form_field_holder'></div>");
				field_div = parent.children(':last');
				if (field.title) {
					field_div.append("<label for='' class='left'/>");
					//"${field['name']}" class="left">${field['title']}</label>
					field_div.children(':last').attr('for',field.name);
					field_div.children(':last').append(field.title);
				}
				field_div.append("<input class='field' type='"+field.dataType+"' value='' name=''/>");
				//field_div.children(':last').attr('type',); 
				field_div.children(':last').attr('value',field_value);
				field_div.children(':last').attr('name',field.name);
			} 
		} catch (err) {
			// log to firebug console
			console.log("%s: %o", "ERROR", err);
		}

	}
	
	/**
	 * Write KaraCos json form
	 * 
	 */
	$.kc_write_kc_form = function(form,action,acturl,parent){
		try {
			parent.append("<form enctype='multipart/form-data' method='POST' action='' class='main_form'></form>");
			form_widget = parent.children(':last');
			form_widget.attr("action", acturl);
			form_widget.append("<fieldset></fieldset>");
			fieldset = form_widget.children(':last');
			fieldset.append("<input type='hidden' name='method' value=''/>");
			fieldset.children(':last').attr("value", action);
			fieldset.append("<legend></legend>");
			if (form.title)
				fieldset.children(':last').append(form.title);
			if (form.notice) {
				fieldset.append("<p></p>");
				fieldset.children(':last').append(form.notice);
			}
			if (form.fields) {
				var arLen=form.fields.length;
				for ( var i=0, len=arLen; i<len; ++i ) {
					$.kc_write_kc_field(form.fields[i],fieldset);
				}
			}
			if (form.submit)
				submit = form.submit;
			else
				submit = action;
			fieldset.append("<p><input type='submit' class='button' value=''/></p>");
			fieldset.children(':last').children(':last').attr('value',submit);
		} catch (err) {
			// log to firebug console
			console.log("%s: %o", "ERROR", err);
		}
		};
		
	/**
	 * Write KaraCos json action
	 * 
	 */	
	$.kc_write_kc_action = function(action,parent){
		try {
			parent.html("");
		} catch (err) {
			console.log("%s: %o", "ERROR", err);
		}
		//parent.append($.toJSON(action));
		try {
			if (action.label){
				parent.dialog( "option" ,"title", action.label);
			}
			//console only works in a firebug enabled browser....
			//TODO: Create custom javascript log handler
			//console.log("%s: %o", "INFO", action);
			//parent.append('form type:');
			//parent.append(typeof action.form);
			//parent.append($.kc_type_of(action.form.fields));
			if ($.kc_type_of(action.form) == "object") {
				$.kc_write_kc_form(action.form, action.action, action.acturl, parent);
			}
			if ($.kc_type_of(action.form) == "array") {
				var arLen=action.form.length;
				for ( var i=0, len=arLen; i<len; ++i ) {
					$.kc_write_kc_form(action['form'][i], action.action, action.acturl, parent);
				}	
			}	
		} catch (err) {
			// log to firebug console (bug if not firebug)
			console.log("%s: %o", "ERROR", err);
		}
		};
		
		/**
		 * 
		 */
		$.set_wysiwyg = function(area){
			area.wysiwyg({
			controls: {
			  strikeThrough : { visible : true },
			  underline     : { visible : true },
			  
			  separator00 : { visible : true },
			  
			  justifyLeft   : { visible : true },
			  justifyCenter : { visible : true },
			  justifyRight  : { visible : true },
			  justifyFull   : { visible : true },
			  
			  separator01 : { visible : true },
			  
			  indent  : { visible : true },
			  outdent : { visible : true },
			  
			  separator02 : { visible : true },
			  
			  subscript   : { visible : true },
			  superscript : { visible : true },
			  
			  separator03 : { visible : true },
			  
			  undo : { visible : true },
			  redo : { visible : true },
			  
			  separator04 : { visible : true },
			  
			  insertOrderedList    : { visible : true },
			  insertUnorderedList  : { visible : true },
			  insertHorizontalRule : { visible : true },
			  
			  h4mozilla : { visible : true && $.browser.mozilla, className : 'h4', command : 'heading', arguments : ['h4'], tags : ['h4'], tooltip : "Header 4" },
			  h5mozilla : { visible : true && $.browser.mozilla, className : 'h5', command : 'heading', arguments : ['h5'], tags : ['h5'], tooltip : "Header 5" },
			  h6mozilla : { visible : true && $.browser.mozilla, className : 'h6', command : 'heading', arguments : ['h6'], tags : ['h6'], tooltip : "Header 6" },
			  
			  h4 : { visible : true && !( $.browser.mozilla ), className : 'h4', command : 'formatBlock', arguments : ['<H4>'], tags : ['h4'], tooltip : "Header 4" },
			  h5 : { visible : true && !( $.browser.mozilla ), className : 'h5', command : 'formatBlock', arguments : ['<H5>'], tags : ['h5'], tooltip : "Header 5" },
			  h6 : { visible : true && !( $.browser.mozilla ), className : 'h6', command : 'formatBlock', arguments : ['<H6>'], tags : ['h6'], tooltip : "Header 6" },
			  
			  separator07 : { visible : true },
			  
			  cut   : { visible : true },
			  copy  : { visible : true },
			  paste : { visible : true }
			}
	  });
	}
	// ############################
	})(jQuery);
