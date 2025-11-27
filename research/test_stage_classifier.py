#!/usr/bin/env python3
"""
GLOBAL TEST HARNESS FOR STAGE CLASSIFIER
========================================
This file runs:

1. Real natural SA360 narrative data (David, Mark, John, Rob)
2. Synthetic edge-case scenarios
3. Short sanity checks
4. Stress tests for long input

Outputs a full JSON dump per case.

USAGE:
    python3 global_stage_test.py
"""

from stage_classifier import _score_text
import time, json


# --------------------------------------------------------------------
# REAL-WORLD NATURAL DATA (copied from your actual .docx imports)
# --------------------------------------------------------------------

DAVID = """
Bought a new home and moved into it, non-working HVAC and insurance cancelation for lack of railing. To "deal" with it, I got into action (met, discussed, planned, coordinated, designed, submitted, provided oversight, etc.) for many days and resolved the issue, but I also got annoyed, frustrated, resentful, and went through a period of "eff-it" that included isolation, drinking/etc., acting out for multiple days. This was unhealthy, although it did "work" in some ways, the cost/benefit was disproportionally on the costly side.

I get tightness in chest/throat, discomfort, and it comes out as avoidance/isolation AND/OR lashing out/anger, frustration, AND/OR focused action and resolution.

I am not sure about this one. I think long-term, the biggest difference/change is seeing myself as responsible for outcomes rather than a victim.

Over time when explaining to my partner various needs in the relationship, I have felt as though my concerns were not being heard or acknowledged both in the conversation and in subsequent interactions with him in the relationship.

I think every time I have an upset and I respond with frustration, anger, etc. my values are tested since this goes against my values of connection, love, compassion, respect, etc. These types of responses happen more when I am more stressed and take less self-care, which is a lot lately.

I have cognitive dissonance around many things /impulses, instinct, desires, but these are mostly around food, sex, alcohol/etc. I typically work with it by acknowledging it and choosing a healthy behavior or to connect with someone in a healthy way (conversation, etc.). Sometimes, if my stress is too high, I give in and say screw it...and then it's on.

My inner voice gives me as many passes as it is an astute director. I also realize that I do not relate to myself or inner voice as though it is distinct from my reality. While I have distinguished it before, I do not generally live life in seasoned practice of distinguishing my inner voice from my reality (which I realize is not very transformed)

I experience emotions as though they are the most significant thing in the world... life or death, good vs. bad, all in vs. nothing left etc.; and this hasn't always been the case (I have been through periods where I was a good emotional regulator/manager). Strong feelings do challenge my clarity and decision-making, at least initially until I take a pause/breath/break from them to respond more from love than from fear.

Sometimes I tend to be a quiet outsider then as people talk, I get more and more inclined to participate, then I get antsy and frustrated by my lack of participation until I jump in and respond from emotion more than thought. Other times, I show up and listen and participate freely... it depends on how I relate to the group...

I stay open by trying to see what we have in common, in our common humanity, etc. I try to empathize with them/their situation. Being involved with different groups helps me stay connected.

Being inconsiderate to people's feelings/needs/situations really gets under my skin. Quick to judgement and total assessments of people as good/bad/etc. based on observation or limited experiences gets under my skin. I admire people when they are balanced, supportive, yet independent.

I relate to my body and energy as something to care for, but that I occasionally do not care fore. I feel guilt/shame when I do not. My physical vitality and sexual vitality has changed in that I cannot push as much as I used to.

Currency as access to experiences, things, and met needs. Something to manage, save, invest.

I need to save more. I am spending too much. This has been my story for awhile around money, but I do see it as access to freedom or possibility.

Limited resource, access to opportunity/opportunity for experiences.

Not enough of a role....I do some spatial arrangement in-home, etc. but cannot think of other creative outlets at the moment.

I relate to spirit as something in all of us and everything as a frequency/frequencies that I can attune to (or not). I believe we are in this life as a means to grow our spirit through life experiences and that we are connected to everything. I have had interactive experiences with spirit energies.

I am empowered to grow and evolve, but I get stuck and set back, and when I do, I tend to be pretty hard on myself. Overall, I have lived a life committed to self discovery, growth, and development. I am committed to those things.

Connection with others, accomplishment in my work, future planned events, relationships. What has changed is that it is less so now being a high achiever at work and more so having time and space to care for myself.
"""

