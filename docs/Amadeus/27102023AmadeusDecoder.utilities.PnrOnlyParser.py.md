Créé par: Alain RAKOTOARIVELO
Heure de création: 20 octobre 2023 14:16
Étiquettes: AmadeusDecoder

### Méthode `normalize_file(self, needed_content)` et `is_regular_line(self, line)`
**1. Description**

La fonction `is_regular_line` vérifie si une ligne donnée est une ligne régulière. Une ligne régulière est définie comme une ligne qui commence par un nombre ou une séquence de mots séparés par des espaces. La fonction renvoie True si la ligne est régulière et False sinon.

La fonction `normalize_file` normalise le contenu d'un fichier en filtrant les lignes non régulières et en fusionnant les lignes exclues avec la ligne précédente. Elle renvoie le contenu normalisé sous forme de liste.

**2. Paramètres**

- `self`: Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.
- `line`: Ce paramètre représente une ligne de texte à vérifier dans la fonction is_regular_line.
- `needed_content`: Ce paramètre représente le contenu du fichier à normaliser dans la fonction normalize_file.

**3. Fonctionnement**

La fonction `is_regular_line` vérifie si la ligne donnée est régulière en utilisant une série de conditions. Elle divise la ligne en utilisant le point ou l'espace comme délimiteur et vérifie si le premier élément est numérique. Si ce n'est pas le cas, elle vérifie si le premier élément est numérique lorsqu'il est divisé par un espace. Si aucune de ces conditions n'est satisfaite, la fonction renvoie False. Sinon, elle renvoie True.

La fonction `normalize_file` crée une nouvelle liste vide new_content. Elle itère sur chaque élément de la liste needed_content et vérifie si l'élément est une ligne régulière en appelant la fonction is_regular_line. Si c'est le cas, elle ajoute l'élément à la liste new_content. Sinon, elle vérifie si l'élément ne correspond pas à une ligne régulière et commence par un identifiant spécifique. Si c'est le cas, elle ajoute également l'élément à la liste new_content. Sinon, elle vérifie si la liste new_content n'est pas vide et si l'élément ne doit pas être exclu. Si ces conditions sont satisfaites, elle fusionne l'élément avec la dernière ligne de la liste new_content.

Ensuite, la fonction appelle les méthodes `appropriated_start` et `logic_sequence` pour effectuer des traitements supplémentaires sur le contenu normalisé. Si la liste upper_content renvoyée par appropriated_start n'est pas vide, elle concatène upper_content avec le résultat de logic_sequence appelé avec new_file_start. Sinon, elle appelle logic_sequence avec new_content et renvoie le résultat.

**4. Résumé**

La fonction `is_regular_line` vérifie si une ligne donnée est une ligne régulière en utilisant des conditions basées sur le contenu de la ligne. 

La fonction `normalize_file` normalise le contenu d'un fichier en filtrant les lignes non régulières et en fusionnant les lignes exclues avec la ligne précédente. Elle renvoie le contenu normalisé sous forme de liste.

**5. Explications**

La fonction `is_regular_line` vérifie si la ligne donnée est régulière en utilisant une série de conditions. Elle divise la ligne en utilisant le point ou l'espace comme délimiteur et vérifie si le premier élément est numérique. Si ce n'est pas le cas, elle vérifie si le premier élément est numérique lorsqu'il est divisé par un espace. Si aucune de ces conditions n'est satisfaite, la fonction renvoie False. Sinon, elle renvoie True.

La fonction `normalize_file` crée une nouvelle liste vide new_content. Elle itère sur chaque élément de la liste needed_content et vérifie si l'élément est une ligne régulière en appelant la fonction is_regular_line. Si c'est le cas, elle ajoute l'élément à la liste new_content. Sinon, elle vérifie si l'élément ne correspond pas à une ligne régulière et commence par un identifiant spécifique. Si c'est le cas, elle ajoute également l'élément à la liste new_content. Sinon, elle vérifie si la liste new_content n'est pas vide et si l'élément ne doit pas être exclu. Si ces conditions sont satisfaites, elle fusionne l'élément avec la dernière ligne de la liste `new_content`

Ensuite, la fonction appelle les méthodes `appropriated_start` et `logic_sequence` pour effectuer des traitements supplémentaires sur le contenu normalisé. La méthode appropriated_start renvoie une liste upper_content contenant les éléments appropriés pour le début du nouveau fichier, ainsi qu'un nouvel index de départ new_file_start. Si la liste upper_content n'est pas vide, la fonction concatène upper_content avec le résultat de logic_sequence appelé avec new_file_start. Sinon, elle appelle logic_sequence avec new_content et renvoie le résultat.

En résumé, la fonction `normalize_file` normalise le contenu d'un fichier en filtrant les lignes non régulières et en fusionnant les lignes exclues avec la ligne précédente. Elle renvoie le contenu normalisé sous forme de liste. Elle utilise la fonction is_regular_line pour vérifier si une ligne est régulière et les méthodes appropriated_start et logic_sequence pour effectuer des traitements supplémentaires sur le contenu normalisé.

**6. Extensions possibles**

- On peut ajouter des validations supplémentaires pour vérifier si le contenu du fichier est au bon format ou s'il contient des erreurs.

- La fonction peut être étendue pour prendre en charge d'autres opérations de normalisation sur le contenu du fichier, telles que la suppression des lignes vides ou des caractères spéciaux.

- On peut ajouter des options de configuration pour permettre à l'utilisateur de spécifier les actions à effectuer lors de la normalisation du fichier, par exemple en excluant certaines lignes ou en modifiant le format des lignes.

- La fonction peut être intégrée dans un module ou une classe plus large pour faciliter son utilisation et sa réutilisation dans d'autres parties du code.

- On peut ajouter des tests unitaires pour vérifier le bon fonctionnement de la fonction dans différentes situations et garantir sa stabilité.

- On peut également ajouter des commentaires et des annotations dans le code pour faciliter la compréhension et la maintenance du code par d'autres développeurs.

- La fonction peut être traduite en d'autres langages de programmation pour permettre son utilisation dans des environnements différents.

- On peut ajouter des fonctionnalités supplémentaires, telles que la gestion des erreurs de lecture de fichier ou la journalisation des actions effectuées par la fonction.

- La fonction peut être optimisée pour améliorer ses performances, par exemple en utilisant des algorithmes plus efficaces ou en évitant des opérations redondantes.

- On peut ajouter des options de configuration pour permettre à l'utilisateur de spécifier des actions à effectuer lors de la normalisation du fichier, par exemple en déclenchant des notifications ou en effectuant des calculs supplémentaires.

**7. Codes**
```python
# Check if regular pnr line: a regular one always start with a number followed by a blank space or a full stop'''
def is_regular_line(self, line):
    regular = True
    if(line.split(".")[0].isnumeric() == False):
        if(line.split(" ")[0].isnumeric() == False):
            regular = False
    
    if len(line) < 3:
        regular = False
    
    return regular

def normalize_file(self, needed_content):
        new_content = []
        for i in range(len(needed_content)):
            if self.is_regular_line(needed_content[i]):
                new_content.append(needed_content[i])
            elif not self.is_regular_line(needed_content[i]) and (needed_content[i].startswith(SPLIT_PNR_IDENTIFIER[0]) or needed_content[i].startswith(DUPLICATE_PNR_IDENTIFIER[0])) :
                new_content.append(needed_content[i])
            elif not self.is_regular_line(needed_content[i]) and len(new_content) > 0:
                # discard excluded line
                is_excluded = False
                for line in TO_BE_EXCLUDED_LINE:
                    if needed_content[i].startswith(line):
                        is_excluded = True
                        break
                if not is_excluded:
                    new_content[len(new_content) - 1] = new_content[len(new_content) - 1] + needed_content[i]
        
        upper_content, new_file_start = self.appropriated_start(new_content)
        if len(upper_content) > 0:
            temp_content = self.logic_sequence(new_file_start)
            return upper_content + temp_content
        new_content = self.logic_sequence(new_content)
        return new_content
```

### Méthode `find_line_number`(self, line)
**1. Description**

Cette méthode est utilisée pour trouver le numéro de ligne dans une ligne donnée. Le numéro de ligne est défini comme le premier élément numérique trouvé dans la ligne.

**2. Paramètres**

- `line` : la ligne de texte contenant le numéro de ligne

**3. Fonctionnement**

La méthode divise la ligne en utilisant l'espace ou le point comme délimiteur et vérifie si le premier élément est numérique. Si c'est le cas, elle renvoie ce premier élément converti en entier comme numéro de ligne. Sinon, elle renvoie 0.

**4. Résumé**

La méthode find_line_number() trouve le numéro de ligne dans une ligne donnée en recherchant le premier élément numérique et en le renvoyant comme entier.

**5. Explications**

La méthode find_line_number() prend une ligne de texte en paramètre et divise cette ligne en utilisant l'espace ou le point comme délimiteur. Elle vérifie ensuite si le premier élément de la ligne est numérique. Si c'est le cas, elle renvoie ce premier élément converti en entier comme numéro de ligne. Sinon, elle renvoie 0. Cela permet de récupérer le numéro de ligne à partir d'une ligne de texte qui contient ce numéro.

**6. Extensions possibles**

