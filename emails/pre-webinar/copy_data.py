# Pre-webinar sequence: Aiden's copy (Oct 22 doc), with only the fixes listed in CHANGES.
# Block syntax: plain string = paragraph ("\n" = line break) · "BTN:Label|URL" · "SMALL:text" · "LIST:a||b||c"
# Inline: [text](URL) links, **bold**. URL keys: WJ, GCAL, ICS, CS:<name> (case study link, still needed).

AIDEN = 'Aiden from Vacarya'
REHAN = 'Rehan from Vacarya'

EMAILS = [
  dict(n=1, day='Registration', when='Immediately', purpose='Registration Confirmed', timing='Immediate', sender=AIDEN,
       subject="You're in. Here's your link",
       preview='Date, time, your link, and one quick favour.',
       body=[
         '{{contact.first_name}},',
         "You're registered for the Airbnb Masterclass. Confirmed.",
         "Here's what you need:",
         '📅 Date: This Wednesday\n🕐 Time: 7PM EST / 4PM PST\n💻 Link: [Live Masterclass](WJ)',
         "Before you close this email, do one thing if you haven't yet.",
         '👉 [ADD THIS TO YOUR CALENDAR](GCAL) 👈',
         "It takes 10 seconds, and the people who add it are 3X more likely to show up live. And the ones who show up live? They're the ones who walk away knowing the exact steps to get started on Airbnb and skip the majority of trial-and-error.",
         "And I likely won't do a replay. Just being real.",
         "I'm keeping this training intentionally small because I'm actually trying to help you, not talk to a bunch of people who are half-listening while folding laundry or walking their dog.",
         "So if you're in, be IN!",
         "One more thing. Hit reply and tell me: What's the #1 question you want answered about Airbnb arbitrage going into this?",
         "I'm building this entire thing around the questions I get here.",
         'See you on the call.',
         'Aiden',
         'BTN:ADD EVENT TO CALENDAR|GCAL',
         'SMALL:Using Apple Calendar or Outlook? [Add it here](ICS).',
       ]),
  dict(n=2, day='Registration', when='10 min after sign-up', purpose='The Realization', timing='+10 Min', sender=AIDEN,
       subject='This sounds backwards at first',
       preview='It has nothing to do with buying property.',
       body=[
         '{{contact.first_name}},',
         'Before we talk on Wednesday, I want to leave you with something to sit with.',
         'A realization.',
         "It sounds completely backwards at first, but once I understood it, I never looked at Airbnb the same way again.",
         "I'll show you exactly what I mean when we hop on the live training. But here's the piece I'll leave you with for now:",
         'Not only is buying property the worst possible way into short-term rentals, it actually has nothing to do with the money you make in this business at all.',
         "I know it sounds ridiculous. We've all been taught that Airbnb is real estate, and real estate builds equity.",
         "We've been told that one our whole lives. Which is exactly why everyone looks at this business the wrong way.",
         "But the thing that actually drives this business is something else entirely.\n(And no, it's not leasing either)",
         'The largest players in hospitality figured this out years ago and built their entire empires around it while we were focused on "building equity".',
         'Once you understand it, the whole business starts making a lot more sense.',
         "I'll leave you with that. The rest, when we talk on Wednesday.",
         'See you there,\n-Aiden',
         'P.S. I first met Patricia through a free live workshop I did a couple years ago. At the time, she thought buying property was the only way to make money on Airbnb. Now she has 18 Airbnb properties. [See for yourself.](CS:patricia)',
       ]),
  dict(n=3, day='Monday', when='Mon 9:00 AM ET', purpose='Saturated', timing='Mon 9AM', sender=AIDEN,
       subject='Let me ruin a sentence for you',
       preview='"Airbnb is saturated" is only half a sentence.',
       body=[
         '{{contact.first_name}},',
         "On Wednesday I'm going to walk you through the exact strategy we use to set up profitable Airbnbs in any city in North America (Yes, I said any).",
         'But before that, I need to ruin a sentence for you.',
         'The sentence "Airbnb is saturated."',
         "The reason it's a worthless sentence is the same reason Wednesday is going to be one of the more interesting 60 minutes or so you've spent in a long time.",
         "It's because saturated cities don't exist.",
         'Stick with me here.',
         "You've probably heard the opposite a thousand times.\nThat the good markets are gone.\nThat you needed to be in five years ago.\nThat Airbnb is dead. I get it.",
         "But it simply isn't true.",
         "And the reason it isn't true is one of my favourite things to walk people through, because it just clicks once you see it.",
         "Here's the small piece I'll give you now.",
         '"Airbnb is saturated" isn\'t just a wrong sentence.\nIt\'s a sentence with the second half cut off.',
         "On Wednesday I'll finish that sentence for you.",
         "By the end of the training, you'll understand how to find profitable Airbnb properties in any market.",
         '-Aiden',
         "P.S. Here's a [case study of Rob](CS:rob), who is making serious money in notoriously ‘saturated’ markets like Dallas, Houston, and more using the exact strategy you're about to learn. He has 15 properties now.",
       ]),
  dict(n=4, day='Monday', when='Mon 1:00 PM ET', purpose='Second Job', timing='Mon 1PM', sender=AIDEN,
       subject='Am I just buying myself a second job?',
       preview='The question almost every smart person asks.',
       body=[
         '{{contact.first_name}},',
         "There's a question almost every smart person asks themselves before they consider Airbnb.",
         "Maybe you've asked it too. I definitely did.",
         '"Am I just buying myself a second job?"\n"I don\'t have enough time for this…"',
         'I want to get that out of the way before Wednesday.',
         "I've heard that question on more calls than I can count. And every time, my answer is the same:",
         'No. Not if you build it the right way.',
         "On Wednesday, I'm going to show you how to run Airbnb arbitrage in 3-5 hours a week regardless of how many properties you have.",
         'The funny thing is, it usually comes down to one move you make at the very start.',
         "The people running this in a few hours a week made it. (Like [Helen](CS:helen) for example)\nThe ones answering guests at 2AM, obviously, didn't.",
         'With the right systems in place the business runs while you do..well, whatever, actually.',
         "The good news for you though is that I've already spent the last six years figuring this out and building these systems so you don’t have to.",
         "Anyways, I'll show you the move that makes this all possible on Wednesday.",
         '-Aiden',
         "P.S. Just a reminder, I won't be sending out replays for this one.",
       ]),
  dict(n=5, day='Monday', when='Mon 6:00 PM ET', purpose='Operator Not Owner', timing='Mon 6PM', sender=AIDEN,
       subject='The thing that confuses everybody',
       preview="You're the operator, not the owner.",
       body=[
         '{{contact.first_name}},',
         'Let me clear up the biggest point of confusion before we go live.',
         'When people hear "Airbnb," they picture buying a house. A mortgage and down-payment. Property taxes.',
         'That is not this.',
         'Airbnb arbitrage means you control the property and rent it out to guests without buying it. You are not the owner. You are the operator.',
         'The owner gets a reliable tenant. The guests get a great place to stay. You keep the spread in the middle. Everybody wins.',
         'Now here is the objection that trips people up. "But I am not building equity."',
         'Fair question. So let me ask you one back. Would you rather own a slow appreciating asset that ties up a hundred grand of your money, or would you rather have cash flow hitting your account every single month starting now?',
         'Equity is money you might get someday if you sell. Cash flow is money you get this month, and next month, and the month after that.',
         'Allow me to let you in on a little secret: 98% of hotel companies DO NOT own their buildings. And there is a good reason for it. It’s slow.',
         'When you see how the math actually works on the training, it’s incredibly likely you will never look at Airbnb the same.',
         'See you on Wednesday.',
         '-Aiden',
         'P.S. Here is a recent [case study from our Vacarya partner Mike](CS:mike), who was incredibly skeptical at first. In less than 10 weeks he now has 7 properties.',
       ]),
  dict(n=6, day='Tuesday', when='Tue 9:00 AM ET', purpose='Why Smart People Fail', timing='Tue 9AM', sender=AIDEN,
       subject='Why smart people still fail at this',
       preview='The information is the easy part.',
       body=[
         '{{contact.first_name}},',
         'I want to be honest with you, because a lot of people in this space will not be.',
         'You can absolutely learn Airbnb arbitrage on your own. The information is out there. Some people make it work. Hell, I did.',
         'But here is what nobody tells you, and what I wish I knew all those years ago.',
         'The information is the easy part. The execution is where this business all falls apart.',
         'Finding properties that make money. Convincing buildings to allow you to lease from them. Flying over to design and set these up. Pricing correctly so you are maximizing the money you make. Understanding regulations that change from one city to the next.',
         'Each one of those is a skill. And behind each skill is a ton of trial and error and costly mistakes.',
         'I know this because I have the largest arbitrage operation in North America. I’ve made every expensive mistake in the book, and then some.',
         "This works out great for you though, because you'll be able to skip all this entirely and start making money, well, pretty much right away.",
         'That is the difference between doing it yourself and having it built for you by us.',
         'One takes years of trial and error, uncertainty, risk, and wasted cash (speaking from experience).',
         'The other by-passes all of that, right to the profit.',
         'The only problem here is that you don’t believe me. Which is totally fair. Talk is cheap.',
         '[Hear it from our Vacarya partner Josh instead.](CS:josh)',
         "I'm not trying to sell you anything here. I just want you to understand why the cheaper route on paper doesn't always turn out to be cheaper in practice.",
         'See you on Wednesday.',
         '-Aiden',
       ]),
  dict(n=7, day='Tuesday', when='Tue 1:00 PM ET', purpose='Who Is Real', timing='Tue 1PM', sender=AIDEN,
       subject='How to tell who is actually real',
       preview='A simple filter you can run on anyone. Including me.',
       body=[
         '{{contact.first_name}},',
         'You have seen them. The guy renting a lambo for the afternoon, filming in front of it, telling you how easy it is to get rich with Airbnb.',
         'I cannot stand these guys. They are taking a fantastic business model and ruining its image with flashy marketing to try to sell their crappy coaching programs.',
         'Here is a simple filter you can run on anyone in this space, including me. As a matter of fact, I highly encourage you to.',
         'Ask them for numbers that are actually hard to fake. Not screenshots of bank accounts or Airbnb revenue. Those prove very little.',
         "I'm talking about real operational scale. The kind that takes years to build.",
         'I will go first.',
         'Last year we did $12.5 million dollars in revenue. All from Airbnb. $0 from “coaching”.',
         'That is about $1.58 million a month.\nWe have 493 active properties now.\nWe have hosted over 65,000+ stays in the past year alone.\nWe have more than 100 Vacarya partners running under our brand right now.',
         'Some of them are clearing over a million a year on their OWN. [(see for yourself)](CS:million)',
         'I encourage you to look around this industry and find someone operating at even 1/10th of our scale.',
         'You can’t. Because they’re in the business of “coaching”. We’re in the business of Airbnb.',
         "And about those scary Airbnb headlines you keep seeing. Most of them are about people who overpaid for a house in the wrong market and now can't cover their mortgage.",
         "That's an ownership problem, not an operator problem. And it has absolutely nothing to do with the model we'll be covering.",
         "In the live workshop, I'll show you why those headlines aren't just overblown, but why they're entirely irrelevant to what we're doing.",
         'See you at the live training.',
         '-Aiden',
       ]),
  dict(n=8, day='Tuesday', when='Tue 6:00 PM ET', purpose='Never Run A Business', timing='Tue 6PM', sender=AIDEN,
       subject='If you have never run a business before',
       preview='The real reason people hesitate.',
       body=[
         '{{contact.first_name}},',
         'There is a good chance you have never owned a business. Most of the people who register haven’t.',
         'So let me speak to the fear directly, because it is the real reason people hesitate even when the numbers look great.',
         'The fear is not really about Airbnb arbitrage, or Vacarya, or even business in general.',
         'It is "who am I to do this?"',
         'You have spent years being good at your job.\nFollowing a process someone else built.\nGetting rewarded for being reliable.',
         'Nothing wrong with that. These are real skills.',
         'The truth is running your own business just asks for a slightly different version of you.',
         'Not smarter, or more special. Just someone willing to own the outcome instead of waiting to be told what to do.',
         'That’s what it was for me, anyways.',
         'Now here is the part that makes it easier.',
         'You do not have to figure this out from scratch. The systems already exist. The playbook is already written. I’ve already gone through the hard parts. You would be stepping into something that already works with 6+ years of experience behind you, not inventing it.',
         'Some of you have been burned before. Maybe you paid a coach, received a course and a pat on the back, and were left to sink on your own. So trust me. I get the skepticism.',
         'You should be skeptical. This would make you smart in my eyes.',
         "All I ask is that you give this a fair shot. Ask the hard questions, even challenge what I say, but remember that you'll never hit a home run if you refuse to swing the bat.",
         'See you on Wednesday.',
         '-Aiden',
         'P.S. Our Vacarya partner, Ravi, is a great example of this. And [look where he is today!](CS:ravi)',
       ]),
  dict(n=9, day='Wednesday', when='Wed 2:00 PM ET (T-5 hrs)', purpose='Tonight Reminder', timing='Wed T-5H', sender=AIDEN,
       subject='Tonight at 7PM EST',
       preview='A year from now, do you want to be in the same spot?',
       body=[
         'Hey {{contact.first_name}} - quick reminder:',
         "Our Airbnb live masterclass is tonight, and I don't want you missing out.",
         '⏰ Time: 7pm Eastern / 4pm Pacific\n🔗 Join Link: [Live Masterclass](WJ)',
         'Now right on cue, if your brain is already doing the whole "I just don\'t have time for this masterclass tonight…"',
         'Let me flip that and ask you:',
         'A year from now, do you really want to be in the same spot?',
         "The reason you're so busy IS the exact reason you should show up later.",
         "It's ironic, but true.",
         "The whole point of tonight is to teach you how to build a second income stream that isn't tied to your hours, right?!",
         "Now, I can't promise you'll join and become an Airbnb millionaire (Although it's happened quite a few times now).",
         'But I can promise you this:',
         "I'll walk you through the exact strategy we've used across 493 properties and over $15M+ a year in earnings, and you'll leave with a clear framework to have your Airbnb business up and running in the next 90 days.",
         "I mean, statistically speaking… if we can do over $1.8M a month, surely I can help you get to $5K, right?! If I can't even do that after all these years, then I may as well quit while I'm ahead and start handing out job applications.",
         'Listen, this might be the thing that changes the direction of your life like it was for me. Or it won\'t.',
         "But either way, you'll leave with an answer.",
         'At some point, doing nothing starts costing you too. Just being real.',
         'See you at 7.',
         '- Aiden',
       ]),
  dict(n=10, day='Wednesday', when='Wed 6:00 PM ET (T-1 hr)', purpose='One Hour', timing='Wed T-1H', sender=AIDEN,
       subject='See you in an hour',
       preview='Close your other tabs and grab a notebook.',
       body=[
         '{{contact.first_name}}, the countdown is ON.',
         "In 60 minutes we go live with the Airbnb Masterclass, and you're going to want to be there from the jump.",
         '🕗 Time: 7pm Eastern / 4pm Pacific (we start on time)\n📍 Join Link: [Live Masterclass](WJ)',
         "Remember, here's what's waiting for you:",
         'LIST:How to find a profitable Airbnb property in any city, even the ones everyone thinks are "too saturated."||How to set up an Airbnb property without EVER stepping foot in the city.||How to run your properties in 3–5 hours a week, regardless of how many you have.',
         "Oh, and there's one more thing I've purposely held back until tonight that will completely change the way you see Airbnb forever. For the better or worse.",
         'And just a heads up:',
         "You’ll have to pay to watch this live. It's just not financial.",
         'All I ask from you is that you pay with your attention, and I will teach you everything I possibly can in the timeframe we have. My word. (did i get you?!)',
         "So here's what I want you to do:",
         '- Close your other tabs\n- Grab a notebook\n- Be ready when the doors open',
         'See you in an hour.',
         '- Aiden',
         "P.S. You can join with the link below although I'm sure WebinarJam has sent you 20+ emails by now.",
         'BTN:CLICK TO JOIN LIVE|WJ',
       ]),
  dict(n=11, day='Wednesday', when='Wed 6:30 PM ET (T-30 min)', purpose='Before We Go Live', timing='Wed T-30M', sender=AIDEN,
       subject='Before we go live',
       preview='This is not a 90-minute infomercial.',
       body=[
         '{{contact.first_name}},',
         'The training is almost here, and I want you to actually get something out of it, so let me set your expectations.',
         'This is not a 90 minute infomercial. If you have sat through one of those, you know the feeling. This is not that.',
         'Here is what you are going to walk away understanding:',
         'LIST:How to find a profitable Airbnb property in any city, even the ones everyone thinks are "too saturated."||How to set up an Airbnb property without EVER stepping foot in the city.||How to run your properties in 3–5 hours a week, regardless of how many you have.',
         'Whether we ever work together or not, you will leave knowing more about this model than almost anyone talking about it online.',
         'And one final reminder that there will be NO replays.',
         'Block the time. Close the other tabs. Bring that one objection you are still holding onto, because I promise I have heard it, and I will take it on head first.',
         'See you in 30 minutes',
         '-Aiden',
         'BTN:CLICK TO JOIN LIVE|WJ',
       ]),
  dict(n=12, day='Wednesday', when='Wed 7:15 PM ET (+15 min)', purpose='We Are Live', timing='Wed +15M', sender=REHAN,
       subject="We're live (doors close at 7:25)",
       preview='Aiden is covering something important right now.',
       body=[
         'Hey {{contact.first_name}},',
         "It's Rehan from Vacarya.",
         "We're a few minutes into tonight's live training, and Aiden is covering something I think is particularly important for anyone considering getting into short-term rentals.",
         "There's a big difference between investing in real estate, and building a business around it.",
         'And understanding that difference can completely change how you think about deploying your capital, generating cash flow, and scaling.',
         "It's something Aiden learned firsthand while building an operation of over 400 Airbnb properties without purchasing the real estate itself.",
         "If you're seriously considering entering this space, I think you'll find this conversation valuable.",
         'BTN:JOIN THE LIVE TRAINING|WJ',
         'We started at 7:00 PM, and access closes at 7:25 PM.',
         "There won't be a replay.",
         'See you inside,\nRehan\nVacarya Team',
       ]),
]

