# Utilisation d’EmailFetcher

Créé par: Alain RAKOTOARIVELO
Heure de création: 18 octobre 2023 08:22
Étiquettes: EmailFetcher

### fonction `__parse_singlepart_message()`
#### Description
La fonction __parse_singlepart_message() est une fonction auxiliaire utilisée par la fonction scrape() pour analyser les e-mails singlepart. Elle récupère la date d'envoi de l'e-mail et le corps du message, qui est du texte brut.

#### Paramètres

* `email_message (email.message)` : Le message e-mail à analyser.
* `val_dict (dict)` : Un dictionnaire contenant les données du message de chaque partie du message. Sera retourné après sa mise à jour.

#### Fonctionnement

1. La fonction commence par récupérer la date d'envoi de l'e-mail.
2. Ensuite, la fonction récupère le corps du message, qui est du texte brut.
3. Enfin, la fonction ajoute le corps du message au dictionnaire `val_dict` et renvoie le dictionnaire.

#### Résumé

La fonction `__parse_singlepart_message()` permet d'analyser les e-mails singlepart. Elle récupère la date d'envoi de l'e-mail et le corps du message, qui est du texte brut.

#### Explications

La fonction `__parse_singlepart_message()` utilise la bibliothèque Python `email` pour analyser les e-mails singlepart. La méthode `get_payload()` est utilisée pour récupérer le corps du message.

#### Extensions possibles

La fonction `__parse_singlepart_message()` pourrait être améliorée pour prendre en charge d'autres types de messages singlepart, tels que les messages HTML.

#### Codes
```python
def __parse_singlepart_message(self, email_message, val_dict):
    """Helper function for parsing singlepart email messages.

    Args:
        email_message (email.message): The email message to parse.
        val_dict (dict): A dictionary containing the message data from each
            part of the message. Will be returned after it is updated.

    Returns:
        The dictionary containing the message data for each part of the
        message.

    """

    # Get the message body, which is plain text
    val_dict["email_date"] = email_message['email_date']
    #print("EMAIL DATE: ", email_message['date'])
    val_dict["Plain_Text"] = email_message.get_payload(decode=True).decode('ISO-8859-1')
    return val_dict
```

### fonction `__parse_multipart_message()`
#### Description
La fonction `__parse_multipart_message()` est une fonction auxiliaire utilisée par la fonction scrape() pour analyser les e-mails multipart. Elle récupère la date d'envoi de l'e-mail, l'expéditeur, les pièces jointes et le texte brut de l'e-mail.

#### Paramètres

* `email_message (email.message)` : Le message e-mail à analyser.
* `val_dict (dict)` : Un dictionnaire contenant les données du message de chaque partie du message. Sera retourné après sa mise à jour.

#### Fonctionnement

1. La fonction commence par récupérer la date d'envoi de l'e-mail et l'expéditeur.
2. Ensuite, la fonction parcourt chaque partie de l'e-mail.
3. Si la partie est une pièce jointe, la fonction enregistre la pièce jointe dans un fichier.
4. Si la partie est du texte brut, la fonction ajoute le texte brut au dictionnaire `val_dict`.
5. Enfin, la fonction renvoie le dictionnaire `val_dict`.

#### Résumé

La fonction `__parse_multipart_message()` permet d'analyser les e-mails multipart. Elle récupère la date d'envoi de l'e-mail, l'expéditeur et les pièces jointes. Elle ajoute également le texte brut de l'e-mail au dictionnaire `val_dict`.

#### Explications

La fonction `__parse_multipart_message()` utilise la bibliothèque Python `email` pour analyser les e-mails multipart. La méthode `get_filename()` est utilisée pour récupérer le nom de la pièce jointe. La méthode `get_content_type()` est utilisée pour récupérer le type de contenu de la pièce jointe. La méthode `get_payload()` est utilisée pour récupérer le contenu de la pièce jointe.

#### Extensions possibles

La fonction `__parse_multipart_message()` pourrait être améliorée pour prendre en charge d'autres types de pièces jointes, tels que les images et les vidéos.

