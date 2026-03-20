import React from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, KeyboardAvoidingView, Platform, ImageBackground, Modal } from 'react-native';
import { useState, useRef } from 'react';
import { useDog } from '../../store';

const RAILWAY_URL = 'https://ask-my-dog-production.up.railway.app';

export default function HomeScreen() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dog] = useDog();
  const [drama, setDrama] = useState('high');
  const [style, setStyle] = useState('doggish');
  const [dramaOpen, setDramaOpen] = useState(false);
  const [styleOpen, setStyleOpen] = useState(false);
  const scrollRef = useRef(null);

  async function askDog() {
    if (!question.trim()) return;
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
      setHistory(prev => [...prev, {
        question: currentQuestion,
        response: data.dog_response,
        trainer: data.trainer_note,
        easter_egg: data.easter_egg,
      }]);
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
      <ImageBackground source={require('../../assets/images/header-bg.png')} style={styles.headerBg} resizeMode="cover">
        <View style={styles.headerOverlay}>
          <View style={styles.dogBadge}>
            <Text style={styles.dogBadgeEmoji}>🐶</Text>
          </View>
          <View>
            <Text style={styles.header}>Ask My Dog</Text>
            <Text style={styles.subheader}>Chatting with {dog.name}</Text>
            <View style={styles.identityBadge}>
              <Text style={styles.identityBadgeText}>🛡️ {dog.self_identity}</Text>
            </View>
          </View>
        </View>
      </ImageBackground>
    <View style={styles.controlRow}>
      <View style={styles.controlGroup}>
        <Text style={styles.controlLabel}>🎭 Drama level</Text>
        <TouchableOpacity style={styles.dropdownButton} onPress={() => setDramaOpen(true)}>
          <Text style={styles.dropdownButtonText}>
            {['😴 Low','😏 Moderate','😤 High','🤯 Extreme'][['low','moderate','high','extreme'].indexOf(drama)]}
          </Text>
          <Text style={styles.dropdownArrow}>▾</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.controlGroup}>
        <Text style={styles.controlLabel}>🎨 Style</Text>
        <TouchableOpacity style={styles.dropdownButton} onPress={() => setStyleOpen(true)}>
          <Text style={styles.dropdownButtonText}>
            {['🐾 Doggish Dog','🎬 Sitcom Dog','📖 Shakespearean Dog','🎮 RPG Hero Dog','🎵 Snoop Dogg Dog'][['doggish','sitcom','shakespearean','rpg','snoop'].indexOf(style)]}
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
          {[['doggish','🐾 Doggish Dog'],['sitcom','🎬 Sitcom Dog'],['shakespearean','📖 Shakespearean Dog'],['rpg','🎮 RPG Hero Dog'],['snoop','🎵 Snoop Dogg Dog']].map(([val, label]) => (
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
        />
        <TouchableOpacity style={styles.button} onPress={askDog}>
          <Text style={styles.buttonText}>Ask</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafffe', paddingTop: 0 },
  headerBg: { width: '100%' },
  headerOverlay: { backgroundColor: 'rgba(8,80,65,0.5)', padding: 16, paddingTop: 56, flexDirection: 'row', alignItems: 'center', gap: 12 },
  dogBadge: { width: 54, height: 54, borderRadius: 16, backgroundColor: '#1D9E75', borderWidth: 2, borderColor: '#5DCAA5', alignItems: 'center', justifyContent: 'center' },
  dogBadgeEmoji: { fontSize: 26 },
  header: { fontSize: 20, fontWeight: '600', color: '#E1F5EE' },
  subheader: { fontSize: 12, color: '#9FE1CB', marginTop: 2 },
  identityBadge: { backgroundColor: 'rgba(0,0,0,0.25)', borderRadius: 20, paddingHorizontal: 9, paddingVertical: 3, alignSelf: 'flex-start', marginTop: 6 },
  identityBadgeText: { fontSize: 10, color: '#E1F5EE', fontWeight: '500' },
  controlRow: { flexDirection: 'row', paddingHorizontal: 12, paddingVertical: 8, gap: 8, backgroundColor: '#f8fdfa', borderBottomWidth: 0.5, borderColor: '#9FE1CB' },
  controlGroup: { flex: 1 },
  controlLabel: { fontSize: 10, fontWeight: '600', color: '#0F6E56', marginBottom: 4, textTransform: 'uppercase', letterSpacing: 0.5 },
  chat: { flex: 1, padding: 12, backgroundColor: '#fafffe' },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#1D9E75', borderRadius: 15, borderBottomRightRadius: 4, padding: 10, marginBottom: 6, maxWidth: '80%' },
  userText: { color: 'white', fontSize: 14 },
  dogBubble: { alignSelf: 'flex-start', backgroundColor: '#E1F5EE', borderRadius: 15, borderBottomLeftRadius: 4, padding: 10, maxWidth: '80%' },
  dogText: { fontSize: 14, color: '#085041' },
  trainerText: { fontSize: 11, color: '#0F6E56', marginTop: 6, fontStyle: 'italic', borderLeftWidth: 2, borderColor: '#5DCAA5', paddingLeft: 6 },
  achievementText: { fontSize: 12, color: '#E1F5EE', fontWeight: '600', marginTop: 6, backgroundColor: '#1D9E75', borderRadius: 20, paddingHorizontal: 10, paddingVertical: 3, alignSelf: 'flex-start' },
  inputRow: { flexDirection: 'row', padding: 12, borderTopWidth: 0.5, borderColor: '#9FE1CB', backgroundColor: '#fff' },
  input: { flex: 1, backgroundColor: '#f8fdfa', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, fontSize: 14, borderWidth: 0.5, borderColor: '#9FE1CB', color: '#085041' },
  button: { marginLeft: 8, backgroundColor: '#1D9E75', borderRadius: 20, paddingHorizontal: 20, justifyContent: 'center' },
  buttonText: { color: 'white', fontWeight: '600' },
  chip: {}, chipActive: {}, chipText: {},
  dogRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 8, marginBottom: 6 },
  dogAvatar: { width: 28, height: 28, borderRadius: 14, backgroundColor: '#1D9E75', alignItems: 'center', justifyContent: 'center', flexShrink: 0 },
  dogAvatarEmoji: { fontSize: 14 },
  dropdownButton: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: '#fff', borderWidth: 0.5, borderColor: '#5DCAA5', borderRadius: 8, paddingHorizontal: 10, paddingVertical: 7 },
  dropdownButtonText: { fontSize: 11, color: '#085041', flex: 1 },
  dropdownArrow: { fontSize: 12, color: '#1D9E75', marginLeft: 4 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', alignItems: 'center' },
  modalBox: { backgroundColor: '#fff', borderRadius: 16, padding: 16, width: 260, borderWidth: 0.5, borderColor: '#5DCAA5' },
  modalTitle: { fontSize: 13, fontWeight: '600', color: '#085041', marginBottom: 12 },
  modalOption: { paddingVertical: 10, paddingHorizontal: 12, borderRadius: 8, marginBottom: 4 },
  modalOptionActive: { backgroundColor: '#1D9E75' },
  modalOptionText: { fontSize: 14, color: '#085041' },
  modalOptionTextActive: { color: '#fff', fontWeight: '500' },
});