Rendu de l'url d'un Webnode par KaraCos


1. Localisation des fichiers :

Les themes se trouvent :
soit dans karacos :
$KARACOS_HOME/resources/templates
soit dans le répertoire d'une instance de serveur :
$KARACOS_HOME/server/$INSTANCE/resources/templates
soit dans le répertoire d'une application :
$KARACOS_HOME/server/$INSTANCE/deploy/$APP/resources/templates

Chaque répertoire dans un de ces dossiers est un theme pour KaraCos pour peu qu'il contienne un fichier site.
Pour changer le theme, utiliser les url d'administration suivants (une fois connecté au site) :
http://KaraCosDomain/set_user_theme
http://KaraCosDomain/set_theme
*TODO* imlémenter un chooser

1. Structure d'un theme