#### Codes
```python
def __parse_multipart_message(self, path, email_message, val_dict):
        """Helper function for parsing multipart email messages.

        Args:
            email_message (email.message): The email message to parse.
            val_dict (dict): A dictionary containing the message data from each
                part of the message. Will be returned after it is updated.

        Returns:
            The dictionary containing the message data for each part of the
            message.

        """
        #date_utc = datetime.datetime.strptime(email_message['date'], '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=pytz.UTC)
        
        
        """
            __parse_multipart_message: un mail à la fois
            val_dict["email_date"]: Date de l'envoi du mail
            val_dict["email_receiver"]: La personne qui l'a envoyé
        """
        val_dict["email_date"] = email_message['email_date']
        #val_dict["email_date"] = date_utc
        #print("EMAIL DATE: ", email_message['date'])
        val_dict["email_receiver"] = self.__get_to(email_message)
        # For each part
        for part in email_message.walk():
            # If the part is an attachment
            file_name = part.get_filename()
            try:
                if bool(file_name):
                    # Generate file path
                    file_path = os.path.join(path, file_name)
                    try:
                        file_path = os.path.join(path, "PDF_EWA.pdf")
                        file = open(file_path, 'wb')
                    except:
                        file_path = os.path.join(path, "PDF_EWA.pdf")
                        file = open(file_path, 'wb')
                    file.write(part.get_payload(decode=True))
                    file.close()
                    # Get the list of attachments, or initialize it if there isn't one
                    attachment_list = val_dict.get("attachments") or []
                    attachment_list.append("{}".format(file_path))
                    val_dict["attachments"] = attachment_list
                # If the part is plain text
                elif part.get_content_type() == 'text/plain':
                    # Get the body
                    # val_dict["Plain_Text"] = part.get_payload(decode=True).decode('utf-8')
                    val_dict["Plain_Text"] = part.get_payload(decode=True).decode('ISO-8859-1')
            except Exception as e:
                raise e
            
        return val_dict
```

### fonction `scrape(move, unread, delete)`
#### Description
La fonction `scrape()` permet de récupérer les e-mails non lus dans le dossier actuel, de les analyser et de les stocker dans un répertoire. La fonction peut également déplacer les e-mails, les marquer comme non lus ou les supprimer, en fonction des arguments fournis.

#### Paramètres

* `move` (str) : Le dossier vers lequel déplacer les e-mails. Si None, les e-mails ne sont pas déplacés.
* `unread` (bool) : Indique si les e-mails doivent être marqués comme non lus.
* `delete` (bool) : Indique si les e-mails doivent être supprimés.

#### Fonctionnement

1. La fonction commence par vérifier que le serveur est connecté. Si ce n'est pas le cas, elle lève une exception.
2. Ensuite, la fonction recherche les e-mails non lus. Pour chaque e-mail non lu, la fonction récupère le message, l'expéditeur et la date interne.
3. La fonction crée ensuite un répertoire pour chaque e-mail. Si le répertoire n'existe pas, il est créé.
4. Si l'e-mail est composé de plusieurs parties, la fonction appelle la fonction `__parse_multipart_message()` pour analyser chaque partie. Sinon, la fonction appelle la fonction `__parse_singlepart_message()` pour analyser l'e-mail.
5. Enfin, la fonction appelle la fonction `__execute_options()` pour déplacer l'e-mail, le marquer comme non lu ou le supprimer, en fonction des arguments fournis.

#### Résumé

* La fonction `scrape()` permet de récupérer les e-mails non lus dans le dossier actuel, de les analyser et de les stocker dans un répertoire.
* La fonction peut également déplacer les e-mails, les marquer comme non lus ou les supprimer, en fonction des arguments fournis.

#### Explications

* Le paramètre `move` permet de déplacer les e-mails vers un autre dossier. Cela peut être utile pour organiser les e-mails par type, par date, ou par autre critère.
* Le paramètre `unread` permet de marquer les e-mails comme non lus. Cela peut être utile si vous souhaitez les revoir plus tard.
* Le paramètre `delete` permet de supprimer les e-mails. Cela peut être utile si vous ne souhaitez pas les conserver.

