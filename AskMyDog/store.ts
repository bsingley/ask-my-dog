export const defaultDog = {
  name: 'Luna',
  breed: 'lab mix',
  age: '10 months',
  personality_traits: ['curious', 'cautious', 'extremely intelligent'],
  fear_triggers: ['new objects', 'loud sounds'],
  nemesis: 'the vacuum cleaner',
  intelligence: 'average',
  self_identity: 'The Last Guardian',
};

let dog = { ...defaultDog };
let listeners: Array<(d: typeof defaultDog) => void> = [];

export function getDog() {
  return dog;
}

export function setDog(newDog: typeof defaultDog) {
  dog = { ...newDog };
  listeners.forEach(fn => fn(dog));
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

import React from 'react';