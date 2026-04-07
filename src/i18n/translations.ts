export const languages = {
  de: "Deutsch",
  en: "English",
} as const;

export type Lang = keyof typeof languages;

export const defaultLang: Lang = "de";

export const ui = {
  de: {
    "nav.home": "Startseite",
    "nav.about": "\u00dcber uns",
    "nav.contact": "Kontakt",
    "hero.tagline": "Qualit\u00e4t ohne Fachkr\u00e4fte-Abh\u00e4ngigkeit",
    "hero.subtitle":
      "Die Avorix Koch App f\u00fchrt Ihr K\u00fcchenteam Schritt f\u00fcr Schritt durch jedes Rezept \u2014 f\u00fcr gleichbleibende Speisequalit\u00e4t, unabh\u00e4ngig vom Erfahrungsstand.",
    "hero.cta": "Demo vereinbaren",
    "hero.secondary_cta": "Mehr erfahren",
    "hero.cta_note": "Kostenlos & unverbindlich",
    "benefits.title": "Warum Avorix",
    "benefits.1.title": "Konsistente Qualit\u00e4t",
    "benefits.1.text":
      "Standardisierte Prozesse und die Avorix Koch App sichern gleichbleibende Speisenqualit\u00e4t \u2014 unabh\u00e4ngig vom Erfahrungslevel Ihres K\u00fcchenteams.",
    "benefits.2.title": "Weniger Personalabh\u00e4ngigkeit",
    "benefits.2.text":
      "82% der Betriebe melden Fachkr\u00e4ftemangel in der K\u00fcche. Avorix macht Ihren Betrieb unabh\u00e4ngiger von einzelnen Schl\u00fcsselkr\u00e4ften.",
    "benefits.3.title": "Volle Kostenkontrolle",
    "benefits.3.text":
      "Rezeptbasierte Kalkulation, Wareneinsatz-Tracking und standardisierte Portionierung bringen Transparenz in Ihre K\u00fcchenkosten.",
    "cta.title": "Bereit f\u00fcr den n\u00e4chsten Schritt?",
    "cta.text":
      "Erfahren Sie, wie Avorix Ihren K\u00fcchenbetrieb transformieren kann.",
    "cta.button": "Kontakt aufnehmen",
    "about.title": "\u00dcber Avorix",
    "about.intro":
      "Avorix erm\u00f6glicht Hotels und Gastronomiebetrieben, mit Software, standardisierten Prozessen und der Avorix Koch App qualitativ hochwertige Gerichte konsistent anzubieten \u2014 auch ohne ausgebildete K\u00f6che.",
    "about.mission.title": "Unsere Mission",
    "about.mission.text":
      "Der Fachkr\u00e4ftemangel in der Gastronomie ist strukturell. Wir glauben, dass Technologie die L\u00fccke schlie\u00dfen kann \u2014 nicht als Ersatz f\u00fcr gute K\u00f6che, sondern als Werkzeug, das jedem K\u00fcchenteam erm\u00f6glicht, auf hohem Niveau zu arbeiten.",
    "about.focus.title": "Unser Fokus",
    "about.focus.text":
      "Wir starten mit 4-Sterne-Ferienhotels in Tirol und Salzburg \u2014 Betrieben, in denen Halbpension das Kernversprechen ist und die K\u00fcche t\u00e4glich unter Druck steht, konstante Qualit\u00e4t zu liefern.",
    "contact.eyebrow": "Kostenloses Erstgespräch",
    "contact.title": "Demo vereinbaren",
    "contact.intro":
      "Lernen Sie Avorix in einem persönlichen Demo-Gespräch kennen. Wir zeigen Ihnen, wie unsere Lösung Ihren Küchenbetrieb konkret unterstützt.",
    "contact.email": "E-Mail",
    "contact.phone": "Telefon",
    "contact.form.name": "Name",
    "contact.form.email": "E-Mail",
    "contact.form.message": "Nachricht",
    "contact.form.submit": "Absenden",
    "footer.rights": "Alle Rechte vorbehalten.",
    "footer.imprint": "Impressum",
    "footer.privacy": "Datenschutz",
    "nav.kochapp": "Koch App",
    "kochapp.title": "Avorix Koch App",
    "kochapp.tagline": "Schritt für Schritt zur perfekten Küche",
    "kochapp.intro": "Die Avorix Koch App führt Ihr Küchenteam durch jedes Rezept — präzise, visuell und in Echtzeit. Gleichbleibende Qualität, egal wer am Herd steht.",
    "kochapp.how.title": "So funktioniert die Koch App",
    "kochapp.how.step1.title": "Rezept auswählen",
    "kochapp.how.step1.text": "Das Küchenteam wählt das gewünschte Gericht aus der digitalen Rezeptbibliothek — auf Tablet oder Smartphone, direkt in der Küche.",
    "kochapp.how.step2.title": "Schritt-für-Schritt geführt",
    "kochapp.how.step2.text": "Jeder Arbeitsschritt wird klar und verständlich angezeigt — mit Mengenangaben, Zeiten und Fotos. Kein Interpretationsspielraum, keine Fehler.",
    "kochapp.how.step3.title": "Konsistentes Ergebnis",
    "kochapp.how.step3.text": "Das Gericht gelingt nach Standard — unabhängig vom Erfahrungsstand des Kochs. Qualität wird reproduzierbar.",
    "kochapp.features.title": "Funktionen im Überblick",
    "kochapp.features.1.title": "Digitale Rezeptbibliothek",
    "kochapp.features.1.text": "Alle Rezepte zentral verwaltet, jederzeit aktuell und für das gesamte Team zugänglich.",
    "kochapp.features.2.title": "Portionsrechner",
    "kochapp.features.2.text": "Automatische Skalierung auf die benötigte Portionsanzahl — kein Nachrechnen, kein Verschnitt.",
    "kochapp.features.3.title": "Wareneinsatz-Tracking",
    "kochapp.features.3.text": "Transparente Kostenkontrolle durch rezeptbasierte Kalkulation und Wareneinsatz-Auswertung.",
    "kochapp.features.4.title": "Offline-fähig",
    "kochapp.features.4.text": "Die App funktioniert auch ohne stabile Internetverbindung — zuverlässig in jeder Küchensituation.",
    "kochapp.cta.title": "Koch App kennenlernen",
    "kochapp.cta.text": "Vereinbaren Sie eine kostenlose Demo und sehen Sie, wie die Avorix Koch App Ihren Küchenbetrieb transformiert.",
    "kochapp.cta.button": "Demo anfragen",
  },
  en: {
    "nav.home": "Home",
    "nav.about": "About",
    "nav.contact": "Contact",
    "hero.tagline": "Quality Without Staff Dependency",
    "hero.subtitle":
      "The Avorix Kitchen App guides your kitchen team step-by-step through every recipe — delivering consistent food quality, regardless of experience level.",
    "hero.cta": "Book a Demo",
    "hero.secondary_cta": "Learn more",
    "hero.cta_note": "Free & no obligation",
    "benefits.title": "Why Avorix",
    "benefits.1.title": "Consistent Quality",
    "benefits.1.text":
      "Standardized processes and the Avorix Kitchen App ensure consistent food quality — regardless of your kitchen team's experience level.",
    "benefits.2.title": "Less Staff Dependency",
    "benefits.2.text":
      "82% of businesses report a shortage of skilled kitchen staff. Avorix makes your operation less dependent on individual key personnel.",
    "benefits.3.title": "Full Cost Control",
    "benefits.3.text":
      "Recipe-based costing, food cost tracking, and standardized portioning bring transparency to your kitchen expenses.",
    "cta.title": "Ready for the Next Step?",
    "cta.text": "Discover how Avorix can transform your kitchen operations.",
    "cta.button": "Get in touch",
    "about.title": "About Avorix",
    "about.intro":
      "Avorix enables hotels and restaurants to consistently serve high-quality dishes using software, standardized processes, and the Avorix Kitchen App — even without trained chefs.",
    "about.mission.title": "Our Mission",
    "about.mission.text":
      "The skilled labor shortage in hospitality is structural. We believe technology can bridge the gap — not as a replacement for good chefs, but as a tool that enables every kitchen team to operate at a high level.",
    "about.focus.title": "Our Focus",
    "about.focus.text":
      "We start with 4-star resort hotels in Tyrol and Salzburg — properties where half-board is the core promise and the kitchen faces daily pressure to deliver consistent quality.",
    "contact.eyebrow": "Free Initial Consultation",
    "contact.title": "Book a Demo",
    "contact.intro": "Get to know Avorix in a personal demo call. We'll show you exactly how our solution supports your kitchen operations.",
    "contact.email": "Email",
    "contact.phone": "Phone",
    "contact.form.name": "Name",
    "contact.form.email": "Email",
    "contact.form.message": "Message",
    "contact.form.submit": "Send",
    "footer.rights": "All rights reserved.",
    "footer.imprint": "Legal Notice",
    "footer.privacy": "Privacy Policy",
    "nav.kochapp": "Cook App",
    "kochapp.title": "Avorix Cook App",
    "kochapp.tagline": "Step by Step to a Perfect Kitchen",
    "kochapp.intro": "The Avorix Cook App guides your kitchen team through every recipe — precisely, visually, and in real time. Consistent quality, no matter who's at the stove.",
    "kochapp.how.title": "How the Cook App Works",
    "kochapp.how.step1.title": "Choose a Recipe",
    "kochapp.how.step1.text": "The kitchen team selects the desired dish from the digital recipe library — on a tablet or smartphone, directly in the kitchen.",
    "kochapp.how.step2.title": "Step-by-Step Guidance",
    "kochapp.how.step2.text": "Each step is displayed clearly and intuitively — with quantities, timings, and photos. No room for interpretation, no mistakes.",
    "kochapp.how.step3.title": "Consistent Results",
    "kochapp.how.step3.text": "The dish turns out to standard — regardless of the cook's experience level. Quality becomes reproducible.",
    "kochapp.features.title": "Feature Overview",
    "kochapp.features.1.title": "Digital Recipe Library",
    "kochapp.features.1.text": "All recipes managed centrally, always up to date and accessible to the entire team.",
    "kochapp.features.2.title": "Portion Calculator",
    "kochapp.features.2.text": "Automatic scaling to the required number of portions — no manual calculations, no waste.",
    "kochapp.features.3.title": "Food Cost Tracking",
    "kochapp.features.3.text": "Transparent cost control through recipe-based costing and food cost analysis.",
    "kochapp.features.4.title": "Offline-Capable",
    "kochapp.features.4.text": "The app works even without a stable internet connection — reliable in every kitchen situation.",
    "kochapp.cta.title": "Discover the Cook App",
    "kochapp.cta.text": "Book a free demo and see how the Avorix Cook App transforms your kitchen operations.",
    "kochapp.cta.button": "Request a Demo",
  },
} as const;

export function getLangFromUrl(url: URL): Lang {
  const [, lang] = url.pathname.split("/");
  if (lang in languages) return lang as Lang;
  return defaultLang;
}

export function useTranslations(lang: Lang) {
  return function t(key: keyof (typeof ui)[typeof defaultLang]): string {
    return ui[lang][key] || ui[defaultLang][key];
  };
}

export function getLocalizedPath(path: string, lang: Lang): string {
  if (lang === defaultLang) return path;
  return `/${lang}${path}`;
}
