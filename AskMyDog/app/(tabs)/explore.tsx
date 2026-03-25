import { useState, useEffect, useCallback } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, Alert, Modal, FlatList } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { useDog } from '../../store';
import Slider from '@react-native-community/slider';
import { Ionicons } from '@expo/vector-icons';


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

const identityDescriptions: Record<string, string> = {
  'The Last Guardian': 'Ancient protector of the household. Every bark is a battle cry.',
  'Apex Predator': 'At the top of the food chain. Tolerating humans as useful allies. For now.',
  'The Chosen One': 'Prophesied to defeat the vacuum cleaner and unite the yard.',
  'Exiled Royalty': 'Once ruled a great kingdom. Currently plotting a return from the couch.',
  'Escape Artist': 'No fence has ever held them. Freedom is a lifestyle.',
  'I Was Framed': 'Did not chew the couch. Has never done anything wrong. Ever.',
  'Undercover Agent': 'Deep cover operative. The mission is classified.',
  'Evil Genius': 'Every stolen sock is part of an elaborate plan. The humans suspect nothing.',
  'Chaos Incarnate': 'Not malicious. Simply a force of nature that cannot be reasoned with.',
};

export default function PersonaScreen() {
  const [dog, setDog] = useDog();
  const [name, setName] = useState(dog.name);
  const [breed, setBreed] = useState(dog.breed);
  const [age, setAge] = useState(dog.age);
  const [nemesis, setNemesis] = useState(dog.nemesis);
  const [intelligence, setIntelligence] = useState(dog.intelligence);
  const [identity, setIdentity] = useState(dog.self_identity);
  const [saved, setSaved] = useState(false);
  const [isDirty, setIsDirty] = useState(false);
  const [showIdentityPicker, setShowIdentityPicker] = useState(false);
  const [expanded, setExpanded] = useState(false);

useFocusEffect(
  useCallback(() => {
    return () => {
      if (isDirty) {
        Alert.alert(
          'Unsaved changes',
          "You have unsaved changes to your dog's persona. Save before leaving?",
          [
            { text: 'Save', onPress: () => save() },
            { text: 'Keep editing', style: 'cancel' },
            { text: 'Discard', style: 'destructive', onPress: () => setIsDirty(false) },
          ]
        );
      }
    };
  }, [isDirty])
);

function save() {
  setDog({ ...dog, name, breed, age, nemesis, intelligence, self_identity: identity });
  setSaved(true);
  setIsDirty(false);
  setTimeout(() => setSaved(false), 2000);
}

  return (
    <ScrollView style={styles.container}>
      <View style={styles.darkHeader}>
        <Text style={styles.pageTitle}>My Dog</Text>
        <Text style={styles.pageSubtitle}>Customize how your dog thinks and talks</Text>
      </View>

      <View style={styles.dogCard}>
        <View style={{ flex: 1 }}>
          <Text style={styles.dogSummaryName}>{name}</Text>
          <Text style={styles.dogSummaryDetail}>{breed}</Text>
          <Text style={styles.dogSummaryDetail}>{age}</Text>
          <Text style={styles.dogSummaryDetail}>Nemesis: {nemesis}</Text>
        </View>
        <TouchableOpacity onPress={() => setExpanded(!expanded)}>
          <Ionicons name={expanded ? 'close-outline' : 'create-outline'} size={22} color='#4A6278' />
        </TouchableOpacity>
      </View>

      {expanded && (
        <View style={styles.expandedFields}>
          <Text style={styles.label}>Name</Text>
          <TextInput style={styles.input} value={name} onChangeText={val => { setName(val); setIsDirty(true); }} />

          <Text style={styles.label}>Breed</Text>
          <TextInput style={styles.input} value={breed} onChangeText={val => { setBreed(val); setIsDirty(true); }} />

          <Text style={styles.label}>Age</Text>
          <TextInput style={styles.input} value={age} onChangeText={val => { setAge(val); setIsDirty(true); }} />

          <Text style={styles.label}>Nemesis</Text>
          <TextInput style={styles.input} value={nemesis} onChangeText={val => { setNemesis(val); setIsDirty(true); }} />
        </View>
      )}

      
      <View style={{ paddingHorizontal: 24 }}>
        <Text style={styles.label}>Intelligence</Text>
        <Text style={styles.intelligenceDesc}>
          {intelligence === 'genius' && '🧠 Plays 3D chess when you\'re not looking'}
          {intelligence === 'selective' && '😏 Knows exactly what you said. Chooses to ignore it.'}
          {intelligence === 'average' && '🤔 Definitely has a plan...probably.'}
          {intelligence === 'dim' && '😵 Frequently outwitted by furniture.'}
          {intelligence === 'very_dim' && '💫 Two brain cells fighting for third place'}
        </Text>
        <Slider
          style={{ width: '100%', height: 40 }}
          minimumValue={0}
          maximumValue={4}
          step={1}
          value={4 - intelligenceOptions.findIndex(o => o.value === intelligence)}
          onValueChange={val => { setIntelligence(intelligenceOptions[4 - val].value); setIsDirty(true); }}
          minimumTrackTintColor="#2B3A4A"
          maximumTrackTintColor="#C4A882"
          thumbTintColor="#2B3A4A"
        />
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 }}>
            <Text style={{ fontSize: 16, color: '#4A6278' }}>Very Dim</Text>
            <Text style={{ fontSize: 16, color: '#4A6278' }}>Genius</Text>
          </View>
        </View>

      <View style={styles.divider} />

      <View style={{ paddingHorizontal: 24 }}>
        <Text style={styles.label}>Self Identity</Text>
        {identity && (
          <Text style={styles.identityDesc}>{identityDescriptions[identity]}</Text>
        )}
        <TouchableOpacity style={styles.dropdownButton} onPress={() => setShowIdentityPicker(true)}>
          <Text style={styles.dropdownButtonText}>{identity}</Text>
          <Text style={styles.dropdownChevron}>▾</Text>
        </TouchableOpacity>
        

        <Modal visible={showIdentityPicker} transparent animationType="fade">
          <TouchableOpacity style={styles.modalOverlay} onPress={() => setShowIdentityPicker(false)}>
            <View style={styles.modalBox}>
              <FlatList
                data={identities}
                keyExtractor={item => item}
                renderItem={({ item }) => (
                  <TouchableOpacity
                    style={[styles.modalOption, item === identity && styles.modalOptionActive]}
                    onPress={() => { setIdentity(item); setIsDirty(true); setShowIdentityPicker(false); }}>
                    <Text style={[styles.modalOptionText, item === identity && styles.modalOptionTextActive]}>{item}</Text>
                    {item === identity && <Text style={styles.modalOptionText}>✓</Text>}
                  </TouchableOpacity>
                )}
              />
            </View>
          </TouchableOpacity>
        </Modal>
      </View>
      
      <View style={{ paddingHorizontal: 24 }}>
        <TouchableOpacity style={styles.saveButton} onPress={save}>
          <Text style={styles.saveText}>{saved ? '✅ Saved!' : 'Save Persona'}</Text>
        </TouchableOpacity>
      </View>

    </ScrollView> 
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5EFE6' },
  header: { fontSize: 26, fontWeight: '700', color: '#C4A882', marginBottom: 24 },
  label: { fontSize: 16, fontWeight: '600', color: '#4A6278', marginTop: 20, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  input: { backgroundColor: '#fff', borderRadius: 10, padding: 12, fontSize: 16, borderWidth: 0.5, borderColor: '#C4A882', color: '#2B3A4A' },
  chipRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: { backgroundColor: '#E8D5B7', borderRadius: 16, paddingHorizontal: 12, paddingVertical: 6, borderWidth: 0.5, borderColor: '#C4A882' },
  chipActive: { backgroundColor: '#2B3A4A', borderColor: '#2B3A4A' },
  chipText: { fontSize: 16, color: '#2B3A4A', fontWeight: '500' },
  chipTextActive: { fontSize: 16, color: '#F5EFE6', fontWeight: '500' },
  identityOption: { backgroundColor: '#E8D5B7', borderRadius: 10, paddingVertical: 8, paddingHorizontal: 12, borderWidth: 0.5, borderColor: '#C4A882', marginRight: 8, marginBottom: 8 },
  identityActive: { backgroundColor: '#2B3A4A', borderColor: '#2B3A4A' },
  identityText: { fontSize: 18, color: '#2B3A4A' },
  identityTextActive: { fontSize: 18, color: '#F5EFE6' },
  saveButton: { backgroundColor: '#2B3A4A', borderRadius: 20, padding: 16, alignItems: 'center', marginTop: 40, marginBottom: 32 },
  saveText: { color: '#F5EFE6', fontWeight: '600', fontSize: 20 },
  intelligenceDesc: { fontSize: 18, color: '#4A6278', fontStyle: 'italic', marginTop: 4, marginBottom: 4, paddingLeft: 4 },
  identityDesc: { fontSize: 18, color: '#4A6278', fontStyle: 'italic', marginTop: 10, paddingLeft: 4 },
  dropdownButton: { backgroundColor: '#F5EFE6', borderRadius: 10, borderWidth: 0.5, borderColor: '#C4A882', padding: 12, marginTop: 4, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  dropdownButtonText: { fontSize: 16, color: '#2B3A4A' },
  dropdownChevron: { fontSize: 16, color: '#4A6278' },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.3)', justifyContent: 'center', padding: 32 },
  modalBox: { backgroundColor: '#F5EFE6', borderRadius: 14, overflow: 'hidden', borderWidth: 0.5, borderColor: '#C4A882' },
  modalOption: { padding: 16, flexDirection: 'row', justifyContent: 'space-between', borderBottomWidth: 0.5, borderBottomColor: '#C4A882' },
  modalOptionActive: { backgroundColor: '#E8D5B7' },
  modalOptionText: { fontSize: 16, color: '#2B3A4A' },
  modalOptionTextActive: { fontWeight: '700' },
  dogSummaryName: { fontSize: 28, fontWeight: '700', color: '#4A6278', marginBottom: 2 },
  dogSummaryDetail: { fontSize: 18, color: '#4A6278', marginTop: 1 },
  expandedFields: { backgroundColor: '#EDE3D4', borderRadius: 12, padding: 14, marginTop: 4, borderWidth: 0.5, borderColor: '#C4A882' },
  dogCard: { flexDirection: 'row', alignItems: 'flex-start', paddingHorizontal: 24, paddingVertical: 16 },
  divider: { height: 0.5, backgroundColor: '#C4A882', marginTop: 28, marginBottom: 0, opacity: 0.6 },
  pageTitle: { fontSize: 30, fontWeight: '800', color: '#F5EFE6', marginBottom: 4 },
  pageSubtitle: { fontSize: 18, color: '#C4A882', marginBottom: 12, letterSpacing: 0.3 },
  darkHeader: { backgroundColor: '#2B3A4A', paddingHorizontal: 24, paddingTop: 100, paddingBottom: 20 },

});
  