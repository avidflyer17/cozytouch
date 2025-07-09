# Atlantic Cozytouch

Cette intégration Home Assistant se connecte au cloud **Cozytouch** d'Atlantic. Elle permet de contrôler les chaudières, pompes à chaleur et autres appareils compatibles avec le service Cozytouch (différent de l'intégration Overkiz officielle) 😊.

## Fonctionnalités

- Interrogation du cloud via l'API d'Atlantic ☁️
- Entités climatiques avec modes HVAC et ventilateur 🌡️
- Capteurs pour températures, puissance et valeurs de diagnostic 📊
- Entités de type nombre, sélection, horaire et interrupteur 🔘
- Programmation et gestion du mode absence 🗓️
- Journalisation JSON optionnelle pour le débogage 🐞
- Option pour créer des entités pour les capacités inconnues 🔍
- Gestion améliorée des erreurs de connexion 🔒

## Appareils pris en charge

L'intégration a été validée avec :
- **Atlantic Naema 2 Micro 25** chaudière gaz avec thermostat **Navilink Radio‑Connect 128**
- **Atlantic Naema 2 Duo 25** chaudière gaz avec thermostat **Navilink Radio‑Connect 128**
- **Atlantic Naia 2 Micro 25** chaudière gaz avec thermostat **Navilink Radio‑Connect 128**
- **Atlantic Loria Duo 6006 R32** pompe à chaleur avec thermostat **Navilink Radio‑Connect 128**
- **Takao M3** unité de climatisation
- **Kelud 1750W** sèche-serviettes
- **Sauter Asama Connecté II Ventilo 1750W** sèche-serviettes

Un mappage est requis pour chaque modèle. N'hésitez pas à ouvrir une issue pour prendre en charge d'autres appareils.

## Installation

Vous pouvez installer l'intégration via **HACS** ou manuellement.

### HACS

[![Add HACS repository.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=avidflyer17&repository=cozytouch&category=integration)

Plus d'informations à propos de HACS sont disponibles sur [hacs.xyz](https://hacs.xyz/).

### Manuel

Clonez ce dépôt et copiez `custom_components/cozytouch` dans votre dossier de configuration Home Assistant (par exemple : `config/custom_components/cozytouch`).

Redémarrez Home Assistant après avoir copié les fichiers 🔄.

## Configuration

1. Allez dans **Réglages → Appareils et services → Ajouter une intégration**.
2. Recherchez **Cozytouch** et sélectionnez **Atlantic Cozytouch**.
3. Saisissez vos identifiants Cozytouch 🔑.
4. Choisissez l'appareil que vous souhaitez configurer.
5. Activez éventuellement **Créer des entités pour les capacités inconnues** et **Générer un fichier JSON avec les données reçues** pour le débogage.

Si la connexion réussit, l'appareil sélectionné apparaîtra avec les entités disponibles ✅.

## Contribuer

Les issues et pull requests sont les bienvenues. Ouvrez une issue si votre appareil nécessite un mappage supplémentaire.
