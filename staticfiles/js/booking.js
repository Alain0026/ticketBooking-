// Booking specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a booking page
    const bookingForm = document.getElementById('booking-form');
    const eventDetailPage = document.querySelector('.event-detail');
    
    if (bookingForm) {
        initializeBookingForm();
    }
    
    if (eventDetailPage) {
        initializeEventDetailPage();
    }
});

// Initialize booking form functionality
function initializeBookingForm() {
    const form = document.getElementById('booking-form');
    const ticketSelections = document.querySelectorAll('.ticket-selection');
    const cartDataInput = document.getElementById('cart-data');
    const submitBtn = document.getElementById('submit-btn');
    
    let cart = {};
    
    // Initialize ticket quantity controls
    ticketSelections.forEach(selection => {
        const ticketId = selection.dataset.ticketId;
        const price = parseFloat(selection.dataset.price);
        const available = parseInt(selection.dataset.available);
        const minusBtn = selection.querySelector('.minus');
        const plusBtn = selection.querySelector('.plus');
        const quantityInput = selection.querySelector(`#quantity-${ticketId}`);
        
        // Minus button click
        minusBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 0) {
                quantityInput.value = currentValue - 1;
                updateCart(ticketId, currentValue - 1, price);
            }
        });
        
        // Plus button click
        plusBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            let maxValue = Math.min(available, parseInt(quantityInput.max));
            
            if (currentValue < maxValue) {
                quantityInput.value = currentValue + 1;
                updateCart(ticketId, currentValue + 1, price);
            }
        });
        
        // Direct input change
        quantityInput.addEventListener('change', function() {
            let value = parseInt(this.value);
            let maxValue = Math.min(available, parseInt(this.max));
            
            if (isNaN(value) || value < 0) {
                value = 0;
            } else if (value > maxValue) {
                value = maxValue;
            }
            
            this.value = value;
            updateCart(ticketId, value, price);
        });
    });
    
    // Update cart function
    function updateCart(ticketId, quantity, price) {
        if (quantity > 0) {
            cart[ticketId] = {
                quantity: quantity,
                price: price,
                subtotal: quantity * price
            };
        } else {
            delete cart[ticketId];
        }
        
        updateOrderSummary();
        updateSubmitButton();
        updateCartData();
    }
    
    // Update order summary display
    function updateOrderSummary() {
        const orderItemsDiv = document.getElementById('order-items');
        const subtotalEl = document.getElementById('subtotal');
        const feesEl = document.getElementById('fees');
        const totalEl = document.getElementById('total');
        
        let subtotal = 0;
        let itemsHtml = '';
        
        if (Object.keys(cart).length === 0) {
            itemsHtml = '<p class="text-muted text-center py-3">Nessun biglietto selezionato</p>';
        } else {
            Object.entries(cart).forEach(([ticketId, item]) => {
                const ticketName = document.querySelector(`[data-ticket-id="${ticketId}"] h5`).textContent;
                subtotal += item.subtotal;
                
                itemsHtml += `
                    <div class="d-flex justify-content-between mb-2">
                        <div>
                            <strong>${ticketName}</strong><br>
                            <small class="text-muted">${item.quantity} x €${item.price.toFixed(2)}</small>
                        </div>
                        <div class="text-end">
                            €${item.subtotal.toFixed(2)}
                        </div>
                    </div>
                `;
            });
        }
        
        const fees = subtotal * 0.05; // 5% di commissioni
        const total = subtotal + fees;
        
        orderItemsDiv.innerHTML = itemsHtml;
        subtotalEl.textContent = subtotal.toFixed(2);
        feesEl.textContent = fees.toFixed(2);
        totalEl.textContent = total.toFixed(2);
    }
    
    // Update submit button state
    function updateSubmitButton() {
        const hasItems = Object.keys(cart).length > 0;
        submitBtn.disabled = !hasItems;
        
        // Update button appearance
        if (hasItems) {
            submitBtn.classList.remove('btn-secondary');
            submitBtn.classList.add('btn-primary');
        } else {
            submitBtn.classList.remove('btn-primary');
            submitBtn.classList.add('btn-secondary');
        }
    }
    
    // Update hidden cart data input
    function updateCartData() {
        const cartData = {};
        Object.entries(cart).forEach(([ticketId, item]) => {
            cartData[ticketId] = item.quantity;
        });
        cartDataInput.value = JSON.stringify(cartData);
    }
    
    // Form submission
    form.addEventListener('submit', function(e) {
        if (Object.keys(cart).length === 0) {
            e.preventDefault();
            TicketBooking.showToast('Seleziona almeno un biglietto', 'warning');
            return false;
        }
        
        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Elaborazione...';
        submitBtn.disabled = true;
    });
}

