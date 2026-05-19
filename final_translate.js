#!/usr/bin/env node
const fs = require('fs');

// Load i18n.js
let js = fs.readFileSync('i18n.js', 'utf8');

// Find dict
let start = js.indexOf('var dict = ');
let braceStart = js.indexOf('{', start);
let depth = 0;
let end = -1;
for (let i = braceStart; i < js.length; i++) {
    if (js[i] === '{') depth++;
    else if (js[i] === '}') {
        depth--;
        if (depth === 0) { end = i; break; }
    }
}

let dict = JSON.parse(js.substring(braceStart, end + 1));
console.log(`Loaded ${Object.keys(dict).length} entries`);

// The 37 untranslated entries - provide English translations
const translations = {
    "custom.658": "Client is a renowned collector who wanted the yacht to be a 'floating art museum'. Ink wash painting aesthetics integrated into interior, Burmese golden phoebe wood inlaid with Italian Bulgari marble.",
    "cases.428": "Century sea wedding for Asian family, 85m superyacht charter, 120 guests, 7 days 6 nights, route: Bahamas → Cayman Islands. Full wedding planning and execution.",
    "cases.450": "Multinational corporate annual summit yacht management, 3 yachts fleet sailing, 200 executives and guests, zero accidents throughout, awarded 'Best Corporate Annual Event'.",
    "cases.670": "Multinational corporate CEO summit, high-end confidential business meetings, zero-disturbance service, awarded 'Best Corporate Event of the Year'.",
    "cases.780": "Luxury birthday party for 60 guests, 7-day itinerary, fully customized themed activities, awarded 'Best Party of the Year'.",
    "case-020.335": "Proposal successful! Client said it was the most perfect moment of his life.",
    "case-021.335": "Awarded 'Best Sea Party of the Year', royal family member sent personal thank-you letter.",
    "cases-event.279": "Sea event hosting for multinational corporate annual summit, 3-yacht fleet formation sailing, 200 executives and guests, zero accidents throughout. Awarded 'Best Corporate Event'.",
    "case-017.335": "Client announced additional investment on the spot, banquet ROI exceeded expectations.",
    "case-001.580": "The Fantastic Vacation team didn't just deliver a superyacht, they delivered a floating palace. From design to construction, from sea trials to delivery, every detail...",
    "case-014.335": "Most successful gathering ever, already booked same itinerary for next year.",
    "cases-management.301": "Sea activity management for multinational corporate annual summit, 3-yacht fleet formation sailing, 200 executives and guests, zero accidents. Awarded 'Best Corporate Event'.",
    "case-002.573": "This wasn't just a vacation, it was a life-changing journey. The Fantastic Vacation team's attention to detail and professional service redefined our understanding of luxury travel.",
    "case-022.335": "Family members unanimously praised, already booked next year's family gathering.",
    "case-018.335": "Press conference received widespread global media coverage, 100% brand satisfaction.",
    "case-019.335": "98% employee satisfaction, HR director said it was the most successful annual meeting.",
    "case-023.337": "Zero major failures for 3 consecutive years, 100% shipowner satisfaction, renewed 5-year contract.",
    "case-003.577": "The Fantastic Vacation team proved with 5 years of professional service that they are a trustworthy partner. From daily operations to emergency response, from cost optimization to asset appreciation...",
    "case-015.335": "Post-release received 100K+ interactions, brand partner actively contacted for collaboration.",
    "case-024.337": "All indicators after maintenance exceeded factory standards, shipowner said it exceeded expectations.",
    "case-008.256": "16-month comprehensive refit project, interior renovation, power upgrade, smart system installation, awarded 'Refit Project of the Year', yacht market value increased 30%.",
    "case-008.315": "This refit exceeded all expectations. The Fantastic Vacation team transformed this 8-year-old yacht into a brand-new vessel in 16 months.",
    "case-028.337": "Winter zero damage, spring perfect launch, shipowner said it's better than expected.",
    "case-012.337": "Power performance improved 15%, fuel consumption reduced 8%, shipowner very satisfied.",
    "reviews.281": "Professional service, will definitely choose Fantastic Vacation again.",
    "reviews.288": "The most professional yacht team I've ever worked with, every detail was perfect.",
    "reviews.295": "Customized itinerary exceeded expectations, will definitely come again.",
    "reviews.302": "Family gathering was perfect, kids loved it, already booked next year.",
    "reviews.309": "Proposal succeeded! Thank you Fantastic Vacation for the perfect arrangement.",
    "reviews.316": "Corporate event was a huge success, partners praised it, will cooperate again.",
    "case-004.574": "This was the most successful product launch in our company's history. Fantastic Vacation team...",
    "ir-media.175": "Media reports and press releases collection.",
    "case-005.271": "Brand launch event, 85m superyacht, 200 guests, 7 days 6 nights, Mediterranean route. Full event planning and execution.",
    "case-005.573": "The brand launch event received widespread media coverage, 100% brand satisfaction, already booked next year's global roadshow.",
    "case-013.335": "Meeting completed successfully, group president sent personal thank-you letter, promised long-term cooperation.",
    "case-025.337": "Meeting completed successfully, exceeded all expectations, promised long-term cooperation."
};

// Update dict with translations
let updated = 0;
for (const [key, enText] of Object.entries(translations)) {
    if (dict[key]) {
        dict[key].en = enText;
        updated++;
        console.log(`Updated: ${key}`);
    }
}

console.log(`\nUpdated ${updated} entries`);

// Write back
const newDictStr = JSON.stringify(dict, null, 2);
const newJs = js.substring(0, braceStart) + newDictStr + js.substring(end + 1);
fs.writeFileSync('i18n.js', newJs, 'utf8');

console.log('Updated i18n.js successfully!');

// Verify coverage
const total = Object.keys(dict).length;
const translated = Object.values(dict).filter(v => v.en && v.en !== v.zh).length;
console.log(`Total entries: ${total}`);
console.log(`Translated: ${translated}`);
console.log(`Coverage: ${(translated / total * 100).toFixed(1)}%`);
