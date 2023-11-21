### Utilisation d’AmadeusDecoder

Créé par: Alain RAKOTOARIVELO
Heure de création: 19 octobre 2023 12:10
Étiquettes: AmadeusDecoder

### fonction `needed_content(file_content)`
**1. Description**
Cette fonction est utilisée pour extraire le contenu nécessaire à partir d'un fichier. Elle itère à travers chaque ligne du contenu du fichier et vérifie si la ligne commence par certains caractères. Si elle ne commence pas par des caractères spécifiques, elle ajoute la ligne à la liste "neededContent". La fonction retourne ensuite la liste "neededContent".

**2. Paramètres**
- `self` : Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.
- `file_content` : Ce paramètre est une liste contenant le contenu d'un fichier.

**3. Fonctionnement**
La fonction itère à travers chaque ligne de la liste "file_content". Elle vérifie si une ligne commence par `â€¢` ou `*`. Si ce n'est pas le cas, elle vérifie ensuite si la ligne commence par `)>` ou `>`. Si c'est le cas et que ce n'est pas la première ligne (index > 0), la boucle est interrompue à l'aide de l'instruction "break". Sinon, la ligne est ajoutée à la liste "neededContent". Finalement, la fonction retourne la liste "neededContent".

**4. Résumé**
La fonction `needed_content` extrait le contenu d'un fichier en excluant les lignes qui commencent par des caractères spécifiques. Elle retourne une liste du contenu nécessaire.

**5. Explications**
La fonction commence par initialiser une liste vide appelée `neededContent`. Elle itère ensuite à travers chaque ligne de la liste "file_content" à l'aide d'une boucle for.

À l'intérieur de la boucle, elle vérifie si la ligne actuelle commence par `â€¢` ou `*` en utilisant la méthode `startswith`. Si elle ne commence pas par ces caractères, elle passe à la vérification suivante.

Elle vérifie ensuite si la ligne commence par `)>` ou `>`. Si c'est le cas et que ce n'est pas la première ligne (index > 0), elle sort de la boucle à l'aide de l'instruction "break". Cela est fait pour exclure toutes les lignes qui pourraient indiquer la fin du contenu nécessaire.

Si la ligne passe les deux vérifications, elle est ajoutée à la liste `neededContent` à l'aide de la méthode `append`.

Finalement, la fonction retourne la liste `neededContent`.

**6. Extensions possibles**
- La fonction peut être modifiée pour accepter des paramètres supplémentaires afin de personnaliser les caractères à vérifier au début de chaque ligne.

- Une gestion des erreurs peut être ajoutée pour gérer les cas où le paramètre "file_content" n'est pas une liste ou est vide.

- La fonction peut être étendue pour écrire le contenu extrait dans un nouveau fichier ou effectuer un traitement supplémentaire sur celui-ci.

### fonction `read_file()`

#### Description

La fonction `read_file()` lit le contenu d'un fichier et renvoie une liste des lignes du contenu, en ignorant les lignes vides et la ligne d'en-tête du message.

#### Paramètres

* `self` : L'instance de la classe `AmadeusParser` qui appelle la fonction.

#### Fonctionnement

La fonction fonctionne comme suit :

1. Ouvre le fichier en mode lecture.
2. Lit le contenu du fichier ligne par ligne.
3. Supprime les lignes vides et la ligne d'en-tête du message.
4. Renvoie la liste des lignes restantes.

#### Résumé

La fonction `read_file()` permet de lire le contenu d'un fichier et d'en extraire les lignes pertinentes.

#### Explications

La fonction utilise une boucle `for` pour lire le contenu du fichier ligne par ligne. Elle utilise la fonction `strip()` pour supprimer les espaces en début et en fin de ligne. Elle utilise la méthode `get_path()` de l'instance `self` pour obtenir le chemin du fichier.

#### Extensions possibles

La fonction pourrait être améliorée de la manière suivante :

* Pour supporter des formats de fichier différents, la fonction pourrait utiliser la bibliothèque Python `email` pour analyser le contenu du fichier.
* Pour gérer les erreurs de lecture de fichier, la fonction pourrait utiliser la bibliothèque Python `logging` pour enregistrer les erreurs dans un fichier de journal.

#### Exemple d'utilisation

```python
import os

from save_data import AmadeusParser

# Création d'une instance de la classe AmadeusParser
parser = AmadeusParser()

# Définition du chemin du fichier
file_path = os.path.join(os.getcwd(), 'email.txt')

# Lecture du contenu du fichier
contents = parser.read_file(file_path)

# Affichage du contenu du fichier
print(contents)
```

Cet exemple lit le contenu du fichier `email.txt` et affiche la liste des lignes du contenu.s

### fonction `save_data(file_list)`

#### Description

Les codes fournis permettent de sauvegarder les données des e-mails de confirmation de réservation (PNR) dans une base de données. Les codes utilisent la bibliothèque Python `AmadeusParser` pour analyser les e-mails et extraire les informations de réservation.

#### Paramètres

* `file_list (list)` : Une liste de fichiers contenant les données des e-mails à sauvegarder.

#### Fonctionnement

La fonction `save_data()` fonctionne comme suit :

