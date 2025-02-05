function showUpdateForm(investmentId) {
    const newValue = prompt('Enter current value:');
    if (newValue === null) return;
    
    const endDate = prompt('Enter end date (YYYY-MM-DD) or leave empty if ongoing:');
    
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/update_investment/${investmentId}`;
    
    const valueInput = document.createElement('input');
    valueInput.type = 'hidden';
    valueInput.name = 'current_value';
    valueInput.value = newValue;
    
    const dateInput = document.createElement('input');
    dateInput.type = 'hidden';
    dateInput.name = 'end_date';
    dateInput.value = endDate;
    
    form.appendChild(valueInput);
    form.appendChild(dateInput);
    document.body.appendChild(form);
    form.submit();
}

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });
});