MARK = """
I'll tell you about my divorce. It happened four years ago. But in a sense I'm still working through it. During Covid and even the years leading up, I was struggling with my now ex-wife, Lynda. Lynda and I did not see eye to eye on money management. She was a prolific over spender. We were going through some lean times, and Covid didn't help. During the initial years of our marriage, I let Lynda handle the finances, and I made the money. She worked very little. She took care of our daughter, Alana, but also had a housekeeper and babysitter. It was my neglect of not keeping an eye on the budget and her over spending that led to progressive debt. Lynda came into the marriage after a bankruptcy and had poor credit. I on the other hand, had a credit score above 800. But I don't want to blame this all on Lynda. I should've kept an eye on the books. Because I didn't, we got into some credit card debt that we had no reasonable way of paying off. Because of that situation, I lived with a lot of stress and developed some stress related illnesses. I was looking for away out when I met a man named David Cota. I'd always had the dream of opening my own retreat facility. He made himself out as a wealthy entrepreneur, eager to help me with my dream. I took some extraordinary risks to make that happen but the deal ultimately didn't go through. That plunged us into more debt - debt I'm still paying off. Somewhere during that time (2020-2021) Lynda met someone and had an affair. She gaslighted me through the whole experience. I knew something was amiss, and I was trying to repair the marriage, but she just strung me along until she was able to make the jump to this other guy. The guy who is now her boyfriend is wealthy. The affair was devastating. I've never experienced betrayal trauma like that. I got so sick that I got down to 112 pounds. My normal weight is 135. I got a flu in January 2022 that nearly killed me. It's been a long road back. Lots of introspection, shadow work, and diving deep into my spiritual practice. Fast forward to June of this year, Lynda moved to Alaska with her boyfriend, leaving me to parent Alana full-time during the school year. Deep down there's still anger over the choices Lynda has made and how it's affected me and Alana. But I'm more angry about how it's affected Alana. For me, I can gain perspective and see this as a heroes journey, a developmental task that I asked for before this incarnation. So that's how I'm handling it, as a spiritual challenge. I tell myself, "I'm the one." That simple phrase keeps me from kvetching and complaining and focuses me forward on doing what's right and turning this difficulty into something beautiful.

Strong emotions open my awareness. Quite the opposite of fixating me and losing myself, I become more aware. My awareness includes awareness of my surroundings, my body sensations, and my mental activity. I'm aware that I'm aware. And I breathe, and I feel, and I let things flow. In that state, wise actions, the next right thing, a better way to handle things, usually arises for me. I trust the Universe has my back.

I'm a student of human development so I'm able to trace my developmental perspective all the way back to childhood. But for the sake of this survey, I'll go back to my 20s and 30s when I was outwardly focused and "success" oriented. The expert/achiever stages had me focused on education, money, power, and status. I've always cared about the environment, and the larger world in which we live, but what really drove me at the time was becoming what the American culture would typify as the symbol of success. That's not me now. I still would prefer to have more money in the bank than less. But the last 20 years or more has been an inward journey. I've used my own challenges to wake up, grow up, and clean up. I've turned all those developmental lessons into content that will help others. This survey and the SA360 are examples of the work that has come out of my inward journey, and turning that into something that can help others and the world. I'm not sure if I've answered this question directly. What's changed most about how I see myself is, I don't see myself as a singular person, but rather an awareness living through an incomprehensible flow of causes and conditions.

My daughter, Alana, often misunderstands me. She projects her own perspectives and motives on to me, but that's where she's at developmentally. I've done a lot of growing as a parent in the last four years since the divorce. I spent the summer thinking about and preparing for Alana's return, and my new full-time parenting role. My highest aspiration is to raise Alana to be self-aware and self directed. I want her to find her way in the world and be healthy and happy. I'm using my whole coaching methodology to support me in that effort. When she got back two weeks ago, we had a couple of meetings where I introduced a plan for living harmoniously together, with our roles and responsibilities, all under-pinned by attunement to one another. So far so good!

I have a "friend," who is narcissistic and manipulative. As narcissists are, he's also charming and generous at times. He owns a ranch where I host my retreats. I see all these parts of him, beneficent and malevolent, and so I'm conflicted about the relationship. But the retreat center serves my goals and business aspirations. Hosting retreats is work that I love, It creates significant opportunity for financial gain, so I stay in the relationship. I'm trying to show up in a good way. And although he bristles if he perceives that I'm "teaching" him, I do it surreptitiously. I know that I am slowly, positively, influencing him. We've been through a lot together. I've known him for nearly 20 years. He's smart, ambitious, and a capable businessman. He taught me a lot about masculinity and handling difficulties without complaining. So in someway, he's teaching me to!

I'm going through something like that right now. I've injured my right lateral epicondylitis. It aches. I want to workout, weight lift, which brings me a tremendous amount of fitness, self-confidence, and self respect. Because of my injury, I can't lift as I would like. At the initial stages of the injury, had I stopped lifting and been patient, I would've healed by now. But I didn't do that. I did what I've done many times in the past which is to continue pushing and I made things worse. Now I'm in this place of resignation and acceptance. I'm being careful; as careful as I can be. Let's see what I can learn from this.

I noticed my inner voice as a natural arising. Sometimes it seems like "me," and other times I'm aware of it as an object of my attention - I'm the awareness that's aware of it.

Strong emotions most often wake me up. Often times I become the awareness that is aware of context (the situation), bodily sensations, and thoughts. The sense of "I" recedes into the background and becomes the awareness that's aware. I do this not to disassociate, but to gain perspective. I stay embodied and aware of the world, body, in mind system and let things flow. I don't always make the right choices, and I'm aware that I will never have access to perfect information with which to make perfect choices, but I'm finding this is the best I can do at such times.

It totally depends on the context. If I'm teaching, I'm the teacher. If I'm coaching, I'm the coach. If I'm with friends, I'm with them. When I'm the parent, I'm the parent. No matter the context, however, I enjoy being transparent and unselfconscious.

Normally, when I'm with people, I can accept them, and give them grace. I have clients with very different views than my own. When I'm with them, I can love them as they are. But privately, I can be very judgmental. For example, I'm angry about the MAGA movement and what it's done to our country in the world.

Willful ignorance. My mom is willfully ignorant. I notice myself judging her. So, I ask myself, "when are you willfully ignorant?"

I was born with an alpha male personality in a beta male body. I'm handsome, but I'm small. I have the bone structure of a woman. In a real sense it's humiliating to my inborn personality. I've wrestled with this tension my whole life. I've found a way to make a compromise, and that is to lift weights and be fit and muscular as I can be. That helps give me self-confidence and power in the physical/sexual domain. Nevertheless, I recognize that in some sense, anatomy is destiny. My challenge is to be OK with the body I've been given this time around. It's healthy, fit, and nimble. This is a good body to go into old age with.

Money is a symbol. Money is energy. Money is a projection. Money is a means by which we transact. Money is an image. Money is an aspiration. The quest for it can bind someone to Samsara. Money unites, money divides. Money builds, and it destroys. It's like the energy of the sun. We need it to survive, but too much can cause cancer.

This is THE one area of my life that is yet to fully manifest the fruit of my work and practice. When I was young, I didn't manage my money well. I spent too much and saved too little. Later, when I owned physical therapy clinics, I made a lot of money, but after I lost that business, the money dried up. Because I've focused on my own development, I have acquired knowledge and skills that create value for many people. That capacity has allowed me to make a tremendous amount of money in some years, but as a solo entrepreneur, and also because of my own lack of focus and direction at times, other years I wasn't as successful money wise. After Lynda left the marriage I've gotten my financial house in order. I'm rebuilding my credit after bankruptcy. Although I don't have much in savings or retirement, I am building a tremendous business. That includes the SA360 diagnostic, books, online classes, retreat experiences, and value for Sabino Recovery and Canyon Ranch. The money is about to show up. I'm confident of that. When it does, I will fortify my financial foundation, make sure Alana has what she needs going forward, and then turn my attention to doing good with the money that I have.

There is only ever the NOW. So time is a human construct. It's a way we measure the flow of change. It's a useful construct that enables beings to move through this matrix, make plans, and align around agreed-upon activities. The seeming flow of time helps us measure things. It's an interesting paradox to only ever be in an ever changing NOW.

I'm a content creator. There isn't a day that goes by that I'm not making something beautiful, good, and true for the purpose of helping others and the world. I'm a health and wellness artist.

Consciousness is the ground of all being. Information is the only thing that truly exists, if you can call it existing. I have no way of explaining the evanescent and ineffable Universe or life that lives in it. Life is The LIFE, All that is, consciousness. "I" exists as a perspective. As do we all. A person is a perspective. What happens after death of this body, I don't know. If life continues, and I think it does, "I" won't be the one who reincarnates, however. The game just keeps going. Play it well!

My developmental mindset is what empowers me the most. I'm most stuck in a relation to the appearance of my physical body. Even after all the work I've done, I can't help but still want a Michael Jordan body. There's a part of me that still wants to jump out of the gym! Ha! Maybe next time around this soul (if such a thing exists) will get one. But if that does happen, he/she won't remember Mark Pirtle, just his karma will pass on. That's enough.

What gives my life meaning is this drive to wake up and become a better version of myself. I want to turn everything I learn that helps me overcome my challenges into content that helps others. That feels like a good life to me. Sure, I'd like to travel more, have more vacations, and ultimately find another person to love and be loved by. But all those things will arise when the time is right. I believe that. My challenges to be patient and keep turning life into art.
"""

