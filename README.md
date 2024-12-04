# oupoco-api

API for the [Oupoco](https://oupoco.org) project  

Based on the work done by Mylène Maignant during her internship in Lattice lab (summer 2018).


## Utilisation

- en local

`python generation_sonnets.py`

- api en local

`flask --app app run`

- avec docker

  1. construire l’image

  `docker build -t oupoco_api .`
  
  2. lancer le container avec docker-compose

  `docker compose rm`  
  `docker compose up`
  
