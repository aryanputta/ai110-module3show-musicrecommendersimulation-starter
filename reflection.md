# Reflection — Profile Comparisons

## High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile produced scores in the 3–5 range with most points coming from genre and mood matches. The Chill Lofi profile produced higher absolute scores (up to 5.71) because it also received acousticness bonus points on top of the standard genre/mood/energy combination. The key difference in output is not just energy level but texture: lofi results are consistently acoustic and unhurried, while pop results are brighter and louder. Both profiles felt accurate to what a real listener in those categories would expect.

## High-Energy Pop vs. Deep Intense Rock

Both profiles ask for high energy (0.85 and 0.92), but their outputs diverge sharply at positions 2–5. The pop profile fills those spots with indie pop songs that share the happy mood. The rock profile fills them with metal and EDM songs that share the intense mood but not the genre. This difference shows that mood is doing meaningful work: when the rock profile can't find more rock songs, it falls back on mood (intense) as the next strongest signal. The system behaves consistently — it just lacks the catalog depth to serve the rock user as well as the lofi user.

## Chill Lofi vs. Deep Intense Rock

These two profiles represent opposite ends of the energy spectrum. The lofi profile clusters its results tightly: four of the top five songs have energy between 0.35 and 0.42. The rock profile's results are more scattered in genre because the catalog has only one rock song, so lower-ranked results come from whatever genre happened to have high energy. This comparison reveals a catalog imbalance: lofi is well-served because multiple lofi songs exist; rock is not because only one does. The scoring logic is working as intended — the data is the limiting factor.

## Moody Late-Night Synthwave vs. Deep Intense Rock

Both profiles want high energy but their mood targets differ (moody vs. intense). The synthwave profile's top-2 results are both synthwave songs that match exactly. The rock profile's top result is the only rock song in the catalog. Below the top spot, the two profiles share no overlap — the synthwave profile draws on r&b and jazz because those genres appear with "moody" labels, while the rock profile draws on metal and EDM because those appear with "intense" labels. This confirms that mood labels are functioning as meaningful separators between emotionally distinct listening contexts, not just decorative metadata.
