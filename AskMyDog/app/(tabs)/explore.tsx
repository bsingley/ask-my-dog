import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet } from 'react-native';
import { useDog } from '../../store';

const identities = [
  'The Last Guardian',
  'Apex Predator',
  'The Chosen One',
  'Exiled Royalty',
  'Escape Artist',
  'I Was Framed',
  'Undercover Agent',
  'Evil Genius',
  'Chaos Incarnate',
];

const intelligenceOptions = [
  { label: 'Genius', value: 'genius' },
  { label: 'Selective', value: 'selective' },
  { label: 'Average', value: 'average' },
  { label: 'Dim', value: 'dim' },
  { label: 'Very Dim', value: 'very_dim' },
];

export default function PersonaScreen() {
  const [dog, setDog] = useDog();
  const [name, setName] = useState(dog.name);
  const [breed, setBreed] = useState(dog.breed);
  const [age, setAge] = useState(dog.age);
  const [nemesis, setNemesis] = useState(dog.nemesis);
  const [intelligence, setIntelligence] = useState(dog.intelligence);
  const [identity, setIdentity] = useState(dog.self_identity);
  const [saved, setSaved] = useState(false);

function save() {
  setDog({ ...dog, name, breed, age, nemesis, intelligence, self_identity: identity });
  setSaved(true);
  setTimeout(() => setSaved(false), 2000);
}

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.header}>🐾 Dog Persona</Text>

      <Text style={styles.label}>Name</Text>
      <TextInput style={styles.input} value={name} onChangeText={setName} />

      <Text style={styles.label}>Breed</Text>
      <TextInput style={styles.input} value={breed} onChangeText={setBreed} />

      <Text style={styles.label}>Age</Text>
      <TextInput style={styles.input} value={age} onChangeText={setAge} />

      <Text style={styles.label}>Nemesis</Text>
      <TextInput style={styles.input} value={nemesis} onChangeText={setNemesis} />

      <Text style={styles.label}>Intelligence</Text>
      <View style={styles.chipRow}>
        {intelligenceOptions.map(opt => (
          <TouchableOpacity
            key={opt.value}
            style={[styles.chip, intelligence === opt.value && styles.chipActive]}
            onPress={() => setIntelligence(opt.value)}>
            <Text style={styles.chipText}>{opt.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.label}>Self Identity</Text>
      {identities.map(id => (
        <TouchableOpacity
          key={id}
          style={[styles.identityOption, identity === id && styles.identityActive]}
          onPress={() => setIdentity(id)}>
          <Text style={styles.identityText}>{id}</Text>
        </TouchableOpacity>
      ))}

      <TouchableOpacity style={styles.saveButton} onPress={save}>
        <Text style={styles.saveText}>{saved ? '✅ Saved!' : 'Save Persona'}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff9f0', padding: 20, paddingTop: 60 },
  header: { fontSize: 24, fontWeight: 'bold', color: '#b05e2a', marginBottom: 20 },
  label: { fontSize: 13, fontWeight: '600', color: '#888', marginTop: 16, marginBottom: 4 },
  input: { backgroundColor: 'white', borderRadius: 10, padding: 12, fontSize: 15, borderWidth: 1, borderColor: '#ddd' },
  chipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: { backgroundColor: '#e0d0c0', borderRadius: 16, paddingHorizontal: 12, paddingVertical: 6 },
  chipActive: { backgroundColor: '#b05e2a' },
  chipText: { fontSize: 13, color: '#333' },
  identityOption: { backgroundColor: '#e0d0c0', borderRadius: 10, padding: 12, marginBottom: 6 },
  identityActive: { backgroundColor: '#b05e2a' },
  identityText: { fontSize: 14, color: '#333' },
  saveButton: { backgroundColor: '#b05e2a', borderRadius: 20, padding: 16, alignItems: 'center', marginTop: 30, marginBottom: 40 },
  saveText: { color: 'white', fontWeight: 'bold', fontSize: 16 },
});