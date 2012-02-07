Rendu de l'url d'un Webnode par KaraCos


1. Localisation des fichiers :

Les themes se trouvent :
soit dans karacos :
$KARACOS_HOME/resources/templates
soit dans le r�pertoire d'une instance de serveur :
$KARACOS_HOME/server/$INSTANCE/resources/templates
soit dans le r�pertoire d'une application :
$KARACOS_HOME/server/$INSTANCE/deploy/$APP/resources/templates

Chaque r�pertoire dans un de ces dossiers est un theme pour KaraCos pour peu qu'il contienne un fichier site.
Pour changer le theme, utiliser les url d'administration suivants (une fois connect� au site) :
http://KaraCosDomain/set_user_theme
http://KaraCosDomain/set_theme
*TODO* iml�menter un chooser

1. Mappage des url's

Dans KaraCos, chaque url est un appel � une methode d'un objet de type WebNode (ou h�rit�)
 / est toujours d'un type Domain ou un de ses h�ritiers.
/login -> methode login de l'objet Domain
/a/ Objet 'child' nomm� a dans le domaine
/a/edit_content -> methode edit_content de l'objet a

Lorsque l'url est acc�d� avec une requete http GET avec un header Accept: text/html (comportement par d�faut d'un navigateur),
elle est rendue avec le theme associ� � l'utilisateur, � d�faut le theme du domaine.

1. Structure d'un theme

Le fichier site est le point d'entr�e d'un theme. Il est invoqu� avec le contexte suivant :
    
    {
        'instance': NodeObject, # instance of karacos node which is requested
	'action': data, # representation of the action form (if present, None otherwise)
	'result': result # result of invoked method (if present, None otherwise)
    }

de l�, tout est possible, instance �tant un objet du type WebNode ou un de ses enfants, on peut acc�der � ces methodes et/ou � ses donn�es :
---> API KaraCos

Methodes et donn�es courantes :
${instance._get_action_url()} : url de l'instance
${instance['name']} : nom de l'instance (unique dans un parent)
${instance['title']}: Le titre de l'instance rendu dans la balise <title> (default: no title, utiliser /edit_content pour modifier)
En g�n�ral, ${instance['dataName']} renvoie la donn�e qui correspond a l'attribut du m�me nom ('dataName') dans le document couchdb port� par l'instance.
${instance.get_web_childrens_for_id()}: List of browseable childNodes authorized for current user (ls like...)
${instance.__parent__} Le noeud parent de l'instance en cours, self si instance = domain
${instance.__domain__} Le domaine (racine) du noeud courant, self si instance = domain

exemple : afficher les enfants d'un noeud :

    <% childrens = instance.__domain__.get_web_childrens_for_id() %>
    <ul>
    % for child in childrens.keys():
	 <li><a href="${instance._get_action_url()}${childrens[child]}">${childrens[child]}</a></li>
    % endfor
    </ul>

Autre exemples, tests et expressions :

    % if 'dataName' in instance: # test si le document couchdb poss�de un attribut dataName
        <strong property="dataName">${instance['dataName']}</strong>
    % endif

En fonction du type de noeud, les methodes accessibles sont diff�rentes. Voire � l'API des types