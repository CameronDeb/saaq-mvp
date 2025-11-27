#!/usr/bin/env python3
"""
Assertion-free test suite for awareness_quotient.py

This runs:
- REAL-LIKE CASES (David/Mark/Rob/John synthetic approximations)
- STANDARD FUNCTIONAL TESTS (domain-specific)
- EDGE CASES

No assertions — only prints output.
"""

import json
import time
from dataclasses import dataclass
from typing import Callable, Optional
from awareness_quotient import _score_awareness


# ---------------------------
# Data class for test cases
# ---------------------------
@dataclass
class Case:
    name: str
    text: str
    checks: Optional[Callable] = None   # ignored entirely

# ---------------------------
# REAL-LIKE CASES
# ---------------------------
DAVID_LIKE = """
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
"""

MARK_LIKE = """
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

ROB_LIKE = """
I map how system constraints and incentives reinforce existing behavior, and
I reflect on how my decisions ripple outward. I am aware of internal tensions
and try to synthesize competing needs.
"""

JOHN_LIKE = """
I step back from my reactions to see the broader system and my place in it.
I consider others' perspectives and try to hold paradox as I move through
complex situations.
"""

REAL_CASES = [
    Case("David-like (reflective, systemic)", DAVID_LIKE),
    Case("Mark-like (high, systemic+integrative)", MARK_LIKE),
    Case("Rob-like (systemic leadership)", ROB_LIKE),
    Case("John-like (high, reflective, systemic)", JOHN_LIKE),
]


# ---------------------------
# FUNCTIONAL TEST CASES
# ---------------------------

SELF_BASIC = "I notice my reactions and see my patterns."
ER_MIXED = "I pause and take a breath before responding."
PERSPECTIVE = "I try to see the situation from their perspective."
META_STRONG = "I reflect on my thinking and question my assumptions."
SYSTEMS_STRONG = "Patterns in the broader system reveal feedback loops over time."
INTEGRATIVE_STRONG = "Two things can be true; I hold the paradox while integrating both sides."

FUNCTIONAL_CASES = [
    Case("Self-Awareness — basic", SELF_BASIC),
    Case("Emotional Regulation — mixed", ER_MIXED),
    Case("Perspective Awareness — empathy", PERSPECTIVE),
    Case("Meta-Awareness — strong", META_STRONG),
    Case("Systemic Awareness — strong", SYSTEMS_STRONG),
    Case("Integrative Awareness — strong", INTEGRATIVE_STRONG),
]


# ---------------------------
# EDGE CASES
# ---------------------------

EDGE_CASES = [
    Case("Empty text", ""),
    Case("One word", "hi"),
    Case("Random noise", "asdf qwer zx"),
    Case("Long but shallow", "word " * 900),
    Case("Long reflective but dysregulated",
         "I notice my reactions but I lash out and lose control " * 40),
    Case("Perfectly balanced artificial sample",
         "I notice my thoughts, take a breath, see others' perspectives, "
         "map the system, and integrate paradoxes." * 3),
]


# ---------------------------
# Test Runner
# ---------------------------

def run_case(case: Case):
    print(f"\n--- {case.name} ---")
    t0 = time.perf_counter()

    result = _score_awareness(case.text)

    latency = (time.perf_counter() - t0) * 1000
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Latency: {latency:.2f} ms")


def run_suite(cases, name):
    print("\n==============================")
    print(f"  {name}")
    print("==============================")
    for case in cases:
        run_case(case)


def main():
    print("\n==============================")
    print("     AWARENESS QUOTIENT TEST")
    print("==============================")

    run_suite(REAL_CASES, "REAL-LIKE CASES")
    run_suite(FUNCTIONAL_CASES, "STANDARD FUNCTIONAL TESTS")
    run_suite(EDGE_CASES, "EDGE CASES")

    print("\n\n✅ All awareness tests completed. No assertions used.")


if __name__ == "__main__":
    main()