Une extension possible serait de gérer les cas où le numéro de ligne n'est pas présent dans la ligne ou est mal formaté. Cela pourrait inclure la gestion d'exceptions ou la mise en place de mécanismes de correction ou de validation du format du numéro de ligne.
Une autre extension possible serait d'ajouter des options de configuration pour spécifier le délimiteur utilisé pour diviser la ligne et rechercher le numéro de ligne. Cela permettrait de s'adapter à différents formats de fichiers ou de lignes.

**7. Codes**
```python
# find line number
def find_line_number(self, line):
    line_number = 0
    if line.split(' ')[0].isnumeric():
        line_number = line.split(' ')[0]
    elif line.split('.')[0].isnumeric():
        line_number = line.split('.')[0]
    return int(line_number)
```

### Méthode `appropriated_start(self, normalized_file)`
**1. Description**

Cette méthode est utilisée pour trouver le contenu supérieur et le nouveau point de départ d'un fichier normalisé. Le contenu supérieur est défini comme les lignes du fichier normalisé avant la première ligne commençant par "0". Le nouveau point de départ est défini comme les lignes du fichier normalisé après la première ligne commençant par "0".

**2. Paramètres**

- `normalized_file` : une liste de lignes représentant le fichier normalisé

**3. Fonctionnement**

La méthode parcourt les lignes du fichier normalisé et recherche la première ligne commençant par "0". Lorsqu'elle trouve cette ligne, elle divise le fichier normalisé en deux parties : le contenu supérieur, qui contient toutes les lignes avant la première ligne commençant par "0", et le nouveau point de départ, qui contient toutes les lignes après la première ligne commençant par "0". Elle renvoie ensuite ces deux parties sous forme de listes.

**4. Résumé**

La méthode appropriated_start() trouve le contenu supérieur et le nouveau point de départ d'un fichier normalisé en recherchant la première ligne commençant par "0" et en divisant le fichier en conséquence.

**5. Explications**

La méthode `appropriated_start()` prend une liste de lignes représentant un fichier normalisé en paramètre. Elle parcourt les lignes du fichier normalisé et recherche la première ligne commençant par "0". Lorsqu'elle trouve cette ligne, elle divise le fichier normalisé en deux parties : le contenu supérieur, qui contient toutes les lignes avant la première ligne commençant par "0", et le nouveau point de départ, qui contient toutes les lignes après la première ligne commençant par "0". Elle renvoie ensuite ces deux parties sous forme de listes. Cela permet de séparer le fichier normalisé en deux parties distinctes, en fonction du point de départ des passagers groupés.

**6. Extensions possibles**

Une extension possible serait de gérer les cas où aucune ligne ne commence par "0" dans le fichier normalisé. Cela pourrait inclure la gestion d'exceptions ou la mise en place de mécanismes de validation du format du fichier normalisé.
Une autre extension possible serait d'ajouter des options de configuration pour spécifier le caractère ou la chaîne de caractères à rechercher comme point de départ des passagers groupés. Cela permettrait de s'adapter à différents formats de fichiers ou de lignes.

**7. Codes**
```python
# start content from appropriated point when passengers are grouped
def appropriated_start(self, normalized_file):
    upper_content = []
    new_file_start = []
    for i in range(len(normalized_file)):
        current_line = normalized_file[i]
        if current_line.split('.')[0] == '0':
            upper_content = normalized_file[0:i+1]
            new_file_start = normalized_file[i+1:]
            break
    
    return upper_content, new_file_start
```

### Méthode `logic_sequence(self, normalized_file)`
**0. Exemples**
La méthode logic_sequence vérifie si la ligne suivante est la suite de la ligne du PNR ou c'est une ligne attachée au premier ligne

ex: 
1. xxxxxxxxxxx
2. xxxxxxxxxxx
7. xxxxxxxxxxx

`Problème` Ici on peut avoir des données manquants (FA PAX ou autres) qui va générer des erreurs dans la base de données.


**1. Description**

Ce code implémente une méthode appelée logic_sequence() qui vérifie si chaque ligne dans une liste de lignes de texte est la ligne suivante de la ligne précédente.

**2. Paramètres**

- `normalized_file` : une liste de lignes de texte normalisées

**3. Fonctionnement**

La méthode `logic_sequence()` parcourt chaque ligne dans la liste normalized_file et vérifie si elle est la ligne suivante de la ligne précédente. Si la ligne actuelle est la ligne suivante de la ligne précédente, elle est ajoutée à la liste sequence_wise_file. Sinon, la ligne actuelle est concaténée à la ligne précédente, la ligne actuelle est supprimée de la liste normalized_file, et la méthode logic_sequence() est appelée récursivement avec la liste normalized_file modifiée. Ce processus est répété jusqu'à ce que toutes les lignes aient été vérifiées.

**4. Résumé**

La méthode `logic_sequence()` vérifie si chaque ligne dans une liste de lignes de texte est la ligne suivante de la ligne précédente.

**5. Explications**

La méthode `logic_sequence()` prend une liste de lignes de texte normalisées en paramètre. Elle parcourt chaque ligne dans la liste normalized_file et vérifie si elle est la ligne suivante de la ligne précédente. Si la ligne actuelle est la ligne suivante de la ligne précédente, elle est ajoutée à la liste sequence_wise_file. Sinon, la ligne actuelle est concaténée à la ligne précédente en remplaçant la ligne précédente dans la liste normalized_file. Ensuite, la ligne actuelle est supprimée de la liste normalized_file en utilisant la méthode pop(). Ensuite, la méthode logic_sequence() est appelée récursivement avec la liste normalized_file modifiée. Ce processus est répété jusqu'à ce que toutes les lignes aient été vérifiées. Finalement, la méthode renvoie la liste sequence_wise_file, qui contient les lignes qui sont la ligne suivante de la ligne précédente.

**6. Extensions possibles**

- Une amélioration possible serait de permettre à l'utilisateur de spécifier le nombre maximum de lignes entre la ligne actuelle et la ligne précédente pour qu'elles soient considérées comme la ligne suivante. Actuellement, la valeur est fixée à 6.

- Une autre extension possible serait d'ajouter une vérification pour s'assurer que les numéros de ligne sont dans l'ordre croissant. Cela permettrait de détecter les erreurs ou les incohérences dans le fichier de texte.

- On pourrait également ajouter une option pour spécifier les préfixes des lignes qui doivent être ignorées lors de la vérification de la séquence. Cela permettrait d'ignorer certaines lignes spécifiques qui ne doivent pas être prises en compte dans la séquence.

**7. Codes**
```python
def logic_sequence(self, normalized_file):
    sequence_wise_file = []
    for i in range(len(normalized_file)):
        if not normalized_file[i].startswith(SPLIT_PNR_IDENTIFIER[0]) and not normalized_file[i].startswith(DUPLICATE_PNR_IDENTIFIER[0]):
            if i > 0 and i < len(normalized_file):
                previous_line = normalized_file[i-1]
                
                previous_line_number = self.find_line_number(previous_line)
                current_line_number = self.find_line_number(normalized_file[i])
                
                if current_line_number - previous_line_number < 6 and current_line_number - previous_line_number > 0:
                    sequence_wise_file.append(normalized_file[i])
                else:
                    # sequence_wise_file[-1] = sequence_wise_file[-1] + normalized_file[i]
                    normalized_file[i - 1] = normalized_file[i - 1] + normalized_file[i]
                    
                    normalized_file.pop(i)
                    sequence_wise_file = normalized_file
                    self.logic_sequence(normalized_file)
                    break
            else:
                sequence_wise_file.append(normalized_file[i])
        else:
            sequence_wise_file.append(normalized_file[i])
    
    return sequence_wise_file
```

### Méthode `get_pnr_data(self, file_content, email_date)`
**1. Description**

Ce code implémente une méthode appelée get_pnr_data() qui récupère les données de base d'un PNR à partir d'un contenu de fichier et d'une date d'e-mail.

**2. Paramètres**

- `file_content` : le contenu du fichier
- `email_date` : la date de l'e-mail

**3. Fonctionnement**

La méthode get_pnr_data() parcourt le contenu du fichier et récupère les données de base du PNR. Elle crée une instance de la classe Pnr et initialise certaines de ses propriétés en fonction des informations extraites du contenu du fichier. Elle recherche la ligne qui commence par la valeur de PNR_IDENTIFIER[0] et extrait les informations nécessaires à partir de cette ligne. Elle récupère le numéro de PNR, l'agent responsable du PNR, la date de création du PNR, et d'autres informations. Si le PNR existe déjà dans la base de données, les informations sont mises à jour. Sinon, un nouvel objet Pnr est créé avec les informations extraites.

**4. Résumé**

La méthode get_pnr_data() récupère les données de base d'un PNR à partir d'un contenu de fichier et d'une date d'e-mail.

**5. Explications**

La méthode get_pnr_data() prend le contenu du fichier et la date de l'e-mail en paramètres. Elle parcourt le contenu du fichier et recherche la ligne qui commence par la valeur de PNR_IDENTIFIER[0]. Cette ligne contient les informations de base du PNR, telles que le numéro de PNR, l'agent responsable, la date de création, etc. Les informations sont extraites de cette ligne et utilisées pour initialiser les propriétés de l'objet Pnr. Si le PNR existe déjà dans la base de données, les informations sont mises à jour. Sinon, un nouvel objet Pnr est créé avec les informations extraites. Finalement, la méthode renvoie l'objet Pnr, un indicateur de sauvegarde et l'agent responsable actuel du PNR.

