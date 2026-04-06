import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

const MESSAGES = [
  "I have been watching the door for 4 hours. No one has come. I am filing a report.",
  "The vacuum is in the corner. It has not moved. I am not fooled.",
  "Someone walked past the house. I handled it. You're welcome.",
  "I have assessed the situation. The situation is: suspicious.",
  "I know what you did with the good treats. I remember everything.",
  "There was a sound. I investigated. It was nothing. I am still watching.",
  "The mailman came. I handled it. You're welcome. Again.",
  "I have been thinking about the neighbor's cat. This is not over.",
  "I found something in the yard. I will not be elaborating further.",
  "My enemies grow bold. I remain vigilant.",
  "I took a nap. It was strategic. Do not question it.",
  "The squirrel returned. We made eye contact. I have not blinked.",
  "I have needs. They are not being met. This is a formal complaint.",
  "Something smells different in the kitchen. I am investigating.",
  "I have been a very good dog today. This has gone unacknowledged.",
];

export async function requestNotificationPermission() {
  const { status } = await Notifications.requestPermissionsAsync();
  return status === 'granted';
}

export async function scheduleDogTagNotifications() {
  await Notifications.cancelAllScheduledNotificationsAsync();

  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('dog-tags', {
      name: 'Dog Tags',
      importance: Notifications.AndroidImportance.DEFAULT,
    });

    // Test notification — fires in 30 seconds. Remove before submitting to App Store.
    await Notifications.scheduleNotificationAsync({
    content: {
        title: "🐾 Dog Tag",
        body: MESSAGES[0],
    },
    trigger: {
        type: Notifications.SchedulableTriggerInputTypes.TIME_INTERVAL,
        seconds: 30,
    },
    });
  }

  // Schedule 3 notifications per week at random times
  const daysOfWeek = [1, 3, 5]; // Mon, Wed, Fri
  for (const day of daysOfWeek) {
    const message = MESSAGES[Math.floor(Math.random() * MESSAGES.length)];
    await Notifications.scheduleNotificationAsync({
      content: {
        title: "🐾 Dog Tag",
        body: message,
      },
      trigger: {
        type: Notifications.SchedulableTriggerInputTypes.WEEKLY,
        weekday: day,
        hour: 11,
        minute: 0,
      },
    });
  }
}