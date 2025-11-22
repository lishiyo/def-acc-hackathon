import csv

data = [
    # VI. Household & DIY
    (
        "Household & DIY",
        "Smart Home",
        "How can I set up an automation to turn on lights when I arrive home using Home Assistant?",
    ),
    (
        "Household & DIY",
        "Smart Home",
        "Best Zigbee vs Z-Wave devices for a reliable mesh network.",
    ),
    (
        "Household & DIY",
        "Smart Home",
        "Script to simulate occupancy when on vacation using smart bulbs.",
    ),
    (
        "Household & DIY",
        "Smart Home",
        "Integrating a DIY ESP8266 sensor into Apple HomeKit.",
    ),
    (
        "Household & DIY",
        "Smart Home",
        "Privacy-focused smart voice assistants that don't send audio to the cloud.",
    ),
    (
        "Household & DIY",
        "Woodworking",
        "Step-by-step guide to building a simple floating shelf.",
    ),
    (
        "Household & DIY",
        "Woodworking",
        "Difference between a cross-cut and rip-cut saw blade.",
    ),
    ("Household & DIY", "Woodworking", "How to fix a wobble in a wooden chair leg."),
    (
        "Household & DIY",
        "Woodworking",
        "Finishing techniques: Polyurethane vs Danish Oil.",
    ),
    ("Household & DIY", "Woodworking", "Essential safety gear for using a table saw."),
    (
        "Household & DIY",
        "Energy Efficiency",
        "Cheap ways to insulate old windows for the winter.",
    ),
    (
        "Household & DIY",
        "Energy Efficiency",
        "Is a tankless water heater worth the investment?",
    ),
    ("Household & DIY", "Energy Efficiency", "How to conduct a DIY home energy audit."),
    (
        "Household & DIY",
        "Energy Efficiency",
        "Passive solar heating principles for south-facing windows.",
    ),
    (
        "Household & DIY",
        "Energy Efficiency",
        "Smart thermostat settings to maximize savings.",
    ),
    (
        "Household & DIY",
        "Pest Control",
        "Humane ways to get rid of a raccoon under my deck.",
    ),
    ("Household & DIY", "Pest Control", "Natural remedies for ants in the kitchen."),
    ("Household & DIY", "Pest Control", "How to identify bed bugs early."),
    (
        "Household & DIY",
        "Pest Control",
        "Getting rid of fruit flies with household items.",
    ),
    (
        "Household & DIY",
        "Pest Control",
        "Safe mosquito control for a backyard with pets.",
    ),
    (
        "Household & DIY",
        "Car Maintenance",
        "How do I change the spark plugs on a 2015 Honda Civic?",
    ),
    (
        "Household & DIY",
        "Car Maintenance",
        "Diagnosing a clicking noise when turning the steering wheel.",
    ),
    ("Household & DIY", "Car Maintenance", "How to jump start a car safely."),
    (
        "Household & DIY",
        "Car Maintenance",
        "When to change synthetic oil vs conventional oil.",
    ),
    (
        "Household & DIY",
        "Car Maintenance",
        "Steps to replace a flat tire on the side of the road.",
    ),
    # VII. Mental Health & Wellness
    (
        "Mental Health & Wellness",
        "Burnout Recovery",
        "Strategies for returning to work after a month of burnout leave.",
    ),
    (
        "Mental Health & Wellness",
        "Burnout Recovery",
        "Signs that you are approaching burnout before it hits.",
    ),
    (
        "Mental Health & Wellness",
        "Burnout Recovery",
        "Setting boundaries with a demanding boss to prevent relapse.",
    ),
    (
        "Mental Health & Wellness",
        "Burnout Recovery",
        "Daily habits to separate work stress from home life.",
    ),
    (
        "Mental Health & Wellness",
        "Burnout Recovery",
        "How to explain a burnout gap in a resume positively.",
    ),
    (
        "Mental Health & Wellness",
        "Grief",
        "What are the stages of grief, and is it normal to skip some?",
    ),
    (
        "Mental Health & Wellness",
        "Grief",
        "Coping mechanisms for the first anniversary of a loss.",
    ),
    (
        "Mental Health & Wellness",
        "Grief",
        "How to support a friend who just lost a parent.",
    ),
    (
        "Mental Health & Wellness",
        "Grief",
        "Difference between complicated grief and depression.",
    ),
    (
        "Mental Health & Wellness",
        "Grief",
        "Writing a eulogy that honors the deceased honestly.",
    ),
    (
        "Mental Health & Wellness",
        "Imposter Syndrome",
        "Exercises to combat feeling like a fraud in a new high-level job.",
    ),
    (
        "Mental Health & Wellness",
        "Imposter Syndrome",
        "Reframing negative self-talk into constructive criticism.",
    ),
    (
        "Mental Health & Wellness",
        "Imposter Syndrome",
        "Why do high achievers suffer more from imposter syndrome?",
    ),
    (
        "Mental Health & Wellness",
        "Imposter Syndrome",
        "Mentoring others as a cure for your own self-doubt.",
    ),
    (
        "Mental Health & Wellness",
        "Imposter Syndrome",
        "Documenting wins to prove your competence to yourself.",
    ),
    (
        "Mental Health & Wellness",
        "Nutrition",
        "What are some anti-inflammatory foods to add to my diet?",
    ),
    (
        "Mental Health & Wellness",
        "Nutrition",
        "Meal prep ideas for high protein, low carb lunches.",
    ),
    (
        "Mental Health & Wellness",
        "Nutrition",
        "Is intermittent fasting effective for women over 40?",
    ),
    (
        "Mental Health & Wellness",
        "Nutrition",
        "Understanding the gut-brain axis and probiotics.",
    ),
    (
        "Mental Health & Wellness",
        "Nutrition",
        "Healthy snacks that satisfy sugar cravings.",
    ),
    (
        "Mental Health & Wellness",
        "Social Anxiety",
        "Give me a 'ladder' of exposure therapy challenges for fear of public speaking.",
    ),
    (
        "Mental Health & Wellness",
        "Social Anxiety",
        "Breathing techniques to stop a panic attack in public.",
    ),
    (
        "Mental Health & Wellness",
        "Social Anxiety",
        "How to make small talk without feeling like a robot.",
    ),
    (
        "Mental Health & Wellness",
        "Social Anxiety",
        "Cognitive distortions common in social anxiety disorder.",
    ),
    (
        "Mental Health & Wellness",
        "Social Anxiety",
        "Navigating a networking event alone when you're shy.",
    ),
    # VIII. Entertainment & Pop Culture
    (
        "Entertainment & Pop Culture",
        "Film Analysis",
        "Explain the ending of *2001: A Space Odyssey*.",
    ),
    (
        "Entertainment & Pop Culture",
        "Film Analysis",
        "The use of color theory in Wes Anderson movies.",
    ),
    (
        "Entertainment & Pop Culture",
        "Film Analysis",
        "Why is the 'Hero's Journey' structure so prevalent in Hollywood?",
    ),
    (
        "Entertainment & Pop Culture",
        "Film Analysis",
        "Analyze the editing techniques in the shower scene of Psycho.",
    ),
    (
        "Entertainment & Pop Culture",
        "Film Analysis",
        "Impact of the French New Wave on modern cinema.",
    ),
    (
        "Entertainment & Pop Culture",
        "Music Theory",
        "Why does the 'Millennial Whoop' appear in so many pop songs?",
    ),
    (
        "Entertainment & Pop Culture",
        "Music Theory",
        "Explain the circle of fifths to a beginner guitarist.",
    ),
    (
        "Entertainment & Pop Culture",
        "Music Theory",
        "What makes a chord progression sound 'sad'?",
    ),
    (
        "Entertainment & Pop Culture",
        "Music Theory",
        "Polyrhythms explained with examples.",
    ),
    (
        "Entertainment & Pop Culture",
        "Music Theory",
        "The function of the Tritone interval in classical music.",
    ),
    (
        "Entertainment & Pop Culture",
        "Gaming Lore",
        "Summarize the entire timeline of the *Legend of Zelda* universe.",
    ),
    (
        "Entertainment & Pop Culture",
        "Gaming Lore",
        "Who are the Patriots in Metal Gear Solid?",
    ),
    (
        "Entertainment & Pop Culture",
        "Gaming Lore",
        "The history of the fall of Rapture in BioShock.",
    ),
    (
        "Entertainment & Pop Culture",
        "Gaming Lore",
        "Explain the lore behind the Dark Souls undead curse.",
    ),
    (
        "Entertainment & Pop Culture",
        "Gaming Lore",
        "What is the 'Cake is a Lie' meme origin story?",
    ),
    (
        "Entertainment & Pop Culture",
        "Streaming Tech",
        "What is the best OBS setting for streaming 1080p fast-motion gameplay?",
    ),
    (
        "Entertainment & Pop Culture",
        "Streaming Tech",
        "Dual PC streaming setup diagram and requirements.",
    ),
    (
        "Entertainment & Pop Culture",
        "Streaming Tech",
        "How to fix dropped frames in OBS.",
    ),
    (
        "Entertainment & Pop Culture",
        "Streaming Tech",
        "Best microphone for streaming without picking up keyboard clicks.",
    ),
    (
        "Entertainment & Pop Culture",
        "Streaming Tech",
        "Setting up a stream deck for scene transitions.",
    ),
    (
        "Entertainment & Pop Culture",
        "Comic Books",
        "Who would win in a fight: Superman or Dr. Manhattan? Analyze their powers.",
    ),
    (
        "Entertainment & Pop Culture",
        "Comic Books",
        "Reading order for the Marvel Civil War arc.",
    ),
    (
        "Entertainment & Pop Culture",
        "Comic Books",
        "Difference between DC's Multiverse and Marvel's Multiverse.",
    ),
    (
        "Entertainment & Pop Culture",
        "Comic Books",
        "Origin of the Joker: definitive or multiple choice?",
    ),
    (
        "Entertainment & Pop Culture",
        "Comic Books",
        "Top 5 graphic novels for someone who hates superheroes.",
    ),
    # IX. Niche & Specific Utility
    (
        "Niche & Specific Utility",
        "Ham Radio",
        "How do I study for the Technician Class amateur radio license?",
    ),
    (
        "Niche & Specific Utility",
        "Ham Radio",
        "Building a simple dipole antenna for 20 meters.",
    ),
    (
        "Niche & Specific Utility",
        "Ham Radio",
        "Etiquette for making your first contact on a repeater.",
    ),
    (
        "Niche & Specific Utility",
        "Ham Radio",
        "What is a Baofeng radio and why are they controversial?",
    ),
    (
        "Niche & Specific Utility",
        "Ham Radio",
        "Emergency communication protocols during a blackout.",
    ),
    (
        "Niche & Specific Utility",
        "Fountain Pens",
        "Why is my nib scratching the paper? Troubleshooting guide.",
    ),
    (
        "Niche & Specific Utility",
        "Fountain Pens",
        "How to clean a piston-filler fountain pen safely.",
    ),
    (
        "Niche & Specific Utility",
        "Fountain Pens",
        "Difference between gold and steel nibs flex.",
    ),
    (
        "Niche & Specific Utility",
        "Fountain Pens",
        "Best ink for cheap paper that doesn't feather.",
    ),
    ("Niche & Specific Utility", "Fountain Pens", "Restoring a vintage Parker 51."),
    (
        "Niche & Specific Utility",
        "Coffee Roasting",
        "How to roast coffee beans in a popcorn popper.",
    ),
    (
        "Niche & Specific Utility",
        "Coffee Roasting",
        "Understanding the 'first crack' vs 'second crack'.",
    ),
    (
        "Niche & Specific Utility",
        "Coffee Roasting",
        "Sourcing green coffee beans for home roasting.",
    ),
    (
        "Niche & Specific Utility",
        "Coffee Roasting",
        "Cooling techniques for freshly roasted beans.",
    ),
    (
        "Niche & Specific Utility",
        "Coffee Roasting",
        "Degassing timeline for espresso beans.",
    ),
    (
        "Niche & Specific Utility",
        "Mechanical Keyboards",
        "Explain the difference between Cherry MX Red and Blue switches.",
    ),
    (
        "Niche & Specific Utility",
        "Mechanical Keyboards",
        "How to lube keyboard switches without desoldering.",
    ),
    (
        "Niche & Specific Utility",
        "Mechanical Keyboards",
        "Building a custom 60% keyboard from a kit.",
    ),
    (
        "Niche & Specific Utility",
        "Mechanical Keyboards",
        "What is a gasket mount and does it matter?",
    ),
    (
        "Niche & Specific Utility",
        "Mechanical Keyboards",
        "Group buy culture in mechanical keyboards explained.",
    ),
    (
        "Niche & Specific Utility",
        "Mycology",
        "How to identify a 'Chicken of the Woods' mushroom safely.",
    ),
    (
        "Niche & Specific Utility",
        "Mycology",
        "Spore print technique for mushroom identification.",
    ),
    (
        "Niche & Specific Utility",
        "Mycology",
        "Sterilization methods for growing mushrooms on grain spawn.",
    ),
    (
        "Niche & Specific Utility",
        "Mycology",
        "Differentiating between morels and false morels.",
    ),
    (
        "Niche & Specific Utility",
        "Mycology",
        "Medicinal properties of Lion's Mane mushrooms.",
    ),
    # X. Abstract & Philosophical
    (
        "Abstract & Philosophical",
        "Solipsism",
        "Convince me that I am the only conscious being in the universe.",
    ),
    (
        "Abstract & Philosophical",
        "Solipsism",
        "Arguments against solipsism from a pragmatic perspective.",
    ),
    (
        "Abstract & Philosophical",
        "Solipsism",
        "How does solipsism differ from nihilism?",
    ),
    (
        "Abstract & Philosophical",
        "Solipsism",
        "The 'Brain in a Vat' thought experiment explained.",
    ),
    ("Abstract & Philosophical", "Solipsism", "Is solipsism a falsifiable theory?"),
    (
        "Abstract & Philosophical",
        "The Ship of Theseus",
        "If I replace every part of a car over 10 years, is it the same car?",
    ),
    (
        "Abstract & Philosophical",
        "The Ship of Theseus",
        "Does the Ship of Theseus apply to human cell regeneration?",
    ),
    (
        "Abstract & Philosophical",
        "The Ship of Theseus",
        "Teleportation and the continuity of consciousness problem.",
    ),
    (
        "Abstract & Philosophical",
        "The Ship of Theseus",
        "Digital identity: If I copy my mind to a computer, is it me?",
    ),
    (
        "Abstract & Philosophical",
        "The Ship of Theseus",
        "Legal implications of identity in a Ship of Theseus scenario.",
    ),
    (
        "Abstract & Philosophical",
        "Free Will",
        "Does neuroscientific evidence suggest free will is an illusion?",
    ),
    (
        "Abstract & Philosophical",
        "Free Will",
        "Compatibilism: reconciling determinism and free will.",
    ),
    (
        "Abstract & Philosophical",
        "Free Will",
        "The implications of no free will on the justice system.",
    ),
    ("Abstract & Philosophical", "Free Will", "Libet's experiment and its criticism."),
    (
        "Abstract & Philosophical",
        "Free Will",
        "Existentialist view on radical freedom.",
    ),
    (
        "Abstract & Philosophical",
        "Simulation Theory",
        "What are the statistical arguments for us living in a simulation?",
    ),
    (
        "Abstract & Philosophical",
        "Simulation Theory",
        "Glitches in the matrix: anecdotal evidence or cognitive bias?",
    ),
    (
        "Abstract & Philosophical",
        "Simulation Theory",
        "Bostrom's Trilemma explained simply.",
    ),
    (
        "Abstract & Philosophical",
        "Simulation Theory",
        "How could we test if we are in a simulation?",
    ),
    (
        "Abstract & Philosophical",
        "Simulation Theory",
        "Religious parallels in Simulation Theory.",
    ),
    (
        "Abstract & Philosophical",
        "Teleportation",
        "If a teleporter deconstructs you and rebuilds you, did you die?",
    ),
    (
        "Abstract & Philosophical",
        "Teleportation",
        "The 'Prestige' problem: killing the original copy.",
    ),
    (
        "Abstract & Philosophical",
        "Teleportation",
        "Quantum entanglement and teleportation of information.",
    ),
    (
        "Abstract & Philosophical",
        "Teleportation",
        "Philosophical zombie argument applied to teleported clones.",
    ),
    (
        "Abstract & Philosophical",
        "Teleportation",
        "Would you step into a Star Trek transporter? Why or why not?",
    ),
]

with open("questions.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