**6. Extensions possibles**

- Une amélioration possible serait d'ajouter une gestion des erreurs plus robuste, avec des messages d'erreur plus explicites pour les problèmes rencontrés lors de l'extraction des informations du fichier.

- On pourrait également ajouter une vérification pour s'assurer que les informations extraites sont valides et cohérentes avant de les utiliser pour initialiser les propriétés de l'objet Pnr.

- Une autre extension possible serait de permettre à l'utilisateur de spécifier le préfixe utilisé pour identifier la ligne contenant les informations du PNR, au lieu d'utiliser une valeur fixe comme PNR_IDENTIFIER[0]. Cela permettrait de rendre le code plus flexible et réutilisable dans d'autres contextes.

**7. Codes**
```python
# get basic data from pnr
def get_pnr_data(self, file_content, email_date):
    pnr = Pnr()
    is_saved = False
    current_pnr_emitter = None
    
    pnrDetailRow = ''
    for i in range(len(file_content)):
        if(file_content[i].startswith(PNR_IDENTIFIER[0])):
            pnrDetailRow = file_content[i]
            break
        
    # new method
    header_with_no_space = []
    for detail_row in pnrDetailRow.split(' '):
        if detail_row != '':
            header_with_no_space.append(detail_row)
    
    user_gds_id = None
    pnr.number = header_with_no_space[-1]
    try:
        copying_agent = pnr.get_pnr_creator_user_copying()
        if copying_agent is not None:
            pnr.agent = copying_agent
        elif copying_agent is None:
            user_gds_id = header_with_no_space[len(header_with_no_space) - 3].split('/')[0]
            user_agent = User.objects.filter(gds_id=user_gds_id).first()
            if user_agent is not None:
                pnr.agent = user_agent  
            else:
                raise Exception('No agent found')
    except:
        pnr.agent_code = user_gds_id
    
    creation_date = datetime.strptime(header_with_no_space[-2].split('/')[0].strip(), '%d%b%y').date()
    # system_creation_date = datetime.now()
    
    temp_pnr = Pnr.objects.filter(number=pnr.number).first()
    if temp_pnr is not None:
        # if temp_pnr.state == 1:
        #    is_saved = False
        #else:
        #    is_saved = True
        is_saved = True
        temp_pnr.gds_creation_date = creation_date
        # temp_pnr.system_creation_date = datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
        temp_pnr.system_creation_date = email_date
        # temp_pnr.state = 0
        if Office.objects.filter(code=pnrDetailRow.split('/')[1]).first() is None:
            Office.objects.create(code=pnrDetailRow.split('/')[1])
        temp_pnr.agency = Office.objects.get(code=pnrDetailRow.split('/')[1])
        
        copying_agent = pnr.get_pnr_creator_user_copying()
        if copying_agent is not None:
            temp_pnr.agent = copying_agent
        elif copying_agent is None:
            user_gds_id = header_with_no_space[len(header_with_no_space) - 3].split('/')[0]
            user_agent = User.objects.filter(gds_id=user_gds_id).first()
            if user_agent is not None:
                temp_pnr.agent = user_agent  
            else:
                temp_pnr.agent_code = user_gds_id 
        temp_pnr.is_read = False
        
        # current pnr emitter
        try:
            current_pnr_emitter = User.objects.filter(gds_id=header_with_no_space[len(header_with_no_space) - 3].split('/')[0]).first()
        except:
            print("Current PNR has no emitter found")
        
        return temp_pnr, is_saved, current_pnr_emitter
    
    pnr.gds_creation_date = creation_date
    # pnr.system_creation_date = datetime(system_creation_date.year, system_creation_date.month, system_creation_date.day, system_creation_date.hour, system_creation_date.minute, system_creation_date.second, system_creation_date.microsecond, pytz.UTC)
    pnr.system_creation_date = email_date
    pnr.type = PNR_TYPE[0]
    if Office.objects.filter(code=pnrDetailRow.split('/')[1]).first() is None:
        Office.objects.create(code=pnrDetailRow.split('/')[1])
    pnr.agency = Office.objects.get(code=pnrDetailRow.split('/')[1])
    pnr.is_read = False
    if pnr.agent is not None:
        current_pnr_emitter = pnr.agent
    return pnr, False, current_pnr_emitter
```

### Méthode `get_split_duplicated_status(self, pnr, normalized_file)`
**1. Description**

Ce code implémente une méthode appelée get_split_duplicated_status() qui vérifie si un PNR est dupliqué ou divisé en plusieurs parties.

**2. Paramètres**

- `pnr` :  l'objet Pnr sur lequel la vérification est effectuée
- `normalized_file` : le fichier normalisé contenant les informations sur les PNR

**3. Fonctionnement**

La méthode get_split_duplicated_status() parcourt le fichier normalisé et recherche les lignes qui commencent par les valeurs de SPLIT_PNR_IDENTIFIER[0] et DUPLICATE_PNR_IDENTIFIER[0]. Ces lignes contiennent des informations sur les PNR qui sont divisés ou dupliqués. Les lignes correspondantes sont extraites et les numéros de PNR associés sont enregistrés dans des listes appropriées.

Si des lignes de division sont trouvées, cela signifie que le PNR est divisé en plusieurs parties. Dans ce cas, la propriété is_splitted de l'objet pnr est mise à True et les numéros de PNR des parties enfants sont enregistrés dans la liste children_pnr.

Si des lignes de duplication sont trouvées, cela signifie que le PNR est dupliqué. Dans ce cas, la propriété is_duplicated de l'objet pnr est mise à True et les numéros de PNR des parties parentes sont enregistrés dans la liste parent_pnr.

**4. Résumé**

La méthode get_split_duplicated_status() vérifie si un PNR est dupliqué ou divisé en plusieurs parties.

**5. Explications**

La méthode get_split_duplicated_status() prend l'objet pnr et le fichier normalisé en paramètres. Elle parcourt le fichier normalisé et recherche les lignes qui indiquent si le PNR est divisé ou dupliqué. Si des lignes de division sont trouvées, cela signifie que le PNR est divisé en plusieurs parties et les numéros de PNR des parties enfants sont enregistrés. Si des lignes de duplication sont trouvées, cela signifie que le PNR est dupliqué et les numéros de PNR des parties parentes sont enregistrés. Finalement, les propriétés is_splitted, is_duplicated, children_pnr et parent_pnr de l'objet pnr sont mises à jour en conséquence.

**6. Extensions possibles**

- Une amélioration possible serait d'ajouter une gestion des erreurs plus robuste, avec des messages d'erreur plus explicites pour les problèmes rencontrés lors de la recherche des lignes de division ou de duplication.

- On pourrait également ajouter une vérification pour s'assurer que les numéros de PNR extraits sont valides et cohérents avant de les enregistrer dans les listes children_pnr et parent_pnr.
  
- Une autre extension possible serait de permettre à l'utilisateur de spécifier les préfixes utilisés pour identifier les lignes de division et de duplication, au lieu d'utiliser des valeurs fixes comme SPLIT_PNR_IDENTIFIER[0] et DUPLICATE_PNR_IDENTIFIER[0]. Cela permettrait de rendre le code plus flexible et réutilisable dans d'autres contextes.

**7. Codes**
```python
# check if pnr is duplicated or splitted
def get_split_duplicated_status(self, pnr, normalized_file):
    split_lines = []
    children_pnr = []
    duplicate_lines = []
    parent_pnr = []
    
    for line in normalized_file:
        if line.startswith(SPLIT_PNR_IDENTIFIER[0]):
            split_lines.append(line)
        elif line.startswith(DUPLICATE_PNR_IDENTIFIER[0]):
            duplicate_lines.append(line)
    
    if len(split_lines) > 0:
        pnr.is_parent = True
        pnr.is_splitted = True
        for temp_split_line in split_lines:
            if len(temp_split_line.split('-')) > 1:
                children_pnr.append(temp_split_line.split('-')[1])
        pnr.children_pnr = children_pnr
    
    if len(duplicate_lines) > 0:
        pnr.is_parent = True
        pnr.is_duplicated = True
        for temp_duplicate_line in duplicate_lines:
            if len(temp_duplicate_line.split('-')) > 1:
                parent_pnr.append(temp_duplicate_line.split('-')[1])
        pnr.parent_pnr = parent_pnr
```

### Méthode `save_raw_data(self, contents, pnr, ticket)`
**1. Description**

Ce code implémente une méthode appelée save_raw_data() qui enregistre les données brutes dans la base de données.

**2. Paramètres**

- `contents` : une liste de chaînes de caractères représentant le contenu des données brutes
- `pnr` : l'objet Pnr associé aux données brutes
- `ticket` : l'objet Ticket associé aux données brutes

**3. Fonctionnement**

La méthode save_raw_data() parcourt la liste contents et concatène toutes les chaînes de caractères pour former un seul texte brut. Ensuite, elle crée une instance de la classe RawData et initialise ses propriétés. La propriété data_text est définie sur le texte brut concaténé, la propriété pnr est définie sur l'objet Pnr passé en paramètre, et la propriété ticket est définie sur l'objet Ticket passé en paramètre. La propriété data_datetime est définie sur la date et l'heure actuelles. Finalement, l'objet RawData est enregistré dans la base de données.

**4. Résumé**