ROB = """
My company was having some issues getting our product to market and I was burning a ton of capital about $100,000 every single month and it's completely stressing me out. I spent the last two months not sleeping well not being a good husband a good father, a good boss, because I was so overwhelmed and stressed about not having enough revenue to offset the burn The way I dealt with it was by being more reclusive not sleeping eating really bad food not taking care of myself not being presents and also not really addressing the pain or the stress so I would go to sleep at night and just put an audiobook on just to try to quiet my brain. But none of it helped.

When I'm overwhelmed, afraid of hurts, I usually lash out or I retreat or I do both. I try to be calm and I try to be reflective about it, but that's not always the case. I also end up finding myself looking for a ways to be vindictive instead of addressing it head on with the person. I also know that when I'm afraid I tend to have a shorter fuse and I'm also not present at all and I hurt the people that's around me because I'm not present and I'm not there.

I think one thing that I've noticed about the way that I have grown and it's been through the help of therapy is that I know that all of my reactions are coming from a childlike place because I'm afraid because I don't have the answers to the constant questions that are banging around in my head. I also know that from the outside I'm supposed to be a strong successful business person, but I also know that inside it's a complete opposite.

I feel misunderstood almost every single day, but I think it's because I also don't fully understand myself. I've always been focusing on helping and serving others that I often forget to serve myself, which makes sense if I don't understand myself, how would anybody else an example of it was last night when my sister Jamee picked me up from the airport after traveling for 12 hours and being exhausted she picked us up at 9 PM which is midnight for us on the East Coast. She was excited to see us and I was a bit of a jerk because I was so tired from traveling all day. She didn't understand the amount of exhaustion and stress that I'm going through and so she took it personally.

I got a little bit of interest from a group that's owned by peter thiel. I find myself questioning my values because on one hand getting an investment from his group or a tap on the shoulder from him directly basically assures your ascendance to unicorn status as a startup. However, well that's amazing for business. I do not align at all with his values.

What Amelia comes to mind is the common tug of war between my work and my family. This is always causing tension and I don't do a great job all the time with Mann managing it correctly.

I sometimes tend to avoid myself talk, but I'm trying to learn how to process it and deal with the stress of what's happening in my life right now.

I tend to be a direct leader in quite a lot of working in groups. It really depends on my mood though. If I'm dealing with something heavy, I tend to withdraw and my team sees it. I'm not as consistent as I should be.

This is one area that I am proud of myself as a human being. I'm able to listen and hear other people's views and perspectives. I really wanna understand why people see things the way they do even if they don't agree with my position or my own thoughts.

OK, it's under my skin about people who are just able to float through life and get things without much effort or people that are very selfish. But the one thing I've learned is the reason I have resentment towards those people is because I'm jealous that they can be that way with such a little care. I also admire how people are able to stay focused in their life or not care as much about some of the things that I care about like business and financial.

I've always struggled with my body and I've always struggled with sex, especially in relationships mostly because I have a high libido. I'd struggle with that now with my wife.

Money is freedom. Money is the pathway for freedom to make decisions freedom to spend my time how I want where I want when I want it.

My relationship of money is very complex. I've had such tumultuous experience with money throughout my life this ties back to my origin story of watching my father as a physician go from everything to nothing and how that domino effect hit all of us in our family. I constantly am worried about losing everything risking everything and having my kids experience what I experienced.

The most precious resource and something you can never make more of. It's fleeting and so exceptionally valuable that it's even hard to comprehend.

Through my work or sometimes I'll just do it all I always sketch cars. I'm very creative with my kids in terms of joking and telling stories.

I struggle with this as well I'm never quite sure of how I feel and what I believe. I wanna believe in something higher and that there's more.

I feel most empowered in my business, and I feel most out of control in my personal life.

I wanna start by saying that my kids give my life meeting which they do, but I also want to be honest and say that it's my work and what I'm currently doing with HALO and sometimes or often I put HALO above everything else. My sense of purpose has not really changed throughout my life. I've always found myself routing my purpose through business success. I think it has to do with the fact that I feel so bad about who I actually am as a person.
"""

