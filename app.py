from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Configuration de la base de données
# db_host = 'bdd-postgresql.postgres.database.azure.com' # Adresse du serveur PostgreSQL Azure
# db_name = 'insee' # Nom de la base de données
# db_user = 'adminaz900'  # Nom d'utilisateur de la base de données
# db_password = 'greta-2023'  # Mot de passe de la base de données

# config via string de connexion
url = os.getenv("URL")

# Route pour le point d'API /test
@app.route('/coucou')
def coucou():
     return "<p>Hello, World!</p>"


@app.route('/test')
def get_insee_dept():
    try:
        # # Connexion à la base de données
        # connection = psycopg2.connect(
        #     host=db_host,
        #     database=db_name,
        #     user=db_user,
        #     password=db_password
        # )

        connection = psycopg2.connect(url)
        
        # Création d'un curseur pour exécuter les requêtes SQL
        cursor = connection.cursor()
        
        # Exécution d'une requête SELECT pour récupérer les éléments de la table 'insee_dept'
        query = "SELECT dep, cheflieu, \"Chef-lieu\", ncc, nccenr FROM insee_dept"
        cursor.execute(query)
        
        # Récupération des résultats
        results = cursor.fetchall()
        
        # Fermeture du curseur et de la connexion à la base de données
        cursor.close()
        connection.close()
        
        # Conversion des résultats en format JSON
        data = []
        for result in results:
            dep, cheflieu, chef_lieu, ncc, nccenr = result
            data.append({
                'dep': dep,
                'cheflieu': cheflieu,
                'Chef-lieu': chef_lieu,
                'ncc': ncc,
                'nccenr': nccenr
            })
        
        # Retourne les données en tant que réponse JSON
        return jsonify(data)
    
    except psycopg2.Error as e:
        # En cas d'erreur lors de la connexion à la base de données
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host= '0.0.0.0') # rajouter les hosts autorisés à se connecter a l'app en plus du localhost qui est par défaut
