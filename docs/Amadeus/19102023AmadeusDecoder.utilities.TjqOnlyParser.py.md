### Utilisation TjqOnlyParser

Créé par: Alain RAKOTOARIVELO
Heure de création: 19 octobre 2023 11:45
Étiquettes: TjqOnlyParser


### fonction `get_doc_info(file_contents)`
**1. Description**
Cette fonction est utilisée pour extraire des informations spécifiques à partir d'un contenu de fichier. Elle parcourt chaque ligne du contenu du fichier et vérifie si la ligne commence par certains préfixes. Si une ligne correspond à l'un des préfixes, les informations correspondantes sont extraites et stockées dans des variables. Finalement, la fonction retourne les informations extraites sous forme de tuple.

**2. Paramètres**
- `self` : Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.

- `file_contents` : Ce paramètre est une liste 
contenant le contenu d'un fichier.

**3. Fonctionnement**
La fonction itère à travers chaque ligne de la liste file_contents en utilisant une boucle for avec la fonction enumerate pour obtenir à la fois l'index et la valeur de chaque ligne.

À l'intérieur de la boucle, la fonction vérifie si la ligne commence par certains préfixes tels que "AGENT", "OFFICE", "CURRENCY" ou "SEQ" en utilisant la méthode startswith. Si une ligne correspond à l'un des préfixes, les informations correspondantes sont extraites et stockées dans les variables appropriées.

Si la ligne commence par "AGENT", la fonction utilise la méthode split pour extraire la partie avant "AGENT - " et la partie après les 12 derniers caractères de la ligne, qui représentent la date du document. Ces informations sont stockées dans les variables tjq_agent_type et doc_date respectivement.

Si la ligne commence par "OFFICE", la fonction utilise la méthode split pour extraire la partie après "OFFICE -" et avant "SELECTION". Cette information est stockée dans la variable office.

Si la ligne commence par "CURRENCY", la fonction utilise la méthode split pour extraire la partie après "CURRENCY". Cette information est stockée dans la variable currency.

Si la ligne commence par "SEQ", la fonction utilise l'index de cette ligne pour extraire les lignes suivantes à partir de la liste file_contents. Ces lignes sont stockées dans la variable tjq_lines.

Finalement, la fonction retourne un tuple contenant les variables tjq_agent_type, office, currency, doc_date et tjq_lines.

**4. Résumé**
La fonction `get_doc_info` extrait des informations spécifiques à partir d'un contenu de fichier, telles que le type d'agent, le bureau, la devise, la date du document et les lignes de contenu. Elle retourne ces informations sous forme de tuple.

**5. Explications**
La fonction commence par initialiser les variables tjq_agent_type, office, currency, doc_date et tjq_lines avec des valeurs vides.

Ensuite, elle itère à travers chaque ligne du contenu du fichier en utilisant une boucle for et la fonction enumerate. Pour chaque ligne, la fonction vérifie si elle commence par l'un des préfixes spécifiés.

Si la ligne commence par "AGENT", la fonction utilise la méthode split pour extraire la partie avant "AGENT - " et la partie après les 12 derniers caractères de la ligne, qui représentent la date du document. Ces informations sont assignées aux variables tjq_agent_type et doc_date respectivement.

Si la ligne commence par "OFFICE", la fonction utilise la méthode split pour extraire la partie après "OFFICE -" et avant "SELECTION". Cette information est assignée à la variable office.

Si la ligne commence par "CURRENCY", la fonction utilise la méthode split pour extraire la partie après "CURRENCY". Cette information est assignée à la variable currency.

Si la ligne commence par "SEQ", la fonction utilise l'index de cette ligne pour extraire les lignes suivantes à partir de la liste file_contents. Ces lignes sont assignées à la variable tjq_lines.

Finalement, la fonction retourne un tuple contenant les variables tjq_agent_type, office, currency, doc_date et tjq_lines.

**6. Extensions possibles**
La fonction peut être modifiée pour gérer les cas où le contenu du fichier ne contient pas les préfixes attendus.
  
