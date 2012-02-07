KaraCos API
===========

API de base KaraCos Core:
../uml/DbObjects.png

Vue générale :
../uml/SemanticwebEngine.png

exposition HTTP (sur l'url d'un objet) :

Type	|   	Data        			|    Réponse
--------|---------------------------------------|----------------------------------------
GET 	|   	Accept: 'text/html'		|    rendu template (voir TEMPLATES)
--------|---------------------------------------|----------------------------------------
GET  	|   	Accept: 'application/json'	|    
--------|---------------------------------------|----------------------------------------
POST	|	Accept: 'application/json'	|
	|	Content-Type:application/json	|    reponse REST par la methode 
	|     data: {				|     methodName de l'objet
	|		"method": "methodName",	|    params doit contenir les parametres
	|		"id": 1			|    attendus par la methode
	|		"params": {}		|    id = 1 (pas encore utilisé)
	|	}				|
--------|---------------------------------------|----------------------------------------

sur chaque objet exposé, on peut appeler en POST get_user_actions_forms :
{"method":"get_user_actions_forms","params":{},"id":1}

Ca retourne la liste des methodes 'autorisées' sur l'objet pour l'utilisateur courant, ainsi que les
parametres attendus, un contrat d'appel qui devra respecter la structure du POST décrite ci-dessus


Exemple

Requête:
--------

    POST /
    Accept: application/json
    
    data: {
	"method": "get_user_actions_forms",
	"id": 1,
	"params": {}
    }

Réponse:
--------

    { "success": true", "message": "get_user_actions_forms succeeded", 
      "data": 
	{
		"email": "anonymous@karacos",
		"user": "anonymous@karacos",
		"id": "2077e5c421fb488db8b7ad13d9be3cd3",
		"actions": [
			{"action": "get_user_actions", "acturl": "/"},
			{
				"action": "login", "acturl": "/",
				"form": [
					{"fields": [{"dataType": "TEXT", "name": "email", "title": "Addresse email"}, {"dataType": "PASSWORD", "name": "password", "title": "Mot de passe"}], 
						"submit": "Valider", 
						"title": "Vous connecter directement au site (Connexion)"}, 
					{"fields": [{"dataType": "TEXT", "name": "email", "title": "Addresse email"}, {"dataType": "HIDDEN", "name": "register", "value": "register", "title": "Creez votre identifiant"}], 
						"submit": "S'enregistrer", 
						"title": "Cr&eacute;er un compte (Pas encore inscrit ?)"}],
				"label": "S'authentifier"
			}, 
			{
				"action": "set_lang_session",
				"acturl": "/",
				"form": {
					"fields": [
						{"dataType": "TEXT", "formType": "SELECT", "values": ["en-US"], "name": "lang", "title": "New Language"}
						  ], 
					"submit": "Change", 
					"title": "Change user lang"
				}, 
				"label": "Change user language"
			}, 
			{"action": "fragment", "acturl": "/"}, 
			{"action": "get_user_actions_forms", "acturl": "/"}, 
			{"action": "register", "acturl": "/", "form": {"fields": [{"dataType": "TEXT", "name": "email", "title": "Addresse email"}], "submit": "Valider", "title": "S'enregister"}, "label": "S'inscrire"}, 
			{"action": "_process_facebook_cookie", "acturl": "/"}, 
			{"action": "validate_user", "acturl": "/"}, 
			{"action": "modify_person_data", "acturl": "/"}, 
			{"action": "create_password", "acturl": "/", "form": {"fields": [{"dataType": "PASSWORD", "name": "password", "title": "Mot de passe"}, {"dataType": "PASSWORD", "name": "confirmation", "title": "Confirmez le mot de passe"}], "submit": "Valider", "title": "Saisissez votre mot de passe"}}, 
			{"action": "set_user_email", "acturl": "/"}, 
			{"action": "product", "acturl": "/"}
		], 
	}
    }
