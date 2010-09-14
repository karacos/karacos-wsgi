(function($) {

    $._renderValue = function(value) {
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
                return $($.formatJSON(val, {html: true}));
              }
            }
            var elem = render(value);

        elem.find("dd:has(dl)").hide().prev("dt").addClass("collapsed");
        elem.find("dd:not(:has(dl))").addClass("inline").prev().addClass("inline");
        elem.find("dt.collapsed").click(function() {
          $(this).toggleClass("collapsed").next().toggle();
        });

        return elem;
      }

    /**
          */
    $.formatJSON = function(val, options) {
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
 };})(jQuery);