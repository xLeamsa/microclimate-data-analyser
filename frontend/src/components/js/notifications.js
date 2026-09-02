export function requestNotificationPermission() {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

export function notificationsEnabled() {
    return 'Notification' in window && Notification.permission === 'granted';
}

export function sendNotification(title, body) {
    if (!notificationsEnabled()) return;
    try {
        // eslint-disable-next-line no-new
        new Notification(title, { body });
    } catch (error) {
        console.error('Could not show notification:', error);
    }
}