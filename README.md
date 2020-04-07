# COVID-19 Regulation Checker

_Disclaimer : This project is a purely individual effort, and is not endorsed or supported by any organization. The implementation is a prototype, and comes with no warranties as such. The encoding used is a proof-of-concept, and should **not** be used to interpret any laws._


The novel coronavirus (COVID-19) outbreak has led to an unprecendented crisis around the world. Thousands of people around the world got infected and, unfortunately, thousands lost their lives. While the disease, without doubt, has been among the worst crises faced by humanity, it has ushered in an astonishing period of collaborative effort to tackle the problem. 

While doctors, health care officials, pharmaceutical companies and medical schools have been working tirelessly in the frontline to treat people and to work on cures/vaccines, a range of computational solutions have been proposed to aid the fight against COVID-19. Such computational solutions include designing contact tracing frameworks, designing more effect testing strategies, etc. 

This project aims to contribute to such efforts in a small way. 

## Problem Statement
The problem statement is as follows: an effective way of combating the spread of COVID-19 is to enforce lockdowns and social distancing. To this effect, governments around the world have been issuing orders which enumerate which services stand suspended, and which ones are allowed to continue. For the sake of concreteness, I'll consider the situation in India. There are multiple orders being issued by the central government, as well as the respective state governments. This presents two challenges:

- _Conformance Problem_: How does one ensure that all the issued orders are actually compatible with each other? In other words, are there two orders O1 and O2 where, due to ambiguity, one can parse a service to be allowed in O1 while it is disallowed in O2?

- _Query Problem_: How does an ordinary citizen query these orders to check which service is actually enabled? When some of these orders were issued, there was a lot of confusion regarding which services are actually permitted. This resulted in essential services getting stopped in several regions, and contributed to the spread of rumors.

Some articles highlighting the issues arising due to the aforementioned problems are available <a target="_blank" href="https://indianexpress.com/article/coronavirus/trucks-stuck-rail-staff-stopped-online-delivery-staff-assaulted-essential-supplies-hit-hurdle/">here</a> and <a target="_blank" href="https://www.business-standard.com/article/companies/india-s-e-commerce-sector-comes-to-halt-due-to-lockdowns-120032301749_1.html">here</a>.

A first solution is to simply store a mapping from services to a status (indicating whether it is permitted). Such a key-value store may be stored as a SQL table, for example, which would allow efficient query processing, thereby solving the second problem, but not the conformance problem. As of this writing, I am not aware of any automated techniques which tackle the conformance problem for these government orders, and manual audits seem like the only solution. 

## Proposed Solution
There are two main observations here: first, the government orders can essentially be thought of as "constraints", and second, the sensitive nature of the topic necessitates the constraints to be specified in an unambiguous fashion. 

To tackle this, I have used <a target="_blank" href="https://github.com/Z3Prover/z3">Z3</a>, which is an industrial strength Satisfiability Modulo Theories (SMT) solver from <a target="_blank" href="https://www.microsoft.com/en-us/research/">Microsoft Research</a>. In a nutshell, an SMT solver takes as input a set of constraints (over a set of variables). It then uses _decision procedures_ to determine if the set of constraints can be satisfied. If yes, the constraints are said to be _satisfiable_, and the solver returns a _model_, which specifies the value of each variable which makes the set of constraints true. Otherwise, the solver returns saying the constraints are _unsatisfiable_. You can find more information about Z3 <a target="_blank" href="http://theory.stanford.edu/~nikolaj/programmingz3.html">here</a> and <a target="_blank" href="https://github.com/Z3Prover/z3/wiki#background">here</a>. 

### Encoding

- Encode each "service" as a boolean variable. For example, I create the boolean variables `restaurants`, `police`, and `hospital_service` to represent the status of restaurants, law enforcement officials and hospitals, respectively. In the code, I have partitioned these variables based on their categories (`transportation`, `shops`, `law_enforcement`, etc).

- Any service which is ordered to remain closed according to an order generates a constraint which negates the corresponding boolean variable. As an example, most orders require shops dealing with non-essential items to remain closed, which generates the constraints `constraints.append(restaurants == False)` and `constraints.append(apparels == False)` (with `apparels` representing clothing stores).

- Exceptions to the closure order are indicated by setting the corresponding boolean variable to true. For example, most orders necessitate that grocery and pharmacies remain open, which generates the constraints `constraints.append(grocery == True)` and `constraints.append(pharmacy == True)`.

- I define "aggregate" boolean variables to club together several services. As an example, there is a boolean variable `essential_services`, and I add implications from `essential_services` to `fire_services`, `hospital_services`, etc. This means that any order which sets `essential_services` to true (using a statement like "all essential services must remain open"), then _all_ the associated services implied by `essential_services` must also be set to true.

### Results
I translated several orders (enumerated below) in different functions. For example, the order from the Government of West Bengal is encoded in `encode_WBGovtOrder`, the order from Karanataka is encoded in `encode_KarnatakaGovtOrder`, and so on. Each function returns a set of constraints, based on the encoding of the corresponding order. A main function aggregates the set of constraints, and feeds it to Z3 for a solution.

Two things can happen at this point. Either Z3 returns _unsat_, which implies that the set of constraints cannot be satisfied together. This implies that there is some order which is shutting down a service, while another is requiring it stay open. In my experiments, this did not happen, which answers the Conformance problem in the positive: the different orders which I looked at do not contradict each other.

The other alternative is that Z3 returns _sat_, which means that there is an set of assignments to the boolean variables which satisfies all the constraints. The checker now walks through the model to figure out the variable assignments, so that the user can issue queries. As an example, you can query if apparel stores are open, and the Regulation Checker will return `False`. 

## Using the tool
Getting the tool up and running is really simple, and you require an installation of Z3 and Python3. To install Z3, simply download a pre-built binary, and setup your path to point to the binary. You also need to install the Python bindings for Z3, by executing the command `pip install z3-solver`. That's it! You can now run the tool by executing `python3 Covid19RegulationChecker.py`. 

## What's next?
Quite a lot actually. The implementation right now is a very simple proof-of-concept, and can be extended in several ways. One way is to improve the encoding to make it more precise, and capture contraints at finer granularity. As an example, right now the Regulation Checker enforces that all restaurants are closed, whereas in reality several restaurants are permitting take-away. The other way to contribute is to encode additional orders. 

There is clearly some benefits in using the language of SMT to unambiguously specify orders. However, the current implementation is too low-level to be generally useful. Is there a way to add a front-end, where a user can specify these orders more easily, and a translator uses the encoding scheme to generate Z3 queries? Food for thought...

I'd love to have your thoughts and inputs in this project! Please feel free to raise issues and PRs!

And most importantly, stay safe!


## Orders issuednot
- <a target="_blank" href="https://mha.gov.in/sites/default/files/PR_ConsolidatedGuidelinesofMHA_28032020.pdf"> Ministry of Home Affairs Lockdown Guidelines </a> dated 24/03/2020, modified 27/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158513429651307401.pdf"> Andaman and Nicobar UT wide lockdown </a> dated 19/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158513429651307401.pdf"> Andaman and Nicobar Lockdown of Transport </a> dated 19/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158511551351307401.pdf"> West Bengal order</a> dated 22/03/2020
- <a target="_blank" href="https://static.mygov.in/rest/s3fs-public/mygov_158505684451307401.pdf"> Karnataka Order Covid-19</a> dated 13/03/2020


