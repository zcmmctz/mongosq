import { useQuasar } from 'quasar';

class NotificationService {
  private $q: ReturnType<typeof useQuasar> | null = null;

  private getQuasar() {
    if (!this.$q) {
      this.$q = useQuasar();
    }
    return this.$q;
  }

  /**
   * Show success notification
   */
  success(message: string, timeout: number = 3000) {
    this.getQuasar().notify({
      type: 'positive',
      message,
      timeout,
      position: 'top-right',
      actions: [
        {
          icon: 'close',
          color: 'white',
          handler: () => {
            /* ... */
          }
        }
      ]
    });
  }

  /**
   * Show error notification
   */
  error(message: string, timeout: number = 5000) {
    this.getQuasar().notify({
      type: 'negative',
      message,
      timeout,
      position: 'top-right',
      actions: [
        {
          icon: 'close',
          color: 'white',
          handler: () => {
            /* ... */
          }
        }
      ]
    });
  }

  /**
   * Show warning notification
   */
  warning(message: string, timeout: number = 4000) {
    this.getQuasar().notify({
      type: 'warning',
      message,
      timeout,
      position: 'top-right',
      actions: [
        {
          icon: 'close',
          color: 'white',
          handler: () => {
            /* ... */
          }
        }
      ]
    });
  }

  /**
   * Show info notification
   */
  info(message: string, timeout: number = 3000) {
    this.getQuasar().notify({
      type: 'info',
      message,
      timeout,
      position: 'top-right',
      actions: [
        {
          icon: 'close',
          color: 'white',
          handler: () => {
            /* ... */
          }
        }
      ]
    });
  }
}

// Create singleton instance
export const notificationService = new NotificationService();
