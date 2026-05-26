// BKJV Dynamic Bible Reader Script
document.addEventListener('DOMContentLoaded', () => {
  
  // DOM Elements
  const testamentSelect = document.getElementById('testament-select');
  const bookSelect = document.getElementById('book-select');
  const chapterGrid = document.getElementById('chapter-grid');
  const bibleContent = document.getElementById('bible-content');
  const pageNumSpan = document.getElementById('page-num');
  const headerLeft = document.getElementById('header-left');
  
  const btnPrint = document.getElementById('btn-print');
  const btnReader = document.getElementById('btn-reader');
  const layoutWrapper = document.getElementById('layout-wrapper');
  
  const fontDec = document.getElementById('font-dec');
  const fontInc = document.getElementById('font-inc');
  const fontValSpan = document.getElementById('font-size-val');
  
  const themeCream = document.getElementById('theme-cream');
  const themeLight = document.getElementById('theme-light');
  const themeDark = document.getElementById('theme-dark');
  const themeButtons = [themeCream, themeLight, themeDark];
  
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const searchClearBtn = document.getElementById('search-clear-btn');
  
  const tooltip = document.getElementById('covenant-tooltip');
  const tooltipText = document.getElementById('tooltip-text');

  // Mobile layout elements
  const menuToggleBtn = document.getElementById('menu-toggle-btn');
  const sidebarCloseBtn = document.getElementById('sidebar-close-btn');
  const sidebarOverlay = document.getElementById('sidebar-overlay');
  const appSidebar = document.getElementById('app-sidebar');

  // Constants
  const NT_BOOKS = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
  ];
  
  // Power Word / Covenant Lexicon Definitions (Strong's references)
  const LEXICON = {
    "delegated authority": "<strong>Strong's G1849 (Exousia)</strong>: Legal right, delegated authority, or executive standing. BKJV translates this as <em>delegated authority</em> or <em>legal authority</em> to clarify that the believer has a badge of office to command, not power to beg.",
    "legal authority": "<strong>Strong's G1849 (Exousia)</strong>: Legal right, delegated authority, or executive standing. BKJV translates this as <em>delegated authority</em> or <em>legal authority</em> to clarify that the believer has a badge of office to command, not power to beg.",
    "supernatural power": "<strong>Strong's G1411 (Dunamis)</strong>: Miraculous, explosive, inherent ability or force. BKJV translates this as <em>supernatural power</em> or <em>miraculous power</em> to highlight the active muscle of the Holy Spirit operating within.",
    "miraculous power": "<strong>Strong's G1411 (Dunamis)</strong>: Miraculous, explosive, inherent ability or force. BKJV translates this as <em>supernatural power</em> or <em>miraculous power</em> to highlight the active muscle of the Holy Spirit operating within.",
    "grudge": "<strong>Strong's G3709 (Orge) / G4307 (Proskomma)</strong>: An offense, resentment, or personal blockage. Jesus warns that holding a grudge anchors the heart in double-mindedness, disabling the word spoken with the mouth.",
    "sins": "<strong>Strong's G266 (Hamartia) / G3900 (Paraptoma)</strong>: Sins, transgressions, or missing the mark. Forgiveness cleanses the legal pathway, ensuring your authority is not compromised by a guilty conscience.",
    "sickness": "<strong>Strong's H2483 (Choliy) / G769 (Astheneia)</strong>: Sickness, physical malady, or weakness. BKJV systematically replaces 'infirmity' with 'sickness' to make the physical reality of what Jesus bore obvious.",
    "sicknesses": "<strong>Strong's H2483 (Choliy) / G769 (Astheneia)</strong>: Sicknesses, physical maladies, or weaknesses. BKJV systematically replaces 'infirmities' with 'sicknesses' to make the physical reality of what Jesus bore obvious.",
    "disease": "<strong>Strong's H2483 (Choliy) / G769 (Astheneia)</strong>: Disease or physical malady. BKJV replaces archaic 'infirmity' terms with 'disease' to emphasize complete physical health.",
    "diseases": "<strong>Strong's H2483 (Choliy) / G769 (Astheneia)</strong>: Diseases or physical maladies. BKJV replaces archaic 'infirmities' terms with 'diseases' to emphasize complete physical health.",
    "wounds": "<strong>Strong's H2250 (Chabburah) / G3468 (Molops)</strong>: Whipping welts, scars, or scourging wounds. Purchased at the Roman whipping post as the legal currency for physical healing.",
    "scourging wounds": "<strong>Strong's H2250 (Chabburah) / G3468 (Molops)</strong>: Whipping welts, scars, or scourging wounds. Purchased at the Roman whipping post as the legal currency for physical healing.",
    "love": "<strong>Strong's G26 (Agape)</strong>: Covenant love. BKJV replaces the archaic noun 'charity' (which modern readers associate with handouts) with 'love' to reflect the direct relationship of agape."
  };

  // State Variables
  let currentBook = "Matthew";
  let currentChapter = "1";
  let currentFontSize = 14;

  // Close sidebar drawer on mobile/tablet screens
  function closeSidebarOnMobile() {
    if (appSidebar && window.innerWidth <= 1024) {
      appSidebar.classList.remove('open');
      sidebarOverlay.classList.remove('visible');
    }
  }

  // Initialize App
  function init() {
    populateBookDropdown();
    loadChapter(currentBook, currentChapter);
    setupEventListeners();
  }

  // Populate Books based on Testament Selection
  function populateBookDropdown() {
    const selectedTestament = testamentSelect.value;
    bookSelect.innerHTML = '';
    
    // Sort all books from BIBLE_DATA
    const availableBooks = Object.keys(BIBLE_DATA);
    
    availableBooks.forEach(book => {
      const isNT = NT_BOOKS.includes(book);
      if ((selectedTestament === "NT" && isNT) || (selectedTestament === "OT" && !isNT)) {
        const option = document.createElement('option');
        option.value = book;
        option.textContent = book;
        bookSelect.appendChild(option);
      }
    });
    
    // Set default book to first element in list
    if (bookSelect.options.length > 0) {
      currentBook = bookSelect.options[0].value;
      populateChapterGrid(currentBook);
    }
  }

  // Populate Chapter Grid
  function populateChapterGrid(book) {
    chapterGrid.innerHTML = '';
    if (!BIBLE_DATA[book]) return;
    
    const chapters = Object.keys(BIBLE_DATA[book]);
    
    chapters.forEach(chap => {
      const btn = document.createElement('button');
      btn.className = 'chapter-btn';
      if (chap === currentChapter) btn.classList.add('active');
      btn.textContent = chap;
      btn.addEventListener('click', () => {
        // Toggle active button
        document.querySelectorAll('.chapter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentChapter = chap;
        loadChapter(currentBook, currentChapter);
        closeSidebarOnMobile();
      });
      chapterGrid.appendChild(btn);
    });
  }

  // Parse Text for Bold Directives, Zero-Pronouns, and Lexicon Highlighting
  function parseScriptureText(text) {
    if (!text) return "";
    
    // 1. Bold Directives: Match **text** and replace with <strong>
    let parsed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // 2. Lexicon Words: Highlight and add tooltip links
    // Match exact phrase case-insensitively using word boundaries
    const lexiconTerms = Object.keys(LEXICON);
    lexiconTerms.forEach(term => {
      const regex = new RegExp(`\\b(${term})\\b`, 'gi');
      parsed = parsed.replace(regex, `<span class="term-highlight" data-term="${term.toLowerCase()}">$1</span>`);
    });
    
    // 3. Zero-Pronouns: Highlight common universal covenant noun replacements
    const zeroPronouns = [
      "that individual", "this individual", "a defiled individual", "the individual", 
      "the believer", "the believers", "the believer's", "believers", 
      "their heart", "their mouth", "the mouth", "those things"
    ];
    zeroPronouns.forEach(noun => {
      const regex = new RegExp(`\\b(${noun})\\b`, 'gi');
      parsed = parsed.replace(regex, `<span class="zero-pronoun-tag">$1</span>`);
    });
    
    return parsed;
  }

  // Load selected Book and Chapter into reading panel
  function loadChapter(book, chapter) {
    if (!BIBLE_DATA[book] || !BIBLE_DATA[book][chapter]) {
      // Fallback if chapter doesn't exist
      chapter = "1";
      currentChapter = "1";
    }
    
    const chapterData = BIBLE_DATA[book][chapter];
    const verses = chapterData.verses;
    const insight = chapterData.insight;
    
    let htmlContent = '';
    
    // Render Book Title Headers
    htmlContent += `<h2 class="book-title">${book}</h2>`;
    htmlContent += `<div class="book-subtitle">Based King James Version (BKJV)</div>`;
    htmlContent += `<div class="section-divider"></div>`;
    htmlContent += `<h3 class="chapter-title">Chapter ${chapter}</h3>`;
    
    // Render Verses
    htmlContent += `<div class="verse-list">`;
    const verseNumbers = Object.keys(verses).sort((a, b) => parseInt(a) - parseInt(b));
    
    if (verseNumbers.length === 0) {
      htmlContent += `<p class="body-text">No verses found in this chapter.</p>`;
    } else {
      verseNumbers.forEach(vNum => {
        const verseText = verses[vNum];
        const parsedText = parseScriptureText(verseText);
        htmlContent += `
          <div class="verse-row">
            <span class="verse-number">${vNum}</span>
            <span class="verse-text">${parsedText}</span>
          </div>`;
      });
    }
    htmlContent += `</div>`;
    
    // Render Operational Insight Box if present
    if (insight) {
      const parsedInsight = parseScriptureText(insight);
      htmlContent += `
        <div class="operational-insight-box">
          <span class="insight-label">Operational Insight</span>
          <p class="insight-text">${parsedInsight}</p>
        </div>`;
    }
    
    // Inject HTML
    bibleContent.innerHTML = htmlContent;
    
    // Update running header and page number
    headerLeft.textContent = `${book.toUpperCase()} CHAPTER ${chapter}`;
    
    // Set simulated page number
    const pageHash = getPageNumber(book, chapter);
    pageNumSpan.textContent = pageHash;
    
    // Rebind tooltip listeners on newly added highlights
    setupTooltipListeners();
  }

  // Simple pseudo-random page generator based on book order
  function getPageNumber(book, chapter) {
    const books = Object.keys(BIBLE_DATA);
    const bookIdx = books.indexOf(book);
    const basePage = (bookIdx * 12) + parseInt(chapter);
    return basePage + 100; // offset
  }

  // Setup Event Listeners
  function setupEventListeners() {
    // Dropdowns
    testamentSelect.addEventListener('change', () => {
      populateBookDropdown();
      currentChapter = "1";
      loadChapter(currentBook, currentChapter);
      closeSidebarOnMobile();
    });
    
    bookSelect.addEventListener('change', () => {
      currentBook = bookSelect.value;
      populateChapterGrid(currentBook);
      currentChapter = "1";
      loadChapter(currentBook, currentChapter);
      closeSidebarOnMobile();
    });
    
    // View Mode Toggle
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

    // Font Sizing
    fontDec.addEventListener('click', () => {
      if (currentFontSize > 11) {
        currentFontSize--;
        fontValSpan.textContent = `${currentFontSize}px`;
        bibleContent.style.fontSize = `${currentFontSize / 14}rem`;
      }
    });

    fontInc.addEventListener('click', () => {
      if (currentFontSize < 26) {
        currentFontSize++;
        fontValSpan.textContent = `${currentFontSize}px`;
        bibleContent.style.fontSize = `${currentFontSize / 14}rem`;
      }
    });

    // Themes
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
    
    // Search Database
    searchInput.addEventListener('input', runSearch);
    searchClearBtn.addEventListener('click', () => {
      searchInput.value = '';
      searchResults.classList.add('hidden');
      searchClearBtn.classList.add('hidden');
    });

    // Mobile Sidebar Drawer Toggles
    if (menuToggleBtn) {
      menuToggleBtn.addEventListener('click', () => {
        appSidebar.classList.add('open');
        sidebarOverlay.classList.add('visible');
      });
    }

    if (sidebarCloseBtn) {
      sidebarCloseBtn.addEventListener('click', () => {
        appSidebar.classList.remove('open');
        sidebarOverlay.classList.remove('visible');
      });
    }

    if (sidebarOverlay) {
      sidebarOverlay.addEventListener('click', () => {
        appSidebar.classList.remove('open');
        sidebarOverlay.classList.remove('visible');
      });
    }

    // Close tooltip when clicking anywhere else
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.term-highlight') && !e.target.closest('#covenant-tooltip')) {
        tooltip.classList.remove('visible');
        setTimeout(() => {
          if (!tooltip.classList.contains('visible')) {
            tooltip.classList.add('hidden');
          }
        }, 200);
      }
    });

    // Hide tooltip when content scrolls
    const contentViewport = document.querySelector('.content-viewport');
    if (contentViewport) {
      contentViewport.addEventListener('scroll', () => {
        tooltip.classList.remove('visible');
        tooltip.classList.add('hidden');
      });
    }
  }

  function clearThemes() {
    layoutWrapper.classList.remove('theme-cream', 'theme-light', 'theme-dark');
    themeButtons.forEach(btn => btn.classList.remove('active'));
  }

  // Database Search Functionality
  function runSearch() {
    const query = searchInput.value.trim().toLowerCase();
    if (query.length < 2) {
      searchResults.classList.add('hidden');
      searchClearBtn.classList.add('hidden');
      return;
    }
    
    searchClearBtn.classList.remove('hidden');
    searchResults.innerHTML = '';
    
    let matches = [];
    const books = Object.keys(BIBLE_DATA);
    
    // Scan all verses
    for (const book of books) {
      for (const chapter of Object.keys(BIBLE_DATA[book])) {
        const verses = BIBLE_DATA[book][chapter].verses;
        for (const vNum of Object.keys(verses)) {
          const text = verses[vNum];
          if (text.toLowerCase().includes(query)) {
            matches.push({
              book,
              chapter,
              vNum,
              text
            });
          }
          if (matches.length >= 15) break; // Limit search results to 15 items
        }
        if (matches.length >= 15) break;
      }
      if (matches.length >= 15) break;
    }
    
    if (matches.length === 0) {
      searchResults.innerHTML = `<div class="search-no-results">No matches found for "${query}"</div>`;
    } else {
      matches.forEach(m => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        item.innerHTML = `
          <div class="search-result-ref">${m.book} ${m.chapter}:${m.vNum}</div>
          <div class="search-result-text">${m.text.replace(/\*\*/g, '')}</div>
        `;
        
        item.addEventListener('click', () => {
          currentBook = m.book;
          currentChapter = m.chapter;
          
          // Re-populate select elements
          const isNT = NT_BOOKS.includes(m.book);
          testamentSelect.value = isNT ? "NT" : "OT";
          populateBookDropdown();
          
          bookSelect.value = m.book;
          populateChapterGrid(m.book);
          
          // Highlight active chapter button
          document.querySelectorAll('.chapter-btn').forEach(btn => {
            if (btn.textContent === m.chapter) {
              btn.classList.add('active');
            } else {
              btn.classList.remove('active');
            }
          });
          
          loadChapter(m.book, m.chapter);
          
          // Hide results box
          searchResults.classList.add('hidden');
          searchInput.value = '';
          searchClearBtn.classList.add('hidden');
          
          // Scroll to the verse
          setTimeout(() => {
            const verseRows = document.querySelectorAll('.verse-row');
            verseRows.forEach(row => {
              const num = row.querySelector('.verse-number').textContent;
              if (num === m.vNum) {
                row.scrollIntoView({ behavior: 'smooth', block: 'center' });
                row.style.backgroundColor = 'var(--electric-blue-transparent)';
                setTimeout(() => {
                  row.style.backgroundColor = 'transparent';
                  row.style.transition = 'background-color 1s ease';
                }, 2000);
              }
            });
          }, 300);
          
          closeSidebarOnMobile();
        });
        
        searchResults.appendChild(item);
      });
    }
    
    searchResults.classList.remove('hidden');
  }

  function showTooltip(el) {
    const term = el.getAttribute('data-term');
    const definition = LEXICON[term];
    if (definition) {
      tooltipText.innerHTML = definition;
      
      // Position calculation
      const rect = el.getBoundingClientRect();
      let left = rect.left + (rect.width / 2) - 125; // Center alignment
      
      // Viewport bounds checking for mobile
      const minPadding = 12;
      if (left < minPadding) {
        left = minPadding;
      }
      if (left + 250 > window.innerWidth - minPadding) {
        left = window.innerWidth - 250 - minPadding;
      }
      
      // Check if tooltip overflows top edge of viewport
      let top = rect.top - tooltip.offsetHeight - 12;
      let positionBelow = false;
      if (top < minPadding) {
        top = rect.bottom + 12;
        positionBelow = true;
      }
      
      tooltip.style.left = `${left}px`;
      tooltip.style.top = `${top}px`;
      
      // Toggle arrow direction styling
      if (positionBelow) {
        tooltip.classList.add('tooltip-below');
      } else {
        tooltip.classList.remove('tooltip-below');
      }
      
      // Adjust arrow position to point exactly at word center
      const arrow = tooltip.querySelector('.tooltip-arrow');
      if (arrow) {
        const wordCenter = rect.left + (rect.width / 2);
        let arrowLeft = wordCenter - left;
        // Keep arrow within tooltip bounds
        if (arrowLeft < 15) arrowLeft = 15;
        if (arrowLeft > 235) arrowLeft = 235;
        arrow.style.left = `${arrowLeft}px`;
      }
      
      tooltip.classList.remove('hidden');
      tooltip.offsetHeight; // trigger reflow
      tooltip.classList.add('visible');
    }
  }

  function hideTooltip() {
    tooltip.classList.remove('visible');
    setTimeout(() => {
      if (!tooltip.classList.contains('visible')) {
        tooltip.classList.add('hidden');
      }
    }, 200);
  }

  // Binding Lexicon Tooltips
  function setupTooltipListeners() {
    const highlights = document.querySelectorAll('.term-highlight');
    
    highlights.forEach(el => {
      // Desktop hover
      el.addEventListener('mouseenter', () => showTooltip(el));
      el.addEventListener('mouseleave', hideTooltip);
      
      // Touch/Click toggle support
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        showTooltip(el);
      });
    });
  }

  // Load
  init();
});