# SMS: straight apostrophes only (a curly one forces UCS-2 = 70 chars per segment). No STOP line: GHL adds it.
SMS = [
  dict(group='On registration', label='SMS 1', when='Immediately', text=
    "Hey {{contact.first_name}}, is that you? It's Aiden.\n\n"
    "I see you registered for this Wednesday's live training at 7 PM EST, where I'll be showing you how to get started with Airbnb without buying property.\n\n"
    "Just wanted to personally reach out and make sure you're planning to join us.\n\n"
    "If you could do me a quick favour and reply \"YES\" to confirm your attendance for Wednesday, I'd really appreciate it!\n\n"
    "Thanks in advance."),
  dict(group='On registration', label='SMS 2', when='If they reply YES (Aiden: wait 10 min)', text=
    "You're confirmed!\n\n"
    "One last thing. If you passed on VIP during registration, I'd really recommend taking another look.\n\n"
    "I put together the exact tools and resources I wish I had when I started.\n\n"
    "My goal is that you don't just leave the training knowing how this business works, but have the actual tools we use to build it, plus a private 1-on-1 with our VP to map out your own launch.\n\n"
    "You can still add it here: https://event.hostvacarya.com/vip\n\n"
    "See you Wednesday!"),
  dict(group='Wednesday countdown', label='SMS 1', when='Wed 10:00 AM ET (morning)', text=
    "Hey {{contact.first_name}}, it's Aiden!\n\n"
    "We're going live tonight at 7 PM EST.\n\n"
    "I'll be walking you through how to build a profitable Airbnb business in as little as 90 days without buying property, using the same model we've used to host over 65,000 stays in the past year.\n\n"
    "Quick question before we go live. What's the one thing you're most interested in learning tonight?\n\n"
    "I'm using everyone's answers to help shape the training, so just reply here and let me know!"),
  dict(group='Wednesday countdown', label='SMS 2', when='Wed 6:00 PM ET (T-1 hr)', text=
    "Hey {{contact.first_name}}, it's Aiden. We go live in just 1 hour!\n\n"
    "I'll be breaking down how we've built an Airbnb business that's collected over $12.5M in the past year and how you can get started with the same model in the next 90 days.\n\n"
    "Keep an eye on your texts and email. I'll send you the link shortly before we start.\n\n"
    "See you at 7 PM!"),
  dict(group='Wednesday countdown', label='SMS 3', when='Wed 6:30 PM ET (T-30 min)', text=
    "Hey it's Aiden, we go live in 30 minutes and I'm sending out the link shortly.\n\n"
    "Will you be joining on a computer or phone?"),
  dict(group='Wednesday countdown', label='SMS 4', when='Wed 6:50 PM ET (T-10 min)', text=
    "We go live in 10! Join in here:\n{{contact.webinar_link}}"),
  dict(group='Wednesday countdown', label='SMS 5', when='Wed 7:00 PM ET (live)', text=
    "{{contact.first_name}}, we're LIVE!\n\n"
    "I'm breaking down the business model behind our 400+ active Airbnb rentals, how we identify profitable properties, and how you can build your own operation without purchasing real estate.\n\n"
    "If you've been considering entering the short-term rental space, this is a conversation worth being part of.\n\n"
    "Join us here:\n{{contact.webinar_link}}"),
  dict(group='Wednesday countdown', label='SMS 6', when='Wed 7:15 PM ET (+15 min)', text=
    "{{contact.first_name}}, just wanted to make sure you've made it in?\n\n"
    "We have limited room capacity tonight, and spots are filling up quickly.\n\n"
    "If you haven't joined yet, use the link in my previous text to get in."),
  dict(group='Wednesday countdown', label='SMS 7', when='Wed 7:20 PM ET (last chance)', text=
    "Last chance before we close the live room!\n\n"
    "I'm showing you how we collected over $12,500,000 and hosted 65,557 Airbnb stays in the past year alone.\n\n"
    "Join here:\n{{contact.webinar_link}}"),
]

