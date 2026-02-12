// Baker Street Laboratory - UI Manager
// Handles UI interactions, animations, and visual feedback

class UIManager {
    constructor() {
        this.toastContainer = null;
        this.activeToasts = new Set();
        this.init();
    }

    init() {
        this.createToastContainer();
        this.initializeTooltips();
        this.setupGlobalEventListeners();
    }

    createToastContainer() {
        this.toastContainer = document.getElementById('toast-container');
        if (!this.toastContainer) {
            this.toastContainer = document.createElement('div');
            this.toastContainer.id = 'toast-container';
            this.toastContainer.className = 'toast-container';
            document.body.appendChild(this.toastContainer);
        }
    }

    showToast(message, type = 'info', duration = 4000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = this.getToastIcon(type);
        toast.innerHTML = `
            <div class="toast-content">
                <i class="${icon}"></i>
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Add to container
        this.toastContainer.appendChild(toast);
        this.activeToasts.add(toast);

        // Animate in
        setTimeout(() => {
            toast.classList.add('toast-show');
        }, 10);

        // Auto remove
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);

        return toast;
    }

    removeToast(toast) {
        if (this.activeToasts.has(toast)) {
            toast.classList.add('toast-hide');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
                this.activeToasts.delete(toast);
            }, 300);
        }
    }

    getToastIcon(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    initializeTooltips() {
        // Simple tooltip implementation
        document.addEventListener('mouseover', (e) => {
            const element = e.target.closest('[title]');
            if (element && element.title) {
                this.showTooltip(element, element.title);
            }
        });

        document.addEventListener('mouseout', (e) => {
            const element = e.target.closest('[title]');
            if (element) {
                this.hideTooltip();
            }
        });
    }

    showTooltip(element, text) {
        this.hideTooltip(); // Remove any existing tooltip

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';

        setTimeout(() => {
            tooltip.classList.add('tooltip-show');
        }, 10);

        this.currentTooltip = tooltip;
    }

    hideTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }

    setupGlobalEventListeners() {
        // Handle escape key to close modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
        });

        // Handle click outside modals
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target);
            }
        });
    }

    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('modal-show');
            document.body.classList.add('modal-open');
        }
    }

    closeModal(modal) {
        if (typeof modal === 'string') {
            modal = document.getElementById(modal);
        }
        
        if (modal) {
            modal.classList.add('modal-hide');
            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('modal-show', 'modal-hide');
                document.body.classList.remove('modal-open');
            }, 300);
        }
    }

    closeAllModals() {
        document.querySelectorAll('.modal:not(.hidden)').forEach(modal => {
            this.closeModal(modal);
        });
    }

    showLoading(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }

        if (element) {
            element.classList.add('loading');
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner psychedelic-spinner"></div>
                    <span class="loading-text">${text}</span>
                </div>
            `;
            element.appendChild(loadingOverlay);
        }
    }

    hideLoading(element) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }

        if (element) {
            element.classList.remove('loading');
            const overlay = element.querySelector('.loading-overlay');
            if (overlay) {
                overlay.remove();
            }
        }
    }

    animateElement(element, animation, duration = 1000) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }

        if (element) {
            element.style.animation = `${animation} ${duration}ms ease-in-out`;
            
            return new Promise(resolve => {
                setTimeout(() => {
                    element.style.animation = '';
                    resolve();
                }, duration);
            });
        }
    }

    highlightElement(element, duration = 2000) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }

        if (element) {
            element.classList.add('highlight');
            setTimeout(() => {
                element.classList.remove('highlight');
            }, duration);
        }
    }

    scrollToElement(element, behavior = 'smooth') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }

        if (element) {
            element.scrollIntoView({ behavior, block: 'center' });
        }
    }

    updateProgress(progressBar, percentage) {
        if (typeof progressBar === 'string') {
            progressBar = document.getElementById(progressBar);
        }

        if (progressBar) {
            const fill = progressBar.querySelector('.progress-fill') || progressBar;
            fill.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
            
            const text = progressBar.querySelector('.progress-text');
            if (text) {
                text.textContent = `${Math.round(percentage)}%`;
            }
        }
    }

    createConfirmDialog(message, onConfirm, onCancel) {
        const dialog = document.createElement('div');
        dialog.className = 'modal confirm-dialog';
        dialog.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Confirm Action</h3>
                </div>
                <div class="modal-body">
                    <p>${message}</p>
                </div>
                <div class="modal-footer">
                    <button class="secondary-btn cancel-btn">Cancel</button>
                    <button class="primary-btn confirm-btn">Confirm</button>
                </div>
            </div>
        `;

        document.body.appendChild(dialog);

        const confirmBtn = dialog.querySelector('.confirm-btn');
        const cancelBtn = dialog.querySelector('.cancel-btn');

        confirmBtn.addEventListener('click', () => {
            if (onConfirm) onConfirm();
            this.closeModal(dialog);
            dialog.remove();
        });

        cancelBtn.addEventListener('click', () => {
            if (onCancel) onCancel();
            this.closeModal(dialog);
            dialog.remove();
        });

        this.showModal(dialog);
        return dialog;
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatDate(date) {
        if (typeof date === 'string') {
            date = new Date(date);
        }
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showToast('Copied to clipboard', 'success');
            }).catch(() => {
                this.showToast('Failed to copy to clipboard', 'error');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                this.showToast('Copied to clipboard', 'success');
            } catch (err) {
                this.showToast('Failed to copy to clipboard', 'error');
            }
            document.body.removeChild(textArea);
        }
    }
}
