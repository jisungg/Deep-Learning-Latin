# Deep Learning Latin

## Why is Translating Latin So Hard?
If thereʼs one thing that everyone whoʼs studied Latin could agree on, itʼs that the grammar rules are incredibly hard. The word order is arbitrary, each of the verbs has several cases and all the nouns have gender. Latin has a very complex grammar including cases, genders, declensions and vastly different verb forms for different tenses (of which there are many). For example, nouns are divided into (main) 3 declensions unimaginatively named 1st, 2nd, and 3rd. There are masculine, feminine and neuter genders and 6 cases determined by what role the noun plays in the sentence; nominative, accusative, genitive, dative ablative, locative and vocative (7 if you include vocative). The noun will have a different ending depending on each of these pieces of information. Although these endings are not unique, that gives 54 different combinations. 

Verbs can be very irregular. Verbs belong to one of 3 conjugations (-are, -ere and -ire) and may be regular or irregular. The verb endings for I, you (singular), he/she/it, we, you (plural) and they, are all different, and change again for different tenses. So while “to walk” has just 4 endings (walk, walks, walked, and walking), Latin verbs can run into 30–40. As a result, it is not enough to simply learn the stem or the infinitive (“carry”, “to carry”). You must learn the present tense first-person singular form, the infinitive, the first-person singular imperfect and past participle together (“fero”, “ferre”, “tuli”, “latum”).

Latin was incredibly influential on Romance languages (Spanish, French, Portuguese among others) and therefore Latin
will allow to effectively understand these languages when written as well as, to a lesser extent, spoken. Many people
don't realize the prevalence of Latin in English either, law is full of such references (“habeas corpus”, “mens rea”) as well as idioms (“status quo”, “ad infinitum”).

## Dataset
The training dataset was comprised of three different types of Latin to English translations.
1. Vocabulary list of 12,500 nouns, adjectives, pronouns, adverbs, verbs, and conjunctions
- Portion of the nouns, adjectives were fully declined; the remaining were declined in the nominative and genitive singular case (for the nouns] or declined in the nominative singular case by gender (for the adjectives and pronouns).
- A small portion of the verbs of the 1st, 2nd, 3rd (*-io*), and 4th conjugations were conjugated fully. The rest were split into their participles.
- Vocabulary words were translated with multiple synonyms.
- Useful to translate words literally.
2. 2250 phrases and short sentences from common sayings and textbook examples
- Phrases/sentences that have 2-6 words
- Useful because they have simple grammatical structures and use words commonly found together.
3. 1000 complex Latin sentences taken from classical texts by Caesar, Cicero, and Virgil
- Longer sentences that may have multiple phrases and clauses, in the classical style.
- Useful to translate full sentences and analyze more complex grammatical structures.

This dataset is not available but was curated from [Perseus](https://www.perseus.tufts.edu/hopper/), [The PHI Classical Latin Texts Database](http://latin.packhum.org), [Virtual Language Observatory](https://vlo.clarin.eu/?1), and [11K Latin Texts](https://www.cs.cmu.edu/~dbamman/latin.html).

## Latin Translator
This is an experimental project that took place for a year, working with Mr. Minden of The Buckley School in Sherman Oaks. The PDF contains the bulk of the information and the step-by-step guide I have constructed while going through the steps. 