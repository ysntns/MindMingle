import React, { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Alert, ActivityIndicator, Platform } from 'react-native';
import Slider from '@react-native-community/slider';
import axios from 'axios';

// Geliştirme ortamı için API URL'i.
// Android Emulator için 10.0.2.2, iOS Simulator için localhost kullanabilirsiniz.
// Gerçek cihazda test ediyorsanız bilgisayarınızın IP adresini yazın (örn: http://192.168.1.20:8000/recommend)
const API_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000/recommend' : 'http://localhost:8000/recommend';

export default function App() {
  const [feeling, setFeeling] = useState(5);
  const [activity, setActivity] = useState(5);
  const [energy, setEnergy] = useState(5);
  const [social, setSocial] = useState(5);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    try {
      const response = await axios.post(API_URL, {
        feeling,
        activity,
        energy,
        social
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      Alert.alert("Hata", "Sunucuya bağlanılamadı. Lütfen backend'in çalıştığından emin olun.");
    } finally {
      setLoading(false);
    }
  };

  const renderSlider = (label, value, setValue) => (
    <View style={styles.sliderContainer}>
      <Text style={styles.label}>{label}: {value}</Text>
      <Slider
        style={{width: '100%', height: 40}}
        minimumValue={1}
        maximumValue={10}
        step={1}
        value={value}
        onValueChange={setValue}
        minimumTrackTintColor="#4CAF50"
        maximumTrackTintColor="#000000"
        thumbTintColor="#4CAF50"
      />
    </View>
  );

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <Text style={styles.title}>MINDMINGLE</Text>
        <Text style={styles.subtitle}>Günlük Mental Durum Analizi</Text>

        <View style={styles.form}>
          {renderSlider("Mutluluk Seviyeniz", feeling, setFeeling)}
          {renderSlider("Günlük Aktivite", activity, setActivity)}
          {renderSlider("Enerji Seviyeniz", energy, setEnergy)}
          {renderSlider("Sosyal Etkileşim", social, setSocial)}

          <TouchableOpacity style={styles.button} onPress={handleAnalyze} disabled={loading}>
            {loading ? <ActivityIndicator color="#FFF" /> : <Text style={styles.buttonText}>ANALİZ ET VE TAVSİYE AL</Text>}
          </TouchableOpacity>
        </View>

        {result && (
          <View style={styles.resultContainer}>
            <Text style={styles.moodText}>Ruh Haliniz: <Text style={{fontWeight: 'bold', color: '#4CAF50'}}>{result.mood}</Text></Text>

            <Text style={styles.sectionTitle}>🎥 Önerilen Filmler</Text>
            {result.films.length > 0 ? (
              result.films.map((film, index) => (
                <View key={index} style={styles.itemCard}>
                  <Text style={styles.itemTitle}>{film.title}</Text>
                  <Text style={styles.itemSubtitle}>{film.listed_in}</Text>
                </View>
              ))
            ) : (
              <Text>Öneri bulunamadı.</Text>
            )}

            <Text style={styles.sectionTitle}>🎵 Önerilen Şarkılar</Text>
            {result.songs.length > 0 ? (
              result.songs.map((song, index) => (
                <View key={index} style={styles.itemCard}>
                  <Text style={styles.itemTitle}>{song.track_name}</Text>
                  <Text style={styles.itemSubtitle}>{song['artist(s)_name']}</Text>
                </View>
              ))
            ) : (
              <Text>Öneri bulunamadı.</Text>
            )}
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 50,
  },
  scrollContainer: {
    padding: 20,
    paddingBottom: 50,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#333',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    marginBottom: 30,
  },
  form: {
    backgroundColor: '#FFF',
    padding: 20,
    borderRadius: 10,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  sliderContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
    color: '#333',
  },
  button: {
    backgroundColor: '#4CAF50',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  resultContainer: {
    marginTop: 30,
  },
  moodText: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
    color: '#333',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    paddingBottom: 5,
  },
  itemCard: {
    backgroundColor: '#FFF',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#4CAF50',
  },
  itemTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  itemSubtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
});
