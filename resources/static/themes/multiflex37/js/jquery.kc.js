if (!Array.prototype.indexOf){
  Array.prototype.indexOf = function(elt /*, from*/)
  {
    var len = this.length >>> 0;

    var from = Number(arguments[1]) || 0;
    from = (from < 0)
         ? Math.ceil(from)
         : Math.floor(from);
    if (from < 0)
      from += len;

    for (; from < len; from++)
    {
      if (from in this &&
          this[from] === elt)
        return from;
    }
    return -1;
  };
}



jQuery.kc = {
    type_of : function(v) {
	  if (typeof(v) == "object") {
		if (v === null) return "null";
		if (v.constructor == (new Array).constructor) return "array";
		if (v.constructor == (new Date).constructor) return "date";
		if (v.constructor == (new RegExp).constructor) return "regex";
		return "object";
	  }
	  return typeof(v);
	},
    console: {
        init: function(debugdiv) {
            debugdiv.dialog({
    			autoOpen: false,
    			width: 520,
    			modal: true,
    			buttons: {
    			  "Ok": function() { 
    						$(this).dialog("close"); 
    					}, 
    					 
    				"Clear": function() { 
                    $(this).html("");
    				} 
    			
    			}
    		});
            $.kc.console.window = debugdiv;
        },
        writeMessage: function(){
            if (["debug","info","warn","error"].indexOf(arguments[0].toLowerCase()) != -1) {
                params = arguments[1];
                
                //params.slice();
                level = arguments[0];
                if (typeof window.console != "undefined") {
                    func = window.console[level];
                    func(params);
                } 
                //HERE comes custom debugging output
                //log_object = { "log": params }
                
                var message = $("<div class='ui-widget'></div>");
                //var msg_decor;
                if (level == 'info' || level == 'debug') {
                    container = $("<div class='ui-state-highlight ui-corner-all' style='padding: 0pt 0.7em;'></div>");
                    container.append("<p></p>");
                    if (level == 'info') {
                        container.children(':last').append("<span class='ui-icon ui-icon-info' style='float: left; margin-right: 0.3em;'></span>");
                    }
                    for (var i = 0 ; i < params.length ; i++) {
                        if (typeof params[i] != "object") {
                            container.children(':last').append(params[i] + " ");
                        } else {
                            container.children(':last').append($.kc.json.render(params[i]));
                        }
                    }
                        //container.children(':last').append();
                }
                
                /*
                                            <div class="ui-state-error ui-corner-all" style="padding: 0pt 0.7em;"> 
            				<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: 0.3em;"></span> 
            				<strong>Alert:</strong> Sample ui-state-error style.</p>
            			</div>

                                            */
                if (level == 'error' || level == 'warn') {
                    container = $("<div class='ui-state-error ui-corner-all' style='padding: 0pt 0.7em;'></div>").append("<p></p>");
                    container.children(':last').append("<span class='ui-icon ui-icon-alert' style='float: left; margin-right: 0.3em;'></span>");
                    if (level == 'error'){
                        container.children(':last').append("<strong>[ERROR]</strong> ");
                    } else {
                        container.children(':last').append("<strong>[WARN]</strong> ");
                    }
                    for (var i = 0 ; i < params.length ; i++) {
                        if (typeof params[i] != "object") {
                            container.children(':last').append(params[i] + ", ");
                        } else {
                            container.children(':last').append($.kc.json.render(params[i]));
                        }
                    }
                }
                
                container.appendTo(message);
                message.appendTo($.kc.console.window);
                
                //$.kc.console.window.append($.kc.json.render(params));
                $.kc.console.window.dialog('open');
                //    message.
                
            } else {
                alert("unknow log level");
            }
        },        
        log: function() {
            if (arguments.length > 1){
                if (typeof arguments[0] == "string") {
                    if (["debug","info","warn","error"].indexOf(arguments[0].toLowerCase()) != -1) {
                        //Our first parameter is a level
                        
                        params = Array.prototype.slice.call(arguments);
                        level = params.splice(0,1);
                        
                        if (typeof $.kc.console[level] == "function") {
                            func = $.kc.console[level];
                            func(params);
                        }
                    } else {
                        $.kc.console.debug(params);
                    }
                }
            }
        },
        getparams: function(val) {
            var params;
            if ($.kc.type_of(val) == "array") {
                if (val.length == 1) {
                    params = val[0];
                } else {
                    params = val;
                }
            } else {
                params = val;
            }
            return params;
        },
        debug: function(){
            params = $.kc.console.getparams(Array.prototype.slice.call(arguments));
            $.kc.console.writeMessage("debug",params);
        },
        info: function(){
            params = $.kc.console.getparams(Array.prototype.slice.call(arguments));
            $.kc.console.writeMessage("info",params);
        },
        warn: function(){
            params = $.kc.console.getparams(Array.prototype.slice.call(arguments));
            $.kc.console.writeMessage("warn",params);
        },
        error: function(){
            params = $.kc.console.getparams(Array.prototype.slice.call(arguments));
            $.kc.console.writeMessage("error",params);
        }
    },
    json: {
        render: function(value) {
            function render(val) {
                var type = typeof(val);
                if (type == "object" && val !== null) {
                    var list = $("<dl></dl>");
                    for (var i in val) {
                      $("<dt></dt>").text(i).appendTo(list);
                      $("<dd></dd>").append(render(val[i])).appendTo(list);
                    }
                    return list;
                } else {
                    return $($.kc.json.format(val, {html: true}));
                }
            }
            var elem = render(value);

            elem.find("dd:has(dl)").hide().prev("dt").addClass("collapsed");
            elem.find("dd:not(:has(dl))").addClass("inline").prev().addClass("inline");
            elem.find("dt.collapsed").click(function() {
              $(this).toggleClass("collapsed").next().toggle();
            });
            return elem;
        },
        format: function(val, options) {
            try {
              options = $.extend({
                indent: 4,
                linesep: "\n",
                quoteKeys: true
              }, options || {});
              var itemsep = options.linesep.length ? "," + options.linesep : ", ";

              function escape(string) {
                return string.replace(/&/g, "&amp;")
                             .replace(/</g, "&lt;")
                             .replace(/>/g, "&gt;");
              }

              function format(val, depth) {
                var tab = [];
                for (var i = 0; i < options.indent * depth; i++) tab.push("");
                tab = tab.join(" ");

                var type = typeof val;
                switch (type) {
                  case "boolean":
                  case "number":
                  case "string":
                    var retval = JSON.stringify(val);
                    if (options.html) {
                      retval = "<code class='" + type + "'>" + escape(retval) + "</code>";
                    }
                    return retval;

                  case "object": {
                    if (val === null) {
                      if (options.html) {
                        return "<code class='null'>null</code>";
                      }
                      return "null";
                    }
                    if (val.constructor == Date) {
                      return JSON.stringify(val);
                    }

                    var buf = [];

                    if (val.constructor == Array) {
                      buf.push("[");
                      for (var index = 0; index < val.length; index++) {
                        buf.push(index > 0 ? itemsep : options.linesep);
                        buf.push(tab, format(val[index], depth + 1));
                      }
                      if (index >= 0) buf.push(options.linesep, tab.substr(options.indent));
                      buf.push("]");

                    } else {
                      buf.push("{");
                      var index = 0;
                      for (var key in val) {
                        buf.push(index > 0 ? itemsep : options.linesep);
                        var keyDisplay = options.quoteKeys ? JSON.stringify(key) : key;
                        if (options.html) {
                          if (options.quoteKeys) {
                            keyDisplay = keyDisplay.substr(1, keyDisplay.length - 2);
                          }
                          keyDisplay = "<code class='key'>" + escape(keyDisplay) + "</code>";
                          if (options.quoteKeys) {
                            keyDisplay = '"' + keyDisplay + '"';
                          }
                        }
                        buf.push(tab, keyDisplay,
                          ": ", format(val[key], depth + 1));
                        index++;
                      }
                      if (index >= 0) buf.push(options.linesep, tab.substr(options.indent));
                      buf.push("}");
                    }

                    return buf.join("");
                  }
                }
              }

              return format(val, 1);
            } catch (err) {
                $.kc_log(err);
            };
         }// $.kc.json.format
        
      } // $.kc.json
    }
