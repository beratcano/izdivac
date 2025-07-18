
    // Handle slider labels and ticks
    document.querySelectorAll('.slider-input').forEach(slider => {
        const questionId = slider.id.split('_')[1];
        const sliderValueSpan = document.getElementById(`slider_value_${questionId}`);
        const sliderLabelsContainer = document.getElementById(`slider_labels_${questionId}`);
        const sliderTicksContainer = slider.previousElementSibling; // The div with class slider-ticks
        const min = parseInt(slider.min);
        const max = parseInt(slider.max);

        function updateSliderLabelsAndTicks() {
            sliderLabelsContainer.innerHTML = ''; // Clear existing labels
            
            // Get the actual width of the slider input
            const sliderWidth = slider.offsetWidth;

            // Approximate thumb width. This is a common default, but can vary.
            // For more accuracy, one might need to inspect computed styles or use a library.
            const thumbWidth = 16; // Using a common default for better alignment
            
            // The effective track width is the slider width minus the thumb width
            // because the thumb's center travels from thumbWidth/2 to sliderWidth - thumbWidth/2
            const trackWidth = sliderWidth - thumbWidth;

            for (let i = min; i <= max; i++) {
                // Create and position labels
                const label = document.createElement('span');
                label.classList.add('slider-label');
                label.textContent = i;

                const percentage = (i - min) / (max - min);
                const position = percentage * trackWidth + (thumbWidth / 2);
                
                label.style.left = `${position}px`;
                label.style.transform = `translateX(-50%)`;
                sliderLabelsContainer.appendChild(label);
            }

            // Position the ticks dynamically to match the labels
            const ticks = sliderTicksContainer.querySelectorAll('.tick');
            ticks.forEach((tick, index) => {
                // The ticks should correspond to the values from min to max
                const tickValue = min + index; 
                const percentage = (tickValue - min) / (max - min);
                const position = percentage * trackWidth + (thumbWidth / 2);
                tick.style.left = `${position}px`;
                tick.style.transform = `translateX(-50%)`;
            });
        }

        // Initial setup and update on input
        updateSliderLabelsAndTicks();
        slider.addEventListener('input', updateSliderLabelsAndTicks);
        window.addEventListener('resize', updateSliderLabelsAndTicks); // Update on resize
    });
});