const deadline = new Date(DEADLINE_TIMESTAMP).getTime();

function updateStatus() {
    const now = new Date().getTime();
    const remaining = deadline - now;

    const downloadLink = document.getElementById("download-link");

    if (remaining <= 0) {
        document.getElementById("countdown").textContent = "Expired";
        if (downloadLink) {
            downloadLink.textContent = "Access Expired";
            downloadLink.className = "download-link red";
            downloadLink.removeAttribute("href"); // Disable the link
        }
        return;
    }

    const days = Math.floor(remaining / (1000 * 60 * 60 * 24));
    const hours = Math.floor((remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((remaining % (1000 * 60)) / 1000);

    document.getElementById("countdown").textContent =
        `${days}д ${hours}ч ${minutes}мин ${seconds}сек`;

    // Update the color based on remaining time
    if (days > 6) {
        downloadLink.className = "download-link green";
    } else if (days >= 0 && days <= 6) {
        downloadLink.className = "download-link yellow";
    } else {
        downloadLink.className = "download-link red";
    }
}

// Update the countdown and status every second
setInterval(updateStatus, 1000);
updateStatus(); // Initial call to set values immediately
