import { ScrollView, Text, TouchableOpacity, Linking, StyleSheet, View } from 'react-native';

export default function AboutScreen() {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>

        <Text style={styles.heading}>🐾 Ask My Dog</Text>
        <Text style={styles.version}>Version 1.0.0</Text>

        <Text style={styles.tribute}>
            Made for Luna, who is the scruffiest, most dramatic lab mix in the world.
            She didn't help build this app at all, but she supervised from the couch.
        </Text>

        <View style={styles.divider} />

        <TouchableOpacity style={styles.button} onPress={() => Linking.openURL('mailto:your@email.com?subject=Ask My Dog Feedback')}>
            <Text style={styles.buttonText}>💌 Send Feedback</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.button} onPress={() => Linking.openURL('https://venmo.com/u/Beth-Singley-1')}>
            <Text style={styles.buttonText}>🦴 Buy Luna a Treat</Text>
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

});