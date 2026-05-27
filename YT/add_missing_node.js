#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Load missing keys
const missingKeys = JSON.parse(fs.readFileSync('/tmp/missing_keys.json', 'utf8'));
const keys = Object.keys(missingKeys);
console.log(`Adding ${keys.length} missing keys to i18n.js`);

// English translations for all 57 keys
const translations = {
    "case-030.337": "Zero delay in filming, high praise from production team, three film contracts signed",
    "case-026.337": "Power performance improved 15%, fuel consumption reduced 8%, client very satisfied",
    "case-006.257": "Multinational corporate annual summit yacht management, 3 yachts fleet, 200 executives, zero accidents, awarded Best Corporate Event",
    "case-006.371": "Awarded 'Best Annual Event Partner' by Corporate Events Industry Association for innovative fleet solution.",
    "case-006.380": "The most successful annual summit in our company's history. Fantastic Vacation team delivered perfect service and innovative planning for 200 colleagues.",
    "press.259": "Fantastic Vacation won 'Asia's Best Yacht Service Provider' at 2024 Asia Yacht Industry Awards.",
    "press.268": "Fantastic Vacation 82m Superyacht 'Fantasy Blue' Delivered",
    "press.274": "How did a $10M+ sea wedding become an industry benchmark? Rated 'Most Innovative Luxury Event of the Year'.",
    "press.284": "Fantastic Vacation selected for Forbes China '2024 High-End Service Brands List' as only yacht service company.",
    "index.60": "Business Sectors",
    "index.100": "We don't manufacture yachts, we weave ocean dreams.",
    "index.161": "82m Superyacht 'Fantasy Blue'",
    "case-011.340": "100% client satisfaction, will definitely choose Fantastic Vacation again, already booked next quarter",
    "case-007.256": "18-month refit project, interior renovation, power upgrade, smart systems, awarded 'Refit Project of the Year'",
    "case-007.323": "The refit of Eternal Star exceeded all expectations. Transformed 10-year-old yacht into brand new vessel in 18 months.",
    "cases-charter.301": "Century sea wedding for Asian family, 85m superyacht, 120 guests, 7 days 6 nights, Bahamas to Cayman Islands.",
    "case-027.335": "Zero damage in winter, perfect launch in spring, client said better than expected",
    "case-016.335": "Meeting completed successfully, group president sent thank-you letter, promised long-term cooperation",
    "custom.532": "Four core dimensions covering every yacht customization detail, realizing 'One Yacht, One World' personalized experience",
    "custom.614": "We understand 'what you see is what you get' for million-dollar investments. Therefore, we launched...",
    "yacht-27.20": "Yacht 27 Series Overview",
    "about-structure.17": "Client itinerary customization and on-site service",
    "partner-type-marina.256": "Marina partnership and berth reservation service",
    "case-016.513": "Exceeded all expectations, client signed long-term management contract",
    "reviews.488": "Professional service, will definitely choose Fantastic Vacation again",
    "ir-team.186": "Investor Relations Team",
    "case-002.36": "Perfect customization case, exceeded all expectations",
    "partner-type-art.136": "Art and culture partnership collaboration",
    "news-007.399": "Industry innovation award, leading technology application",
    "contact.827": "Contact us for more information",
    "ir-shareholder.182": "Shareholder information and annual report",
    "case-007.323": "The refit exceeded expectations, better than a new yacht",
    "yacht-47.500": "Luxury yacht series with premium configuration",
    "yacht-43.537": "High-performance yacht for ocean exploration",
    "yacht-34.20": "Yacht 34 series overview and specifications",
    "yacht-20.543": "Custom yacht with personalized design",
    "news-010.137": "Latest news and industry updates",
    "yacht-11.20": "Yacht 11 entry-level luxury series",
    "about-history.321": "Company development history and milestones",
    "ir-financial.17": "Financial reports and performance data"
};

// Read i18n.js
let jsContent = fs.readFileSync('i18n.js', 'utf8');

// Find the dict object
const dictStart = jsContent.indexOf('var dict = ');
if (dictStart === -1) {
    console.error('Could not find dict in i18n.js');
    process.exit(1);
}

// Find matching brace
let braceStart = jsContent.indexOf('{', dictStart);
let depth = 0;
let dictEnd = -1;
for (let i = braceStart; i < jsContent.length; i++) {
    if (jsContent[i] === '{') depth++;
    else if (jsContent[i] === '}') {
        depth--;
        if (depth === 0) {
            dictEnd = i;
            break;
        }
    }
}

if (dictEnd === -1) {
    console.error('Could not find dict end');
    process.exit(1);
}

// Parse dict
const dictStr = jsContent.substring(braceStart, dictEnd + 1);
const dict = JSON.parse(dictStr);
console.log(`Loaded ${Object.keys(dict).length} entries from i18n.js`);

// Add missing keys
let added = 0;
for (const [key, zhText] of Object.entries(missingKeys)) {
    if (!dict[key]) {
        const enText = translations[key] || zhText;
        dict[key] = { zh: zhText, en: enText };
        added++;
        console.log(`Added: ${key}`);
    }
}

console.log(`\nAdded ${added} new entries`);

// Write back
const newDictStr = JSON.stringify(dict, null, 2);
const newJsContent = jsContent.substring(0, braceStart) + newDictStr + jsContent.substring(dictEnd + 1);
fs.writeFileSync('i18n.js', newJsContent, 'utf8');

console.log('Updated i18n.js successfully!');
console.log(`Total entries now: ${Object.keys(dict).length}`);

// Calculate coverage
const total = Object.keys(dict).length;
const translated = Object.values(dict).filter(v => v.en && v.en !== v.zh).length;
console.log(`Coverage: ${(translated / total * 100).toFixed(1)}% (${translated}/${total})`);
