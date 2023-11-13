from django.shortcuts import render, redirect
# Cet import va nous permettre d'utiliser les validators de django parmi lesquel on va utiliser celui du test des
# adresses email
from django.core.validators import validate_email
# User est le model par defaut de django dans lequel on va enregistrer nos utilisateurs, c'est ce qui est recommandé
# tant si les champs proposés nous conviennent
from django.contrib.auth.models import User
# le Q object est celui qui va nous permettre d'interroger (faire des queries sur) la base de donnée sur le contenu de
# nos models, genre faire sur eux de test avec des conditions
from django.db.models import Q
# login_required va nou permettre de restreindre l'accès à une url si on est pas connecté
from django.contrib.auth.decorators import login_required
# authenticate est une methode de django qui va nous permettre de recuperer les informations de connexion entrées par
# l'utilisateur et chercher si ces informations existent dans la base de données et elle nous renvoie True ou False
# respectivement si les informations existent dans la base de données ou si elles n'existent pas.
# login va nous permettre de connecter l'utilisateru et logout de le deconnecter
from django.contrib.auth import authenticate, login, logout
# On fait l'importation de notre fichier créé d'envoi de mail de recuperation de mot de passe
from . import email_recovery_password
# Le default_token_generator va nous permettre de générer notre token
from django.contrib.auth.tokens import default_token_generator
# Le force_bytes va nous permettre de forcer la conversion en bytes
from django.utils.encoding import force_bytes
# urlsafe_base64_encode va aussi nous permettre d'encoder le token en base64 et urlsafe_base64_encode va nous permettre
# de decoder ce qui a était encodé
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# codecs va nous servir à faire du décodage des bits
import codecs
# HttpResponseForbidden permet de retourner un message d'interdiction dans une nouvelle page
from django.http import HttpResponseForbidden
# validate password est une methode qui va nous permettre de vérifier si notre mot de passe respecte les conditions
# d'un bon mot de passe selon django et si on veut voir ces différentes conditions c'est dans les settings du projet
from django.contrib.auth.password_validation import validate_password
# ValidationError est une classe qui permet de reconnaitre les erreurs de validations et donne des messages y
# correspondant
from django.core.exceptions import ValidationError


def sign_in_view(request):
    user_is_exist = True
    error_password = False
    error_message = ""
    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        # Instructions de connection
        # Ici on reccherche l'utilisateur dans la base données ayant l'email donné
        user = User.objects.filter(email=email).first()
        # Si l'utilisateur est trouvé
        if user:
            # En django par defaut on teste l'authentification en utilisant le username mais on peut changer ca dans
            # les settings, alors vu qu'ici on va utiliser les paramètres par défaut de django, et comme on a trouvé
            # l'utilisateur avec cette adresse email, on va pouvoir recuperer son username pour le passer à la methode
            # authenticate, alors authenticate prend en parametre le username et le password, on va accede au nom du
            # user en utilisant l'objet user.username vu qu'on l'a trouvé dans la base de données, authenticate prend
            # ces deux paramètres et va dans la base de données pour voir s'il va trouver un utilisateur avec ce
            # username et ce password et va nous renvoyer True si cet utilisateur existe et False si elle n'existe pas,
            # à ce niveau on peut conclure et dire que c'est le mot de passe qui est incorrect vu qu'on avait dejà
            # trouvé le username dans la base de données
            auth_user = authenticate(username=user.username, password=password)
            # Si l'authenticate a donné True
            if auth_user:
                # on peut recupere le l'email et le username de l'utilisateur avec cette manipulation ci bas :
                print(auth_user.email, auth_user.username)
                login(request, auth_user)
                return redirect('dashboard')
            # Si l'authenticate donne False
            else:
                error_password = True
                error_message = "Mot de passe incorrect !"
                print("Mot de passe incorrect !")
        # Si l'adresse mail n'existe pas dans la base de données
        else:
            user_is_exist = False
            error_message = "L'utilisateur n'existe pas !"
            print("L'utilisateur n'existe pas !")
    return render(request, 'account/login.html', {"user_is_exist": user_is_exist, "error_password": error_password, "error_message": error_message})