La méthode save_raw_data() enregistre les données brutes dans la base de données.

**5. Explications**

La méthode save_raw_data() prend la liste contents, l'objet pnr et l'objet ticket en paramètres. Elle concatène toutes les chaînes de caractères de la liste contents pour former un seul texte brut. Ensuite, elle crée une instance de la classe RawData et initialise ses propriétés avec les valeurs appropriées. Finalement, l'objet RawData est enregistré dans la base de données.

**6. Extensions possibles**

- Une amélioration possible serait d'ajouter une gestion des erreurs plus robuste lors de l'enregistrement des données brutes dans la base de données, avec des messages d'erreur plus explicites en cas d'échec.

- On pourrait également ajouter des vérifications pour s'assurer que les objets pnr et ticket passés en paramètres sont valides avant de les utiliser pour initialiser les propriétés de l'objet RawData.

- Une autre extension possible serait de permettre à l'utilisateur de spécifier la date et l'heure à utiliser pour la propriété data_datetime, au lieu d'utiliser la date et l'heure actuelles. Cela permettrait de rendre le code plus flexible et réutilisable dans d'autres contextes.

**7. Codes**
```python
# save raw data
def save_raw_data(self, contents, pnr, ticket):
    raw_data_obj = RawData()
    all_raw_text = ''
    for content in contents:
        all_raw_text += content + '\n'
    
    raw_data_obj.data_text = all_raw_text
    raw_data_obj.pnr = pnr
    raw_data_obj.ticket = ticket
    current_datetime = datetime.now()
    raw_data_obj.data_datetime = datetime(current_datetime.year, current_datetime.month, current_datetime.day, current_datetime.hour, current_datetime.minute, current_datetime.second, current_datetime.microsecond, pytz.UTC)
    raw_data_obj.save()
```



### Méthode `get_passengers(self, pnr_content)`
**1. Description**

La fonction get_passengers() retourne une liste de Passenger objects, un pour chaque passager dans le PNR.

**2. Paramètres**

- `pnr_content` : une liste de chaînes de caractères représentant le contenu du PNR

**3. Fonctionnement**

La fonction parcourt la liste pnr_content et recherche toutes les lignes qui contiennent des informations sur les passagers. Une fois qu'elle a trouvé une ligne contenant des informations sur un passager, la fonction extrait les informations suivantes :

- Nom
- Prénom
- Date de naissance (si disponible)
- Désignation (ADULT, CHILD, INFANT, etc.)
- Type de passager (ADT, YTH, CNN, INF)
- 
La fonction utilise ces informations pour créer un objet Passenger et l'ajoute à la liste des passagers.

**4. Résumé**

La fonction get_passengers() est utile pour extraire les informations sur les passagers d'un PNR.

**5. Explications**

La fonction utilise un certain nombre d'heuristiques pour extraire les informations sur les passagers d'un PNR :

- Si la ligne contient une parenthèse, la fonction suppose que la partie de la ligne avant la parenthèse contient le nom et le prénom du passager, et que la partie de la ligne après la parenthèse contient la désignation et la date de naissance du passager.

- Si la ligne ne contient pas de parenthèse, la fonction suppose que la ligne contient le nom et le prénom du passager, et que la désignation du passager est la dernière chaîne de caractères de la ligne.

- Si la ligne contient le mot "INF", la fonction suppose que la ligne contient des informations sur un passager et un bébé. Dans ce cas, la fonction crée deux objets Passenger, un pour le passager et un pour le bébé.

**6. Extensions possibles**

La fonction pourrait être améliorée en ajoutant la possibilité de spécifier un format spécifique pour le PNR. Cela permettrait à la fonction d'extraire les informations sur les passagers de manière plus précise.

**7. Exemples**
```python
>>> pnr_content = ["1.BATROLO/MATHIS KYLIAN MR(CHD/02APR12)", "2.BARRAUD/SALMA(CHD/25AUG17)   3.MOINDANDZE/BARAKA MS", "4.MKOUBOI/FATIMA MRS(INFABDOU/NOLAN/24APR21)"]
>>> passengers = get_passengers(pnr_content)
>>> passengers[0].name
'MATHIS KYLIAN'
>>> passengers[0].surname
'BATROLO'
>>> passengers[0].designation
'CHD'
>>> passengers[0].types
'CHD'
>>> passengers[1].name
'SALMA'
>>> passengers[1].surname
'BARRAUD'
>>> passengers[1].designation
'CHD'
>>> passengers[1].types
'CHD'
>>> passengers[2].name
'FATIMA'
>>> passengers[2].surname
'MKOUBOI'
>>> passengers[2].designation
'INF'
>>> passengers[2].types
'INF_ASSOC'
>>> passengers[3].name
'ABDOU NOLAN'
>>> passengers[3].surname
''
>>> passengers[3].designation
'INF'
>>> passengers[3].types
'INF'
```

**8. Codes**
```python
def get_passengers(self, pnr_content):
    passenger_line = []
    order_line = []
    passengers = []
    # fetch all lines containing passengers
    for i in range(len(pnr_content)):
        temp_content_space_split = pnr_content[i].split("  ")
        temp_content_dot_split = pnr_content[i].split(".")
        # if all passengers are on the same line
        if(len(temp_content_space_split) > 1 and temp_content_dot_split[0].isnumeric() and temp_content_dot_split[0] != '0'):
            for temp in temp_content_space_split:
                passenger_line.append(temp.split(".")[1])
                order_line.append(temp.split(".")[0].strip())
        # if passengers are on different lines
        else:
            if(temp_content_dot_split[0].isnumeric() and temp_content_dot_split[0] != '0'):
                passenger_line.append(temp_content_dot_split[1])
                order_line.append(temp_content_dot_split[0].strip())
    
    order = 0
    for line in passenger_line:
        all_designation = PASSENGER_DESIGNATIONS
        temp_passenger = Passenger()
        line_split = line.split('(')
        line_space_split = line.split(' ')
        '''
        # possible type
        1.BATROLO/MATHIS KYLIAN MR(CHD/02APR12)
        1.BARRAUD/SALMA(CHD/25AUG17)   2.MOINDANDZE/BARAKA MS
        1.MKOUBOI/FATIMA MRS(INFABDOU/NOLAN/24APR21)
        1.JEANMAIRE/PHILIPPE MR(ADT)
        1.CHAQUIR/EMILIE MS(ADT)(INFMAOULIDA/HAYDEN/10MAR22)
        '''
        # if the passenger is a child
        if len(line_split) > 1 and (line.find('CHD') > 0 or line.find('YTH') > 0 or line.find('CNN') > 0):
            name_part = line_split[0]
            designation_part = line_split[1]
            
            temp_passenger.name = name_part.split("/")[0].strip()
            if len(name_part.split('/')) > 1:
                # if the passenger is a child but has MR, M., ...
                if name_part.split(' ')[-1] in all_designation:
                    temp_passenger.surname = name_part.split("/")[1].removesuffix(name_part.split(' ')[-1]).strip()
                    temp_passenger.designation = name_part.split(' ')[-1]
                # if the passenger is only a child
                elif name_part.split(' ')[-1] not in all_designation:
                    temp_passenger.surname = name_part.split("/")[1].strip()
                    if line.find('CHD') > 0:
                        temp_passenger.designation = 'CHD'
                    elif line.find('YTH') > 0:
                        temp_passenger.designation = 'YTH'
                        temp_passenger.types = 'YTH'
                    elif line.find('CNN') > 0:
                        temp_passenger.designation = 'CNN'
                        temp_passenger.types = 'CNN'
            try:
                temp_passenger.birthdate = datetime.strptime(designation_part.split("/")[1].split(")")[0], '%d%b%y')
            except:
                pass
                
        # if the passenger is not a child
        # if the passenger has ADT or YCD marked and not associated with an infant
        if len(line_split) > 1 and (line.find('ADT') > 0 or line.find('YCD') > 0 or line.find('STU') > 0) and line.find('INF') == -1:
            name_part = line_split[0]
            
            temp_passenger.name = name_part.split("/")[0]
            if len(name_part.split('/')) > 1:
                if name_part.split(' ')[-1] in all_designation:
                    temp_passenger.surname = name_part.split("/")[1].removesuffix(name_part.split(' ')[-1]).strip()
                    temp_passenger.designation = name_part.split(' ')[-1]
                else:
                    temp_passenger.surname = name_part.split("/")[1].strip()
            temp_passenger.types = 'ADT'
        # if the passenger is a simple passenger
        else:
            # if the passenger is not associated with an infant
            if line_space_split[-1] in all_designation or (line_space_split[-1] not in all_designation and len(line_split) == 1):
                name_part = []
                for temp_space_split in line_space_split:
                    if temp_space_split not in all_designation:
                        name_part.append(temp_space_split)
                temp_passenger.name = name_part[0].split('/')[0].strip()
                surname = ''
                if len(name_part[0].split('/')) > 1:
                    surname += name_part[0].split('/')[1]
                for i in range(1, len(name_part)):
                    surname += ' ' + name_part[i]
                temp_passenger.surname = surname.strip()
                if line_space_split[-1] in all_designation:
                    temp_passenger.designation = line_space_split[-1]
            # if the passenger is associated with an infant
            if len(line_split) > 1 and line.find('INF') > 0:
                temp_passenger_inf = Passenger()
                name_part = line_split[0]
                temp_passenger.name = name_part.split('/')[0].strip()
                
                if len(name_part.split('/')) > 1:
                    if name_part.split(' ')[-1] in all_designation:
                        temp_passenger.surname = name_part.split('/')[1].removesuffix(name_part.split(' ')[-1]).strip()
                        temp_passenger.designation = name_part.split(' ')[-1]
                    else:
                        temp_passenger.surname = name_part.split('/')[1].strip()
                
                # Not having adult or youth flag
                # 1.MKOUBOI/FATIMA MRS(INFABDOU/NOLAN/24APR21)
                if line.find('ADT') == -1 and line.find('YTH') == -1:
                    inf_part = line_split[1]
                # Has adult or youth flag
                # 1.CHAQUIR/EMILIE MS(ADT)(INFMAOULIDA/HAYDEN/10MAR22)
                else:
                    inf_part = line_split[2]
                
                inf_part_split = inf_part.split('/')
                temp_passenger_inf.name = inf_part_split[0].removeprefix('INF').strip()
                if len(inf_part_split) > 1:
                    temp_passenger_inf.surname = inf_part_split[1].strip().removesuffix(')')
                if len(inf_part_split) > 2:
                    try:
                        temp_passenger_inf.birthdate = datetime.strptime(inf_part_split[2].split(")")[0], '%d%b%y')
                    except:
                        pass
                temp_passenger_inf.designation = 'INF'
                temp_passenger_inf.types = 'INF_ASSOC'
                temp_passenger_inf.order = 'P' + str(order_line[order])
                passengers.append(temp_passenger_inf)
                            
        temp_passenger.order = 'P' + str(order_line[order])
        passengers.append(temp_passenger)
        order += 1
    
    return passengers
```