// Initialize event detail page functionality
function initializeEventDetailPage() {
    const ticketCards = document.querySelectorAll('.ticket-card');
    const proceedBtn = document.getElementById('proceed-btn');
    let selectedTickets = {};
    
    ticketCards.forEach(card => {
        const ticketId = card.dataset.ticketId;
        
        // Skip if ticket is not available
        if (card.style.opacity === '0.5') {
            return;
        }
        
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on quantity selector
            if (e.target.closest('.quantity-selector')) {
                return;
            }
            
            // Toggle selection
            this.classList.toggle('selected');
            const quantitySelector = this.querySelector('.quantity-selector');
            const quantityDisplay = this.querySelector('.quantity-display');
            
            if (this.classList.contains('selected')) {
                quantitySelector.style.display = 'flex';
                selectedTickets[ticketId] = 1;
                quantityDisplay.textContent = '1';
            } else {
                quantitySelector.style.display = 'none';
                delete selectedTickets[ticketId];
                quantityDisplay.textContent = '0';
            }
            
            updateEventPageTotal();
        });
        
        // Quantity controls
        const minusBtn = card.querySelector('.minus-btn');
        const plusBtn = card.querySelector('.plus-btn');
        const quantityDisplay = card.querySelector('.quantity-display');
        
        if (minusBtn && plusBtn) {
            minusBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                let current = selectedTickets[ticketId] || 0;
                if (current > 1) {
                    selectedTickets[ticketId] = current - 1;
                    quantityDisplay.textContent = current - 1;
                    updateEventPageTotal();
                }
            });
            
            plusBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                let current = selectedTickets[ticketId] || 0;
                const available = parseInt(card.querySelector('.text-muted').textContent) || 0;
                const maxPerOrder = 10;
                
                if (current < Math.min(available, maxPerOrder)) {
                    selectedTickets[ticketId] = current + 1;
                    quantityDisplay.textContent = current + 1;
                    updateEventPageTotal();
                }
            });
        }
    });
    
    // Update total on event page
    function updateEventPageTotal() {
        const totalEl = document.getElementById('total-price');
        let total = 0;
        
        Object.entries(selectedTickets).forEach(([ticketId, quantity]) => {
            const card = document.querySelector(`[data-ticket-id="${ticketId}"]`);
            const price = parseFloat(card.querySelector('.price-tag').textContent.replace('€', ''));
            total += price * quantity;
        });
        
        totalEl.textContent = total.toFixed(2);
        
        // Enable/disable proceed button
        if (proceedBtn) {
            proceedBtn.disabled = Object.keys(selectedTickets).length === 0;
            
            if (!proceedBtn.disabled) {
                // Save selection to sessionStorage
                sessionStorage.setItem('selectedTickets', JSON.stringify(selectedTickets));
            }
        }
    }
    
    // Animate price changes
    function animatePrice(element, newValue) {
        const startValue = parseFloat(element.textContent);
        const endValue = parseFloat(newValue);
        const duration = 300;
        const startTime = Date.now();
        
        function update() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = startValue + (endValue - startValue) * progress;
            
            element.textContent = currentValue.toFixed(2);
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }
}

// Booking confirmation page
function initializeBookingConfirmation() {
    const confirmBtn = document.querySelector('[name="action"][value="confirm"]');
    const cancelBtn = document.querySelector('[name="action"][value="cancel"]');
    
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function() {
            if (!confirm('Confermi di voler procedere con il pagamento?')) {
                return false;
            }
            
            // Show loading state
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Elaborazione pagamento...';
            this.disabled = true;
            cancelBtn.disabled = true;
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            if (!confirm('Sei sicuro di voler annullare questa prenotazione?')) {
                return false;
            }
        });
    }
}

// My bookings page functionality
function initializeMyBookings() {
    // Cancel booking confirmation
    const cancelButtons = document.querySelectorAll('.btn-cancel-booking');
    
    cancelButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Sei sicuro di voler cancellare questa prenotazione? Questa azione non può essere annullata.')) {
                window.location.href = this.href;
            }
        });
    });
    
    // Print ticket functionality
    window.printTicket = function(bookingCode) {
        // Create a printable version of the ticket
        const printWindow = window.open('', '_blank');
        const ticketHtml = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Biglietto - ${bookingCode}</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 20px;
                    }
                    .ticket {
                        border: 2px solid #333;
                        padding: 20px;
                        max-width: 400px;
                        margin: 0 auto;
                    }
                    .qr-code {
                        margin: 20px 0;
                    }
                    h1 {
                        color: #6366f1;
                    }
                </style>
            </head>
            <body onload="window.print()">
                <div class="ticket">
                    <h1>TicketBooking</h1>
                    <h2>Il tuo Biglietto</h2>
                    <div class="qr-code">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${bookingCode}" alt="QR Code">
                    </div>
                    <h3>${bookingCode}</h3>
                    <p>Mostra questo codice all'ingresso</p>
                </div>
            </body>
            </html>
        `;
        
        printWindow.document.write(ticketHtml);
        printWindow.document.close();
    };
}

// Initialize appropriate functions based on current page
document.addEventListener('DOMContentLoaded', function() {
    const path = window.location.pathname;
    
    if (path.includes('/bookings/confirm/')) {
        initializeBookingConfirmation();
    }
    
    if (path.includes('/my-bookings/')) {
        initializeMyBookings();
    }
});

// Export functions for global use
window.BookingModule = {
    initializeBookingForm,
    initializeEventDetailPage,
    initializeBookingConfirmation,
    initializeMyBookings
};