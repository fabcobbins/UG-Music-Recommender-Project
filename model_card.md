# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeSync 1.0**

---

## 2. Intended Use

VibeSync 1.0 is a content-based music recommender built for classroom exploration. It takes a snapshot of what a user says they want — their preferred genre, mood, energy level, acoustic preference, valence, and danceability — and scores every song in an 18-song catalog against that profile. It's designed to surface the most relevant match based on those stated preferences, not based on what's trending or what other users listened to.

This system is for educational use only. It assumes the user can accurately describe their own taste in numerical terms, which is not realistic for a real product. It is not designed for production use, real user data, or any commercial application.

---

## 3. How the Model Works

Every song in the catalog gets evaluated by six independent judges, each looking at one feature. Think of it like six people in a room each voting on whether a song is a good fit, and each person's vote counts for a different amount.

The mood judge asks: does this song's mood match what the user said they want? If yes, full points. If no, zero — there's no partial credit. The genre judge works the same way. The energy judge is different — instead of yes or no, it measures how *close* the song's energy is to the user's target. A song that's slightly off gets a slightly lower score, and the further away it is, the more the score drops. The same math applies to danceability and valence. The acousticness judge is directional — if you said you like acoustic music, it rewards songs with high acousticness; if you said you don't, it does the opposite.

Each judge's result gets multiplied by its assigned weight (mood matters most at 25%, energy and acousticness each at 20%, genre at 15%, danceability at 12%, valence at 8%), and the six numbers are added together for a final score between 0 and 1. Songs are ranked by that score and the top 5 are returned.

---

## 4. Data

The catalog has 18 fictional songs across 12 genres: pop, hip-hop, lofi, rock, metal, EDM, ambient, jazz, indie pop, R&B, soul, folk, country, synthwave, and classical. Each song has 9 attributes: id, title, artist, genre, mood, energy, tempo BPM, valence, danceability, and acousticness.

The original starter dataset had 10 songs. I expanded it to 18 by adding songs in underrepresented genres — hip-hop, metal, EDM, folk, soul, country, classical, and R&B — to make the evaluation more meaningful. Even at 18 songs, the catalog is too small to serve most user profiles well. Genres like jazz, country, soul, and folk each have only one song, which means any user in those genres is almost guaranteed to get cross-genre results. Moods like "euphoric," "nostalgic," "melancholic," "angry," and "sad" also have very limited coverage, which compounds the problem.

---

## 5. Strengths

The system works best when the user's taste aligns with a well-represented genre and mood combination. The lofi profile produced the most accurate results — all three lofi songs ranked in the top 3 with scores above 0.93, which matched intuition exactly. The hip-hop profile also worked well since the only hip-hop song in the catalog happened to match both the genre and mood, earning a near-perfect score.

The scoring breakdown feature is a genuine strength. Every recommendation comes with a line-by-line explanation of which judges fired and why, so the system never hides its reasoning. A user can look at the output and immediately understand why a song ranked where it did, which is more transparency than most real recommenders offer.

---

## 6. Limitations and Bias

The biggest weakness I found is what I'm calling the "filter bubble by extreme values." A song like *Gym Hero* (pop, intense) kept showing up in the top 5 for almost every high-energy profile — hip-hop, rock, even jazz — because it scores near-perfect on energy and acousticness regardless of what genre the user asked for. With only 18 songs in the catalog, one song that sits at extreme values for multiple numeric features will always leak into results it doesn't belong in, and the user has no way to know that's happening.

The second issue is what happens when a user's genre and mood preferences don't overlap in the catalog. I tested a jazz fan who wanted intense music, and the system couldn't find a single jazz song that matched the mood — so it just recommended pop and rock songs instead and the genre score never fired once. The system doesn't tell the user "no match found," it just quietly gives them something different without explanation.

