const { exec } = require('child_process');

// Lancer la commande 'node server.js'
const child = exec('node pnr_unordering.js');

// Gérer la sortie de la commande
child.stdout.on('data', (data) => {
    console.log(`Sortie standard : ${data}`);
});

child.stderr.on('data', (data) => {
    console.error(`Sortie d'erreur : ${data}`);
});