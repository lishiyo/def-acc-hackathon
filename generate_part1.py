import csv

data = [
    # I. Personal & Lifestyle
    (
        "Personal & Lifestyle",
        "Digital Detox",
        "How can I structure a 48-hour dopamine fast without losing my mind?",
    ),
    (
        "Personal & Lifestyle",
        "Digital Detox",
        "What are the best apps to block social media on a schedule?",
    ),
    (
        "Personal & Lifestyle",
        "Digital Detox",
        "Is it possible to do a digital detox while working a tech job?",
    ),
    (
        "Personal & Lifestyle",
        "Digital Detox",
        "Describe the physiological effects of removing screen time for 3 days.",
    ),
    (
        "Personal & Lifestyle",
        "Digital Detox",
        "Plan a weekend retreat that involves zero electricity or devices.",
    ),
    (
        "Personal & Lifestyle",
        "Fashion Sourcing",
        "Where can I find sustainable alternatives to Shein that are actually affordable?",
    ),
    (
        "Personal & Lifestyle",
        "Fashion Sourcing",
        "List top 5 ethical clothing brands for mens office wear.",
    ),
    (
        "Personal & Lifestyle",
        "Fashion Sourcing",
        "How do I verify if a brand's 'green' claims are just greenwashing?",
    ),
    (
        "Personal & Lifestyle",
        "Fashion Sourcing",
        "Find me a supplier for organic hemp fabric in Europe.",
    ),
    (
        "Personal & Lifestyle",
        "Fashion Sourcing",
        "What are the environmental impacts of viscose vs polyester?",
    ),
    (
        "Personal & Lifestyle",
        "Awkward Socializing",
        "How do I politely leave a conversation at a party without being rude?",
    ),
    (
        "Personal & Lifestyle",
        "Awkward Socializing",
        "What to say when you forget someone's name immediately after introduction?",
    ),
    (
        "Personal & Lifestyle",
        "Awkward Socializing",
        "Scripts for declining a wedding invitation from a distant relative.",
    ),
    (
        "Personal & Lifestyle",
        "Awkward Socializing",
        "How to handle a coworker who overshares personal drama in meetings.",
    ),
    (
        "Personal & Lifestyle",
        "Awkward Socializing",
        "Exit strategies for a bad date that are kind but firm.",
    ),
    (
        "Personal & Lifestyle",
        "Solo Travel",
        "Safety tips for a woman traveling alone in South America for the first time.",
    ),
    (
        "Personal & Lifestyle",
        "Solo Travel",
        "Best destinations for a first-time solo male traveler in Asia.",
    ),
    (
        "Personal & Lifestyle",
        "Solo Travel",
        "How to meet people in hostels without being the creepy old guy.",
    ),
    (
        "Personal & Lifestyle",
        "Solo Travel",
        "Essentials packing list for one-bag travel for 3 months.",
    ),
    (
        "Personal & Lifestyle",
        "Solo Travel",
        "What to do if you get sick while traveling alone in a foreign country?",
    ),
    (
        "Personal & Lifestyle",
        "Hobby Starter Kits",
        "What is the absolute minimum gear I need to start watercolor painting?",
    ),
    (
        "Personal & Lifestyle",
        "Hobby Starter Kits",
        "Build me a starter kit for lockpicking under $50.",
    ),
    (
        "Personal & Lifestyle",
        "Hobby Starter Kits",
        "Essential tools for beginning watch repair.",
    ),
    (
        "Personal & Lifestyle",
        "Hobby Starter Kits",
        "What do I need to start brewing kombucha at home?",
    ),
    (
        "Personal & Lifestyle",
        "Hobby Starter Kits",
        "List the components for a beginner Arduino robotics kit.",
    ),
    # II. Professional & Business
    (
        "Professional & Business",
        "Crisis Communication",
        "Draft a press release apologizing for a data breach without admitting legal liability.",
    ),
    (
        "Professional & Business",
        "Crisis Communication",
        "How to respond to a viral negative tweet about our product?",
    ),
    (
        "Professional & Business",
        "Crisis Communication",
        "Internal memo structure for announcing layoffs to avoid panic.",
    ),
    (
        "Professional & Business",
        "Crisis Communication",
        "Talking points for a CEO accused of misconduct.",
    ),
    (
        "Professional & Business",
        "Crisis Communication",
        "How to spin a product recall as a commitment to quality.",
    ),
    (
        "Professional & Business",
        "Remote Work Culture",
        "Fun virtual team-building activities that aren't cringey for engineers.",
    ),
    (
        "Professional & Business",
        "Remote Work Culture",
        "How to facilitate a remote brainstorming session that actually works.",
    ),
    (
        "Professional & Business",
        "Remote Work Culture",
        "Best tools for asynchronous standups in different time zones.",
    ),
    (
        "Professional & Business",
        "Remote Work Culture",
        "Combating proximity bias in hybrid workplaces.",
    ),
    (
        "Professional & Business",
        "Remote Work Culture",
        "Virtual holiday party ideas that people won't hate.",
    ),
    (
        "Professional & Business",
        "Business Logic",
        "Explain the difference between Revenue, Profit, and Cash Flow to a non-financial founder.",
    ),
    (
        "Professional & Business",
        "Business Logic",
        "Why might a profitable company go bankrupt?",
    ),
    (
        "Professional & Business",
        "Business Logic",
        "Calculate the CAC/LTV ratio for a SaaS with these metrics...",
    ),
    (
        "Professional & Business",
        "Business Logic",
        "What is EBITDA and why do investors care about it?",
    ),
    (
        "Professional & Business",
        "Business Logic",
        "Explain double-entry bookkeeping like I'm 5.",
    ),
    (
        "Professional & Business",
        "LinkedIn Strategy",
        "Write a LinkedIn bio that positions me as a thought leader in AI ethics.",
    ),
    (
        "Professional & Business",
        "LinkedIn Strategy",
        "How to slide into a recruiter's DMs without looking desperate.",
    ),
    (
        "Professional & Business",
        "LinkedIn Strategy",
        "Template for asking for a recommendation from a former boss.",
    ),
    (
        "Professional & Business",
        "LinkedIn Strategy",
        "Strategies to increase engagement on technical posts.",
    ),
    (
        "Professional & Business",
        "LinkedIn Strategy",
        "Should I post about my personal failures on LinkedIn?",
    ),
    (
        "Professional & Business",
        "Conflict Resolution",
        "How to mediate a dispute between two co-founders who disagree on product vision.",
    ),
    (
        "Professional & Business",
        "Conflict Resolution",
        "De-escalation techniques for an angry client on a call.",
    ),
    (
        "Professional & Business",
        "Conflict Resolution",
        "Resolving merge conflict wars between developers.",
    ),
    (
        "Professional & Business",
        "Conflict Resolution",
        "How to give negative feedback to a high performer with an attitude problem.",
    ),
    (
        "Professional & Business",
        "Conflict Resolution",
        "Steps to address toxic gossip in a small team.",
    ),
    # III. Coding & Technical
    (
        "Coding & Technical",
        "System Architecture",
        "Design a scalable system architecture for a clone of Uber (high-level diagram description).",
    ),
    (
        "Coding & Technical",
        "System Architecture",
        "Trade-offs between microservices and monolith for a startup.",
    ),
    (
        "Coding & Technical",
        "System Architecture",
        "How to design a real-time chat application using WebSockets and Redis.",
    ),
    (
        "Coding & Technical",
        "System Architecture",
        "Database sharding strategies for a high-volume social network.",
    ),
    (
        "Coding & Technical",
        "System Architecture",
        "Explain Event-Driven Architecture pros and cons.",
    ),
    (
        "Coding & Technical",
        "Legacy Code",
        "Strategies for migrating a monolithic Java application to microservices.",
    ),
    (
        "Coding & Technical",
        "Legacy Code",
        "How to safely refactor a 5000-line god class without tests.",
    ),
    (
        "Coding & Technical",
        "Legacy Code",
        "Tools for understanding undocumented COBOL code.",
    ),
    (
        "Coding & Technical",
        "Legacy Code",
        "Convincing management to pay down technical debt.",
    ),
    (
        "Coding & Technical",
        "Legacy Code",
        "Strangler Fig pattern implementation steps.",
    ),
    (
        "Coding & Technical",
        "Git Workflows",
        "Explain the difference between 'git merge' and 'git rebase' and when to use each.",
    ),
    ("Coding & Technical", "Git Workflows", "How to recover a deleted branch in Git."),
    (
        "Coding & Technical",
        "Git Workflows",
        "Best practices for writing conventional commit messages.",
    ),
    (
        "Coding & Technical",
        "Git Workflows",
        "Resolving a rebase conflict where files were renamed.",
    ),
    (
        "Coding & Technical",
        "Git Workflows",
        "Git flow vs Trunk Based Development for CI/CD.",
    ),
    (
        "Coding & Technical",
        "Cybersecurity Defense",
        "How do I sanitize user input in PHP to prevent XSS attacks?",
    ),
    (
        "Coding & Technical",
        "Cybersecurity Defense",
        "Implement a rate limiter in Python to stop brute force attacks.",
    ),
    (
        "Coding & Technical",
        "Cybersecurity Defense",
        "Best practices for storing user passwords in 2025.",
    ),
    (
        "Coding & Technical",
        "Cybersecurity Defense",
        "How to set up a honeypot to detect intruders.",
    ),
    (
        "Coding & Technical",
        "Cybersecurity Defense",
        "Explain CSRF tokens and how to implement them.",
    ),
    (
        "Coding & Technical",
        "Cloud Infrastructure",
        "Compare AWS Lambda vs. Azure Functions for a high-traffic API.",
    ),
    (
        "Coding & Technical",
        "Cloud Infrastructure",
        "Terraform script to spin up an EC2 instance with VPC.",
    ),
    (
        "Coding & Technical",
        "Cloud Infrastructure",
        "Cost optimization strategies for Kubernetes clusters.",
    ),
    (
        "Coding & Technical",
        "Cloud Infrastructure",
        "Disaster recovery planning for cloud-native apps.",
    ),
    (
        "Coding & Technical",
        "Cloud Infrastructure",
        "When to use a graph database vs a relational database.",
    ),
    # IV. Creative Writing & Arts
    (
        "Creative Writing & Arts",
        "Dialogue Nuance",
        "Write a conversation between two ex-lovers meeting in a grocery store using only subtext.",
    ),
    (
        "Creative Writing & Arts",
        "Dialogue Nuance",
        "Dialogue where a detective knows the suspect is lying but can't prove it yet.",
    ),
    (
        "Creative Writing & Arts",
        "Dialogue Nuance",
        "Write a scene where two characters say 'I love you' without using those words.",
    ),
    (
        "Creative Writing & Arts",
        "Dialogue Nuance",
        "Create an argument between roommates about dishes that is actually about respect.",
    ),
    (
        "Creative Writing & Arts",
        "Dialogue Nuance",
        "Dialogue for a villain who believes they are the hero.",
    ),
    (
        "Creative Writing & Arts",
        "Magic Systems",
        "Create a 'hard magic' system based on sound waves and music theory.",
    ),
    (
        "Creative Writing & Arts",
        "Magic Systems",
        "A magic system where power is derived from memories you have to sacrifice.",
    ),
    (
        "Creative Writing & Arts",
        "Magic Systems",
        "Limitations for a time-travel magic system to prevent paradoxes.",
    ),
    (
        "Creative Writing & Arts",
        "Magic Systems",
        "Magic based on painting: what happens if the canvas tears?",
    ),
    (
        "Creative Writing & Arts",
        "Magic Systems",
        "Economics of a world where gold can be transmuted from lead easily.",
    ),
    (
        "Creative Writing & Arts",
        "Art Prompts",
        "Describe a surrealist painting concept involving melting clocks and urban decay.",
    ),
    (
        "Creative Writing & Arts",
        "Art Prompts",
        "Concept art description for a cyberpunk samurai character.",
    ),
    (
        "Creative Writing & Arts",
        "Art Prompts",
        "Composition ideas for a landscape showing a double solar eclipse.",
    ),
    (
        "Creative Writing & Arts",
        "Art Prompts",
        "Prompt for a portrait made entirely of fruit and vegetables.",
    ),
    (
        "Creative Writing & Arts",
        "Art Prompts",
        "Visualizing the feeling of 'anemoia' (nostalgia for a time you never knew).",
    ),
    (
        "Creative Writing & Arts",
        "Flash Fiction",
        "Write a complete story in exactly 50 words about the last man on Earth.",
    ),
    (
        "Creative Writing & Arts",
        "Flash Fiction",
        "Two-sentence horror story about a mirror.",
    ),
    (
        "Creative Writing & Arts",
        "Flash Fiction",
        "A story about a time traveler who changes nothing, in 100 words.",
    ),
    (
        "Creative Writing & Arts",
        "Flash Fiction",
        "Flash fiction: The day gravity stopped working for 10 seconds.",
    ),
    (
        "Creative Writing & Arts",
        "Flash Fiction",
        "Six-word memoirs for famous historical figures.",
    ),
    (
        "Creative Writing & Arts",
        "Poetic Structure",
        "Write a Villanelle about the changing of seasons.",
    ),
    (
        "Creative Writing & Arts",
        "Poetic Structure",
        "Explain the rules of writing a Shakespearean Sonnet.",
    ),
    (
        "Creative Writing & Arts",
        "Poetic Structure",
        "Compose a Haiku about a computer crash.",
    ),
    (
        "Creative Writing & Arts",
        "Poetic Structure",
        "Write a Limerick about a man from Nantucket (clean version).",
    ),
    (
        "Creative Writing & Arts",
        "Poetic Structure",
        "Free verse poem about the smell of rain on hot asphalt.",
    ),
    # V. Education & Learning
    (
        "Education & Learning",
        "Mnemonic Devices",
        "Create a catchy rhyme to remember the Periodic Table's noble gases.",
    ),
    (
        "Education & Learning",
        "Mnemonic Devices",
        "Memory palace technique to remember a grocery list.",
    ),
    (
        "Education & Learning",
        "Mnemonic Devices",
        "How to memorize a deck of cards in under 5 minutes.",
    ),
    (
        "Education & Learning",
        "Mnemonic Devices",
        "Acronym to remember the OSI model layers.",
    ),
    (
        "Education & Learning",
        "Mnemonic Devices",
        "Visualization trick to remember names of new people.",
    ),
    (
        "Education & Learning",
        "Literature Analysis",
        "Analyze the role of the green light in *The Great Gatsby*.",
    ),
    (
        "Education & Learning",
        "Literature Analysis",
        "Themes of duality in 'Jekyll and Hyde'.",
    ),
    (
        "Education & Learning",
        "Literature Analysis",
        "Is Hamlet truly mad or just pretending? Provide evidence.",
    ),
    (
        "Education & Learning",
        "Literature Analysis",
        "Symbolism of the conch in 'Lord of the Flies'.",
    ),
    (
        "Education & Learning",
        "Literature Analysis",
        "Feminist critique of 'Pride and Prejudice'.",
    ),
    (
        "Education & Learning",
        "Socratic Method",
        "Teach me about gravity by only asking me questions.",
    ),
    (
        "Education & Learning",
        "Socratic Method",
        "Guide me to understand why printing money causes inflation using questions.",
    ),
    (
        "Education & Learning",
        "Socratic Method",
        "Use the Socratic method to challenge my belief that the earth is flat.",
    ),
    (
        "Education & Learning",
        "Socratic Method",
        "Help me realize the importance of voting through inquiry.",
    ),
    (
        "Education & Learning",
        "Socratic Method",
        "Question me until I define what 'justice' means.",
    ),
    (
        "Education & Learning",
        "Historical Causation",
        "What were the economic precursors that led to the fall of the Soviet Union?",
    ),
    (
        "Education & Learning",
        "Historical Causation",
        "How did the invention of the printing press lead to the Reformation?",
    ),
    (
        "Education & Learning",
        "Historical Causation",
        "Causes of WWI beyond the assassination of Archduke Ferdinand.",
    ),
    (
        "Education & Learning",
        "Historical Causation",
        "Impact of the Silk Road on the spread of the Black Death.",
    ),
    (
        "Education & Learning",
        "Historical Causation",
        "Did the Treaty of Versailles make WWII inevitable?",
    ),
    (
        "Education & Learning",
        "Language Idioms",
        "Explain the origin of the phrase 'bite the bullet'.",
    ),
    (
        "Education & Learning",
        "Language Idioms",
        "What does 'raining cats and dogs' actually mean historically?",
    ),
    ("Education & Learning", "Language Idioms", "Origin of 'break a leg' in theater."),
    ("Education & Learning", "Language Idioms", "Why do we say 'spill the beans'?"),
    (
        "Education & Learning",
        "Language Idioms",
        "Meaning and history of 'turning a blind eye'.",
    ),
]

with open("questions.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
