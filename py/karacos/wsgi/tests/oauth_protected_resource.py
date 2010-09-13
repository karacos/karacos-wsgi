# -*- coding: utf-8 -*-
try:
    import wsgiref
except ImportError:
    raise ImportError("""
wsgiref is required to run this example, but not required by the wsgioauth
package.  You must install wsgiref before you can run this file.  One way to
install it is through easy_install by using the following command in your
console:  easy_install wsgiref
""")
from wsgiref.simple_server import make_server
from wsgioauth.mock import app_factory, echo_app, filter_factory

consumer = ('dpf43f3p2l4k3l03', # key
            'kd94hf93k423kf44', # secret
            )

if __name__ == '__main__':
    # Create the administration app.  The administration app isn't used in
    #   this example, but you may want to try using it outside of the
    #   example.
    admin_app = app_factory()

    # Instantiate the storage so that we can add the example consumer.
    mock_storage = admin_app.storage_factory({}, {})
    mock_storage.add_consumer(*consumer)

    # Create the OAuth protected application.
    oauth_protected_app = filter_factory(echo_app)

    def mapper(environ, start_response):
        """Routes the request to the correct application."""
        if environ['PATH_INFO'].find('oauth_admin') >= 0:
            return admin_app(environ, start_response)
        else:
            return oauth_protected_app(environ, start_response)
    server = make_server('localhost', 61080, mapper)
    print("Serving the echo application at:  http://localhost:61080/")
    print("Serving the admin application at:  "
        "http://localhost:61080/oauth_admin")
    server.serve_forever()
