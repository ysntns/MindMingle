import React, { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, ActivityIndicator, Platform, Dimensions, StatusBar, Image } from 'react-native';
import Slider from '@react-native-community/slider';
import axios from 'axios';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';

// API URL (Emülatör veya Gerçek Cihaz IP'si)
const API_URL = Platform.OS === 'android' ? 'http://10.0.2.2:8000/recommend' : 'http://localhost:8000/recommend';

const { width } = Dimensions.get('window');

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
      // Yapay gecikme (loading hissi için)
      setTimeout(() => {
        setResult(response.data);
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error(error);
      alert("Sunucuya bağlanılamadı. Backend'i kontrol edin.");
      setLoading(false);
    }
  };

  const getMoodIcon = (mood) => {
    switch (mood) {
      case 'Çok Mutlu': return 'emoticon-excited-outline';
      case 'Mutlu': return 'emoticon-happy-outline';
      case 'Keyifli': return 'emoticon-cool-outline';
      case 'Melankolik': return 'weather-partly-rainy'; // cloud-rain yerine weather-partly-rainy kullanıldı (MaterialCommunityIcons)
      case 'Üzgün': return 'emoticon-sad-outline';
      default: return 'emoticon-neutral-outline';
    }
  };

  const getMoodColor = (mood) => {
    switch (mood) {
      case 'Çok Mutlu': return '#FFD700'; // Gold
      case 'Mutlu': return '#4CAF50'; // Green
      case 'Keyifli': return '#2196F3'; // Blue
      case 'Melankolik': return '#9C27B0'; // Purple
      case 'Üzgün': return '#607D8B'; // Blue Grey
      default: return '#4CAF50';
    }
  };

  const renderCustomSlider = (label, icon, value, setValue, minLabel, maxLabel) => (
    <View style={styles.sliderWrapper}>
      <View style={styles.labelRow}>
        <Ionicons name={icon} size={24} color="#333" style={{ marginRight: 10 }} />
        <Text style={styles.label}>{label}</Text>
        <Text style={styles.valueText}>{value}/10</Text>
      </View>
      <Slider
        style={{width: '100%', height: 40}}
        minimumValue={1}
        maximumValue={10}
        step={1}
        value={value}
        onValueChange={setValue}
        minimumTrackTintColor="#4CAF50"
        maximumTrackTintColor="#ddd"
        thumbTintColor="#2E7D32"
      />
      <View style={styles.minMaxRow}>
        <Text style={styles.minMaxText}>{minLabel}</Text>
        <Text style={styles.minMaxText}>{maxLabel}</Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1B5E20" />

      {/* HEADER */}
      <View style={styles.header}>
        <MaterialCommunityIcons name="brain" size={40} color="#fff" />
        <Text style={styles.headerTitle}>MindMingle</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContainer} showsVerticalScrollIndicator={false}>

        {!result ? (
          <View style={styles.introContainer}>
            <Text style={styles.introTitle}>Hoş Geldiniz 👋</Text>
            <Text style={styles.introText}>
              Bugün nasıl hissettiğinizi analiz edelim ve size en uygun film & müzik önerilerini sunalım.
            </Text>
          </View>
        ) : null}

        {/* FORM SECTION */}
        <View style={styles.card}>
          <Text style={styles.sectionHeader}>Duygu Durum Analizi</Text>
          {renderCustomSlider("Mutluluk", "happy-outline", feeling, setFeeling, "Düşük", "Yüksek")}
          {renderCustomSlider("Aktivite", "bicycle-outline", activity, setActivity, "Pasif", "Aktif")}
          {renderCustomSlider("Enerji", "battery-charging-outline", energy, setEnergy, "Yorgun", "Enerjik")}
          {renderCustomSlider("Sosyal", "people-outline", social, setSocial, "Yalnız", "Sosyal")}

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleAnalyze}
            disabled={loading}
            activeOpacity={0.8}
          >
            {loading ? (
              <ActivityIndicator color="#FFF" />
            ) : (
              <View style={{flexDirection: 'row', alignItems: 'center'}}>
                <MaterialCommunityIcons name="magic-staff" size={24} color="#fff" style={{marginRight: 8}} />
                <Text style={styles.buttonText}>TAVSİYE AL</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>

        {/* RESULTS SECTION */}
        {result && (
          <View style={[styles.resultSection, { borderColor: getMoodColor(result.mood) }]}>
            <View style={styles.moodHeader}>
              <MaterialCommunityIcons name={getMoodIcon(result.mood)} size={60} color={getMoodColor(result.mood)} />
              <View style={{marginLeft: 15}}>
                <Text style={styles.moodLabel}>Ruh Haliniz</Text>
                <Text style={[styles.moodResult, { color: getMoodColor(result.mood) }]}>{result.mood}</Text>
              </View>
            </View>

            <Text style={styles.recommendationTitle}>🎥 Film Önerileri</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
              {result.films.length > 0 ? (
                result.films.map((film, index) => (
                  <View key={index} style={styles.mediaCard}>
                    <View style={styles.mediaIconPlaceholder}>
                      <Ionicons name="film-outline" size={32} color="#fff" />
                    </View>
                    <Text style={styles.mediaTitle} numberOfLines={2}>{film.title}</Text>
                    <Text style={styles.mediaSubtitle} numberOfLines={1}>{film.listed_in}</Text>
                  </View>
                ))
              ) : <Text style={styles.noDataText}>Öneri bulunamadı.</Text>}
            </ScrollView>

            <Text style={styles.recommendationTitle}>🎵 Müzik Önerileri</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
              {result.songs.length > 0 ? (
                result.songs.map((song, index) => (
                  <View key={index} style={styles.mediaCard}>
                    <View style={[styles.mediaIconPlaceholder, { backgroundColor: '#1DB954' }]}>
                      <Ionicons name="musical-notes-outline" size={32} color="#fff" />
                    </View>
                    <Text style={styles.mediaTitle} numberOfLines={2}>{song.track_name}</Text>
                    <Text style={styles.mediaSubtitle} numberOfLines={1}>{song['artist(s)_name']}</Text>
                  </View>
                ))
              ) : <Text style={styles.noDataText}>Öneri bulunamadı.</Text>}
            </ScrollView>
          </View>
        )}

        <View style={{height: 50}} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F7FA',
  },
  header: {
    backgroundColor: '#2E7D32',
    height: 100,
    paddingTop: 40,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    elevation: 5,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowOffset: {width: 0, height: 2},
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginLeft: 10,
    letterSpacing: 1,
  },
  scrollContainer: {
    padding: 20,
  },
  introContainer: {
    marginBottom: 20,
    alignItems: 'center',
  },
  introTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  introText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
    shadowOffset: {width: 0, height: 2},
    marginBottom: 20,
  },
  sectionHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    paddingBottom: 10,
  },
  sliderWrapper: {
    marginBottom: 20,
  },
  labelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#444',
    flex: 1,
  },
  valueText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  minMaxRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 10,
  },
  minMaxText: {
    fontSize: 10,
    color: '#999',
  },
  button: {
    backgroundColor: '#2E7D32',
    paddingVertical: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 10,
    elevation: 3,
    shadowColor: '#2E7D32',
    shadowOpacity: 0.3,
    shadowOffset: {width: 0, height: 4},
  },
  buttonDisabled: {
    backgroundColor: '#A5D6A7',
  },
  buttonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  resultSection: {
    marginTop: 10,
    borderTopWidth: 5,
    backgroundColor: '#fff',
    borderRadius: 15,
    padding: 20,
    elevation: 4,
  },
  moodHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    padding: 15,
    backgroundColor: '#FAFAFA',
    borderRadius: 10,
  },
  moodLabel: {
    fontSize: 14,
    color: '#888',
  },
  moodResult: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  recommendationTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 15,
    marginBottom: 10,
    marginLeft: 5,
  },
  horizontalScroll: {
    marginBottom: 10,
  },
  mediaCard: {
    width: 140,
    marginRight: 15,
    backgroundColor: '#F5F5F5',
    borderRadius: 10,
    padding: 10,
  },
  mediaIconPlaceholder: {
    width: '100%',
    height: 100,
    backgroundColor: '#E53935', // Netflix Red default
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  mediaTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  mediaSubtitle: {
    fontSize: 11,
    color: '#666',
  },
  noDataText: {
    color: '#999',
    fontStyle: 'italic',
    marginLeft: 10,
  }
});
