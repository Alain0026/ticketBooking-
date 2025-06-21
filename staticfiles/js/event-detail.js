// Event Detail Page JavaScript

// Variabile globale per i biglietti selezionati
window.selectedTickets = {};

function proceedToBooking(event, eventSlug) {
    event.preventDefault();
    
    if (Object.keys(window.selectedTickets).length === 0) {
        alert('Seleziona almeno un biglietto prima di procedere!');
        return false;
    }
    
    // Salva la selezione nel sessionStorage
    sessionStorage.setItem('selectedTickets', JSON.stringify(window.selectedTickets));
    
    // Redirect alla pagina di prenotazione
    window.location.href = `/bookings/create/${eventSlug}/`;
}

document.addEventListener('DOMContentLoaded', function() {
    const ticketCards = document.querySelectorAll('.ticket-card');
    const totalPriceEl = document.getElementById('total-price');
    const proceedBtn = document.getElementById('proceed-btn');
    
    ticketCards.forEach(card => {
        const ticketId = card.dataset.ticketId;
        const price = parseFloat(card.dataset.price);
        const availableQty = parseInt(card.dataset.available) || 0;
        const quantitySelector = card.querySelector('.quantity-selector');
        const quantityDisplay = card.querySelector('.quantity-display');
        const minusBtn = card.querySelector('.minus-btn');
        const plusBtn = card.querySelector('.plus-btn');
        
        // Se non ci sono biglietti disponibili, disabilita la card
        if (availableQty === 0) {
            card.style.opacity = '0.5';
            card.style.cursor = 'not-allowed';
            return;
        }
        
        // Click sulla card per selezionare/deselezionare
        card.addEventListener('click', function(e) {
            // Non fare nulla se si clicca sui pulsanti quantità
            if (e.target.closest('.quantity-selector')) return;
            
            if (card.classList.contains('selected')) {
                // Deseleziona
                card.classList.remove('selected');
                quantitySelector.style.display = 'none';
                delete window.selectedTickets[ticketId];
                quantityDisplay.textContent = '0';
            } else {
                // Seleziona
                card.classList.add('selected');
                quantitySelector.style.display = 'flex';
                window.selectedTickets[ticketId] = 1;
                quantityDisplay.textContent = '1';
            }
            updateTotal();
        });
        
        // Pulsante meno
        if (minusBtn) {
            minusBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                let qty = window.selectedTickets[ticketId] || 0;
                if (qty > 1) {
                    window.selectedTickets[ticketId] = qty - 1;
                    quantityDisplay.textContent = window.selectedTickets[ticketId];
                    updateTotal();
                }
            });
        }
        
        // Pulsante più
        if (plusBtn) {
            plusBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                let qty = window.selectedTickets[ticketId] || 0;
                if (qty < Math.min(availableQty, 10)) {
                    window.selectedTickets[ticketId] = qty + 1;
                    quantityDisplay.textContent = window.selectedTickets[ticketId];
                    updateTotal();
                }
            });
        }
    });
    
    function updateTotal() {
        let total = 0;
        let hasSelection = false;
        
        ticketCards.forEach(card => {
            const ticketId = card.dataset.ticketId;
            const price = parseFloat(card.dataset.price);
            const qty = window.selectedTickets[ticketId] || 0;
            
            if (qty > 0) {
                total += price * qty;
                hasSelection = true;
            }
        });
        
        totalPriceEl.textContent = total.toFixed(2);
        
        // Abilita/disabilita il pulsante prenota
        if (proceedBtn) {
            if (hasSelection) {
                proceedBtn.classList.remove('disabled');
                proceedBtn.style.opacity = '1';
                proceedBtn.style.pointerEvents = 'auto';
            } else {
                proceedBtn.classList.add('disabled');
                proceedBtn.style.opacity = '0.5';
                proceedBtn.style.pointerEvents = 'none';
            }
        }
    }
    
    // Inizializza lo stato del pulsante
    updateTotal();
});