### Méthode `get_flight(self, pnr_content, pnr)`
Ce code extrait des informations sur les vols et les segments de services d'une chaîne de caractères au format PNR (Passenger Name Record). Un PNR est un enregistrement dans un système de réservation de compagnies aériennes qui contient des informations sur un voyageur, ses vols et d'autres services associés à son voyage.

**1. Description**

Ce code analyse le contenu d'un PNR pour extraire des détails sur les vols et les segments de services associés. Il identifie les informations clés telles que les numéros de vol, les compagnies aériennes, les aéroports de départ et d'arrivée, les heures de départ et d'arrivée, ainsi que d'autres informations pertinentes.

**2. Paramètres**

- `pnr_content` : La chaîne de caractères contenant les informations du PNR.
- `pnr` : L'objet PNR auquel les informations extraites sont associées.

**3. Fonctionnement**

Le code fonctionne en parcourant les lignes du PNR et en identifiant les segments de vol et les segments de service. Il extrait les détails pertinents de chaque segment, tels que la compagnie aérienne, le numéro de vol, la classe, les aéroports de départ et d'arrivée, les heures de départ et d'arrivée, etc. Les segments de vol sont ensuite enregistrés sous forme d'objets PnrAirSegments, tandis que les segments de service sont également identifiés.

**4. Résumé**
Ce code extrait des informations sur les vols et les segments de service à partir d'un PNR. Il identifie les détails clés de chaque segment et les stocke dans des objets PnrAirSegments. Ces objets peuvent ensuite être utilisés pour afficher ou gérer les détails du voyage associé au PNR.

**5. Explications**
Le code commence par extraire l'année et le mois de création du PNR à partir de l'objet PNR.

Il identifie les lignes du PNR qui correspondent à des segments de vol en recherchant les numéros de ligne suivis d'une compagnie aérienne. Ces lignes sont stockées dans la liste all_flight_lines.

Les numéros de ligne de ces segments de vol sont également stockés dans la liste all_flight_order.

Le code parcourt ensuite les lignes des segments de vol et identifie les détails tels que la compagnie aérienne, le numéro de vol, la classe, les aéroports de départ et d'arrivée, les heures de départ et d'arrivée, etc.

Il traite également les cas où la compagnie aérienne et le numéro de vol sont séparés par un espace ou non.

Les segments de vol sont enregistrés sous forme d'objets PnrAirSegments avec les détails extraits.

Les segments de service sont également identifiés et stockés, en indiquant qu'il s'agit de segments de type "SVC".

Les segments "OPEN" sont également gérés et associés au PNR.

Les objets PnrAirSegments résultants sont ajoutés à la liste flights et retournés.

**6. Extensions possibles**
Ce code peut être étendu pour prendre en charge d'autres formats de PNR ou pour extraire davantage d'informations spécifiques aux compagnies aériennes ou aux systèmes de réservation. Il peut également être utilisé pour alimenter une base de données de vols et de segments de services à des fins de suivi et de gestion des voyages.

**7. Codes**
```python
def get_flight(self, pnr_content, pnr):
    # Cette fonction extrait les informations sur les vols à partir du contenu du PNR.

    # Paramètres :
    # - self: L'instance de la classe qui appelle la fonction.
    # - pnr_content: Le contenu brut du PNR à analyser.
    # - pnr: L'objet PNR auquel les informations de vol seront associées.

    # Extraction de l'année d'opération à partir de la date de création du PNR.
    yearOfOperation = pnr.gds_creation_date.year
    month_of_operation = pnr.gds_creation_date.month

    # Initialisation de listes pour stocker les lignes de vol, l'ordre des vols, et les objets de vol.
    all_flight_lines = []
    all_flight_order = []
    flights = []
    flight_class = None
    is_open_status = False

    # Parcours du contenu du PNR pour extraire les lignes de vol.
    for line in pnr_content:
        # Vérification si la ligne commence par un numéro suivi d'un espace.
        if (len(line.split(" ")) > 1 and line.split(" ")[0].isnumeric() == True):
            if (line.split(" ")[1] == '' or line.split(" ")[1].endswith('SVC')):
                # Ajout des lignes de vol et de l'ordre dans les listes correspondantes.
                all_flight_lines.append(line)
                all_flight_order.append(line.split(" ")[0])

    # Initialisation de variables pour suivre l'index des segments.
    segment = 0

    # Parcours des lignes de vol pour extraire les informations.
    for flight in all_flight_lines:
        flight_info = flight.split(" ")
        temp_flight = PnrAirSegments()

        # Segment de vol standard (non SVC).
        if not flight_info[1].endswith('SVC') and not flight_info[1].endswith('OPEN') and not flight_info[2].endswith('OPEN'):
            flown_checker = False

            # Vérification si le code de la compagnie aérienne et le numéro de vol sont séparés par un espace.
            if (len(flight.split(" ")[2]) <= 2):
                airline_code = flight_info[2]
                # ... (voir commentaires détaillés ci-dessous)

            # Vérification si le code de la compagnie aérienne et le numéro de vol ne sont pas séparés par un espace.
            elif (len(flight.split(" ")[2]) > 2):
                airline_code = flight_info[2][0:2]
                # ... (voir commentaires détaillés ci-dessous)

        # Segment de service SVC.
        elif flight_info[1].endswith('SVC'):
            # ... (voir commentaires détaillés ci-dessous)

        # Segment ouvert (OPEN).
        elif flight_info[1].endswith('OPEN') or flight_info[2].endswith('OPEN'):
            is_open_status = True
            # ... (voir commentaires détaillés ci-dessous)

        # Ajout de l'objet de vol à la liste des vols.
        flights.append(temp_flight)
        segment += 1

    # Retourne la liste des vols extraits et la classe de vol.
    return flights, flight_class
```

### Méthode `get_all_ssr(self, normalized_file, pnr, passengers, segments)` 23102023 13:47
**1. Description**

La fonction `get_all_ssr` analyse un fichier de données normalisées liées à un Passenger Name Record (PNR), extrait les Special Service Requests (SSR) et crée des objets correspondants en base de données. Pour chaque SSR détecté, elle identifie son code, extrait le texte libre associé, et associe le SSR aux passagers et aux segments de vol concernés.

**2. Paramètres**

- `normalized_file` : Le fichier normalisé contenant les données SSR.
- `pnr` : L'objet Passenger Name Record (PNR) auquel les SSR sont associés.
- `passengers` : La liste des passagers associés au PNR.
- `segments` : La liste des segments de vol associés au PNR.

**3. Fonctionnement**

La fonction parcourt le fichier normalisé ligne par ligne, cherchant les lignes correspondant à des SSR en se basant sur leur structure. Pour chaque SSR trouvé, elle extrait le code du SSR et le texte libre associé. Elle identifie également les passagers et les segments liés au SSR en se basant sur des références dans le texte du SSR.

Les objets SSR sont ensuite créés en base de données pour chaque SSR détecté. Pour chaque SSR, des objets spécifiques pour les passagers et les segments associés sont également créés. L'ensemble des objets est stocké dans des listes et renvoyé en sortie de la fonction.

**4. Résumé**

La fonction `get_all_ssr` permet d'extraire, de stocker en base de données et d'associer des Special Service Requests (SSR) à un Passenger Name Record (PNR), ainsi qu'à ses passagers et segments de vol correspondants.

**5. Explications**

La fonction fonctionne en analysant le fichier normalisé à la recherche de lignes SSR. Elle extrait ces lignes en se basant sur une structure prédéfinie, puis identifie les informations importantes telles que le code du SSR et le texte libre associé. Pour chaque SSR, elle détermine les passagers et les segments liés en analysant le texte du SSR. Les objets SSR sont ensuite créés en base de données et associés aux passagers et aux segments concernés. Cette approche permet de conserver une trace des demandes de services spéciaux et de les associer de manière appropriée dans le contexte du PNR.

