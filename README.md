# State Machine Scripts & project assembly
The purpose of this github page is to provide you with the tools and explanations to set up a fully compile-able arduino folder complete with state machines structures, software timers, debounced button reading and other supplemental modules. Though it is ment for somewhat more experienced programmers I welcome new commers to try this out.

#My motivation
When I was still learning for my bachelor degree in electronics, I had to write a paper about a topic of choise and I wrote a paper about bug prevention. Programming without bugs is very difficult to prevent. And on the level on which we program it is next to impossible. There are however things we can do. If you start a new project, you want to be able to do

When I started with my first 'real' job, I had to program a bicycle wheel taping machine. And I started out in C. Though the machine was not that complicated, I had difficulty doing the job. During development of the software for this machine and following machines, a lot of time went into adjusting the structure of the software. The taper software currently still exists out of a switch-case which uses numbers for case-labels and where state++ is used to transist from state to another. The readability is poor and it is an annoying job to make changes. The software came with lots of bugs, of which most were avoidable.

All software in the company was a complete mess. It was undocumentated, comments were in dutch and english. the states of their simplisitc state machines were not modulair. 'inc state' or in C 'state++' was used a lot instead of constants, every state had a label of letters and numbers instead of names and some files contained 20000 lines of code. It is still a payne to add states. There was no methods for an entry state. One-time-only stuff which had to happen for a state had to happen in the previous state. Adding a new state ment screwing arround with numbers and transplanting parts of codes. And the worst part, their version control was a complete mess. In some folders there were several extensions to be found; .ASM, .A, .BAC, and no extension. Alles files had the same content, on top of that the entire folder was copied so you'd have folderX (Copy 18) present. And yes 18 was the highest copy number I came accros.

With all my knowledge I obtained from coding myself, coding with other people, bugs, looking at (copy 18) and undocumentated and poorly written software. I realized that some drastic changes were needed. Some of the things I learned:

- how to implement a well-written modulair state machines
- how to manage project files.
- how macros can actually increase readability
- how to work with git

When writing my paper about preventing bugs was, I learned that 'repeatability' was part of preventing bugs. With this I mean the ability to reproduce earlier achiefed results without bugs. And this triggered something within me. When taking all my learned lessons in account I came to the one logical conlusion, people make a lot of mistakes. The one logical solution? Code generation.

#Code generation.
The solution to tackle as much problems as possible is to generate as much code as possible. The simple python and shell scripts I have developed can do the following things:

- They can generate entire state machine skeletons using a computer made state diagram
- They can assembly a fully arduino compilable projec folder
- They can create files for software timer
- IO can be generated using a simple text file

Further more I am adding supporting modules for SW such as a library to debounce buttons and listen to rising and falling flanks. Libraries for keypads as well for RTC modules will also be in this folder.

The scripts will be used in the alarm clock example to set up an entire new project. I will show all steps which must me made for setting up a project. For this we will use a checklist.

#My state machine implementation.
There are an infinite ways to make a finite state machine or FSM. I have seen my share in terror in some of the wrong ways and in some of the complicated ways.

Therefor I devised a state machine which is as human readable as possible. I use macro's to mold my function into states and state machines. Most 'good programmers' are 100% allergic for macro's and they always cry the same phrase: "by replacing code by non-standard code, you make your code harder to read for other people". In fact these people are allergic to all code which is not standard. I am here not only to remind these people that this is not a proven fact, I am here to prove the opposite of this 'claim'. The macro's I use are written so that you do not even have to know how they precisely look like. Besides this, the macros are generated by scripts, the usage of these macros are also generated by scripts and they are generated above the first usage. So if you really want to see how they look like, scroll up. And if you really have to look how they are used, just scroll down.

Before I show some code I'll explain briefly how my state machines work. And why I have chosen for that manner.

My state machine exists out of a switch-case of which every case performs a function call to an other function, the state. This state function returns true when the state is finished. When that is the case, the switch-case will select a new function.


