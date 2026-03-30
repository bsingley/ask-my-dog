import React, { useState, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, KeyboardAvoidingView, Platform, ImageBackground, Modal, Image, Keyboard, Animated } from 'react-native';
import { useDog } from '../../store';
import * as StoreReview from 'expo-store-review';

const RAILWAY_URL = 'https://ask-my-dog-production.up.railway.app';

export default function HomeScreen() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState<{ question: string; response: string; trainer: string; easter_egg?: string }[]>([]);
  const [loading, setLoading] = useState(false);
  const [dog] = useDog();
  const [drama, setDrama] = useState('low');
  const [style, setStyle] = useState('doggish');
  const [dramaOpen, setDramaOpen] = useState(false);
  const [styleOpen, setStyleOpen] = useState(false);
  const scrollRef = useRef<ScrollView>(null);
  const headerHeight = useRef(new Animated.Value(260)).current;
  const [headerCollapsed, setHeaderCollapsed] = useState(false);

  function toggleHeader() {
    const toValue = headerCollapsed ? 260 : 80;
    Animated.timing(headerHeight, {
      toValue,
      duration: 300,
      useNativeDriver: false,
    }).start(() => setHeaderCollapsed(!headerCollapsed));
}      

  async function askDog() {
    if (!question.trim()) return;
    Keyboard.dismiss();
    setLoading(true);
    const currentQuestion = question;
    setQuestion('');

    try {
      const response = await fetch(`${RAILWAY_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: currentQuestion,
          dog: dog,
          drama: drama,
          style: style,
          history: history.slice(-3),
        }),
      });
      const data = await response.json();
      setHistory(prev => {
        const newHistory = [...prev, {
          question: currentQuestion,
          response: data.dog_response,
          trainer: data.trainer_note,
          easter_egg: data.easter_egg,
        }];
        if (newHistory.length === 5) {
          StoreReview.isAvailableAsync().then(available => {
            if (available) StoreReview.requestReview();
          });
        }
        return newHistory;
      });
    } catch (e) {
      console.log('Error:', e);
      setHistory(prev => [...prev, {
        question: currentQuestion,
        response: 'Woof... something went wrong.',
        trainer: '',
      }]);
    }
    setLoading(false);
  }

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
      <TouchableOpacity onPress={toggleHeader} activeOpacity={1}>
        <Animated.View style={[styles.headerBg, { height: headerHeight, overflow: 'hidden' }]}>
          <ImageBackground source={require('../../assets/images/dog-header.png')} style={{ width: '100%', height: 260 }} resizeMode="cover">        
            <View style={styles.headerOverlay}>
              <View style={styles.headerTextBlock}>
              <Text style={styles.header}>Ask My Dog</Text>
              <Text style={styles.subheader}>{dog.name}</Text>
                <View style={styles.identityBadge}>
                  <Text style={styles.identityBadgeText}>🛡️ {dog.self_identity}</Text>
                </View>
              </View>
            </View>
          </ImageBackground>
        </Animated.View>
      </TouchableOpacity>
    <View style={styles.controlRow}>
      <View style={styles.controlGroup}>
        <Text style={styles.controlLabel}>🎨 Style</Text>
        <TouchableOpacity style={styles.dropdownButton} onPress={() => setStyleOpen(true)}>
          <Text style={styles.dropdownButtonText}>
            {['🐾 Doggish Dog','🎬 Sitcom Dog','📖 Shakespeare Dog','🎮 RPG Hero Dog','🎵 Snoop Dogg Dog'][['doggish','sitcom','shakespeare','rpg','snoop'].indexOf(style)]}
          </Text>
          <Text style={styles.dropdownArrow}>▾</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.controlGroup}>
        <Text style={styles.controlLabel}>🎭 Drama level</Text>
        <TouchableOpacity style={styles.dropdownButton} onPress={() => setDramaOpen(true)}>
          <Text style={styles.dropdownButtonText}>
            {['😴 Low','😏 Moderate','😤 High','🤯 Extreme'][['low','moderate','high','extreme'].indexOf(drama)]}
          </Text>
          <Text style={styles.dropdownArrow}>▾</Text>
        </TouchableOpacity>
      </View>

    </View>

    <Modal visible={dramaOpen} transparent animationType="fade">
      <TouchableOpacity style={styles.modalOverlay} onPress={() => setDramaOpen(false)}>
        <View style={styles.modalBox}>
          <Text style={styles.modalTitle}>🎭 Drama level</Text>
          {[['low','😴 Low'],['moderate','😏 Moderate'],['high','😤 High'],['extreme','🤯 Extreme']].map(([val, label]) => (
            <TouchableOpacity key={val} style={[styles.modalOption, drama === val && styles.modalOptionActive]} onPress={() => { setDrama(val); setDramaOpen(false); }}>
              <Text style={[styles.modalOptionText, drama === val && styles.modalOptionTextActive]}>{label}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </TouchableOpacity>
    </Modal>
    <Modal visible={styleOpen} transparent animationType="fade">
      <TouchableOpacity style={styles.modalOverlay} onPress={() => setStyleOpen(false)}>
        <View style={styles.modalBox}>
          <Text style={styles.modalTitle}>🎨 Style</Text>
          {[['doggish','🐾 Doggish Dog'],['sitcom','🎬 Sitcom Dog'],['shakespeare','📖 Shakespeare Dog'],['rpg','🎮 RPG Hero Dog'],['snoop','🎵 Snoop Dogg Dog']].map(([val, label]) => (
            <TouchableOpacity key={val} style={[styles.modalOption, style === val && styles.modalOptionActive]} onPress={() => { setStyle(val); setStyleOpen(false); }}>
              <Text style={[styles.modalOptionText, style === val && styles.modalOptionTextActive]}>{label}</Text>
            </TouchableOpacity>
          ))}
      </View>
      </TouchableOpacity>
    </Modal>
      <ScrollView style={styles.chat} ref={scrollRef} onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}>        
            {history.map((entry, i) => (
          <View key={i}>
            <View style={styles.userBubble}>
              <Text style={styles.userText}>{entry.question}</Text>
            </View>
            <View style={styles.dogRow}>
              <View style={styles.dogAvatar}>
                <Text style={styles.dogAvatarEmoji}>🐶</Text>
              </View>
              <View style={styles.dogBubble}>
                <Text style={styles.dogText}>{entry.response}</Text>
                {entry.trainer ? <Text style={styles.trainerText}>🎓 {entry.trainer}</Text> : null}
                {entry.easter_egg ? <Text style={styles.achievementText}>🏆 Achievement Unlocked: {entry.easter_egg}
                </Text> : null}            
              </View>
            </View>
          </View>
        ))}
        {loading && <ActivityIndicator size="large" color="#b05e2a" style={{ margin: 20 }} />}
      </ScrollView>
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={question}
          onChangeText={setQuestion}
          placeholder="Ask your dog something..."
          onSubmitEditing={askDog}
          blurOnSubmit={true}
          returnKeyType="send"
        />        
        <TouchableOpacity style={styles.button} onPress={askDog}>
          <Text style={styles.buttonText}>Ask</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5EFE6', paddingTop: 0 },
  headerBg: { width: '100%' },
  headerOverlay: {
    height: 260,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'flex-start',
    paddingLeft: 28,
    paddingBottom: 24,
  },
  headerTextBlock: { flex: 1, paddingRight: 12 },
  header: { fontSize: 30, fontWeight: '700', color: '#2B3A4A' },
  subheader: { fontSize: 28, color: '#4A6278', marginTop: 6 },
  controlRow: { flexDirection: 'row', paddingHorizontal: 12, paddingVertical: 8, gap: 8, backgroundColor: '#F5EFE6', borderBottomWidth: 0.5, borderColor: '#C4A882' },
  controlGroup: { flex: 1 },
  controlLabel: { fontSize: 18, fontWeight: '600', color: '#4A6278', marginBottom: 4, textTransform: 'uppercase', letterSpacing: 0.5 },
  chat: { flex: 1, padding: 12, backgroundColor: '#F5EFE6' },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#2B3A4A', borderRadius: 15, borderBottomRightRadius: 4, padding: 10, marginBottom: 6, maxWidth: '80%' },
  userText: { color: '#F5EFE6', fontSize: 16 },
  dogBubble: { alignSelf: 'flex-start', backgroundColor: '#E8D5B7', borderRadius: 15, borderBottomLeftRadius: 4, padding: 10, maxWidth: '80%' },
  dogText: { fontSize: 16, color: '#2B3A4A' },
  trainerText: { fontSize: 14, color: '#4A6278', marginTop: 6, fontStyle: 'italic', borderLeftWidth: 2, borderColor: '#C4A882', paddingLeft: 6 },
  achievementText: { fontSize: 16, color: '#F5EFE6', fontWeight: '600', marginTop: 6, backgroundColor: '#2B3A4A', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 3, alignSelf: 'flex-start' },
  inputRow: { flexDirection: 'row', padding: 12, borderTopWidth: 0.5, borderColor: '#C4A882', backgroundColor: '#F5EFE6' },
  input: { flex: 1, backgroundColor: '#fff', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, fontSize: 16, borderWidth: 0.5, borderColor: '#C4A882', color: '#2B3A4A' },
  button: { marginLeft: 8, backgroundColor: '#2B3A4A', borderRadius: 20, paddingHorizontal: 20, justifyContent: 'center' },
  buttonText: { color: '#F5EFE6', fontWeight: '600', fontSize: 14 },
  chip: {}, chipActive: {}, chipText: {},
  dogRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 8, marginBottom: 6 },
  dogAvatar: { width: 28, height: 28, borderRadius: 14, backgroundColor: '#4A6278', alignItems: 'center', justifyContent: 'center', flexShrink: 0 },
  dogAvatarEmoji: { fontSize: 14 },
  dropdownButton: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#fff', borderWidth: 0.5, borderColor: '#C4A882', borderRadius: 8, paddingHorizontal: 10, paddingVertical: 7 },
  dropdownButtonText: { fontSize: 14, color: '#2B3A4A', flex: 1 },
  dropdownArrow: { fontSize: 12, color: '#4A6278', marginLeft: 4 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalBox: { backgroundColor: '#F5EFE6', borderRadius: 16, padding: 16, width: 260, borderWidth: 0.5, borderColor: '#C4A882' },
  modalTitle: { fontSize: 16, fontWeight: '600', color: '#2B3A4A', marginBottom: 12 },
  modalOption: { paddingVertical: 10, paddingHorizontal: 12, borderRadius: 8, marginBottom: 4 },
  modalOptionActive: { backgroundColor: '#2B3A4A' },
  modalOptionText: { fontSize: 14, color: '#2B3A4A' },
  modalOptionTextActive: { color: '#F5EFE6', fontWeight: '500' },
  identityBadge: { backgroundColor: 'rgba(0,0,0,0.25)', borderRadius: 20, paddingHorizontal: 9, paddingVertical: 3, alignSelf: 'flex-start', marginTop: 8 },
  identityBadgeText: { fontSize: 16, color: '#ffffff', fontWeight: '500' },
});