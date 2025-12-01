document.addEventListener("DOMContentLoaded", function () {
  /**
   * Function to auto-dismiss notifications after a set duration
   */
  function autoDismissNotifications(delay = 5000) {
    // Get alerts inside the notification container
    const alerts = document.querySelectorAll("#notification-container .alert");

    alerts.forEach((alert) => {
      const progressBar = alert.querySelector(".progress-bar");

      // Check if progress bar exists and animate it
      if (progressBar) {
        const delay = parseInt(progressBar.dataset.duration, 10);

        // Start the progress bar animation
        progressBar.style.animationDuration = `${delay}ms`;
        progressBar.classList.add("progress-bar-animated");

        // Initialize Bootstrap Alert
        const bsAlert = new bootstrap.Alert(alert);

        // Set timer to dismiss the alert
        setTimeout(() => {
          bsAlert.close();
        }, delay);
      }
    });

    // Remove the notification container if there are no alerts left
    const notificationContainer = document.getElementById(
      "notification-container"
    );
    if (notificationContainer) {
      // Check if there are any alerts left
      const remainingAlerts = notificationContainer.querySelectorAll(".alert");
      if (remainingAlerts.length === 0) {
        // Set timer to remove the container
        setTimeout(() => {
          notificationContainer.remove();
        }, delay + 600);
      }
    }
  }

  // FUNCTION CALLS
  autoDismissNotifications();
});