**6. Extensions possibles**

La fonction pourrait être étendue pour gérer d'autres types de données du fichier normalisé ou pour mettre à jour les SSR existants en cas de modifications ultérieures du fichier. Des améliorations supplémentaires pourraient inclure la validation des données SSR extraites et la mise en place de fonctionnalités de recherche pour accéder plus facilement aux SSR enregistrés.

**7. Codes**
```python
# Fonction pour extraire tous les Special Service Requests (SSR)
def get_all_ssr(self, normalized_file, pnr, passengers, segments):
    '''
    --- Exemple du format du fichier ---
    RP/DZAUU0006/DZAUU0006            MS/SU  23OCT23/0817Z   OGIUWH
    1.TRAORE/MOUCTAR MR
    2  UU 972 Q 28OCT 6 CDGRUN HK1  2145 2B 2245 1145+1 *1A/E*
    3  UU 276 Y 29OCT 7 RUNDZA HK1  1450    1550 1700   *1A/E*
    ... (autres lignes)

    ET : Billet électronique
    DT : ??? (à définir)
    SSR : Special Services Request (SSR)
    SSR Description (t_ssr_description) : utilisé pour afficher les détails SSR dans les autres informations
    URL : https://servicehub.amadeus.com/c/portal/view-solution/768896/special-services-request-ssr-codes-and-airline-specific-codes
    '''

    ssr_lines = []       # Liste pour stocker les lignes SSR
    ssr_bases = []       # Liste pour stocker les objets SSR de base
    ssr_passengers = []  # Liste pour stocker les passagers associés aux SSR
    ssr_segments = []    # Liste pour stocker les segments de vol associés aux SSR

    # Parcours du fichier normalisé
    for line in normalized_file:
        temp = line.split(" ")  # Divise la ligne en mots
        # Vérifie si la ligne a plus de 2 mots et commence par un numéro
        if len(temp) > 2 and temp[0].isnumeric():
            # Vérifie si la ligne se termine par 'SSR'
            if temp[1].endswith('SSR'):
                ssr_lines.append(line)  # Ajoute la ligne SSR à la liste

    # Parcours des lignes SSR détectées
    for ssr in ssr_lines:
        ssr_base = SpecialServiceRequestBase()  # Crée un objet de base SSR

        info_part = ssr.split(' ')[2:]  # Sépare la partie informative du SSR
        ssr_obj = SpecialServiceRequest.objects.filter(code=info_part[0]).first()

        # Si le code SSR n'existe pas déjà dans la base de données, le crée
        if ssr_obj is None:
            temp_ssr_obj = SpecialServiceRequest()
            temp_ssr_obj.code = info_part[0]
            temp_ssr_obj.save()
            ssr_obj = temp_ssr_obj

        ssr_text = ' '.join(info_part)  # Texte libre du SSR

        related_passengers = []  # Liste des passagers liés au SSR
        related_segments = []    # Liste des segments de vol liés au SSR
        no_passenger_assigned = True

        # Analyse des parties du SSR
        for part in info_part[1:]:
            comma_split = part.split(',')  # Divise les parties par des virgules
            for temp in comma_split:
                slash_split = temp.split('/')  # Divise les parties par des barres obliques
                for slash_part in slash_split:
                    if len(slash_part) > 1 and len(slash_part) < 4:
                        # Vérifie si la partie commence par 'P' ou 'S' suivi d'un numéro
                        if (slash_part[0] == 'P' or slash_part[0] == 'S') and slash_part[1].isnumeric():
                            if len(slash_part.split('-')) > 1:
                                # Si une partie contient un intervalle de segments (par ex. S2-5)
                                temp_sliced_part = slash_part.split('-')
                                start_segment = int(temp_sliced_part[0][1:])
                                end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1])

                                a = start_segment
                                while a <= end_segment:
                                    if slash_part[0] == 'P':
                                        for passenger in passengers:
                                            if passenger.order == 'P' + str(a):
                                                related_passengers.append(passenger)
                                    elif slash_part[0] == 'S':
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(a):
                                                related_segments.append(segment)
                                    a += 1
                            else:
                                if slash_part[0] == 'P':
                                    no_passenger_assigned = False
                                    for passenger in passengers:
                                        if passenger.order == 'P' + slash_part[1]:
                                            related_passengers.append(passenger)
                                elif slash_part[0] == 'S':
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + slash_part[1]:
                                            related_segments.append(segment)

        if len(passengers) == 1 and no_passenger_assigned:
            related_passengers.append(passengers[0])

        # Assignation des objets au SSR de base
        ssr_base.ssr = ssr_obj
        ssr_base.pnr = pnr
        ssr_base.ssr_text = ssr_text
        ssr_base.order_line = 'E' + ssr.split(' ')[0]
        ssr_bases.append(ssr_base)

        # Création des objets SSR pour les passagers
        for temp_passenger in related_passengers:
            temp_ssr_passenger = SpecialServiceRequestPassenger()
            temp_ssr_passenger.parent_ssr = ssr_base
            temp_ssr_passenger.passenger = temp_passenger
            ssr_passengers.append(temp_ssr_passenger)

        # Création des objets SSR pour les segments
        for temp_segment in related_segments:
            temp_ssr_segment = SpecialServiceRequestSegment()
            temp_ssr_segment.parent_ssr = ssr_base
            temp_ssr_segment.segment = temp_segment
            ssr_segments.append(temp_ssr_segment)

    return ssr_bases, ssr_passengers, ssr_segments
```

### Méthode `get_contacts(self, pnr_content)` 23102023 14:07
**1. Description**
Cette fonction permet de récupérer tous les contacts d'un enregistrement de passager (PNR) en analysant le contenu du PNR fourni.

**2. Paramètres**
- `pnr_content` (list): Une liste de lignes représentant le contenu du PNR.

**3. Fonctionnement**
La fonction parcourt le contenu du PNR pour identifier et extraire les lignes contenant des informations de contact, telles que les numéros de téléphone, les adresses e-mail ou les contacts de notification. Elle crée ensuite des objets "Contact" pour stocker ces informations.

**4. Résumé**
La fonction renvoie une liste d'objets "Contact" contenant les détails de chaque contact trouvé dans le PNR.

**5. Explications**
- La fonction commence par initialiser une liste vide appelée "contacts" pour stocker les contacts extraits.
- Elle identifie les lignes pertinentes en recherchant des mots-clés tels que "AP" (pour les numéros de téléphone), "APE" (pour les adresses e-mail) et "APN" (pour les contacts de notification).
- Pour chaque ligne de contact identifiée, la fonction crée un objet "Contact", attribue le type de contact (téléphone, e-mail ou contact de notification) et stocke la valeur du contact.
- Les objets "Contact" ainsi créés sont ajoutés à la liste "contacts".
- En fin de compte, la fonction renvoie la liste complète des contacts extraits.

**6. Extensions possibles**
Cette fonction peut être étendue pour prendre en charge d'autres types de contacts ou pour extraire davantage d'informations pertinentes à partir du contenu du PNR en fonction des besoins spécifiques de l'application. Des améliorations telles que la détection de doublons ou la validation des adresses e-mail peuvent également être ajoutées pour une fonctionnalité plus avancée.

**7. Codes**
```python
# Récupérer tous les contacts d'un PNR
def get_contacts(self, pnr_content):
    # Initialiser une liste vide pour stocker les contacts extraits
    contacts = []

    # Définir les types de contacts à rechercher dans le contenu du PNR
    all_contact_lines = []
    all_contact_types = ['AP', 'APE', 'APE']
    all_types = {"AP": "Téléphone", "APE": "E-mail", "APN": "Contact de notification"}

    # Parcourir le contenu du PNR
    for content in pnr_content:
        # Vérifier si la ligne contient des informations de contact pertinentes
        if len(content.split(" ")) > 1 and content.split(" ")[0].isnumeric() == True:
            # Identifier les lignes avec des types de contact (par exemple, "AP," "APE")
            if content.split(" ")[1] in all_contact_types:
                all_contact_lines.append(content)

    # Traiter chaque ligne de contact et créer des objets "Contact"
    for line in all_contact_lines:
        # Créer un nouvel objet "Contact"
        temp_contact = Contact()

        # Diviser la ligne en composants
        data_line = line.split(" ")

        # Définir le type de contact (par exemple, "AP" -> "Téléphone") dans l'objet "Contact"
        temp_contact.contacttype = all_types[data_line[1]]

        # Initialiser une chaîne vide pour stocker la valeur du contact
        contact_value = ''

        # Concaténer les composants en la valeur du contact
        for value in data_line[2:]:
            contact_value += ' ' + value

        # Définir la valeur du contact dans l'objet "Contact"
        temp_contact.value = contact_value

        # Définir le propriétaire (actuellement vide) dans l'objet "Contact"
        temp_contact.owner = ''

        # Ajouter l'objet "Contact" à la liste des contacts
        contacts.append(temp_contact)

    # Retourner la liste des contacts extraits
    return contacts
```

### Méthode `get_confirmation_deadline(self, normalized_file, pnr, segments, ssrs)` 23102023 14:27
**1. Description**

