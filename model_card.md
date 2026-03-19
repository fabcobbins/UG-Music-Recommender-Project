# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

The biggest weakness I found is what I'm calling the "filter bubble by extreme values." A song like *Gym Hero* (pop, intense) kept showing up in the top 5 for almost every high-energy profile — hip-hop, rock, even jazz — because it scores near-perfect on energy and acousticness regardless of what genre the user asked for. With only 18 songs in the catalog, one song that sits at extreme values for multiple numeric features will always leak into results it doesn't belong in, and the user has no way to know that's happening.

The second issue is what happens when a user's genre and mood preferences don't overlap in the catalog. I tested a jazz fan who wanted intense music, and the system couldn't find a single jazz song that matched the mood — so it just recommended pop and rock songs instead and the genre score never fired once. The system doesn't tell the user "no match found," it just quietly gives them something different without explanation.

Mood being the heaviest weight (0.25) also creates an unequal experience depending on your taste. If you're a lofi or pop listener, your mood is probably in the catalog. If you're into something niche like country or soul, the catalog only has one or two songs for your genre and they might not match your mood at all — meaning the most important judge in the system is dead weight for you specifically. That's a real fairness problem if this were used in a real product.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