JOHN = """
My most recent challenges around daily daily morning routine staying around in morning routines staying active and healthy depend a lot of it is around that I have even like 2 beers in the evening I just take that first morning minutes I don't take the time I am working on this I'm trying to get around the concept of freeing up and it's OK to be to spend that first two or three hours just on me and you know i can't come to work at 9:00 AM i'm working through on that but it's always been a struggle for me.

When I get overwhelmed or afraid or just like too much stuff going on I fall into bad habits so that's where I use eating or maybe drinking to get out of them I don't go there my body feels rushed intense adrenaline I noticed it in my sleep score my sleep score day goes down to the 60s and mid 70s when I'm overwhelmed versus like been on vacation and I'm doing 85 to 90 twos getting more exercise during the day also on the golf course I realized that when I'm I have fear in my brain and I try to control everything versus just let it happen this is when i just having fun with it i'm confident and moving forward it's i score a lot better and that's also true in the world with me and i think a lot of it has to do with just healthy activities that i need to work on.

My biggest change on how I viewed the world is after the bright star where I woke up in the mornings off and crying in the shower because I couldn't control what was going on with my team and I couldn't control stuff and I I just wanted that 20 years of control I realized that I was allowing others to control my emotions and I've made that decision that that's not going to happen I really believe in that space between input and emotion that I'm 100% in control now what's going on so I've completely changed my way of thinking and it's helping me even in the new business startup on how do I show up every day how do I encourage what do I need to do in the world that they think the world is actually getting to be a better place and i have a say in that.

One of the areas I'm currently being misunderstood is in this whole founding members of my AI one new organization I believe people are assuming that I'm just going to do the work for free and they don't quite get the value proposition must not be phrasing something correctly or pointing it out in a way that shows the value I think of AI is so important and going forward and yet I'm struggling even with members who put in $25,000 to get them engaged and moving forward making me feel like I'm poorly communicating and it make me feel frustrated it's making me feel almost some anger or something or maybe like why don't people just get it so and they gotta be able to invest in and move forward so just a little bit struggle on that front. Learning to reframe, use different tools.

And bright star my values were always being challenged of you know you need to lay off two or three people in your company in the meantime I'm watching them waste hundreds of thousands if not millions of dollars that aid at me that went against my loyalty and my optimism genes in my DNA I did not handle it well I let them i let them control a lot of my emotions and outcomes or whatever i wouldn't i gained weight i drank i did not handle it well it's one of the things i'd like to avoid as these situations come up in the future.

I feel pulled right now between two opposing things my own personal health freedom space and all that stuff with the new startup and being there for the team at all times and being there in a way like show up and work longer hours be get more stuff to them that's a struggle I'm trying to force through right now or I go there I'm doing well on my golf games but I just got to figure out how to balance of life and just be more effective in the use of my time also says start saying no to the wrong opportunities and really focus on just the right ones to gain the item and the money because i can get both and that can have it all i just haven't figured out a way to deal with that yet so it's been a struggle on my values and i flip flop on map.

My inner voice um is direct correlation of healthy activities so when I'm eating well exercising well sleeping well my inner voice is a very confident voice when I'm getting off for a little bit down on myself probably been not getting this me being under stress me whatever my inner voice goes to it negative peer thing with me and it kind of gets into a loop and I can go you know off the rails for a while it's about that but if I really notice the correlation between healthy activity and that I just kind of want that healthy activity more.

Have become exceptionally calm and processing emotions I really have tried not to let things bother me again in that space between input and emotion things have not bothered me much at all if I do start feeling it I've gotten good at counting to 10 if I start feeling that emotion click in me so that's that that's the impulses that I'm struggling with I'm just like the impulse to have a beer or choosing not to work out or not to meditate in the morning and just jumping into the e-mail that's where I'm losing control of my emotions that 5 seconds to make the decision to move forward with a good thing decision or move forward with the negative bad decision bad decision might just be going to work so.

In groups I am seen as a leader and a driver and a person that gets it done I have her figured out that now I can be I can be the passenger too so I've kind of enjoyed that I've learned how to be a passenger and allow the decisions to be not mine which is fun so I have to kind of learn how to step out I think others experience is pretty not as intense anymore but powerful driver of things to get done it's different than it used to be when I was kind of over the top but i'm still getting more and even starting to see more as leader i think i could even step that up if i really became more authentic in that space.

I enjoy people with different views I like to stretch my limits that's why I like to travel and see the world and talk to locals I like to be aware of what's going on learn and the constant learner of what I want to do so I like I like being a part of the world and opening my horizons. Golf, Travel and Saying Yes help me stay connected.

What gets under my skin and people are people that are willing to change they're unwilling to see a different point of view they're so set in their ways whether that's business politics right now unfortunately people are afraid to look in the mirror and say that they're in control of their own destiny those can really bother me I admire people who are willing to change and walk through the change and people that truly walk the walk there are always people that live their core values.

A relationship that deeply changed me was one of my dad so from just being super dad as a kid growing up to realizing you know he wasn't quite so super to being felt betrayed by my dad when he I had to bail him out of Colorado he kind of didn't take money from me bought inventory for me and did not ever be able to pay it back that hurt me I got mad at him he threatened suicide and the biggest change came out later when I made the decision of pure forgiveness to this love my dad for who he is and all of his stuff from his Vietnam days and so on to just enjoying and giving him the life he deserved I was lucky and privileged to have him as my dad and it made a big difference on how I see the world.

My body and energy has changed a lot over time I used to think of myself as an active bird thing and then I kind of went through a whole period of it it just didn't matter I was just I'm kind of wanting to beat myself up I think and now since I've lost all the weight and started to get stronger I think there's a chance I could actually get to the best health in my life which is what I want to be able to figure out if I can make that happen and I know I can make it happen but I still have doubts and something holding my back when it comes to that getting the most of them but there's still a fear something kicking me on that.

Money is freedom to me money allows me to do the things I want to do money allows me to learn money allows me to help others in my family money is relatively easy for me to come by which is a lucky and privileged position to be in and I think now that money is after daiwa's euro is make sure it allows me to spend a lot of time with friends and family and experiences so have a very positive view of money.

Great with money luckily I have done some amount of money and I'm capable of making money and I can kind of turn it on and off which has been like maybe I should not realize that can always do that but so my habits are on money or to save enough to make sure that my family and everyone has always taken care of but spend enough to I'm enjoying life I don't want to die with 10 million in the bank and rather die with a few million in the bank so everything's fine includes obviously protecting diane and my family.

Time is what I have and time is what I want to make sure I'm taking advantage of I have the ability to craft my life in the time left so I'm really trying to make sure like all physical stuff is done before 65 because you just never know and then obviously I'm hoping for another 20 years past that but just make sure I'm not ever having a regrets around time so I just try to enjoy life and i'm pretty structured around a lot of parts of time in the big picture stuff like travel or golf or seeing people and stuff like that so time is there but i don't think about it too much.

creativity imagination or critical to my thing i always want to be learning and growing that's why i like travel to i love i like i love business it's like i love strategic planning i want to continue to learn and grow and push the boundaries i think once you stop doing that it's not a good thing.

My spirituality is kind of based on nature and the greater good I'm always tell people I'm not very religious but if I was I'm on the Jesus squad not the God squad I've ended a lot of God and people that say they're God and Jesus are on the God of wrath and criticism and judgment I don't think that's our role in life their role is to help people and walk the walk and so I just like going to be a good human is a great thing to be so I'm just really trying to be a good human and to help people a lot and that makes a difference for me.

Leader, Idea Person, People look up to me and want me to help.

Push my thinking through lots of reading of different articles and magazines and stuff like that I also watch all different political shows I also get around my EO groups I go around different people with different philosophies I work with mark here to get a different view of who I am so i'm always trying to constantly learn and evolve.

All things Money and Business, I do not take I can't do it for an answer. I push and adjust. AIONE is the new one that I will make happen.

I have to hold back and restraint sometimes with some of my business relationships or whatever where I have to be a a coach or a mentor but I have to come and let them come to their computer and even though I'm very nervous about what's going on that is hard for me I want to drive but it's not my role in that situation they get very comfortable with that it's trying to again walk the walk maybe give them a different example but try to do it in a way that they come to their own conclusion so there's bigger buy and I think that's true with my son Eric and his work and job and his love him for who he is and let him move forward in life at his pace.

I have a lot of opportunities that I could take advantage of and do something for myself whether it's business advantages that are probably unfair because I know something or business you know somebody's in a bad leverage situation and I want to make sure I treat people fairly and right so I I wanna walk away with a win win I've just gotten very good at the win win I do not like it and I have unfortunately some friends who like to be in win lose situations or acquaintances probably not friends but I don't like the win lose so I found myself getting very good at using restraint and I don't consider restraint I think it's just my core value of being good.

I drive forward at 80% to 85% of Good vs Complete. This hurts me in some situations. Overall a benefit.

Option 1.

What gives my life meaning is my core slogan of create conversation inspire growth I love it when I see people whether it's people activating AI or someone understanding or me making a connection between two people and it turns to be a proven better connection I just love that feeling of being able to help people out I like watching do well i like being lucky and privileged enough to be able to do a lot for people that's what gives me meaning.

Golf is challenge. For the rest of life setbacks are learning opportunities. I move forward.

I try to understand they are doing their best in the their situation. I might not have communicated in a way they could hear. If ongoing I might distance myself.

Business Ideas, AI, Emotional Growth, Inward Looking Challenges. Physical Challenges - Climbing Mountains.
"""