Mood being the heaviest weight (0.25) also creates an unequal experience depending on your taste. If you're a lofi or pop listener, your mood is probably in the catalog. If you're into something niche like country or soul, the catalog only has one or two songs for your genre and they might not match your mood at all — meaning the most important judge in the system is dead weight for you specifically. That's a real fairness problem if this were used in a real product.

---

## 7. Evaluation

I tested six different user profiles to see how the system behaved across different tastes: a hip-hop listener (Nine Vicious), a high-energy pop fan, a late-night lofi studier, a heavy rock listener, and two adversarial edge cases — someone with conflicting preferences (high energy but sad mood) and a jazz fan who wanted intense music.

The lofi profile worked basically perfectly. All three lofi songs in the catalog showed up in the top 3, in the right order, and the results matched exactly what you'd expect someone studying at 2am to want. That one felt right immediately.

The most surprising result was *Gym Hero* — a pop gym song — showing up in the top 5 for the hip-hop profile, the rock profile, and even the jazz profile. For a non-programmer, here's why that happens: the system doesn't actually understand music. It just looks at numbers. Gym Hero has a very high energy score and a very low acousticness score, which means it gets near-perfect marks on two of the six judges for almost any user who wants loud, non-acoustic music. The system sees "high energy, not acoustic" and says "this matches" — it doesn't understand that a hip-hop fan probably doesn't want a pop track, even if the energy feels similar. It's like a food recommender suggesting a fast food burger every time someone says they want "something filling" — technically correct on one measurement, but not what anyone actually meant.

The jazz + intense profile was also revealing. There's no jazz song in the catalog with an intense mood, so the genre score never fired once across the entire top 5. The system silently gave the user a list of rock and pop songs with no warning. A real product would need to handle this differently — probably by telling the user "we couldn't find a match in your genre" rather than just substituting something else.

---

## 8. Future Work

The most important improvement would be **multi-context user profiles**. Right now a user has one profile — one genre, one set of moods, one energy target. But real listeners don't work like that. Someone might be into Nine Vicious (Atlanta trap, high energy, intense) but also Jay Z (classic hip-hop, smoother) and YoungBoy (melodic rap) and also have a completely different soft side for something like TV Girl (indie pop, nostalgic, chill). All of those represent the same person, just in different moods or contexts — morning commute vs. late night vs. gym. Instead of forcing one flat profile, the system should let a user store multiple "vibes" and pick which one they're in at any given moment. That way the data going into the scoring engine is actually specific, and the recommendations stop being all over the place just because the user likes a wide range of music.

The second improvement is simply **a bigger catalog**. 18 songs is too small to serve most profiles well. A realistic catalog would need at least a few hundred songs to ensure every genre and mood combination has meaningful coverage. Right now if you want jazz, country, or soul you basically only have one option each — the system can't recommend within your genre, it just recommends outside of it.

A third improvement would be **diversity enforcement**. Right now nothing stops the system from returning the same artist five times or five songs with nearly identical energy scores. A real recommender would inject variety — making sure no two results are from the same artist, or that the top 5 covers a spread of energy levels even if they all match on mood and genre.

---

## 9. Personal Reflection

This project was smooth and actually got me interested in something I didn't expect to care about — data collection. The biggest thing I learned is how much the quality and size of your dataset determines everything else. Working with only 18 songs made it obvious really fast. The scoring logic was solid, the math was working correctly, but the results still felt off in certain cases — not because the algorithm was wrong, but because there just wasn't enough data for it to work with. You can't recommend good jazz if you only have one jazz song.

What surprised me is how a system this simple can still *feel* like a real recommender when the conditions are right. The lofi profile in particular — when everything lined up, the top 3 results were exactly what you'd expect. It felt like Spotify for a second. That made me realize the algorithm isn't the hard part. The hard part is having data that's rich enough, diverse enough, and accurate enough to let the algorithm do its job. Building the foundation right — a clean scoring system with good weights and transparent reasoning — matters way more early on than trying to add complexity. When you eventually do get more data, a strong foundation means the whole system scales up instead of falling apart.
