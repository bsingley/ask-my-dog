import React from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

const STORAGE_KEY = 'dog_profile';

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