def sign_up_view(request):
    # Variable pour detecter l'erreur d'email
    error_email = False
    # Variable pour détecter l'erreur de mot de passe de confirmation
    error_password = False
    # variable pour detecter l'erreur d'un enregistrement d'un utilisateur existant déjà
    user_is_exist = False
    error_message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

        # Test d'email valide avec le validator de django validate_email
        try:
            validate_email(email)
        except:
            error_email = True
            error_message = "Entrez un email valide !"
        # Test sur le mot de passe de confirmation
        if not error_email:
            if password != repassword:
                error_password = True
                error_message = "Veuillez entre le meme mot de passe !"
        # Test sur l'enregistrement d'un utilisateur existant
        if not(error_password or error_email):
            # la methode first permet de recuperer la première occurrence de notre question ou query dans la base de
            # données
            user = User.objects.filter(Q(email=email) & Q(username=name)).first()
            # cette interrogation renvoi un object correspondant à la demande ou si elle ne trouve rien de correspondant
            # elle renvoi None
            if user:
                user_is_exist = True
                error_message = f"L'utilisateur avec le nom {name} et l'email {email} existe déja !"
                print(f"L'utilisateur avec le nom {name} et l'email {email} existe déja !")
            # Test pour passer à l'enregistrement de l'utilisateur si toutes les bonnes conditions pour enregistrer un
            # utilisateur sont validées
            if not user_is_exist:
                print("===" * 5, "NEW POST: Succes !", "===" * 5)
                # On enregistre notre utilisateur avec des champs du model User de django prédéfinis et qu'on peut
                # trouver sur internet sur le site de la documentation django
                user = User(
                    username=name,
                    email=email,
                )
                # Alors pour enregistrer le mot de passe avec ce modèl de django on enregistre le mot de passe à part de la
                # facon ci-dessous : et après on enregistre dans la base de données
                user.set_password(password)
                user.save()

                return redirect('sign_in')

    context = {
        'error_email': error_email,
        'error_password': error_password,
        'error_message': error_message,
        'user_is_exist': user_is_exist,
    }

    return render(request, 'account/index.html', context)


# C'est ce décorateur qui nous permet de rendre cette vue accessible seulement si on est déja connecté et dans ses
# paramètres login_url prend la valeur de l'url sur lequel on va nous rediriger si on tente d'acceder à cette page sans
# etre connecté.
# Sans oublier que pour que ca marche on ne doit pas aussi etre connecté dans l'interface d'administration dans le meme
# navigateur
@login_required(login_url='sign_in')
def dashboard_view(request):
    return render(request, 'account/admin.html')


def log_out_view(request):
    logout(request)
    return redirect('sign_in')


def forgot_password_view(request):
    error_message = ""
    user_is_exist = True
    if request.method == "POST":
        email = request.POST.get('email', None)
        user = User.objects.filter(email=email).first()
        if user:
            # Ici à partir du user on crée le token
            token = default_token_generator.make_token(user)
            # Ici on crypte le user id
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            # Ici, on recuperer le nom de domaine du site et vu qu'on utilise le serveur de django alors on aura son
            # adresse IP et si on etait en ligne on va recuperer le domaine en ligne
            nom_domain = request.META['HTTP_HOST']
            # On recupere les élément qui vont composé l'url qu'on va envoyé
            url = {
                'nom_domain': nom_domain,
                'token': token,
                'user_id': user_id
                   }
            object_email = 'Récupération de mot de passe'
            email_recovery_password.email_sender('elkanan10@gmail.com', user.email, object_email, url)
            print("Send email...")
        else:
            print(f"Il n'y a pas un compte associé à l'email {email}")
    return render(request, 'account/forgot_password.html')


def update_password_view(request, token, user_id):
    error_message = ""
    error_password = False
    success_password = False
    try:
        user_id = urlsafe_base64_decode(user_id)
        decode_user_id = codecs.decode(user_id, 'utf-8')
        print(token, decode_user_id)
        user = User.objects.get(id=user_id)
        print(user)
    except:
        return HttpResponseForbidden("L'utilisateur est introuvable")
    check_token = default_token_generator.check_token(user, token)
    print(check_token)
    if not check_token:
        return HttpResponseForbidden("Votre token est invalide ou a expiré")
    if request.method == "POST":
        new_password = request.POST.get('new_password', None)
        renew_password = request.POST.get('renew_password', None)
        if new_password == renew_password:
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
                user.save()
                success_password = True
                error_message = "Mot de passe mise à jour avec succès !"
            except ValidationError as e:
                error_password = True
                error_message = str(e)

        else:
            error_password = True
            error_message = "Les deux mots de passes ne sont pas identiques"
            print("Les deux mots de passes ne sont pas identiques")

    return render(request, 'account/update_password.html',
                  {"error_password": error_password, "success_password": success_password, "error_message": error_message})