1. Elle boucle sur la liste des fichiers.
2. Pour chaque fichier, elle crée une instance de la classe `AmadeusParser`.
3. Elle définit le chemin du fichier et la date de l'e-mail.
4. Elle lit le contenu du fichier.
5. Elle récupère les informations nécessaires du contenu du fichier.
6. Si le fichier est un e-mail de type TJQ, elle appelle la fonction `parse_tjq()` pour analyser les données du fichier et extraire les informations de réservation.
7. Sinon, elle appelle la fonction `parse_pnr()` pour analyser les données du fichier et extraire les informations de réservation.

#### Résumé

La fonction `save_data()` permet de sauvegarder les données des e-mails de confirmation de réservation (PNR) dans une base de données. Les codes utilisent la bibliothèque Python `AmadeusParser` pour analyser les e-mails et extraire les informations de réservation.

#### Explications

La fonction `save_data()` utilise la bibliothèque Python `AmadeusParser` pour analyser les e-mails. La bibliothèque `AmadeusParser` fournit des fonctions pour analyser les différents types d'e-mails Amadeus.

#### Extensions possibles

Les codes fournis pourraient être améliorés de la manière suivante :

* Prendre en charge d'autres types d'e-mails, tels que les e-mails de modification de réservation (RQ), les e-mails d'émission de billet (TKT) et les e-mails d'émission de document électronique (EMD).
* Prendre en charge des options supplémentaires pour la sauvegarde des données dans la base de données, telles que la spécification de la table de destination.
  
#### Examples d'utilisation
```python
# Importation des bibliothèques
import os
import datetime

# Importation de la fonction `save_data()`
from save_data import save_data

# Définition de la liste des fichiers
file_list = [
    {'file_path': 'email1.txt', 'email_date': '2023-10-19'},
    {'file_path': 'email2.txt', 'email_date': '2023-10-19'},
]

# Sauvegarde des données des e-mails
save_data(file_list)
```

Dans cet exemple, la liste file_list contient deux fichiers, email1.txt et email2.txt. La fonction save_data() est appelée avec cette liste en paramètre. La fonction boucle sur la liste et, pour chaque fichier, elle appelle la fonction parse_file() de la classe AmadeusParser pour analyser les données du fichier et extraire les informations de réservation. Les informations de réservation sont ensuite sauvegardées dans une base de données.

#### Codes 
```python
def save_data(self, file_list):
    for file in file_list:
        temp = AmadeusParser()
        temp.set_path(file['file_path'])
        temp.set_email_date(file['email_date'])
        contents = temp.read_file()
        needed_content = temp.needed_content(contents)
        # save pnr data
        if len(contents) > 0:
            if contents[0].startswith('AGY'): # TJQ
                try:
                    temp.parse_tjq(needed_content)
                except Exception as e:
                    print('File (TJQ) with error: ' + str(temp.get_path()))
                    with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                        error_file.write('{}: \n'.format(datetime.datetime.now()))
                        error_file.write('File (TJQ) with error: {} \n'.format(str(temp.get_path())))
                        traceback.print_exc(file=error_file)
                        error_file.write('\n')
                    if (str(e) == "connection already closed"):
                        Sending.send_email_pnr_parsing(temp.get_path())
                    continue
            else:
                for j in range(len(contents)):
                    if contents[j].startswith('RPP'):
                        temp.set_is_archived(True)
                        continue
                    if contents[j].startswith('RP') and not contents[j].startswith('RPP'):
                        try:
                            temp.parse_pnr(contents[j:], needed_content, temp.get_email_date())
                            break
                        except Exception as e:
                            print('File (PNR Altea) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (PNR Altea) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
                    if contents[j].startswith('VOTRE NUMERO DE DOSSIER'):
                        try:
                            needed_content = contents[j:]
                            temp.parse_not_issued_zenith(needed_content)
                            break
                        except Exception as e:
                            print('File (EWA) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (TST) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
                    if contents[j].startswith('EMD'):
                        try:
                            temp.parse_emd(temp.needed_content(contents[j:]), temp.get_email_date())
                            break
                        except:
                            print('File (EMD) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (EMD) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
                    if contents[j].startswith('TKT'):
                        try:
                            temp.parse_ticket(temp.needed_content(contents[j:]), temp.get_email_date())
                            break
                        except:
                            print('File (Ticket) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (Ticket) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
                    if contents[j].startswith('TST'):
                        try:
                            temp.parse_tst(temp.needed_content(contents[j:]))
                            break
                        except:
                            print('File (TST) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (TST) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
                    if contents[j].startswith('FEE MODIFY REQUEST'):
                        try:
                            temp.sf_decrease_request_update(temp.needed_content(contents[j:]))
                            break
                        except:
                            print('File (REQUEST) with error: ' + str(temp.get_path()))
                            with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
                                error_file.write('{}: \n'.format(datetime.datetime.now()))
                                error_file.write('File (REQUEST) with error: {} \n'.format(str(temp.get_path())))
                                traceback.print_exc(file=error_file)
                                error_file.write('\n')
                            if (str(e) == "connection already closed"):
                                Sending.send_email_pnr_parsing(temp.get_path())
                            continue
```