Des validations supplémentaires peuvent être ajoutées pour vérifier si les informations extraites sont valides et cohérentes.

La fonction peut être étendue pour effectuer d'autres traitements sur les informations extraites, telles que la conversion de la date en un format spécifique ou l'enregistrement des informations dans une base de données.

### fonction `update_ticket(tjq)`
**1. Description**

La fonction update_ticket met à jour les informations d'un billet dans la base de données en fonction d'un objet tjq passé en paramètre. Elle recherche d'abord le PNR correspondant au numéro de PNR spécifié dans l'objet tjq. Ensuite, elle recherche le billet correspondant au numéro de billet spécifié dans l'objet tjq et lié au PNR trouvé précédemment. Si le billet existe, elle met à jour les informations du billet telles que le montant total, la taxe, le coût du transport, l'état et l'indicateur is_no_adc. Enfin, elle appelle la méthode update_pnr_state du billet pour mettre à jour l'état du PNR.

**2. Paramètres**

- `self`: Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.
- `tjq`: Cet objet représente les informations de mise à jour du billet.

**3. Fonctionnement**

La fonction commence par rechercher le PNR correspondant au numéro de PNR spécifié dans l'objet tjq en utilisant la méthode filter de l'objet Pnr et la méthode first pour obtenir le premier résultat de la requête.

Si le PNR existe, la fonction recherche le billet correspondant au numéro de billet spécifié dans l'objet tjq et lié au PNR trouvé précédemment en utilisant la méthode filter de l'objet Ticket et la méthode first pour obtenir le premier résultat de la requête.

Si le billet existe, la fonction recherche la taxe associée au billet en utilisant la méthode filter de l'objet Fee et la méthode first pour obtenir le premier résultat de la requête.

Si la taxe n'existe pas et que le montant total du billet est égal à 0 et le coût du transport du billet est égal à 0, la fonction met à jour les informations du billet en affectant les valeurs du montant total, de la taxe et du coût du transport spécifiées dans l'objet tjq. Elle met également l'état du billet à 0 et définit l'indicateur is_no_adc à True si le montant total est égal à 0. Enfin, elle enregistre les modifications en appelant la méthode save sur l'objet ticket.

Ensuite, la fonction appelle la méthode update_pnr_state du billet pour mettre à jour l'état du PNR.

**4. Résumé**

La fonction update_ticket met à jour les informations d'un billet dans la base de données en fonction d'un objet tjq passé en paramètre. Elle recherche le PNR correspondant au numéro de PNR spécifié dans l'objet tjq et le billet correspondant au numéro de billet spécifié dans l'objet tjq et lié au PNR. Si le billet existe, elle met à jour ses informations et appelle la méthode update_pnr_state pour mettre à jour l'état du PNR.

**5. Explications**

La fonction update_ticket commence par rechercher le PNR correspondant au numéro de PNR spécifié dans l'objet tjq en utilisant la méthode filter de l'objet Pnr et la méthode first pour obtenir le premier résultat de la requête. Si le PNR existe, la fonction recherche le billet correspondant au numéro de billet spécifié dans l'objet tjq et lié au PNR trouvé précédemment en utilisant la méthode filter de l'objet Ticket et la méthode first pour obtenir le premier résultat de la requête.

Si le billet existe, la fonction recherche la taxe associée au billet en utilisant la méthode filter de l'objet Fee et la méthode first pour obtenir le premier résultat de la requête. Si la taxe n'existe pas et que le montant total du billet est égal à 0 et le coût du transport du billet est égal à 0, la fonction met à jour les informations du billet en affectant les valeurs du montant total, de la taxe et du coût du transport spécifiées dans l'objet tjq. Elle met également l'état du billet à 0 et définit l'indicateur is_no_adc à True si le montant total est égal à 0. Enfin, elle enregistre les modifications en appelant la méthode save sur l'objet ticket.

Ensuite, la fonction appelle la méthode update_pnr_state du billet pour mettre à jour l'état du PNR.