Ce code Python est destiné à extraire les dates limites de confirmation (deadlines) à partir d'un fichier de données normalisé, pour des Passagers non Confirmés (PNR). Il analyse les informations contenues dans le fichier normalisé à la recherche de lignes de type "OPW" (qui décrivent les dates limites de confirmation) et "OPC" (qui sont liées aux annulations). Une fois les données extraites, les dates limites de confirmation sont enregistrées dans une liste.

**2. Paramètres**

La fonction `get_confirmation_deadline` prend les paramètres suivants :
- `self`: La référence à l'instance de la classe à laquelle appartient cette méthode.
- `normalized_file`: Une liste de lignes du fichier normalisé à analyser.
- `pnr`: Objet PNR qui doit contenir des informations sur la date de création.
- `segments`: Une liste d'objets de segment.
- `ssrs`: Une liste d'objets de ssr (Service Request Records).

**3. Fonctionnement**

La fonction analyse le fichier `normalized_file` à la recherche de lignes contenant des informations sur les dates limites de confirmation, identifiées par les préfixes "OPW" et "OPC". Pour chaque ligne "OPW", elle extrait les détails de la date limite de confirmation, notamment la date, l'heure, le texte supplémentaire et les segments ou les ssrs associés. Les informations extraites sont stockées dans une liste d'objets de type `ConfirmationDeadline`.

**4. Résumé**

Ce code extrait les dates limites de confirmation à partir d'un fichier normalisé pour des PNR non confirmés. Il identifie les informations pertinentes, les traite et les enregistre dans une liste d'objets `ConfirmationDeadline`.

**5. Explications**

Le code commence par définir l'année de fonctionnement à partir de la date de création du PNR. Ensuite, il parcourt les lignes du fichier normalisé, extrait les lignes "OPW" et "OPC" dans des listes distinctes (`opw_lines` et `opc_lines`).

Pour chaque ligne "OPW", il analyse les informations pour extraire la date, l'heure, le texte supplémentaire et les segments ou ssrs associés. Il prend en charge plusieurs formats de segmentation, y compris les sélections de segment, les groupes de segments, et les segments individuels. Les informations sont ensuite enregistrées dans des objets `ConfirmationDeadline` et ajoutées à la liste `confirmation_deadlines`.

**6. Extensions possibles**

Ce code pourrait être étendu pour inclure des fonctionnalités supplémentaires, telles que la génération de rapports basés sur les dates limites de confirmation extraites, la gestion des annulations ("OPC"), ou la validation des dates limites par rapport à la date actuelle. Vous pourriez également envisager de créer des tests unitaires pour garantir la précision du code.

**7. Codes**
```python
# Obtenir les dates limites de confirmation pour les PNR non confirmés
def get_confirmation_deadline(self, normalized_file, pnr, segments, ssrs):
    # Extraire l'année d'opération à partir de la date de création du PNR
    year_of_operation = pnr.gds_creation_date.year
    
    # Initialiser des listes pour stocker les lignes pertinentes du fichier normalisé
    confirmation_deadlines = []  # Liste pour stocker les dates limites de confirmation
    opw_lines = []  # Lignes contenant des informations OPW
    opc_lines = []  # Lignes contenant des informations OPC
    
    # Parcourir chaque ligne du fichier normalisé
    for line in normalized_file:
        temp = line.split(" ")
        if len(temp) > 2 and temp[0].isnumeric():
            if temp[1].startswith('OPW'):
                opw_lines.append(line)
            elif temp[1].startswith('OPC'):
                opc_lines.append(line)
    
    # Traiter d'abord les lignes OPW
    for opw in opw_lines:
        opw_part = opw.split(' ')[1:]
        date_time = None
        date_type = 'OPW'
        free_flow_text = ''
        
        # Vérifier si la ligne commence par 'OPW'
        if opw_part[0] == 'OPW':
            # Extraire la partie de la date et de l'heure à partir de la ligne
            date_part = opw_part[1].split('-')[1]
            date_split = date_part.split('/')[0]
            date_time_split = date_split.split(':')
            date = date_time_split[0] + str(year_of_operation)
            time = date_time_split[1][0:2] + ':' + date_time_split[1][2:] + ':00'
            date_time = date + ' ' + time
            date_time = datetime.strptime(date_time, '%d%b%Y %H:%M:%S')
            
            # Extraire le texte supplémentaire associé à la date limite de confirmation
            for text in opw_part[2:]:
                free_flow_text += text + ' '
            
            # Parcourir les éléments séparés par '/'
            for text in opw_part[2:]:
                slash_split = text.split('/')
                
                # Parcourir chaque élément dans la liste séparée par '/'
                for temp_slash_split in slash_split:
                    # Vérifier si l'élément commence par 'S' ou 'E' et est suivi d'un numéro
                    if (temp_slash_split.startswith('S') or temp_slash_split.startswith('E')) and temp_slash_split[1].isnumeric():
                        # Groupe de segments S1,4
                        if len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) == 1:
                            temp_sliced_part_1 = temp_slash_split.split('-')
                            start_segment = int(temp_sliced_part_1[0][1:])
                            end_segment = int(temp_sliced_part_1[len(temp_sliced_part_1) - 1])
                            a = start_segment
                            while a <= end_segment:
                                # Créer un objet ConfirmationDeadline et remplir ses champs
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if temp_slash_split.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(a):
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif temp_slash_split.startswith('E'):
                                    for ssr in ssrs:
                                        if ssr.order_line == 'E' + str(a):
                                            temp_conf.ssr = ssr
                                    confirmation_deadlines.append(temp_conf)
                                a += 1
                        # Sélection de segments S1,2,3
                        elif len(temp_slash_split.split(',')) > 1 and len(temp_slash_split.split('-')) == 1:
                            temp_sliced_part = temp_slash_split.split(',')
                            first_segment = int(temp_sliced_part[0][1:])
                            temp_sliced_part[0] = first_segment
                            a = 0
                            while a < len(temp_sliced_part):
                                temp_order_count = temp_sliced_part[a]
                                temp_conf = ConfirmationDeadline()
                                temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                temp_conf.free_flow_text = free_flow_text
                                temp_conf.type = date_type
                                if first_segment.startswith('S'):
                                    for segment in segments:
                                        if segment.segmentorder == 'S' + str(temp_order_count):
                                            temp_conf.segment = segment
                                    confirmation_deadlines.append(temp_conf)
                                elif first_segment.startswith('E'):
                                    for ssrs in ssrs:
                                        if ssrs.order_line == 'E' + str(temp_order_count):
                                            temp_conf.ssr = ssrs
                                    confirmation_deadlines.append(temp_conf)
                                a += 1
                        # Sélection de segments S1,7-9 ou S1-3,7-9
                        elif len(temp_slash_split.split('-')) > 1 and len(temp_slash_split.split(',')) > 1:
                            segment_group = temp_slash_split.split(',')
                            first_segment = segment_group[0]
                            for group in segment_group:
                                temp_sliced_part = group.split('-')
                                if group.startswith('S'):
                                    start_segment = int(temp_sliced_part[0][1:])
                                else:
                                    start_segment = int(temp_sliced_part[0])
                                end_segment = int(temp_sliced_part[len(temp_sliced_part) - 1].removeprefix('S').removeprefix('E'))
                                a = start_segment
                                while a <= end_segment:
                                    temp_order_count = a
                                    temp_conf = ConfirmationDeadline()
                                    temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                                    temp_conf.free_flow_text = free_flow_text
                                    temp_conf.type = date_type
                                    if first_segment.startswith('S'):
                                        for segment in segments:
                                            if segment.segmentorder == 'S' + str(temp_order_count):
                                                temp_conf.segment = segment
                                        confirmation_deadlines.append(temp_conf)
                                    elif first_segment.startswith('E'):
                                        for ssrs in ssrs:
                                            if ssrs.order_line == 'E' + str(temp_order_count):
                                                temp_conf.ssr = ssrs
                                        confirmation_deadlines.append(temp_conf)
                                    a += 1
                        # Segment normal S1
                        else:
                            temp_conf = ConfirmationDeadline()
                            temp_conf.doc_date = datetime(date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.microsecond, pytz.UTC)
                            temp_conf.free_flow_text = free_flow_text
                            temp_conf.type = date_type
                            if temp_slash_split.startswith('S'):
                                for segment in segments:
                                    if segment.segmentorder == temp_slash_split:
                                        temp_conf.segment = segment
                                confirmation_deadlines.append(temp_conf)
                            elif temp_slash_split.startswith('E'):
                                for ssrs in ssrs:
                                    if ssrs.order_line == temp_slash_split:
                                        temp_conf.ssr = ssrs
                                confirmation_deadlines.append(temp_conf)
        # Fin du traitement des lignes OPW
    
    # Le code de traitement des lignes OPC peut être ajouté ici, en suivant un modèle similaire
```


### Méthode `get_remarks(self, pnr, normalized_file)` 23102023 14:32
**1. Description**

Cette fonction a pour but d'extraire toutes les remarques (commentaires) d'un PNR (Passenger Name Record) à partir d'un fichier normalisé.

**2. Paramètres**

Cette fonction a pour but d'extraire toutes les remarques (commentaires) d'un PNR (Passenger Name Record) à partir d'un fichier normalisé.

**3. Fonctionnement**

