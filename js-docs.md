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