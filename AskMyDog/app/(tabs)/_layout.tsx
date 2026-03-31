import { Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Tabs } from 'expo-router';
import React from 'react';
import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { useColorScheme } from '@/hooks/use-color-scheme';

export default function TabLayout() {
  const colorScheme = useColorScheme();
  const insets = useSafeAreaInsets();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#2B3A4A',
        tabBarInactiveTintColor: '#C4A882',
        tabBarStyle: { 
          backgroundColor: '#F5EFE6', 
          borderTopColor: '#C4A882', 
          borderTopWidth: 0.5,
          height: Platform.OS === 'android' ? 100 : 70,
          paddingBottom: Platform.OS === 'android' ? 65 : 10,
          paddingTop: 8,
        },
        tabBarLabelStyle: { fontSize: 14, fontWeight: '600', marginTop: 2 },
        headerShown: false,
        tabBarButton: HapticTab,
      }}>
      <Tabs.Screen
        name="index"
        options={{
          title: 'Chat',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="bubble.left.and.bubble.right.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="explore"
        options={{
          title: 'My Dog',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="pawprint.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="about"
        options={{
          title: 'About',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="info.circle.fill" color={color} />,
        }}
      />
    </Tabs>
  );
}