document.addEventListener("DOMContentLoaded", function () {
    const consentModal = document.getElementById("consentModal");
    const acceptBtn = document.getElementById("acceptConsentBtn");

    // Check if the user has already accepted policies
    const isConsentAccepted = localStorage.getItem("userLegalConsent");

    if (!isConsentAccepted && consentModal) {
        consentModal.classList.add("active");
    }

    if (acceptBtn) {
        acceptBtn.addEventListener("click", function () {
            // Save consent in browser storage
            localStorage.setItem("userLegalConsent", "true");
            // Hide modal
            consentModal.classList.remove("active");
        });
    }
});
