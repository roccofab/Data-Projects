#!/usr/bin/env python3
"""
Script di test per verificare che la dashboard funzioni correttamente
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.eda import eda_metrics as em
import pandas as pd

def test_data_availability():
    """Test per verificare la disponibilità dei dati"""
    print("🔍 Testando la disponibilità dei dati...")
    
    # Test dati di produzione
    print("\n📊 Testando dati di produzione...")
    prod_data = em.get_production_data()
    if prod_data.empty:
        print("❌ Dati di produzione non disponibili")
        return False
    else:
        print(f"✅ Dati di produzione disponibili: {len(prod_data)} righe")
        print(f"   Colonne: {list(prod_data.columns)}")
    
    # Test dati di consumo
    print("\n💰 Testando dati di consumo...")
    cons_data = em.get_consumption_data()
    if cons_data.empty:
        print("❌ Dati di consumo non disponibili")
        return False
    else:
        print(f"✅ Dati di consumo disponibili: {len(cons_data)} righe")
        print(f"   Colonne: {list(cons_data.columns)}")
    
    # Test dati meteo
    print("\n🌤️ Testando dati meteo...")
    weather_data = em.get_weather_data()
    if weather_data.empty:
        print("❌ Dati meteo non disponibili")
        return False
    else:
        print(f"✅ Dati meteo disponibili: {len(weather_data)} righe")
        print(f"   Colonne: {list(weather_data.columns)}")
    
    return True

def test_metrics_functions():
    """Test per verificare che le funzioni di metriche funzionino"""
    print("\n🧮 Testando funzioni di metriche...")
    
    try:
        # Test harvest_efficiency_per_year
        harvest_eff = em.harvest_efficiency_per_year()
        if harvest_eff.empty:
            print("❌ harvest_efficiency_per_year() restituisce DataFrame vuoto")
        else:
            print("✅ harvest_efficiency_per_year() funziona")
        
        # Test avg_yield_per_plant
        avg_yield = em.avg_yield_per_plant()
        if avg_yield.empty:
            print("❌ avg_yield_per_plant() restituisce DataFrame vuoto")
        else:
            print("✅ avg_yield_per_plant() funziona")
        
        # Test oil_yield_per_year
        oil_yield = em.oil_yield_per_year()
        if oil_yield.empty:
            print("❌ oil_yield_per_year() restituisce DataFrame vuoto")
        else:
            print("✅ oil_yield_per_year() funziona")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore durante il test delle funzioni: {e}")
        return False

def main():
    """Funzione principale di test"""
    print("🚀 Avvio test della dashboard...")
    
    # Test disponibilità dati
    data_available = test_data_availability()
    
    if not data_available:
        print("\n❌ Test fallito: Dati non disponibili")
        print("💡 Suggerimenti:")
        print("   1. Verifica la connessione al database")
        print("   2. Controlla le variabili d'ambiente")
        print("   3. Assicurati che le tabelle esistano nel database")
        return False
    
    # Test funzioni di metriche
    metrics_working = test_metrics_functions()
    
    if not metrics_working:
        print("\n❌ Test fallito: Funzioni di metriche non funzionano")
        return False
    
    print("\n✅ Tutti i test sono passati!")
    print("🎉 La dashboard dovrebbe funzionare correttamente")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