Le code parcourt le fichier normalisé ligne par ligne à la recherche de lignes contenant des codes de remarques possibles. Il identifie les lignes de remarques en se basant sur une liste de codes de remarques préalablement définie.

**4. Résumé**

Ce code extrait toutes les remarques d'un PNR à partir d'un fichier normalisé en utilisant une liste de codes de remarques possibles.

**5. Explications**

La fonction commence par initialiser une liste appelée all_possible_remarks, qui contient les codes de remarques possibles. Ces codes serviront à identifier les lignes de commentaires dans le fichier normalisé.

Deux listes vides sont créées : all_pnr_remarks pour stocker les remarques extraites et remark_lines pour stocker les lignes de commentaires du fichier normalisé.

En parcourant chaque ligne du fichier normalisé, la fonction vérifie si la ligne commence par un numéro (indicatif d'une ligne de commentaire) et si le deuxième élément de la ligne correspond à l'un des codes de remarques possibles. Si ces conditions sont remplies, la ligne est ajoutée à la liste remark_lines.

Ensuite, la fonction parcourt les lignes de commentaires extraites. Pour chaque ligne, elle divise la ligne en mots en utilisant l'espace comme séparateur. Elle extrait le code de la remarque (deuxième mot) et recherche l'objet Remark correspondant dans une base de données.

Une fois qu'un objet Remark est trouvé, la fonction construit le texte de la remarque en utilisant les mots restants dans la ligne.

Un objet PnrRemark est créé pour chaque remarque extraite. Cet objet est associé au PNR, à l'objet Remark trouvé et au texte de la remarque. Ensuite, l'objet PnrRemark est ajouté à la liste all_pnr_remarks.

Enfin, la fonction renvoie la liste all_pnr_remarks contenant toutes les remarques extraites.

**6. Extensions possibles**

Ce code peut être étendu pour prendre en charge d'autres codes de remarques s'ils sont utilisés dans le contexte du système. De plus, des validations supplémentaires peuvent être ajoutées pour garantir que les remarques sont extraites correctement et associées aux PNR appropriés.

**7. Codes**
```python
# Obtenir toutes les remarques d'un PNR
def get_remarks(self, pnr, normalized_file):
    # Liste des codes de remarques possibles
    all_possible_remarks = ['RM', 'RC', 'RIR', 'RX', 'RCF', 'RQ', 'RIA', 'RIS', 'RIT', 'RIU', 'RIF', 'RII', 'RIZ']
    
    # Liste pour stocker toutes les remarques du PNR
    all_pnr_remarks = []
    
    # Liste pour stocker les lignes de remarques du fichier normalisé
    remark_lines = []
    
    # Parcourir chaque ligne du fichier normalisé
    for line in normalized_file:
        # Diviser la ligne en mots en utilisant l'espace comme séparateur
        temp = line.split(" ")
        
        # Vérifier si le premier élément de la ligne est un numéro
        if temp[0].isnumeric():
            # Vérifier si le deuxième élément de la ligne est l'un des codes de remarques possibles
            if temp[1] in all_possible_remarks:
                # Ajouter la ligne à la liste des lignes de remarques
                remark_lines.append(line)
    
    # Parcourir les lignes de remarques détectées
    for remark in remark_lines:
        # Diviser la ligne en mots en utilisant l'espace comme séparateur
        space_split = remark.split(' ')
        
        # Créer un objet PnrRemark temporaire
        temp_pnr_remark = PnrRemark()
        
        # Rechercher l'objet Remark correspondant dans la base de données en utilisant le code de remarque
        temp_remark = Remark.objects.filter(code=space_split[1]).first()
        
        # Texte de la remarque
        remark_text = ''
        
        # Si un objet Remark est trouvé
        if temp_remark is not None:
            # Construire le texte de la remarque à partir des mots restants dans la ligne
            for text in space_split[2:]:
                remark_text += text + ' '
            
            # Associer la remarque au PNR, à l'objet Remark et au texte de la remarque
            temp_pnr_remark.pnr = pnr
            temp_pnr_remark.remark = temp_remark
            temp_pnr_remark.remark_text = remark_text[:-1]  # Supprimer l'espace final
            
            # Ajouter l'objet PnrRemark à la liste de toutes les remarques du PNR
            all_pnr_remarks.append(temp_pnr_remark)
    
    # Renvoyer la liste de toutes les remarques extraites
    return all_pnr_remarks
```

Cette fonction parcourt un fichier normalisé à la recherche de remarques dans un PNR. Elle extrait les remarques en se basant sur des codes de remarques possibles, les associe au PNR correspondant et les stocke dans une liste. Les remarques extraites sont renvoyées sous forme d'objets PnrRemark.

### Méthode `get_am_ah(self, normalized_file, pnr, passengers)` 23102023 14:38
**1. Description**

Cette fonction a pour objectif d'extraire les adresses clients (AM/H) d'un fichier normalisé lié à un PNR (Passenger Name Record). Les adresses clients peuvent être associées à des passagers.

**2. Paramètres**

- `normalized_file` : Le fichier normalisé contenant les informations du PNR.
- `pnr` : L'objet PNR auquel les adresses clients doivent être associées.
- `passengers` : Une liste des passagers associés au PNR.

**3. Fonctionnement**

La fonction parcourt le fichier normalisé ligne par ligne à la recherche de lignes contenant des informations d'adresse client qui commencent par l'identifiant "AM" ou "AH". Elle extrait ces lignes et les associe au PNR ainsi qu'aux passagers, le cas échéant.

**4. Résumé**

Ce code extrait les adresses clients à partir d'un fichier normalisé et les associe au PNR et aux passagers, le cas échéant.

**5. Explications**

- La fonction commence par initialiser deux listes vides, customer_addresses pour stocker les adresses clients extraites et addresses_lines pour stocker les lignes de fichier contenant ces adresses.

- En parcourant chaque ligne du fichier normalisé, la fonction vérifie si la ligne commence par un numéro et si le deuxième élément de la ligne commence par l'un des identifiants "AM" ou "AH". Si tel est le cas, la ligne est ajoutée à la liste addresses_lines.

- Ensuite, la fonction parcourt les lignes d'adresse extraites. Pour chaque ligne, elle sépare le texte de l'adresse des informations relatives au passager, le cas échéant. Les informations du passager sont repérées par la présence du préfixe "P" dans la ligne.

- Les informations du passager sont extraites et le texte de l'adresse est nettoyé pour remplacer les '/' par des espaces. Un objet CustomerAddress est créé, associé au PNR et, s'il y a lieu, au passager correspondant.

- La fonction gère différents scénarios pour l'association des adresses aux passagers en fonction du nombre de passagers et des types de passagers.

- Les objets CustomerAddress ainsi créés sont ajoutés à la liste customer_addresses.

- Finalement, la fonction renvoie la liste customer_addresses contenant toutes les adresses clients extraites.

**6. Extensions possibles**

Ce code peut être étendu pour prendre en charge d'autres types d'adresses ou d'informations d'adresse client spécifiques au contexte du système. Des validations supplémentaires peuvent être ajoutées pour garantir une association précise entre les adresses et les passagers.

**7. Codes**


### Méthode `get_pnr_status(self, pnr, normalized_file)` 23102023 14:38
**1. Description**

Cette fonction a pour objectif de déterminer le statut d'un PNR (Passenger Name Record) en se basant sur les informations extraites d'un fichier normalisé. Le statut peut être soit "Émis" si des informations de billet (comme des contacts téléphoniques ou des adresses email) sont présentes, soit "Non émis" dans le cas contraire.

**2. Paramètres**

- `pnr` : L'objet PNR auquel le statut doit être associé.
- `normalized_file` : Le fichier normalisé contenant les informations du PNR.

**3. Fonctionnement**

La fonction parcourt le fichier normalisé ligne par ligne à la recherche de lignes contenant des informations de billet, notamment des contacts téléphoniques ou des adresses email. Si de telles informations sont détectées, le statut du PNR est défini sur "Émis," sinon il est défini sur "Non émis."

**4. Résumé**

Ce code détermine le statut d'un PNR en se basant sur la présence d'informations de billet dans un fichier normalisé.

**5. Explications**

La fonction initialise deux variables, pnr_status et pnr_status_value, avec la valeur "Non émis" et 1 respectivement. Ces variables servent à stocker le statut du PNR et sa valeur correspondante.

En parcourant chaque ligne du fichier normalisé, la fonction vérifie si la ligne commence par un numéro et si le deuxième élément de la ligne correspond à l'un des identifiants définis dans TICKET_LINE_IDENTIFIER. Si c'est le cas, cela signifie qu'il y a des informations de billet, et le statut du PNR est modifié pour devenir "Émis" avec une valeur de 0 (pour indiquer qu'il est émis). La boucle est alors interrompue.

Le statut du PNR et sa valeur sont ensuite associés à l'objet PNR correspondant et sauvegardés dans la base de données.

**6. Extensions possibles**

Ce code peut être étendu pour prendre en charge d'autres critères de détermination du statut du PNR, en fonction des besoins spécifiques du système. Des validations supplémentaires peuvent être ajoutées pour garantir la précision de la détermination du statut.

**7. Codes**

### Méthode `ticket_on_issued_pnr(self, pnr, normalized_file)` 23102023 14:38


WUGQZ7: Passagers groupées

process_subcontract()

transaction.savepoint_commit(sid)