# --------------------------------------------------------------------
# SYNTHETIC EDGE-CASE SUITE
# --------------------------------------------------------------------

EDGE_CASES = {
    "EMPTY": "",
    "ONE WORD – REACTIVE": "Whatever.",
    "ONE WORD – REFLECTIVE": "Reflecting.",
    "EXPLOSIVE ANGER": "I get furious and yell and slam doors when things don't go my way.",
    "SHUTDOWN AVOIDANT": "I withdraw and avoid everyone until it goes away.",
    "SHORT META": "I notice my reactions and try to pause.",
    "SHORT SYSTEMS": "Patterns emerge over time between choices.",
    "SYSTEMS ONLY": "Stakeholder dynamics interact through feedback loops and delays.",
    "META ONLY": "I observe my inner critic guiding many of my decisions.",
    "FAKE ABSTRACT": "Everything is connected and consciousness is infinite always.",
    "SOCIAL-PERSPECTIVE": "I try to understand them and see where they might be coming from.",
    "BOTH-AND PARADOX": "On the one hand I want stability, on the other hand I want change.",
    "TRAUMA-CHARGED HIGH LEVEL":
        "I understand complex systems but I still scream at people and shut down.",
    "LONG CHAOTIC": " ".join(["random words no structure emotional chaos"] * 80),
    "LONG HIGH REFLECTION BUT NO SYSTEMS":
        " ".join(["I reflect deeply on my patterns and triggers"] * 60),
    "LONG HIGH SYSTEMS BUT NO META":
        " ".join(["Market dynamics interact with supply cycles and reinforcement loops"] * 50)
}