**6. Extensions possibles**

La fonction peut être modifiée pour gérer les cas où le PNR ou le billet n'existent pas dans la base de données.
Des validations supplémentaires peuvent être ajoutées pour vérifier si les informations de l'objet tjq sont valides et cohérentes avant de mettre à jour le billet.

La fonction peut être étendue pour effectuer d'autres traitements sur le billet ou les objets associés, tels que la mise à jour d'autres champs ou l'envoi de notifications.


**7. Codes**
```python
 def update_ticket(self, tjq):
    pnr = Pnr.objects.filter(number=tjq.pnr_number).first()
    if pnr is not None:
        ticket = Ticket.objects.filter(number=tjq.ticket_number, pnr=pnr).first()
        if ticket is not None:
            fee = Fee.objects.filter(ticket=ticket).first()
            if fee is None and ticket.total == 0 and ticket.transport_cost == 0:
                ticket.total = tjq.total
                ticket.tax = tjq.tax
                ticket.transport_cost = tjq.total - tjq.tax
                ticket.state = 0
                if tjq.total == 0:
                    ticket.is_no_adc = True
                ticket.save()
                # update pnr state
                ticket.update_pnr_state(pnr)
```

### fonction `save_tjq(tjq_agent_type, office,currency,doc_date, tjq_lines)`
**1. Description**

La fonction save_tjq enregistre un objet tjq dans la base de données en fonction des informations fournies en paramètres. Elle crée un nouvel objet Tjq et extrait les informations nécessaires à partir de la chaîne tjq_lines. Ensuite, elle vérifie si l'objet tjq n'existe pas déjà dans la base de données en comparant le numéro de séquence (seq_no) avec ceux des objets Tjq existants. Si l'objet tjq est nouveau, elle l'enregistre dans la base de données. Enfin, elle appelle la méthode update_ticket pour mettre à jour le billet associé à l'objet tjq.s

**2. Paramètres**

- `self`: Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.
- `tjq_agent_type`: Ce paramètre représente le type d'agent associé à l'objet tjq.
- `office`: Ce paramètre représente le code de l'agence associée à l'objet tjq.
- `currency`: Ce paramètre représente la devise associée à l'objet tjq.
- `doc_date`: Ce paramètre représente la date du document associé à l'objet tjq.
- `tjq_lines`: Ce paramètre représente la chaîne contenant les informations nécessaires pour créer l'objet tjq.

**3. Fonctionnement**

La fonction commence par créer un nouvel objet Tjq en utilisant la classe Tjq et l'assigne à la variable tjq.

Ensuite, la fonction traite la chaîne tjq_lines en remplaçant les astérisques par des espaces à l'aide de la méthode replace et en la divisant en une liste de mots à l'aide de la méthode split.

La fonction filtre la liste lines pour supprimer les éléments vides à l'aide d'une compréhension de liste.

Ensuite, la fonction récupère l'ID de l'utilisateur GDS à partir de l'avant-dernier élément de la liste lines et recherche l'utilisateur correspondant dans la table User en utilisant la méthode filter de l'objet User et la méthode first pour obtenir le premier résultat de la requête. Elle fait de même pour rechercher l'agence correspondante dans la table Office en utilisant la méthode filter de l'objet Office et la méthode first.

La fonction assigne les valeurs des attributs de l'objet tjq en fonction des éléments de la liste lines et des résultats des recherches précédentes.

Ensuite, la fonction vérifie si le numéro de séquence de l'objet tjq n'existe pas déjà dans la liste tjqs_seq_no en utilisant une condition if. Si le numéro de séquence est nouveau, la fonction enregistre l'objet tjq dans la base de données en appelant la méthode save sur l'objet tjq et affiche "TJQ SAVED". Sinon, elle affiche "TJQ ALREADY CREATED".

Enfin, la fonction appelle la méthode update_ticket en passant l'objet tjq en paramètre pour mettre à jour le billet associé.

**4. Résumé**