#### Extensions possibles

La fonction `scrape()` peut être modifiée pour répondre à des besoins spécifiques. Par exemple, la fonction pourrait être modifiée pour :

* Ne récupérer que les e-mails provenant de certaines adresses e-mail.
* Ne récupérer que les e-mails contenant certains mots-clés dans l'objet ou le corps de l'e-mail.
* Analyser les pièces jointes des e-mails.

Ces extensions peuvent être réalisées en modifiant la fonction `__parse_multipart_message()` ou en ajoutant de nouvelles fonctions.

#### Codes
```python
def scrape(self, move=None, unread=False, delete=False):
    """Scrape unread emails from the current folder.

    Args:
        move (str): The folder to move the emails to. If None, the emails
            are not moved. Defaults to None.
        unread (bool): Whether the emails should be marked as unread.
            Defaults to False.
        delete (bool): Whether the emails should be deleted. Defaults to
            False.

    Returns:
        A list of the file paths to each scraped email.

    """

    # Ensure server is connected
    if type(self.server) is not IMAPClient:
        raise ValueError("server attribute must be type IMAPClient")

    # List containing the file paths of each file created for an email message
    msg_dict = {}
    folder = {}

    # Search for unseen messages
    messages = self.server.search("UNSEEN")
    # For each unseen message
    for uid, message_data in self.server.fetch(messages, ['RFC822', 'INTERNALDATE']).items():
        try:
            # Get the message
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            # Get who the message is from
            from_email = self.__get_from(email_message)
            
            # Generate the dict key for this email
            key = "{}_{}".format(uid, from_email)
            
            # Create directory for this email
            path = ABSOLUTE_PATH_SERVICE_RUNNER['test'] + os.path.join(self.attachment_dir, key)
            if not os.path.exists(path):
                os.mkdir(path)
            
            # Generate the value dictionary to be filled later
            val_dict = {}

            # Display notice
            print("PROCESSING: Email UID = {} from {}".format(uid, from_email))

            # Add the subject
            subject = ''
            try:
                subject = self.__get_subject(email_message).strip()
            except Exception as e:
                subject = str(e)
            val_dict["Subject"] = subject
            internaldate = message_data[b'INTERNALDATE']
            email_message['email_date'] = internaldate

            # If the email has multiple parts
            if email_message.is_multipart():
                val_dict = self.__parse_multipart_message(path, email_message, val_dict)

            # If the message isn't multipart
            else:
                val_dict = self.__parse_singlepart_message(email_message, val_dict)

            msg_dict[key] = val_dict
            folder[key] = path
            
            # If required, move the email, mark it as unread, or delete it
            self.__execute_options(uid, move, unread, delete)
        except Exception as e:
            self.__execute_options(uid, move, unread, delete)
            error_path = os.path.join(os.getcwd(), 'error.txt')
            with open(error_path, 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
            traceback.print_exc()

    # Return the dictionary of messages and their contents
    return msg_dict, folder
```

### fonction `__idle(self, process_func=write_txt_file, **kwargs)`

#### Description
La fonction `__idle()` est une fonction auxiliaire qui permet d'attendre et de traiter les nouveaux e-mails entrants dans un dossier e-mail.

#### Paramètres

* `process_func` (fonction): Une fonction appelée pour traiter les e-mails. La fonction doit prendre uniquement la liste des chemins de fichiers renvoyés par la fonction `scrape()` comme argument. Par défaut, la fonction `write_txt_file()` du module `email_processing` est utilisée.
* `**kwargs` (dict): Des arguments supplémentaires pour le traitement des e-mails. Les arguments facultatifs incluent :
    * `move` (str): Le dossier vers lequel déplacer les e-mails. S'il n'est pas défini, les e-mails ne seront pas déplacés.
    * `unread` (bool): Indique si les e-mails doivent être marqués comme non lus. S'il n'est pas défini, les e-mails sont conservés comme lus.
    * `delete` (bool): Indique si les e-mails doivent être supprimés. S'il n'est pas défini, les e-mails ne sont pas supprimés.

