## La méthode insertAdjacentHTML()

Si votre application plante parce que le code ajoute le client dans la dernière position de la liste, et qu'il y a déjà beaucoup de clients dans la liste select__customersList, vous pouvez éviter cela en utilisant la méthode insertAdjacentHTML() au lieu de innerHTML.

La méthode insertAdjacentHTML() permet d'insérer du HTML à un emplacement spécifique à l'intérieur de l'élément sans toucher à son contenu actuel. Vous pouvez utiliser la valeur "afterbegin" pour insérer le nouvel élément au début de la liste.

Voici comment modifier votre code pour insérer le client en première position de la liste :

```javascript
if (response) {
  await new Promise(resolve => setTimeout(resolve, 0));
  select__customersList.insertAdjacentHTML('afterbegin', `
    <option value=${response.clientId} selected="true"> ${response.clientIntitule} </option>
  `);
}
```

Dans ce nouveau code, nous avons remplacé l'utilisation de innerHTML par insertAdjacentHTML(). Nous avons passé la chaîne de caractères qui représente l'élément HTML que nous voulons ajouter comme deuxième argument. Nous avons également passé la valeur "afterbegin" comme premier argument pour indiquer que nous souhaitons insérer le nouvel élément au début de la liste.

En utilisant cette approche, nous pouvons insérer le nouvel élément au début de la liste sans avoir besoin de changer le contenu complet de la liste. Cela peut être utile lorsque la liste contient déjà beaucoup d'éléments et que le changement fréquent de l'ensemble de la liste peut ralentir les performances de l'application.

## La méthode event.target.closest(selector) :

Exemple avec un menu de navigation :
Supposons que vous ayez un menu de navigation avec des liens et que vous souhaitiez détecter si l'utilisateur a cliqué en dehors du menu pour le fermer. Vous pouvez utiliser la méthode event.target.closest(selector) pour vérifier si l'élément cliqué se trouve en dehors du menu. Voici un exemple :
```js
document.addEventListener('click', function(event) {
  var menu = document.querySelector('#menu');
  if (menu && !event.target.closest('#menu')) {
    // L'élément cliqué se trouve en dehors du menu, fermer le menu ici
    menu.classList.remove('open');
  }
});
```

Exemple avec une boîte de dialogue modale :
Supposons que vous ayez une boîte de dialogue modale et que vous souhaitiez détecter si l'utilisateur a cliqué en dehors de la boîte pour la fermer. Utilisez la méthode event.target.closest(selector) pour vérifier si l'élément cliqué se trouve en dehors de la boîte modale. Voici un exemple :
```js
document.addEventListener('click', function(event) {
  var modal = document.querySelector('#modal');
  if (modal && !event.target.closest('#modal')) {
    // L'élément cliqué se trouve en dehors de la boîte modale, fermer la boîte modale ici
    modal.style.display = 'none';
  }
});
```
Exemple avec une liste déroulante :
Supposons que vous ayez une liste déroulante personnalisée et que vous souhaitiez la fermer lorsque l'utilisateur clique en dehors de la liste. Utilisez la méthode event.target.closest(selector) pour vérifier si l'élément cliqué se trouve en dehors de la liste déroulante. Voici un exemple :
```js
document.addEventListener('click', function(event) {
  var dropdown = document.querySelector('.dropdown');
  if (dropdown && !event.target.closest('.dropdown')) {
    // L'élément cliqué se trouve en dehors de la liste déroulante, fermer la liste déroulante ici
    dropdown.classList.remove('open');
  }
});
```
Ces exemples illustrent comment utiliser la méthode event.target.closest(selector) pour détecter les clics en dehors d'un élément spécifique et effectuer des actions en conséquence. N'oubliez pas d'adapter le sélecteur CSS (selector) à votre structure HTML et aux éléments que vous souhaitez cibler.