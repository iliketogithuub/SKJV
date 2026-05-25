// BKJV Interactive Layout Controls
document.addEventListener('DOMContentLoaded', () => {
  
  // 1. Sidebar Tab Switching
  const navItems = document.querySelectorAll('.nav-item');
  const panels = document.querySelectorAll('.content-panel');
  const headerLeft = document.getElementById('header-left');
  
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      // Remove active from all items
      navItems.forEach(nav => nav.classList.remove('active'));
      // Add active to clicked
      item.classList.add('active');
      
      // Hide all panels
      panels.forEach(panel => panel.classList.remove('active'));
      
      // Show targeted panel
      const targetId = item.getAttribute('data-target');
      const targetPanel = document.getElementById(`panel-${targetId}`);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
      
      // Update running header left
      if (targetId === 'front-matter') {
        headerLeft.textContent = 'THE SUPERNATURAL GOSPEL';
      } else if (targetId === 'john-1') {
        headerLeft.textContent = 'JOHN CHAPTER 1';
      } else if (targetId === 'mark-11') {
        headerLeft.textContent = 'MARK CHAPTER 11';
      } else if (targetId === 'titus-1') {
        headerLeft.textContent = 'TITUS CHAPTER 1';
      }
    });
  });

  // 2. View Mode Toggle (Print Page vs. E-Reader)
  const btnPrint = document.getElementById('btn-print');
  const btnReader = document.getElementById('btn-reader');
  const layoutWrapper = document.getElementById('layout-wrapper');

  btnPrint.addEventListener('click', () => {
    btnPrint.classList.add('active');
    btnReader.classList.remove('active');
    layoutWrapper.classList.remove('reader-mode');
    layoutWrapper.classList.add('print-mode');
  });

  btnReader.addEventListener('click', () => {
    btnReader.classList.add('active');
    btnPrint.classList.remove('active');
    layoutWrapper.classList.remove('print-mode');
    layoutWrapper.classList.add('reader-mode');
  });

  // 3. Font Size Controls
  let currentFontSize = 14; // Base em or px font size index
  const fontValSpan = document.getElementById('font-size-val');
  const bibleContent = document.getElementById('bible-content');
  const fontDec = document.getElementById('font-dec');
  const fontInc = document.getElementById('font-inc');

  const updateFontSize = () => {
    fontValSpan.textContent = `${currentFontSize}px`;
    bibleContent.style.fontSize = `${currentFontSize / 14}rem`;
  };

  fontDec.addEventListener('click', () => {
    if (currentFontSize > 11) {
      currentFontSize--;
      updateFontSize();
    }
  });

  fontInc.addEventListener('click', () => {
    if (currentFontSize < 24) {
      currentFontSize++;
      updateFontSize();
    }
  });

  // 4. Theme Switching
  const themeCream = document.getElementById('theme-cream');
  const themeLight = document.getElementById('theme-light');
  const themeDark = document.getElementById('theme-dark');
  const themeButtons = [themeCream, themeLight, themeDark];

  const clearThemes = () => {
    layoutWrapper.classList.remove('theme-cream', 'theme-light', 'theme-dark');
    themeButtons.forEach(btn => btn.classList.remove('active'));
  };

  themeCream.addEventListener('click', () => {
    clearThemes();
    layoutWrapper.classList.add('theme-cream');
    themeCream.classList.add('active');
  });

  themeLight.addEventListener('click', () => {
    clearThemes();
    layoutWrapper.classList.add('theme-light');
    themeLight.classList.add('active');
  });

  themeDark.addEventListener('click', () => {
    clearThemes();
    layoutWrapper.classList.add('theme-dark');
    themeDark.classList.add('active');
  });

  // 5. Covenant Lexicon Tooltips
  const tooltip = document.getElementById('covenant-tooltip');
  const tooltipText = document.getElementById('tooltip-text');
  const highlightedTerms = document.querySelectorAll('.term-highlight');

  const termDefinitions = {
    grudge: "<strong>Strong's G3709 (Orge) / G4307 (Proskomma)</strong>: An offense or personal blockage. Jesus warns that holding a grudge anchors the heart in double-mindedness, disabling the word spoken with the mouth.",
    sins: "<strong>Strong's G266 (Hamartia)</strong>: Transgressions or missing the mark. Forgiveness cleanses the legal pathway, ensuring your authority is not compromised by a guilty conscience."
  };

  highlightedTerms.forEach(term => {
    term.addEventListener('mouseenter', (e) => {
      const termKey = term.getAttribute('data-term');
      const definition = termDefinitions[termKey];
      if (definition) {
        tooltipText.innerHTML = definition;
        
        // Position tooltip above the element
        const rect = term.getBoundingClientRect();
        tooltip.style.left = `${rect.left + (rect.width / 2) - 120}px`; // Centered
        tooltip.style.top = `${window.scrollY + rect.top - tooltip.offsetHeight - 12}px`;
        
        tooltip.classList.remove('hidden');
        // Force reflow
        tooltip.offsetHeight;
        tooltip.classList.add('visible');
      }
    });

    term.addEventListener('mouseleave', () => {
      tooltip.classList.remove('visible');
      setTimeout(() => {
        if (!tooltip.classList.contains('visible')) {
          tooltip.classList.add('hidden');
        }
      }, 200);
    });
  });
});