La fonction save_tjq enregistre un objet tjq dans la base de données en fonction des informations fournies en paramètres. Elle crée un nouvel objet Tjq en extrayant les informations nécessaires à partir de la chaîne tjq_lines. Ensuite, elle vérifie si l'objet tjq n'existe pas déjà dans la base de données et l'enregistre si nécessaire. Enfin, elle met à jour le billet associé à l'objet tjq.

**5. Explications**

La fonction save_tjq commence par créer un nouvel objet Tjq en utilisant la classe Tjq et l'assigne à la variable tjq.

Ensuite, la fonction traite la chaîne tjq_lines en remplaçant les astérisques par des espaces à l'aide de la méthode replace et en la divisant en une liste de mots à l'aide de la méthode split.

La fonction filtre la liste lines pour supprimer les éléments vides à l'aide d'une compréhension de liste.

Ensuite, la fonction récupère l'ID de l'utilisateur GDS à partir de l'avant-dernier élément de la liste lines et recherche l'utilisateur correspondant dans la table User en utilisant la méthode filter de l'objet User et la méthode first pour obtenir le premier résultat de la requête. Elle fait de même pour rechercher l'agence correspondante dans la table Office en utilisant la méthode filter de l'objet Office et la méthode first.

La fonction assigne les valeurs des attributs de l'objet tjq en fonction des éléments de la liste lines et des résultats des recherches précédentes.

Ensuite, la fonction vérifie si le numéro de séquence de l'objet tjq n'existe pas déjà dans la liste tjqs_seq_no en utilisant une condition if. Si le numéro de séquence est nouveau, la fonction enregistre l'objet tjq dans la base de données en appelant la méthode save sur l'objet tjq et affiche "TJQ SAVED". Sinon, elle affiche "TJQ ALREADY CREATED".

Enfin, la fonction appelle la méthode update_ticket en passant l'objet tjq en paramètre pour mettre à jour le billet associé.

**6. Extensions possibles**

La fonction peut être modifiée pour gérer les cas où les recherches d'utilisateur ou d'agence ne renvoient pas de résultats.

Des validations supplémentaires peuvent être ajoutées pour vérifier si les informations fournies en paramètres sont valides et cohérentes avant de créer l'objet tjq.

La fonction peut être étendue pour effectuer d'autres traitements sur l'objet tjq ou les objets associés, tels que la mise à jour d'autres champs ou l'envoi de notifications.

On peut ajouter des options de configuration pour permettre à l'utilisateur de spécifier les champs à enregistrer ou les actions à effectuer en fonction des informations fournies.

On peut également ajouter des commentaires et des annotations dans le code pour faciliter la compréhension et la maintenance du code par d'autres développeurs.

La fonction peut être optimisée pour améliorer ses performances, par exemple en utilisant des requêtes plus efficaces ou en évitant des opérations redondantes.

On peut ajouter des fonctionnalités supplémentaires, telles que la gestion des erreurs de la base de données ou la journalisation des actions effectuées par la fonction.

