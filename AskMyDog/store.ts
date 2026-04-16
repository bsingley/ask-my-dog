import React from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STORAGE_KEY = 'dog_profile';

const ACHIEVEMENTS_KEY = 'achievements';

export const ALL_EGGS = ['🐿️ Squirrel Brain', '🛁 The Ultimate Betrayal', '🐶 Bestest Doggo Ever', '😤 Pure Outrage'];

let achievements: string[] = [];
let achievementListeners: Array<(a: string[]) => void> = [];

export function getAchievements() {
  return achievements;
}

export async function loadAchievements() {
  try {
    const saved = await AsyncStorage.getItem(ACHIEVEMENTS_KEY);
    if (saved) {
      achievements = JSON.parse(saved);
      achievementListeners.forEach(fn => fn(achievements));
    }
  } catch (e) {
    console.log('Failed to load achievements:', e);
  }
}

export function unlockAchievement(name: string) {
  if (!achievements.includes(name)) {
    achievements = [...achievements, name];
    achievementListeners.forEach(fn => fn(achievements));
    AsyncStorage.setItem(ACHIEVEMENTS_KEY, JSON.stringify(achievements)).catch(e =>
      console.log('Failed to save achievements:', e)
    );
  }
}

export function useAchievements(): [string[], typeof unlockAchievement] {
  const [value, setValue] = React.useState(achievements);
  React.useEffect(() => {
    achievementListeners.push(setValue);
    return () => {
      achievementListeners = achievementListeners.filter(fn => fn !== setValue);
    };
  }, []);
  return [value, unlockAchievement];
}

export const defaultDog = {
  name: 'Luna',
  breed: 'lab mix',
  age: '10 months',
  personality_traits: ['curious', 'cautious', 'extremely intelligent'],
  fear_triggers: ['new objects', 'loud sounds'],
  nemesis: 'the vacuum cleaner',
  intelligence: 'average',
  self_identity: 'The Last Guardian',
  photo: 'dog_photo_1',
};

let dog = { ...defaultDog };
let listeners: Array<(d: typeof defaultDog) => void> = [];
let dogTagMessage: string | null = null;
let tagListeners: Array<(m: string | null) => void> = [];

export function setDogTagMessage(message: string | null) {
  dogTagMessage = message;
  tagListeners.forEach(fn => fn(message));
}

export function useDogTagMessage(): [string | null, typeof setDogTagMessage] {
  const [value, setValue] = React.useState(dogTagMessage);
  React.useEffect(() => {
    tagListeners.push(setValue);
    return () => {
      tagListeners = tagListeners.filter(fn => fn !== setValue);
    };
  }, []);
  return [value, setDogTagMessage];
}


export function getDog() {
  return dog;
}

export async function loadDog() {
  try {
    const saved = await AsyncStorage.getItem(STORAGE_KEY);
    if (saved) {
      dog = { ...defaultDog, ...JSON.parse(saved) };
      listeners.forEach(fn => fn(dog));
    }
  } catch (e) {
    console.log('Failed to load dog profile:', e);
  }
}

export function setDog(newDog: typeof defaultDog) {
  dog = { ...newDog };
  listeners.forEach(fn => fn(dog));
  AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(dog)).catch(e =>
    console.log('Failed to save dog profile:', e)
  );
}

export function useDog(): [typeof defaultDog, typeof setDog] {
  const [value, setValue] = React.useState(dog);
  React.useEffect(() => {
    listeners.push(setValue);
    return () => {
      listeners = listeners.filter(fn => fn !== setValue);
    };
  }, []);
  return [value, setDog];
}