#### Fonctionnement

La fonction `__idle()` fonctionne de la manière suivante :

1. Elle définit les variables `move`, `unread` et `delete` en fonction des paramètres `**kwargs`.
2. Elle démarre l'écoute du serveur en appelant la méthode `idle()` du serveur.
3. Elle définit un délai d'attente de 15 minutes.
4. Tant que le délai d'attente n'est pas dépassé, elle vérifie toutes les secondes si le serveur a reçu de nouveaux e-mails.
    * Si le serveur a reçu de nouveaux e-mails, elle suspend l'écoute en appelant la méthode `idle_done()` du serveur.
    * Elle appelle ensuite la fonction `scrape()` pour traiter les nouveaux e-mails. La fonction `scrape()` renvoie une liste de chemins de fichiers vers les e-mails récupérés.
    * Elle appelle ensuite la fonction `process_func()` pour traiter les e-mails récupérés.
    * Une fois le traitement terminé, elle relance l'écoute du serveur en appelant la méthode `idle()` du serveur.
5. Une fois le délai d'attente dépassé, elle arrête l'écoute du serveur en appelant la méthode `idle_done()` du serveur.

#### Résumé

La fonction `__idle()` :

* Démarre l'écoute du serveur e-mail.
* Vérifie toutes les secondes si le serveur a reçu de nouveaux e-mails.
    * Si le serveur a reçu de nouveaux e-mails, les traite en appelant les fonctions `scrape()` et `process_func()`.
* Arrête l'écoute du serveur e-mail une fois le délai d'attente dépassé.

Dans cet exemple, la fonction `process_func()` est appelée pour traiter les e-mails récupérés par la fonction `scrape()`. La fonction `process_func()` peut être utilisée pour effectuer des actions sur les e-mails, telles que les enregistrer dans un fichier, les analyser ou les supprimer.

#### Codes
```python
def __idle(self, process_func=write_txt_file, **kwargs):
    """Helper function, idles in an email folder processing incoming emails.

    Args:
        process_func (function): A function called to further process the
            emails. The function must take only the list of file paths
            returned by the scrape function as an argument. Defaults to the
            example function write_txt_file in the email_processing module.
        **kwargs (dict): Additional arguments for processing the email.
            Optional arguments include:
                move (str): The folder to move emails to. If not set, the
                    emails will not be moved.
                unread (bool): Whether the emails should be marked as unread.
                    If not set, emails are kept as read.
                delete (bool): Whether the emails should be deleted. If not
                    set, emails are not deleted.

    Returns:
        None

    """

    # Set the relevant kwarg variables
    move = kwargs.get('move')
    unread = bool(kwargs.get('unread'))
    delete = bool(kwargs.get('delete'))

    # Start idling
    self.server.idle()
    print("Connection is now in IDLE mode.")
    # Set idle timeout to 15 minutes
    inner_timeout = get_time() + 60
    # Until idle times out
    # while True:
    while (get_time() < inner_timeout):
        # Check for a new response every 1 seconds
        try:
            responses = self.server.idle_check(timeout=1)
            # print("Server sent:", responses if responses else "nothing")
            # If there is a response
            if (responses):
                # Suspend the idling
                self.server.idle_done()
                try:
                    # Process the new emails
                    msgs, folder = self.scrape(move=move, unread=unread, delete=delete)
                    # Run the process function
                    file_list, attachment_list = process_func(msgs, folder)
                    
                    if len(attachment_list) == 0:
                        print("1")
                        print(file_list)
                        from AmadeusDecoder.utilities.AmadeusParser import AmadeusParser
                        amadeus_parser = AmadeusParser()
                        amadeus_parser.save_data(file_list)
                    else:
                        print("2")
                        from AmadeusDecoder.utilities.ZenithParser import ZenithParser
                        zenith_parser = ZenithParser()
                        zenith_parser.save_data(attachment_list)
                        print('files:', attachment_list)
                except Exception as e:
                    raise e
                finally:
                    # Restart idling
                    self.server.idle()
        except Exception as e:
            error_path = os.path.join(os.getcwd(), 'error.txt')
            with open(error_path, 'a') as error_file:
                error_file.write('{}: \n'.format(datetime.datetime.now()))
                traceback.print_exc(file=error_file)
                error_file.write('\n')
            traceback.print_exc()
    # Stop idling
    self.server.idle_done()
    return
```




