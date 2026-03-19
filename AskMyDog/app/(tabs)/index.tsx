import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, KeyboardAvoidingView, Platform } from 'react-native';
import { useDog } from '../../store';
import { useState, useRef } from 'react';

const RAILWAY_URL = 'https://ask-my-dog-production.up.railway.app';

export default function HomeScreen() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dog] = useDog();
  const [drama, setDrama] = useState('high');
  const [style, setStyle] = useState('doggish');
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
      <Text style={styles.header}>🐾 Ask My Dog</Text>
      <Text style={styles.subheader}>Chatting with {dog.name}</Text>
      <View style={styles.controlRow}>
        <TouchableOpacity style={[styles.chip, drama === 'low' && styles.chipActive]} onPress={() => setDrama('low')}>
          <Text style={styles.chipText}>🐾 Low</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, drama === 'moderate' && styles.chipActive]} onPress={() => setDrama('moderate')}>
          <Text style={styles.chipText}>🐕 Moderate</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, drama === 'high' && styles.chipActive]} onPress={() => setDrama('high')}>
          <Text style={styles.chipText}>👑 High</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, drama === 'extreme' && styles.chipActive]} onPress={() => setDrama('extreme')}>
          <Text style={styles.chipText}>🦸 Extreme</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.controlRow}>
        <TouchableOpacity style={[styles.chip, style === 'doggish' && styles.chipActive]} onPress={() => setStyle('doggish')}>
          <Text style={styles.chipText}>🐾 Doggish</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, style === 'sitcom' && styles.chipActive]} onPress={() => setStyle('sitcom')}>
          <Text style={styles.chipText}>🎬 Sitcom</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, style === 'shakespearean' && styles.chipActive]} onPress={() => setStyle('shakespearean')}>
          <Text style={styles.chipText}>📖 Shakespeare</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, style === 'rpg' && styles.chipActive]} onPress={() => setStyle('rpg')}>
          <Text style={styles.chipText}>🎮 RPG</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.chip, style === 'snoop' && styles.chipActive]} onPress={() => setStyle('snoop')}>
          <Text style={styles.chipText}>🎵 Snoop</Text>
        </TouchableOpacity>
      </View>
        <ScrollView style={styles.chat} ref={scrollRef} onContentSizeChange={() => scrollRef.current?.scrollToEnd({ animated: true })}>        
            {history.map((entry, i) => (
          <View key={i}>
            <View style={styles.userBubble}>
              <Text style={styles.userText}>{entry.question}</Text>
            </View>
            <View style={styles.dogBubble}>
              <Text style={styles.dogText}>{entry.response}</Text>
              {entry.trainer ? <Text style={styles.trainerText}>🎓 {entry.trainer}</Text> : null}
              {entry.easter_egg ? <Text style={styles.achievementText}>🏆 Achievement Unlocked: {entry.easter_egg}</Text> : null}            </View>
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
  container: { flex: 1, backgroundColor: '#fff9f0', paddingTop: 60 },
  header: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 4, color: '#b05e2a' },
  subheader: { fontSize: 14, textAlign: 'center', color: '#888', marginBottom: 8 },
  chat: { flex: 1, padding: 16 },
  userBubble: { alignSelf: 'flex-end', backgroundColor: '#b05e2a', borderRadius: 16, padding: 12, marginBottom: 8, maxWidth: '80%' },
  userText: { color: 'white', fontSize: 15 },
  dogBubble: { alignSelf: 'flex-start', backgroundColor: '#f0e0cc', borderRadius: 16, padding: 12, marginBottom: 16, maxWidth: '80%' },
  dogText: { fontSize: 15, color: '#333' },
  trainerText: { fontSize: 12, color: '#888', marginTop: 6, fontStyle: 'italic' },
  inputRow: { flexDirection: 'row', padding: 12, borderTopWidth: 1, borderColor: '#e0d0c0' },
  input: { flex: 1, backgroundColor: 'white', borderRadius: 20, paddingHorizontal: 16, paddingVertical: 10, fontSize: 15, borderWidth: 1, borderColor: '#ddd' },
  button: { marginLeft: 8, backgroundColor: '#b05e2a', borderRadius: 20, paddingHorizontal: 20, justifyContent: 'center' },
  buttonText: { color: 'white', fontWeight: 'bold' },
  controlRow: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 12, marginBottom: 6, gap: 6 },
  chip: { backgroundColor: '#e0d0c0', borderRadius: 16, paddingHorizontal: 12, paddingVertical: 6 },
  chipActive: { backgroundColor: '#b05e2a' },
  chipText: { fontSize: 12, color: '#333' },
  achievementText: { fontSize: 13, color: '#b05e2a', fontWeight: 'bold', marginTop: 6 },
});