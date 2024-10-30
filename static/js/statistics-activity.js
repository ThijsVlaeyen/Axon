async function fetchActivityData() {
    const response = await fetch('/api/activity'); // Adjust to your API endpoint
    const data = await response.json();

    const activityCount = {};
    
    data.forEach(item => {
        const date = item.date;
        const totalActivity = item.total_activity;
        activityCount[date] = totalActivity;
    });

    const activityData = Array(365).fill(0);
    const today = new Date();

    // Fill in activityData with total counts for the last 365 days
    for (let i = 0; i < 365; i++) {
        const pastDate = new Date();
        pastDate.setDate(today.getDate() - i);
        const formattedDate = pastDate.toISOString().split('T')[0];

        activityData[364 - i] = activityCount[formattedDate] || 0; // Fill from the end
    }

    return activityData;
}

function createActivityGrid(activityData) {
    const gridContainer = document.querySelector('.activity-container');

    const today = new Date();
    const currentDayOfWeek = (today.getDay() + 6) % 7;
    const daysInYear = 365;
    let dayCount = 0;

    for (let day = 0; day < 7; day++) {
        for (let week = 0; week < 53; week++) {
            const square = document.createElement('div');
            
            if ((week === 0 && day < currentDayOfWeek + 1) || (week === 52 && day > currentDayOfWeek)) {
                square.classList.add('grid-item-blank');
                gridContainer.appendChild(square);
            } 

            else if (dayCount < daysInYear) {
                square.classList.add('grid-item');
                const count = activityData[week * 7 + day - currentDayOfWeek];
                dayCount++
                if (count === 0) {
                } else if (count < 5) {
                    square.classList.add('low-activity');
                } else if (count < 10) {
                    square.classList.add('medium-activity');
                } else if (count < 20) {
                    square.classList.add('high-activity');
                } else if (count >= 20) {
                    square.classList.add('very-high-activity');
                }
                gridContainer.appendChild(square);
            }
        }
    }
}

// Call this function when setting up the grid
async function setupActivityGrid() {
    const activityData = await fetchActivityData();
    createActivityGrid(activityData);
}

// Initialize the grid when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', setupActivityGrid);
