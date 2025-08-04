import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.Analysis.Reccomandation_Models import kmeans_reccomender, data_preprocessing
import pandas as pd
from flask import send_from_directory

app = Flask(__name__)
CORS(app)   #CORS(app) allows any browser to access the backend

@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(current_directory), 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(current_directory), path)

#get current directory path and build the path to the cleaned_data.csv file
current_directory = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_directory, '..', 'src', 'Data_Cleaning', 'cleaned_data.csv')
df = pd.read_csv(path)
df_norm = data_preprocessing(df)

def convert_normalized_price_to_original(normalized_price, df_original):
    """
    Convert normalized price back to original price format
    """
    # Get the original price range
    min_price = df_original['final_price'].min()
    max_price = df_original['final_price'].max()
    
    # Convert normalized price back to original scale
    original_price = normalized_price * (max_price - min_price) + min_price
    
    # Format to 2 decimal places
    return round(original_price, 2)

@app.route('/recommend', methods=['GET'])
def reccomend():
    asin = request.args.get('asin')  # get asin parameter
    num_recs = int(request.args.get('num_recs', 5)) 
    if not asin:
        return jsonify({'error': 'missing ASIN code'}), 400
    try:
        reccomendation = kmeans_reccomender(df_norm, asin, num_recs)
        if reccomendation.empty:
           return jsonify({'error': 'No similar books found or invalid ASIN'}), 200
        
        # Convert normalized prices back to original format
        for idx, row in reccomendation.iterrows():
            normalized_price = row['final_price']
            original_price = convert_normalized_price_to_original(normalized_price, df)
            reccomendation.at[idx, 'final_price'] = original_price
        
        result = reccomendation.to_dict(orient='records')
        return jsonify({'recommendation': result})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({'error': str(e)}), 500

# For production deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
    
    
    