
function authManager() {
	
	/**
	 * 
	 */
	
	/**
	 * Draw authentication header in elem.
	 * If no elem specified, looksup for #header_auth_button
	 * @param elem jQuery object where button will be written (can be multiple)
	 */
	function authenticationHeader(elem){
		var that = this,
		isconnected = this.isUserConnected(),
		username = this.user_actions_forms.user,
		logout,
		login,
		fblogin;
		if (elem === undefined) {
			// default id
			elem = jQuery('#header_auth_button');
		}
		if (elem.length !== 0) { // if not none
			elem.empty();
			if (isconnected) {
				if (this.user_actions_forms.fullname) {
					username = this.user_actions_forms.fullname;
				}
				elem.append('<p>Bienvenue '+ username +'</p>');
				//TODO i18n
				logout = jQuery('<button role="menuitem">Se déconnecter</button>');
				logout.click(function(){
					that.logout();
				});
				elem.append(logout);
			} else {
				elem.append('<button role="menuitem">Se connecter avec facebook</button>');
				elem.append('<button role="menuitem">Se connecter (inscription au site)</button>');
				
			}
		}
	};
	
	/**
	 * 
	 * 
	 */
	function processFBCookie(){
		var that = this;
		jQuery.ajax({ url: "/_process_facebook_cookie",
			context: document.body,
			type: "GET",
			async: true,
			dataType: "json",
			contentType: 'application/json',
			success: function(data) {
				that.user_actions_forms = data.data;
			}});
	};
	
	
	function isUserConnected(){
		var that = this;
		if (this.user_actions_forms.user.search('anonymous') >= 0) {
			// user not connected in karacos
			FB.getLoginStatus(function(response) {
				if (response.session) { // logged in and connected user, someone you know
					// process login to karacos with fb id
					that.processFBCookie();
					return true;
				} else { // Not connected in KaraCos nor in facebook
					return false;
				}
			});
		} else { // user known in karacos
			return true;
		}
	}
	/**
	 * 
	 */
	function logout() {
		KaraCos.action({url:"/",
			action:"logout", 
			params:{},
			callback: function(){
				
			}FB.logout();
			}
		});
	};
	
	/**
	 * 
	 * @param callback
	 * @returns
	 */
	function provideLoginUI(callback){
		var that = this;
		this.loginWindow = $('#login_form_window');
		if (this.loginWindow.length === 0) {
			jQuery('body').append('<div id="login_form_window"/>');
			this.loginWindow = $('#login_form_window');
		} // sa.length
		
		KaraCos.getForm({
			url: "/",
			form: "login",
			callback: function(data, form) {
				
				var login_form_template = jsontemplate.Template(form);
				that.loginWindow.empty().append(login_form_template.expand(data));
				$('#karacos_login_accordion').accordion({
					autoHeight: false,
					navigation: true});
				$.each($('.kc_fb_box'), function (index, elem) {
					FB.XFBML.parse(elem);
				});
				that.loginWindow.find('.form_login_button').button()
				.click(function() {
					var data = { method: "",
							params: {},
							id: 1}
					$.each($(this).closest('form').serializeArray(), function(i, field) {
						if (field.name === "method") {
							data.method = field.value;
						} else {
							data.params[field.name] = field.value;
						}
					}); // each
					jQuery.ajax({ url: "/",
						dataType: "json",
						async: false,
						contentType: 'application/json',
						context: document.body,
						type: "POST",
						data: $.toJSON(data),
						success: function(data) {
							if (data.success) {
								that.loginWindow.dialog('close');
								if (typeof callback !== "undefined") {
									callback();
								}
							}
						},
					}); // POST login form
				});  // click
				that.loginWindow.dialog({width: '600px', modal:true}).show();
			} // get form success
		});			
	};
	// Start the constructor
	jQuery.getScript('http://connect.facebook.net/en_US/all.js', function() { 
		FB.init({ 
			appId:'61168221137', cookie:true, 
			status:true, xfbml:true 
		});
		/* Below are facebook events
		 * Facebook events :
		 * auth.login -- fired when the user logs in
		 * auth.logout -- fired when the user logs out
		 * auth.sessionChange -- fired when the session changes
		 * auth.statusChange -- fired when the status changes
		 * xfbml.render -- fired when a call to FB.XFBML.parse() completes
		 * edge.create -- fired when the user likes something (fb:like)
		 * edge.remove -- fired when the user unlikes something (fb:like)
		 * comment.create -- fired when the user adds a comment (fb:comments)
		 * comment.remove -- fired when the user removes a comment (fb:comments)
		 * fb.log -- fired on log message
		 */
		FB.Event.subscribe('auth.login', function(response) {
			that.authenticationHeader();
		});
		FB.Event.subscribe('auth.logout', function(response) {
			that.authenticationHeader();
		});
	}); // get script facebook
	KaraCos.getForm({url:'/get_user_actions_forms',
		callback:function(data) {
			GENTICS.Aloha.Log.info(that,data);
			that.user_actions_forms = data.data;
		});
	return function() {
		return that;
	}
	
}