CASE_STUDIES = {
  'patricia': 'Patricia (Email 2)', 'rob': 'Rob (Email 3)', 'helen': 'Helen (Email 4)', 'mike': 'Mike (Email 5)',
  'josh': 'Josh (Email 6)', 'million': '"see for yourself" partners clearing $1M+/yr (Email 7)', 'ravi': 'Ravi (Email 8)',
}

CHANGES = [
  'Join links: <code>{{contact.webinarlink}}</code> (Main key) → <code>{{contact.webinar_link}}</code>, each person\'s own WebinarJam link. SMS 4, 5 and 7 use it too instead of the shared room link.',
  '<code>{{ custom_values.webinar_date }}</code> doesn\'t exist → "This Wednesday".',
  '<code>{{contact.webinar_calendar_invite}}</code> doesn\'t exist → Google Calendar link + Apple/Outlook link. Both always pick the next Wednesday 7 PM and put the person\'s own join link inside the event.',
  'SMS <code>{{appointment.*}}</code> (no appointment exists) → "this Wednesday" / "7 PM EST". <code>{vip link]</code> → https://event.hostvacarya.com/vip.',
  'Typos: Email 3 "On Thursday" → "On Wednesday". Email 9 "in less the next 90 days" → "in the next 90 days". Email 6 "Understand regulations" → "Understanding regulations". "P.S" → "P.S.". Double space in Email 8. SMS: "i\'m" → "I\'m".',
  'Email 7 had no sign-off → added "-Aiden" like the others.',
  'SMS: straight apostrophes only (a curly one doubles the cost). No "Reply STOP" line, GHL adds it.',
  'New subject lines for Emails 1, 2, 3, 4, 9, 10, 12, plus preview text for all 12. Emails 5–8 and 11 keep Aiden\'s subjects.',
  'Numbers left exactly as Aiden wrote them.',
]
