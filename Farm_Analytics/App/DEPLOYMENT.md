# Guida al Deployment su Render

## Configurazione delle Variabili d'Ambiente

Per far funzionare correttamente la dashboard su Render, è necessario configurare le seguenti variabili d'ambiente:

### Variabili Richieste

1. **DB_HOST**: L'host del database MySQL
2. **DB_PORT**: La porta del database (default: 3306)
3. **DB_USER**: Il nome utente del database
4. **DB_PASSWORD**: La password del database
5. **DB_NAME**: Il nome del database

### Come Configurare su Render

1. Vai al dashboard di Render
2. Seleziona il tuo servizio
3. Vai alla sezione "Environment"
4. Aggiungi le seguenti variabili:

```
DB_HOST=your_database_host
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

### Esempio di Configurazione

Se stai usando un database MySQL su un servizio cloud come PlanetScale, AWS RDS, o Google Cloud SQL:

```
DB_HOST=your-instance.region.provider.com
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_secure_password
DB_NAME=farm_analytics
```

### Verifica della Configurazione

Dopo aver configurato le variabili d'ambiente:

1. Riavvia il servizio su Render
2. Controlla i log per eventuali errori di connessione
3. Verifica che la dashboard mostri i dati correttamente

### Risoluzione Problemi

Se la dashboard mostra "Data not Available":

1. Verifica che le variabili d'ambiente siano configurate correttamente
2. Controlla che il database sia accessibile da Render
3. Verifica che le tabelle `production_data` e `consumption_data` esistano nel database
4. Controlla i log di Render per errori di connessione

### Database Locale per Test

Per testare localmente, crea un file `.env` nella directory `App/` con:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_local_password
DB_NAME=farm_analytics
```
