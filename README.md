# COVID-19 Regulation Checker
The novel coronavirus (COVID-19) outbreak has led to an unprecendented crisis around the world. Thousands of people around the world got infected and, unfortunately, thousands lost their lives. While the disease, without doubt, has been among the worst crises faced by humanity, it has ushered in an astonishing period of collaborative effort to tackle the problem. 

While doctors, health care officials, pharmaceutical companies and medical schools have been working tirelessly in the frontline to treat people and to work on cures/vaccines, a range of computational solutions have been proposed to aid the fight against COVID-19. Such computational solutions include designing contact tracing frameworks, designing more effect testing strategies, etc. 

This project aims to contribute to such efforts in some small way. 

## Problem Statement
The problem statement is as follows: an effective way of combating the spread of COVID-19 is to enforce lockdowns and social distancing. To this effect, governments around the world have been issuing orders which enumerate which services stand suspended, and which ones are allowed to continue. For the sake of concreteness, I'll consider the situation in India. There are multiple orders being issued by the central government, as well as the respective state governments. This presents two challenges:

- _Conformance Problem_: How does one ensure that all the issued orders are actually compatible with each other? In other words, are there two orders O1 and O2 where, due to ambiguity, one can parse a service to be allowed in O1 while it is disallowed in O2?

- _Query Problem_: How does an ordinary citizen query these orders to check which service is actually enabled? When some of these orders were issued, there was a lot of confusion regarding which services are actually permitted. This resulted in essential services getting stopped in several regions, and contributed to the spread of rumors.

Some articles highlighting the issues arising due to the aforementioned problems are available <a target="_blank" href="https://indianexpress.com/article/coronavirus/trucks-stuck-rail-staff-stopped-online-delivery-staff-assaulted-essential-supplies-hit-hurdle/">here</a> and <a target="_blank" href="https://www.business-standard.com/article/companies/india-s-e-commerce-sector-comes-to-halt-due-to-lockdowns-120032301749_1.html">here</a>.

A first solution is to simply store a mapping from services to a status (indicating whether it is permitted). Such a key-value store may be stored as a SQL table, for example, which would allow efficient query processing, thereby solving the second problem, but not the conformance problem. As of this writing, I am not aware of any automated techniques which tackle the conformance problem for these government orders, and manual audits seem the only solution. 

## Proposed Solution
There are two main observations here: first, the government orders can essentially be thought of as "constraints", and second, the sensitive nature of the topic necessitates the constraints to be specified in an unambiguous fashion. 

To tackle this, I have used <a target="_blank" href="https://github.com/Z3Prover/z3">Z3</a>, which is an industrial strength SMT solver from <a target="_blank" href="https://www.microsoft.com/en-us/research/">Microsoft Research</a>. In a nutshell, an SMT solver takes as input a set of constraints over a set of variables. It then uses _decision procedures_ to determine if the set of constraints can be satisfied. If yes, the constraints are said to be _satisfiable_, and the solver returns a _model_, which specifies the value of each variable which makes the set of constraints true. Otherwise, the solver returns saying the constraints are _unsatisfiable_. 




## Orders issued
- <a target="_blank" href="https://mha.gov.in/sites/default/files/PR_ConsolidatedGuidelinesofMHA_28032020.pdf"> Ministry of Home Affairs Lockdown Guidelines </a> dated 24/03/2020, modified 27/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158513429651307401.pdf"> Andaman and Nicobar UT wide lockdown </a> dated 19/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158513429651307401.pdf"> Andaman and Nicobar Lockdown of Transport </a> dated 19/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158511551351307401.pdf"> West Bengal order</a> dated 22/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158505684451307401.pdf"> Karnataka Order Covid-19</a> dated 13/03/2020

