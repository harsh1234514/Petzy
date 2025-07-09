// Main JavaScript for EcommerceShop

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all product cards and section elements
    document.querySelectorAll('.product-card, .category-card, .section-title').forEach(el => {
        observer.observe(el);
    });

    // Quantity input handlers
    document.querySelectorAll('.quantity-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            const currentValue = parseInt(input.value);
            const isIncrement = this.classList.contains('btn-increment');
            
            if (isIncrement) {
                input.value = currentValue + 1;
            } else if (currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            // Trigger change event for cart updates
            input.dispatchEvent(new Event('change'));
        });
    });

    // Star rating system
    document.querySelectorAll('.rating').forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        const input = rating.querySelector('input[type="hidden"]');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const ratingValue = index + 1;
                
                // Update input value
                if (input) {
                    input.value = ratingValue;
                }
                
                // Update star display
                stars.forEach((s, i) => {
                    s.classList.toggle('filled', i < ratingValue);
                });
            });
            
            star.addEventListener('mouseenter', function() {
                const hoverValue = index + 1;
                stars.forEach((s, i) => {
                    s.style.color = i < hoverValue ? '#ffc107' : '#ddd';
                });
            });
        });
        
        rating.addEventListener('mouseleave', function() {
            const currentValue = input ? parseInt(input.value) || 0 : 0;
            stars.forEach((s, i) => {
                s.style.color = i < currentValue ? '#ffc107' : '#ddd';
            });
        });
    });

    // Search functionality enhancements
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    // Auto-suggest functionality could be implemented here
                    console.log('Searching for:', query);
                }, 300);
            }
        });
    }

    // Cart operations
    window.addToCart = function(productId, quantity = 1) {
        const btn = event.target;
        const originalText = btn.innerHTML;
        
        // Show loading state
        btn.innerHTML = '<span class="spinner"></span> Adding...';
        btn.disabled = true;
        
        fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update cart count in navbar
                updateCartCount(data.cart_total_items);
                
                // Show success message
                showMessage('Product added to cart!', 'success');
                
                // Update button text
                btn.innerHTML = '<i class="fas fa-check"></i> Added!';
                btn.classList.remove('btn-primary');
                btn.classList.add('btn-success');
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-primary');
                    btn.disabled = false;
                }, 2000);
            } else {
                throw new Error(data.message || 'Failed to add to cart');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to add to cart. Please try again.', 'error');
            btn.innerHTML = originalText;
            btn.disabled = false;
        });
    };

    window.removeFromCart = function(cartItemId) {
        if (confirm('Are you sure you want to remove this item from your cart?')) {
            fetch('/cart/remove/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    cart_item_id: cartItemId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // Reload to update cart display
                } else {
                    throw new Error(data.message || 'Failed to remove item');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('Failed to remove item. Please try again.', 'error');
            });
        }
    };

    window.updateCartQuantity = function(cartItemId, quantity) {
        fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                cart_item_id: cartItemId,
                quantity: quantity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update cart totals without full page reload
                updateCartTotals(data.cart_total_price, data.cart_total_items);
            } else {
                throw new Error(data.message || 'Failed to update quantity');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Failed to update quantity. Please try again.', 'error');
        });
    };

    // Utility functions
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateCartCount(count) {
        const cartBadge = document.querySelector('.navbar .badge');
        if (cartBadge) {
            cartBadge.textContent = count;
            if (count > 0) {
                cartBadge.style.display = 'inline-block';
            } else {
                cartBadge.style.display = 'none';
            }
        }
    }

    function updateCartTotals(totalPrice, totalItems) {
        const totalPriceElements = document.querySelectorAll('.cart-total-price');
        const totalItemsElements = document.querySelectorAll('.cart-total-items');
        
        totalPriceElements.forEach(el => {
            el.textContent = `$${totalPrice}`;
        });
        
        totalItemsElements.forEach(el => {
            el.textContent = totalItems;
        });
        
        updateCartCount(totalItems);
    }

    function showMessage(message, type = 'info') {
        const alertClass = type === 'error' ? 'alert-danger' : 
                          type === 'success' ? 'alert-success' : 'alert-info';
        
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.querySelector('.container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', alertHtml);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                const alert = container.querySelector('.alert');
                if (alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }, 5000);
        }
    }

    // Form validation enhancements
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                
                // Re-enable button after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });

    // Product image gallery
    document.querySelectorAll('.product-gallery img').forEach(img => {
        img.addEventListener('click', function() {
            const mainImage = document.querySelector('.main-product-image');
            if (mainImage) {
                mainImage.src = this.src;
                mainImage.alt = this.alt;
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});