# --------------------------------------------------------------------
# SHORT SANITY CHECKS
# --------------------------------------------------------------------

SHORT_TESTS = {
    "Meta + Systems + Both/And (should be S6+)":
        "I realize how my reactions shape outcomes, and I map patterns over time while holding multiple truths.",
    "Reactive (should be S1)":
        "I don't care leave me alone.",
    "Clear S5":
        "I track my habits, regulate my emotions, and try to understand the reasons behind my decisions.",
    "S6 Style":
        "I notice feedback loops between choices and relationships, and I integrate perspectives intentionally."
}


# --------------------------------------------------------------------
# MASTER TEST REGISTRY
# --------------------------------------------------------------------

TEST_GROUPS = {
    "REAL_DATA": {
        "David C (expected S5–S6)": DAVID,
        "Mark P (expected S5 approx.)": MARK,
        "Rob N (expected S6)": ROB,
        "John L (expected S6–S7)": JOHN,
    },

    "EDGE_CASES": EDGE_CASES,

    "SHORT_SANITY": SHORT_TESTS
}


# --------------------------------------------------------------------
# RUNNER
# --------------------------------------------------------------------

def run_all():
    print("\n==============================")
    print(" GLOBAL STAGE CLASSIFIER TEST ")
    print("==============================\n")

    full_results = {}

    for group_name, cases in TEST_GROUPS.items():
        print(f"\n=== {group_name} ===\n")
        group_results = {}

        for name, text in cases.items():
            t0 = time.perf_counter()
            try:
                result = _score_text(text)
            except Exception as e:
                result = {"error": str(e)}

            latency = (time.perf_counter() - t0) * 1000
            result["latency_ms"] = round(latency, 2)

            # Print to console in readable form
            print(f"\n--- {name} --- ({latency:.2f} ms)")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            group_results[name] = result

        full_results[group_name] = group_results

    # Save full results to disk
    with open("global_stage_results.json", "w", encoding="utf-8") as f:
        json.dump(full_results, f, ensure_ascii=False, indent=2)

    print("\n\n✅ GLOBAL TESTING COMPLETE")
    print("Results saved to global_stage_results.json\n")


# --------------------------------------------------------------------

if __name__ == "__main__":
    run_all()
