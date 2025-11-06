#  Page1: “Your League Journey”

##UI flow: 
Render 2–5 “Chapter” cards. Each card represents a contiguous phase of the player’s year (segments created from turning-point detection). Click to reveal the content (if possible)

##Components
Card header: Chapter N — <agent-generated title>
Mid section: most-used champion avatar for that phase + quick stats (Win Rate, Vision, KDA, CS, Damage).
Footer: short agent-generated narrative explaining this phase.
Chapters are ordered chronologically. Chapter boundaries come from Binseg (e.g., 1/1–3/10, 3/11–…).
The number of cards equals the number of detected segments (min 2, max 5 shown).

##Data Schema
Player Chapter (multiple objects per player)


# Page2: “Your Year in Time Series”

## UI flow:
Top: Multi-metric time-series chart (e.g., WinRate, KDA, CS/min, Damage/min).
Background bands: colored segments (same chapters detected on Page 1). Each band displays the Chapter title from Page 1.
Hover: tooltip shows date/game index + metric values; if inside a segment, also show that segment’s title.

Right/Bottom: Agent chat box to ask questions about “the whole year” or any range/segment. (you can leave this for now! I can implement it later)

##Data Schema
time-series -> PlayerMatchMetrics
Segments -> PlayerChapter


# Page3: "Pro Player Similarity"

## UI flow:
**Top:** Similarity score (0-100%) showing how similar the player is to a pro player.

**Left Side:**
- **Top:** Player name and summoner image
- **Middle:** Your playstyle with playstyle metrics (normalized 0-100 scores):

###TO-DO (still thinking this part)
  - Aggressiveness (early game aggression, solo kills, tower dives)
  - Team Focus (kill participation, team fight presence)
  - Objective Control (dragon/baron participation rate)
  - Vision Control (ward placement patterns, vision score)
  - Farm Efficiency (CS/min relative to role average)
  - Late Game Scaling (performance improvement in long games)

**Right Side:**
- **Top:** Closest matching pro player's name, pro team name
- **Middle:** Same playstyle metrics for the pro player (for comparison)

**Button:** Agent generates explanation of your playstyle and why you are similar to this pro player.

## Data Schema
- similarity score -> SimilarityMatch
- play styles (each for player and pros) -> PlayerPlaystyle


# Page4: "Champion Pool Suggestions"

## UI flow:
**Body:** Display 3 champion suggestion cards for the player to review.

**Each Card:**
- **Main:** Champion name and image
- **Button:** "Why we suggest this champion" - shows agent-generated explanation when clicked

## Data Schema
- recommendation -> ChampionRecommendation


### If we have time
# Page5: "Pro Player Game Video with Suggested Champion"

## UI flow:
Player selects one champion from Page 4 → System uses AI agent to search for similar pro players (from Page 3) who use the chosen champion → Display video

**Main:** Video of pro player playing the chosen champion (searched by AI agent)

**Body:** 
- Explanation of key points in the video
- Which parts the player should focus on watching

## Data Schema
- ProPlayerChampionVideo (links player's chosen champion + similar pro player + video)

