function timeSince(date) {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);

    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
        return interval + " years ago";
    }
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
        return interval + " months ago";
    }
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
        return interval + " days ago";
    }
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
        return interval + " hours ago";
    }
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
        return interval + " minutes ago";
    }
    return Math.floor(seconds) + " seconds ago";
}

// Update all elements with class 'time-since-creation' to show relative time
document.querySelectorAll('.time-since-creation').forEach(function(element) {
    element.textContent = timeSince(element.textContent);
});


document.addEventListener('DOMContentLoaded', function () {
    const patients = document.querySelectorAll('.book');
    const container = document.getElementById('patient-container');
    
    let counter = 0;
    patients.forEach(function (patient) {
        counter++;
        if (counter % 4 === 1) {
            const lineBreak = document.createElement('div');
            lineBreak.classList.add('line-break');
            container.appendChild(lineBreak);
            const row = document.createElement('div');
            row.classList.add('d-flex', 'flex-wrap');
            container.appendChild(row);
        }
        const currentRow = container.lastElementChild;
        currentRow.appendChild(patient);
    });
});

