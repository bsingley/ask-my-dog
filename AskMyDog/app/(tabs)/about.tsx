import { ScrollView, Text, TouchableOpacity, Linking, StyleSheet, View, Switch } from 'react-native';
import React, { useState, useEffect } from 'react';
import * as Notifications from 'expo-notifications';
import { scheduleDogTagNotifications } from '../notifications';
import { useDog } from '../../store';
import * as Print from 'expo-print';
import * as Sharing from 'expo-sharing';

export default function AboutScreen() {
    const [notificationsEnabled, setNotificationsEnabled] = useState(false);
    const [dog] = useDog();

    useEffect(() => {
        Notifications.getPermissionsAsync().then(({ status }) => {
        setNotificationsEnabled(status === 'granted');
        });
    }, []);

    async function toggleNotifications(value: boolean) {
        if (value) {
        const { status } = await Notifications.requestPermissionsAsync();
        if (status === 'granted') {
            await scheduleDogTagNotifications(dog.name);
            setNotificationsEnabled(true);
        }
        } else {
        await Notifications.cancelAllScheduledNotificationsAsync();
        setNotificationsEnabled(false);
        }
    }

return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>

        <Text style={styles.heading}>🐾 Ask My Dog</Text>
        <Text style={styles.version}>Version {require('../../app.json').expo.version}</Text>

        <Text style={styles.tribute}>
            Made for Luna, who is the scruffiest, most dramatic lab mix in the world.
            She didn't help build this app at all, but she supervised from the couch.
        </Text>

        <View style={styles.divider} />

        <View style={styles.dogTagsBox}>
            <View style={styles.toggleRow}>
                <View style={{ flex: 1, marginRight: 12 }}>
                    <Text style={styles.toggleLabel}>Notifications</Text>
                    <Text style={styles.toggleSub}>Dog Tags 🐾 </Text>
                    <Text style={styles.toggleSub}>
                    {notificationsEnabled
                    ? `${dog.name} will send you app notifications a few times a week with an update from the field.`
                    : `Get occasional app notifications from ${dog.name}. No spam — just a few times a week.`}
                </Text>
                </View>
                <Switch
                value={notificationsEnabled}
                onValueChange={toggleNotifications}
                trackColor={{ false: '#C4A882', true: '#2B3A4A' }}
                thumbColor={'#F5EFE6'}
                />
          </View>
          <Text style={styles.dogTagsExample}>
            {`"I have been watching the door for 4 hours. No one has come. I am filing a report."`}
          </Text>
        </View>

        <View style={styles.divider} />

        <TouchableOpacity style={styles.button} onPress={() => Linking.openURL('mailto:beth.singley@gmaill.com?subject=Ask My Dog Feedback')}>
            <Text style={styles.buttonText}>💌 Send Feedback</Text>
        </TouchableOpacity>

        <View style={styles.divider} />

        <TouchableOpacity onPress={() => Linking.openURL('https://bsingley.github.io/ask-my-dog/privacy-policy.md')}>
            <Text style={styles.link}>Privacy Policy</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => Linking.openURL('https://bsingley.github.io/ask-my-dog/terms.md')}>
            <Text style={styles.link}>Terms of Use</Text>
        </TouchableOpacity>
        <Text style={styles.copyright}>© 2026 Beth Singley. All rights reserved.</Text>


    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F5EFE6' },
  content: { padding: 32, alignItems: 'center' },
  heading: { fontSize: 28, fontWeight: '700', color: '#2B3A4A', marginTop: 48, marginBottom: 6 },
  version: { fontSize: 14, color: '#4A6278', marginBottom: 24 },
  tribute: { fontSize: 15, color: '#4A6278', textAlign: 'center', lineHeight: 22, marginBottom: 24 },
  divider: { width: '80%', height: 0.5, backgroundColor: '#C4A882', marginVertical: 24 },
  button: { backgroundColor: '#2B3A4A', borderRadius: 12, paddingVertical: 14, paddingHorizontal: 32, marginBottom: 12, width: '100%', alignItems: 'center' },
  buttonText: { color: '#F5EFE6', fontSize: 16, fontWeight: '600' },
  link: { color: '#4A6278', fontSize: 13, marginBottom: 12, textDecorationLine: 'underline' },
  copyright: { fontSize: 12, color: '#C4A882', marginTop: 24, textAlign: 'center' },
  toggleRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', marginBottom: 8 },
  toggleLabel: { fontSize: 18, fontWeight: '600', color: '#2B3A4A', marginBottom: 10 },
  toggleSub: { fontSize: 16, color: '#4A6278', marginBottom: 6 },
  dogTagsBox: { width: '100%', backgroundColor: '#E8D5B7', borderRadius: 12, padding: 16, marginBottom: 8 },
  dogTagsExample: { fontSize: 13, color: '#4A6278', fontStyle: 'italic', marginTop: 10, lineHeight: 18 },
});