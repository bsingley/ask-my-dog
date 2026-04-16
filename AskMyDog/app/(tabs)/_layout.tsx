import { Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Tabs } from 'expo-router';
import React from 'react';
import { HapticTab } from '@/components/haptic-tab';
import { Ionicons } from '@expo/vector-icons';
import { useColorScheme } from '@/hooks/use-color-scheme';
import { requestNotificationPermission, scheduleDogTagNotifications } from '../notifications';
import * as Notifications from 'expo-notifications';
import { useDog, setDogTagMessage, loadDog, loadAchievements } from '../../store';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const insets = useSafeAreaInsets();

  const [dog] = useDog();
  React.useEffect(() => { loadDog(); }, []);
  React.useEffect(() => { loadAchievements(); }, []);

  React.useEffect(() => {
    requestNotificationPermission().then(granted => {
      if (granted) scheduleDogTagNotifications(dog.name);
    });

    const subscription = Notifications.addNotificationResponseReceivedListener(response => {
      const message = response.notification.request.content.data?.dogTagMessage;
      if (message) setDogTagMessage(String(message));
    });

    return () => subscription.remove();
  }, []);

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#2B3A4A',
        tabBarInactiveTintColor: '#C4A882',
        tabBarStyle: { 
          backgroundColor: '#F5EFE6', 
          borderTopColor: '#C4A882', 
          borderTopWidth: 0.5,
          height: Platform.OS === 'android' ? 120 : 70,
          paddingBottom: Platform.OS === 'android' ? 65 : 10,
          paddingTop: 8,
        },
        tabBarLabelStyle: { fontSize: 14, fontWeight: '600', marginTop: 2 },
        headerShown: false,
        tabBarButton: HapticTab,
      }}>
      <Tabs.Screen
        name="explore"
        options={{
          title: 'My Dog',
          tabBarIcon: ({ color }) => <Ionicons size={26} name="paw" color={color} />,
        }}
      />
      <Tabs.Screen
        name="index"
        options={{
          title: 'Chat',
          tabBarIcon: ({ color }) => <Ionicons size={26} name="chatbubbles" color={color} />,
        }}
      />
      <Tabs.Screen
        name="about"
        options={{
          title: 'About',
          tabBarIcon: ({ color }) => <Ionicons size={26} name="information-circle" color={color} />,
        }}
      />
    </Tabs>
  );
}