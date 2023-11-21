Créé par: Alain RAKOTOARIVELO
Heure de création: 20 octobre 2023 16:46
Étiquettes: AmadeusDecoder

### Méthode `update_segment_status(self, pnr, new_segments)`
**1. Description**
Cette fonction est responsable de la mise à jour du statut des segments de vol sur la base des nouveaux segments fournis. Elle doit être placée avant l'insertion des nouveaux segments dans le système. Cette mise à jour permet de maintenir un état cohérent des segments de vol associés à un PNR (Passenger Name Record).

**2. Paramètres**

- `self` : L'instance de la classe qui appelle la fonction.
- `pnr` : L'objet PNR auquel les segments sont associés.
- `new_segments` : La liste des nouveaux segments de vol à insérer et comparer avec les anciens.

**3. Fonctionnement**

La fonction commence par vérifier si des nouveaux segments sont fournis. Si la liste est vide, la mise à jour n'est pas effectuée.
Elle récupère les anciens segments de vol associés au PNR.
Pour chaque ancien segment de vol, elle collecte des données pertinentes telles que le numéro de vol, l'heure de départ, l'heure d'arrivée et la classe de vol.
Ensuite, elle parcourt les nouveaux segments pour collecter les mêmes données.
La fonction compare les anciennes données de segment avec les nouvelles. Si les données d'un ancien segment ne correspondent pas à celles des nouveaux segments, le statut du segment de vol est mis à jour en le définissant sur 0 (statut inactif).
Pour chaque segment de vol mis à jour, les billets associés sont également mis à jour. Leur état est défini sur 0 (inactif) et leur statut de billet est défini sur 3 (statut annulé).
Enfin, la fonction met à jour l'état du PNR lié au billet et affiche les données des anciens et des nouveaux segments.

**4. Résumé**

Cette fonction garantit que les segments de vol associés à un PNR restent cohérents en mettant à jour leur statut en fonction des nouveaux segments fournis. Elle gère également les mises à jour connexes des billets associés et de l'état du PNR.

**5. Explications**

Cette fonction commence par vérifier si de nouveaux segments sont fournis, ce qui permet d'éviter des opérations inutiles si la liste est vide.
Elle collecte les données clés des anciens segments de vol, y compris le numéro de vol, l'heure de départ, l'heure d'arrivée et la classe de vol.
Ensuite, elle recueille les mêmes données pour les nouveaux segments.
Les anciennes données sont comparées aux nouvelles. Si une différence est détectée, le segment de vol est marqué comme inactif.
Cette mise à jour du statut s'applique également aux billets associés, les marquant comme inactifs et annulant leur statut.
Enfin, elle assure la cohérence de l'état du PNR lié au billet.

**6. Extensions possibles**

Cette fonction pourrait être étendue pour gérer d'autres cas d'utilisation spécifiques aux segments de vol ou pour inclure davantage de données dans la mise à jour.
Vous pourriez envisager d'ajouter des mécanismes de journalisation pour conserver un historique des mises à jour de statut.
Pour une utilisation plus avancée, l'intégration de notifications en cas de mise à jour de statut pourrait être envisagée pour informer les parties concernées.
L'ajout de règles de gestion spécifiques pour différents types de vols ou de billets pourrait rendre cette fonction encore plus polyvalente.
En fonction de vos besoins, une intégration plus étroite avec d'autres parties du système de réservation pourrait être envisagée.

**7. Codes**
```python
# update air segments status on new segments
# Mise à jour du statut des segments de vol pour les nouveaux segments
# À placer avant l'insertion des segments

def update_segment_status(self, pnr, new_segments):
    # Cette fonction prend en charge la mise à jour du statut des segments de vol en fonction des nouveaux segments fournis.

    # Paramètres :
    # - self: L'instance de la classe qui appelle la fonction.
    # - pnr: L'objet PNR auquel appartiennent les segments.
    # - new_segments: Les nouveaux segments de vol à prendre en compte pour la mise à jour.

    if len(new_segments) > 0:
        # Récupération des segments de vol existants liés au PNR.
        old_segments = pnr.segments.all()
        old_segments_data = []

        # Parcours des anciens segments pour collecter leurs données pertinentes.
        for segment in old_segments:
            temp_data = {}
            temp_data['segment_obj'] = segment
            temp_data['data'] = (
                # (segment.segmentorder if segment.segmentorder is not None else '') + \
                (segment.flightno if segment.flightno is not None else '') + \
                (str(segment.departuretime) if segment.departuretime is not None else '') + \
                (str(segment.arrivaltime) if segment.arrivaltime is not None else '') + \
                (segment.flightclass if segment.flightclass is not None else '')
            )
            old_segments_data.append(temp_data)

        new_segments_data = []

        # Parcours des nouveaux segments pour collecter leurs données pertinentes.
        for new_segment in new_segments:
            # (new_segment.segmentorder if new_segment.segmentorder is not None else '') + \
            new_segments_data.append(
                (new_segment.flightno if new_segment.flightno is not None else '') + \
                (str(new_segment.departuretime) if new_segment.departuretime is not None else '') + \
                (str(new_segment.arrivaltime) if new_segment.arrivaltime is not None else '') + \
                (new_segment.flightclass if new_segment.flightclass is not None else '')
            )

        # Parcours des anciennes données de segments.
        for old_data in old_segments_data:
            # Vérification si les données de l'ancien segment ne sont pas présentes dans les nouvelles données.
            if old_data['data'] not in new_segments_data:
                # Mise à jour du statut du segment de vol à 0 (inactif).
                old_data['segment_obj'].air_segment_status = 0
                old_data['segment_obj'].save()

                # Récupération des billets liés à ce segment.
                related_ticket_segments = old_data['segment_obj'].tickets.all()

                # Parcours des billets associés pour mettre à jour leur statut et leur état.
                for related_ticket in related_ticket_segments:
                    temp_ticket = related_ticket.ticket
                    temp_ticket.state = 0
                    temp_ticket.ticket_status = 3
                    temp_ticket.save()

                    # Mise à jour de l'état du PNR en fonction des billets.
                    temp_ticket.update_pnr_state(pnr)

        # Affichage des anciennes données et des nouvelles données à des fins de débogage.
        print('OLD_DATA: ', old_segments_data)
        print('NEW_DATA: ', new_segments_data)
```