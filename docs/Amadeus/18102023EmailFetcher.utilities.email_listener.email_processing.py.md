# Utilisation d’EmailFetcher

Créé par: Alain RAKOTOARIVELO
Heure de création: 19 octobre 2023 09:34
Étiquettes: EmailFetcher

### fonction `write_txt_file(msg_dict, folder)`
#### Description

La fonction `write_txt_file()` permet d'écrire les données des e-mails récupérées par la fonction `scrape()` dans des fichiers texte.

#### Paramètres

* `email_listener (EmailListener)` : L'objet `EmailListener` avec lequel cette fonction est utilisée.
* `msg_dict (dict)` : Le dictionnaire de données des e-mails renvoyé par la fonction `scrape()`.

#### Fonctionnement

1. La fonction commence par créer une liste de fichiers à retourner.
2. Ensuite, la fonction parcourt chaque clé du dictionnaire `msg_dict`.
3. Pour chaque clé, la fonction crée un chemin de fichier pour le fichier texte à créer.
4. Si le fichier texte existe déjà, la fonction passe à la clé suivante.
5. Sinon, la fonction ouvre le fichier texte en écriture.
6. La fonction convertit ensuite les données de l'e-mail en une chaîne de caractères et l'écrit dans le fichier.
7. Enfin, la fonction ferme le fichier texte.

#### Résumé

La fonction `write_txt_file()` permet d'écrire les données des e-mails récupérées par la fonction `scrape()` dans des fichiers texte.

#### Explications

La fonction `write_txt_file()` utilise la fonction `__msg_to_str()` pour convertir les données de l'e-mail en une chaîne de caractères. La fonction `__msg_to_str()` est une fonction auxiliaire qui utilise la bibliothèque Python `email` pour analyser les e-mails et les convertir en chaînes de caractères.

#### Extensions possibles

La fonction `write_txt_file()` pourrait être améliorée pour prendre en charge d'autres formats de fichiers, tels que les fichiers CSV ou JSON. Elle pourrait également être améliorée pour prendre en charge des options supplémentaires pour le traitement des e-mails, telles que la conservation des pièces jointes.

#### Codes
```python
def write_txt_file(msg_dict, folder):
    """Write the email message data returned from scrape to text files.

    Args:
        email_listener (EmailListener): The EmailListener object this function
            is used with.
        msg_dict (dict): The dictionary of email message data returned by the
            scraping function.

    Returns:
        A list of file paths of files that were created and written to.

    """

    # List of files to be returned
    file_list = []
    attachment_list = []
    # For each key, create a file and ensure it doesn't exist
    for key in msg_dict.keys():
        temp_content = {}
        
        email_date = None
        if 'email_date' in msg_dict[key]:
            email_date = msg_dict[key]['email_date']
        file_path = os.path.join(folder[key], "{}.txt".format(key))
        temp_content['email_date'] = email_date
        temp_content['file_path'] = file_path
        
        if os.path.exists(file_path):
            print("File has already been created.")
            continue

        # Open the file
        file = None
        # Convert the message data to a string, and write it to the file
        msg_string = __msg_to_str(msg_dict[key])
        try:
            try:
                file = open(file_path, "w+")
                file.write(msg_string)
            except:
                file = open(file_path, "w+", encoding="utf-8")
                file.write(msg_string)
        except:
            error_path = os.path.join(os.getcwd(), 'error.txt')
            with open(error_path, 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
        finally:
            if file is not None:
                file.close()
        # Add the file name to the return list
        file_list.append(temp_content)
        # Add attachment_list
        if 'attachments' in msg_dict[key]:
            if msg_dict[key]['attachments'][0].split('.')[-1] == 'pdf' :
                temp_content_ewa_pdf = {}
                temp_content_ewa_pdf['email_date'] = email_date
                temp_content_ewa_pdf['attachment'] = msg_dict[key]['attachments']
                
                attachment_list.append(temp_content_ewa_pdf)

    return file_list, attachment_list
```

### fonction `__msg_to_str()`

#### Description

La fonction `__msg_to_str()` permet de convertir un dictionnaire contenant des données d'e-mail en une chaîne de caractères.

#### Paramètres

* `msg (dict)` : Le dictionnaire contenant les données d'e-mail.

#### Fonctionnement

1. La fonction commence par créer une chaîne de caractères vide pour stocker la chaîne de caractères de l'e-mail.
2. Ensuite, la fonction ajoute le sujet de l'e-mail à la chaîne de caractères.
3. Si le corps texte de l'e-mail est défini, la fonction l'ajoute à la chaîne de caractères.
4. Si le corps HTML de l'e-mail est défini, la fonction l'ajoute à la chaîne de caractères.
5. Enfin, la fonction ajoute la liste des pièces jointes à la chaîne de caractères.

#### Résumé

La fonction `__msg_to_str()` permet de convertir un dictionnaire contenant des données d'e-mail en une chaîne de caractères. La chaîne de caractères résultante peut être utilisée pour écrire les données de l'e-mail dans un fichier ou pour les afficher à l'utilisateur.

#### Explications

La fonction `__msg_to_str()` utilise la bibliothèque Python `email` pour analyser les e-mails et extraire les données des e-mails.

#### Extensions possibles

La fonction `__msg_to_str()` pourrait être améliorée pour prendre en charge d'autres formats d'e-mails, tels que les e-mails Rich Text Format (RTF). Elle pourrait également être améliorée pour prendre en charge des options supplémentaires pour le formatage de la chaîne de caractères de l'e-mail, telles que la spécification de la largeur de la chaîne de caractères ou l'inclusion d'un en-tête.

#### Codes 
```python
def __msg_to_str(msg):
    """Convert a dictionary containing message data to a string.

    Args:
        msg (dict): The dictionary containing the message data.

    Returns:
        A string version of the message

    """

    # String to be returned
    msg_string = ""
    
    # Append the subject
    subject = msg.get('Subject')
    msg_string += "Subject\n\n{}\n\n\n".format(subject)

    # Append the plain text
    plain_text = msg.get('Plain_Text')
    if plain_text is not None:
        msg_string += "Plain_Text\n\n{}\n\n\n".format(plain_text)

    # Append the plain html and html
    plain_html = msg.get('Plain_HTML')
    html = msg.get('HTML')
    if plain_html is not None:
        msg_string += "Plain_HTML\n\n{}\n\n\n".format(plain_html)
        msg_string += "HTML\n\n{}\n\n\n".format(html)

    # Append the attachment list
    attachments = msg.get('attachments')
    if attachments is None:
        return msg_string

    msg_string += "attachments\n\n"
    for file in attachments:
        msg_string += "{}\n".format(file)

    return msg_string
```