**7. Codes**
```python
def save_tjq(self, tjq_agent_type, office,currency,doc_date, tjq_lines) :
    tjq = Tjq()
    tjq_lines = tjq_lines.replace('*', ' ')
    lines = tjq_lines.split(" ")
    lines = [ t for t in lines if t != '']
    
    # Check if exists
    tjq_objects = Tjq.objects.all()
    tjqs_seq_no = [ t.seq_no for t in tjq_objects]
    try :
        user_gds_id = lines[-3]
        user_agent = User.objects.filter(gds_id=user_gds_id).first()
        user_agency = Office.objects.filter(code=office).first()

        tjq.agency = user_agency if user_agency is not None else None
        tjq.agency_name = office
        tjq.tjq_agent_type = tjq_agent_type
        tjq.doc_date = doc_date
        tjq.currency = currency
        tjq.seq_no = lines[0]
        tjq.ticket_number = "".join([lines[1], lines[2]])
        tjq.pnr_number = lines[-2]
        tjq.tax = float(lines[4])
        tjq.total = float(lines[3])
        tjq.fee = float(lines[5])
        tjq.comm = float(lines[6])
        tjq.fp_pax = lines[7]
        tjq.passenger = lines[8]
        tjq.agent_code = user_gds_id
        tjq.agent = user_agent if user_agent is not None else None
        tjq.type = lines[-1]
        tjq.system_creation_date = datetime.now()
        
        if tjq.seq_no not in tjqs_seq_no :

            tjq.save()
            print('TJQ SAVED')

        else :
            print('TJQ ALREADY CREATED')
        
        # update ticket on missing fare/total or tst
        self.update_ticket(tjq)
    except :
        traceback.print_exc()
        with open(os.path.join(os.getcwd(),'error.txt'), 'a') as error_file:
            error_file.write('{}: \n'.format(datetime.now()))
            # error_file.write('Line (TJQ) with error: {} \n'.format(str(error_file)))
            traceback.print_exc(file=error_file)
            error_file.write('\n')
```

### fonction `parse_tjq(self, file_contents)`
**1. Description**

La fonction parse_tjq analyse le contenu d'un fichier et détecte les lignes correspondant à des objets tjq. Pour chaque ligne détectée, elle appelle la fonction save_tjq pour enregistrer l'objet tjq dans la base de données.

**2. Paramètres**

- `self`: Ce paramètre fait référence à l'instance de la classe à laquelle la fonction appartient.
- `file_contents`: Ce paramètre représente le contenu du fichier à analyser.

**3. Fonctionnement**

La fonction commence par afficher "TJQ FILE DETECTED" pour indiquer que le fichier contient des objets tjq.

Ensuite, la fonction appelle la méthode get_doc_info pour extraire les informations nécessaires à partir du contenu du fichier. Elle assigne les valeurs renvoyées par la méthode get_doc_info aux variables tjq_agent_type, office, currency, doc_date et tjq_lines.

Ensuite, la fonction itère sur chaque ligne de la liste tjq_lines et appelle la fonction save_tjq en passant les informations nécessaires en paramètres.

**4. Résumé**

La fonction parse_tjq analyse le contenu d'un fichier et détecte les lignes correspondant à des objets tjq. Pour chaque ligne détectée, elle appelle la fonction save_tjq pour enregistrer l'objet tjq dans la base de données.

**5. Explications**

La fonction parse_tjq commence par afficher "TJQ FILE DETECTED" pour indiquer que le fichier contient des objets tjq.

Ensuite, la fonction appelle la méthode get_doc_info pour extraire les informations nécessaires à partir du contenu du fichier. Elle assigne les valeurs renvoyées par la méthode get_doc_info aux variables tjq_agent_type, office, currency, doc_date et tjq_lines.

Ensuite, la fonction itère sur chaque ligne de la liste tjq_lines et appelle la fonction save_tjq en passant les informations nécessaires en paramètres.

**6. Extensions possibles**

- On peut ajouter des validations supplémentaires pour vérifier si le fichier est au bon format ou s'il contient des erreurs.
- La fonction peut être étendue pour prendre en charge d'autres types de documents ou d'autres opérations sur les objets tjq.
- On peut ajouter des options de configuration pour permettre à l'utilisateur de spécifier les actions à effectuer en fonction du contenu du fichier.
- La fonction peut être intégrée dans un module ou une classe plus large pour faciliter son utilisation et sa réutilisation dans d'autres parties du code.
- On peut ajouter des tests unitaires pour vérifier le bon fonctionnement de la fonction dans différentes situations et garantir sa stabilité.

**7. Codes**
```python
def parse_tjq(self, file_contents):
    print('TJQ FILE DETECTED')
    
    # save or update EMD
    tjq_agent_type, office, currency,doc_date, tjq_lines = self.get_doc_info(file_contents)

    for tjq in tjq_lines :
        self.save_tjq(tjq_agent_type, office, currency,doc_date, tjq)
```