### la fonction `listen()`
#### Description
La fonction listen() permet d'écouter un dossier e-mail pour les e-mails entrants et de les traiter.

#### Paramètres
* `timeout (int ou liste)` : Soit un entier représentant le nombre de minutes avant le timeout, soit une liste, formatée comme `[heure, minute]`, de l'heure locale à laquelle le timeout doit se produire.
* `process_func (fonction)` : Une fonction appelée pour traiter davantage les e-mails. La fonction doit prendre uniquement la liste des chemins de fichiers renvoyés par la fonction `scrape()` comme argument. La fonction `write_txt_file()` du module `email_processing` est utilisée par défaut.
* `**kwargs (dict)` : Des arguments supplémentaires pour le traitement des e-mails. Les arguments facultatifs incluent :
    * `move (str)` : Le dossier vers lequel déplacer les e-mails. S'il n'est pas défini, les e-mails ne seront pas déplacés.
    * `unread (bool)` : Indique si les e-mails doivent être marqués comme non lus. S'il n'est pas défini, les e-mails sont conservés comme lus.
    * `delete (bool)` : Indique si les e-mails doivent être supprimés. S'il n'est pas défini, les e-mails ne sont pas supprimés.

#### Fonctionnement

1. La fonction commence par vérifier que le serveur est connecté.
2. Ensuite, la fonction boucle jusqu'à ce que le timeout soit atteint.
3. À chaque boucle, la fonction appelle la fonction `__idle()` pour écouter les nouveaux e-mails entrants.
4. Si de nouveaux e-mails sont reçus, la fonction `__idle()` les traite en appelant la fonction `process_func()`.

#### Résumé

La fonction `listen()` permet d'écouter un dossier e-mail pour les e-mails entrants et de les traiter

#### Explications

La fonction listen() utilise la fonction __idle() pour écouter les nouveaux e-mails entrants. La fonction __idle() utilise la méthode idle() du serveur IMAP pour écouter les nouveaux e-mails.

#### Extensions possibles

La fonction listen() pourrait être améliorée pour prendre en charge d'autres types de serveurs e-mail, tels que les serveurs POP3. Elle pourrait également être améliorée pour prendre en charge d'autres options de traitement des e-mails, telles que le filtrage des e-mails ou l'envoi de notifications.

#### Codes
```python
def listen(self, process_func=write_txt_file, **kwargs):
    """Listen in an email folder for incoming emails, and process them.

    Args:
        timeout (int or list): Either an integer representing the number
            of minutes to timeout in, or a list, formatted as [hour, minute]
            of the local time to timeout at.
        process_func (function): A function called to further process the
            emails. The function must take only the list of file paths
            returned by the scrape function as an argument. Defaults to the
            example function write_txt_file in the email_processing module.
        **kwargs (dict): Additional arguments for processing the email.
            Optional arguments include:
                move (str): The folder to move emails to. If not set, the
                    emails will not be moved.
                unread (bool): Whether the emails should be marked as unread.
                    If not set, emails are kept as read.
                delete (bool): Whether the emails should be deleted. If not
                    set, emails are not deleted.

    Returns:
        None

    """

    # Ensure server is connected
    if type(self.server) is not IMAPClient:
        raise ValueError("server attribute must be type IMAPClient")

    # Run until the timeout is reached
    while True:
        self.__idle(process_func=process_func, **kwargs)
    return
```